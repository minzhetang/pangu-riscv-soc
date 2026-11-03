#!/usr/bin/env python3
"""Bounded B-UART-RX runner and ACTUAL results builder.

Rules:
  * Plan and artifact hashes are checked before any DUT compile/run.
  * Tools are explicit paths; PATH is never modified and no shell is used.
  * Every compile/run has a process timeout; the TB has its own cycle watchdog.
  * PASS requires the native success marker, no failure marker, and a matching
    TEST_PASS block for the case.  A deliberate watchdog run is TIMEOUT.
  * The negative checker is a separate TB with a deliberately wrong expected
    value; it must detect the mismatch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # work/peripherals/rx
PKG = Path(os.environ.get("RX_PKG", str(ROOT.parent.parent.parent))).resolve()
IVERILOG = Path(os.environ.get("RX_IVERILOG", r"D:\iverilog\bin\iverilog.exe"))
VVP = Path(os.environ.get("RX_VVP", r"D:\iverilog\bin\vvp.exe"))
IVL_LIB = Path(os.environ.get("RX_IVL_LIB", r"D:\iverilog\lib\ivl"))
PYTHON = Path(sys.executable)
sys.path.insert(0, str(ROOT.parent / "scripts"))
from runner_common import run_process
HARD_CAP_DEFAULT = 1_000_000

PLAN = ROOT / "tests" / "rx-plan-1.3.5.json"
PLAN_HASH = ROOT / "tests" / "rx-plan-1.3.5.sha256"
RESULTS = ROOT / "results.json"

BASE_LIMITS = [
    "Simulation-only: no PDS synthesis, place-and-route, timing analysis, JTAG, download, Flash, board loopback or temperature test was performed; hardware remains STOPPED.",
    "Only public RX ports are observed; no claim is made about internal nodes or physical metastability/MTBF.",
    "Icarus Verilog 12 logical-cycle simulation does not prove physical baud tolerance, noise immunity, CDC layout or board-level reliability.",
    "N=234 is a representative divider calculation, not a board measurement or a claim that the CPU is running at 27 MHz.",
]


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rel_pkg(path: Path) -> str:
    return path.resolve().relative_to(PKG.resolve()).as_posix()


def rel_root(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def clip(text: str, limit: int = 4_000_000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n[TRUNCATED %d chars]\n" % (len(text) - limit)


def resolve_under(root: Path, text: str, label: str) -> Path:
    """Resolve a relative path under root; reject absolute/drive/.. escapes."""
    from pathlib import PureWindowsPath
    raw = PureWindowsPath(text)
    if raw.is_absolute() or raw.drive or raw.root or any(p == ".." for p in raw.parts):
        raise ValueError("%s path is absolute or escapes: %s" % (label, text))
    candidate = (root / Path(*raw.parts)).resolve()
    candidate.relative_to(root.resolve())
    return candidate


def run_cmd(argv, cwd: Path, timeout_s: int, log_path: Path):
    """Delegate to the shared file-backed bounded process runner."""
    return run_process(argv, cwd, timeout_s, log_path)


def extract_block(log_text: str, test_id: str) -> str:
    begin = log_text.find("TEST_BEGIN " + test_id)
    if begin < 0:
        return ""
    pass_at = log_text.find("TEST_PASS " + test_id, begin)
    fail_at = log_text.find("TEST_FAIL " + test_id, begin)
    ends = [x for x in (pass_at, fail_at) if x >= 0]
    if not ends:
        return log_text[begin:]
    end = min(ends)
    line_end = log_text.find("\n", end)
    return log_text[begin:] if line_end < 0 else log_text[begin:line_end + 1]


def summarize_block(block: str, case_id: str, status: str) -> str:
    if status == "PASS":
        return "%s: TEST_PASS marker; no CHK_FAIL/TEST_FAIL in block" % case_id
    if status == "TIMEOUT":
        return "%s: TB/process timeout before a complete TEST_PASS" % case_id
    if status == "TOOL_ERROR":
        return "%s: compile/tool failure; DUT not run" % case_id
    lines = [x.strip() for x in block.splitlines() if x.strip()]
    return "; ".join(lines)[:4000] if lines else "%s: missing TEST_BEGIN/TEST_PASS block" % case_id


def command_dict(argv, timeout_s: int) -> dict:
    return {
        "argv": [str(x) for x in argv],
        "cwd": "work/peripherals/rx",
        "executed": True,
        "timeout_s": timeout_s,
    }


def make_row(case_id: str, acceptance_id: str, purpose: str, expected: str,
             status: str, actual: str, duration_s: float, command: dict,
             log_paths, wave_paths, plan_sha: str, limitations=None) -> dict:
    if limitations is None:
        limitations = list(BASE_LIMITS)
    return {
        "id": case_id,
        "acceptance_id": acceptance_id,
        "purpose": purpose,
        "expected": expected,
        "expected_sha256": plan_sha,
        "actual": actual,
        "status": status,
        "duration_s": round(float(duration_s), 6),
        "command": command,
        "log_paths": [rel_pkg(Path(x)) for x in log_paths],
        "wave_paths": [rel_pkg(Path(x)) for x in wave_paths],
        "limitations": list(limitations),
    }


def classify_watchdog(run_res):
    """Return (status, reason, marker_line) for the deliberate TB watchdog."""
    if run_res is None:
        return "TOOL_ERROR", "watchdog run not executed", ""
    text = run_res["combined"]
    marker = ""
    for line in text.splitlines():
        if "TB_WATCHDOG_TIMEOUT" in line:
            marker = line.strip()
            break
    if run_res["timed_out"]:
        return "FAIL", "process timeout without accepted TB watchdog evidence", marker
    if run_res["log_truncated"]:
        return "FAIL", "watchdog log truncated; completeness not proven", marker
    if run_res["returncode"] != 0:
        return "FAIL", "watchdog native rc=%s" % run_res["returncode"], marker
    if not marker:
        return "FAIL", "TB watchdog marker not observed", marker
    return "TIMEOUT", "TB-emitted watchdog with native rc=0 and no process timeout", marker


def classify_config(compile_res, run_res):
    """Classify one configuration; global/entry failures must win."""
    if not compile_res.get("ok") or run_res is None:
        return "TOOL_ERROR"
    if run_res.get("log_truncated"):
        return "FAIL"
    if run_res.get("timed_out"):
        return "TIMEOUT"
    if run_res.get("returncode") != 0:
        return "FAIL"
    text = run_res.get("combined", "")
    if "RX_SELFCHECK_PASS" not in text:
        return "FAIL"
    if any(x in text for x in ("CHK_FAIL", "TEST_FAIL", "RX_SELFCHECK_FAIL")):
        return "FAIL"
    return "PASS"


def case_status(overall: str, block: str, case_id: str) -> str:
    if overall in ("TIMEOUT", "TOOL_ERROR"):
        return overall
    if overall != "PASS":
        # A global selfcheck/tool/log failure must propagate even if an
        # individual TEST_PASS block is present.
        return "FAIL"
    if not block:
        return "FAIL"
    if ("TEST_PASS " + case_id) not in block:
        return "FAIL"
    if "TEST_FAIL " + case_id in block or "CHK_FAIL" in block:
        return "FAIL"
    return "PASS"


def main() -> int:
    run_id = datetime.now().strftime("rx-%Y%m%d-%H%M%S")
    log_dir = ROOT / "logs" / run_id
    wave_dir = ROOT / "waves" / run_id
    suffix = 0
    while log_dir.exists() or wave_dir.exists():
        suffix += 1
        run_id = datetime.now().strftime("rx-%Y%m%d-%H%M%S") + "-" + str(suffix)
        log_dir = ROOT / "logs" / run_id
        wave_dir = ROOT / "waves" / run_id
    log_dir.mkdir(parents=True)
    wave_dir.mkdir(parents=True)

    generated_at = now()
    plan = json.loads(PLAN.read_text(encoding="utf-8-sig"))
    plan_actual = sha256(PLAN)
    plan_expected = ""
    if PLAN_HASH.exists():
        parts = PLAN_HASH.read_text(encoding="utf-8-sig").strip().split()
        if parts:
            plan_expected = parts[0].upper()
    plan_hash_ok = bool(plan_expected) and plan_expected == plan_actual

    artifact_lines = []
    artifact_ok = True
    for key in ("rtl", "tb", "negative_tb", "watchdog_tb", "illegal_tb", "ledger_check", "capture"):
        info = plan["artifacts"][key]
        try:
            path = resolve_under(PKG, info["path"], "artifact " + key)
        except ValueError as exc:
            artifact_lines.append("ARTIFACT key=%s ERROR=%s" % (key, exc))
            artifact_ok = False
            continue
        actual = sha256(path) if path.exists() else "MISSING"
        match = actual.upper() == str(info["sha256"]).upper()
        artifact_ok = artifact_ok and match
        artifact_lines.append(
            "ARTIFACT key=%s path=%s expected=%s actual=%s match=%s"
            % (key, info["path"], info["sha256"], actual, "YES" if match else "NO")
        )
    hard_cap = int(plan.get("expected_per_configuration", {}).get("tb_hard_cap", HARD_CAP_DEFAULT))
    cycle_ok = 1 <= hard_cap <= HARD_CAP_DEFAULT
    for cfg in plan.get("configurations", []):
        max_cycles = int(cfg.get("tb_max_cycles", 0))
        if max_cycles < 1 or max_cycles > hard_cap:
            cycle_ok = False
            artifact_lines.append(
                "CYCLE_BUDGET cfg=%s tb_max_cycles=%d hard_cap=%d REJECT"
                % (cfg.get("id", "?"), max_cycles, hard_cap)
            )
    plan_ok = plan_hash_ok and artifact_ok and cycle_ok
    plan_log = log_dir / "plan_check.log"
    write_text(
        plan_log,
        "PLAN_PATH=" + rel_pkg(PLAN) + "\n"
        + "PLAN_SHA256_EXPECTED=" + plan_expected + "\n"
        + "PLAN_SHA256_ACTUAL=" + plan_actual + "\n"
        + "PLAN_HASH_MATCH=" + ("YES" if plan_hash_ok else "NO") + "\n"
        + "\n".join(artifact_lines) + "\n"
        + "PLAN_CHECK=" + ("PASS" if plan_ok else "FAIL") + "\n",
    )
    plan_duration = 0.0

    if not plan_ok:
        # Fail closed before any tool query or DUT compile/run.
        write_text(
            log_dir / "results_FAIL_PLAN.json",
            json.dumps({
                "kind": "ACTUAL",
                "run_id": run_id,
                "generated_at": generated_at,
                "task_id": "B-UART-RX",
                "status": "FAIL",
                "reason": "plan/artifact/cycle-budget gate failed; no DUT run",
                "plan_check_log": rel_pkg(plan_log),
            }, ensure_ascii=False, indent=2) + "\n",
        )
        print("PLAN_CHECK=FAIL; no DUT compile/run")
        return 1

    # Tool version queries are recorded separately; they are not DUT PASS.
    tool_logs = []
    for name, argv in (
        ("iverilog", [IVERILOG, "-V"]),
        ("vvp", [VVP, "-V"]),
        ("python", [PYTHON, "--version"]),
    ):
        p = log_dir / ("tool_" + name + ".log")
        r = run_cmd(argv, ROOT, 10, p)
        tool_logs.append((name, r, p))
    iverilog_version = "UNVERIFIED"
    vvp_version = "UNVERIFIED"
    for name, r, _p in tool_logs:
        text = r["combined"]
        if name == "iverilog":
            m = re.search(r"Icarus Verilog version\s+([^\r\n]+)", text)
            if m:
                iverilog_version = m.group(1).strip()
        elif name == "vvp":
            m = re.search(r"Icarus Verilog runtime version\s+([^\r\n]+)", text)
            if m:
                vvp_version = m.group(1).strip()
    tools = [
        {
            "name": "Icarus Verilog (iverilog)",
            "version": iverilog_version,
            "legal_source": "Existing lawful local Icarus installation recorded in B-ENV; explicit path D:\\iverilog\\bin\\iverilog.exe, PATH unchanged.",
        },
        {
            "name": "Icarus Verilog (vvp)",
            "version": vvp_version,
            "legal_source": "Existing lawful local Icarus installation recorded in B-ENV; explicit path D:\\iverilog\\bin\\vvp.exe, PATH unchanged.",
        },
        {
            "name": "Python (runner/results only)",
            "version": sys.version.split()[0],
            "legal_source": "Existing local Python 3.12 embeddable installation recorded in B-ENV; explicit path, standard library only.",
        },
    ]

    rows = []
    config_runs = {}
    if not plan_ok:
        # Do not compile or run any DUT when the frozen plan/artifacts differ.
        for case in plan["cases"]:
            for cfg in case["configs"]:
                cid = "%s-%s" % (case["id"], cfg)
                rows.append(make_row(
                    cid, case["acceptance_id"], case["purpose"],
                    case["expected"], "TOOL_ERROR",
                    "plan/artifact hash check failed; DUT not run",
                    0.0, command_dict([PYTHON, "-c", "plan/artifact check"], 30),
                    [plan_log], [], plan_actual,
                ))
    else:
        for cfg in plan["configurations"]:
            n = int(cfg["clks_per_bit"])
            max_cycles = int(cfg.get("tb_max_cycles", 200000))
            vvp_rel = "waves/%s/uart_rx_N%d.vvp" % (run_id, n)
            vcd_rel = "waves/%s/uart_rx_N%d.vcd" % (run_id, n)
            compile_argv = [
                IVERILOG, "-B", IVL_LIB, "-g2012", "-Wall", "-s", "tb_uart_rx",
                "-DCLKS_PER_BIT=%d" % n,
                "-DTB_MAX_CYCLES=%d" % max_cycles, "-I", "tb",
                "-o", vvp_rel, "src/uart_rx.v", "tb/rx_public_capture.sv", "tb/tb_uart_rx.sv",
            ]
            compile_log = log_dir / ("compile_N%d.log" % n)
            compile_res = run_cmd(compile_argv, ROOT, 60, compile_log)
            run_argv = [
                VVP, "-N", "-M-", "-M" + str(IVL_LIB), vvp_rel,
                "+WAVE_FILE=" + vcd_rel,
            ]
            run_log = log_dir / ("run_N%d.log" % n)
            run_res = None
            if compile_res["ok"]:
                run_res = run_cmd(run_argv, ROOT, 30, run_log)
            overall = classify_config(compile_res, run_res)
            vcd_path = ROOT / vcd_rel
            vcd_size = vcd_path.stat().st_size if vcd_path.exists() else 0
            config_runs[n] = {
                "compile": compile_res,
                "compile_log": compile_log,
                "compile_argv": compile_argv,
                "run": run_res,
                "run_log": run_log,
                "run_argv": run_argv,
                "vvp": vvp_rel,
                "vcd": vcd_rel,
                "vcd_path": vcd_path,
                "vcd_size": vcd_size,
                "status": overall,
            }
            run_text = run_res["combined"] if run_res else ""
            for case in plan["cases"]:
                if cfg["id"] not in case["configs"]:
                    continue
                cid = "%s-%s" % (case["id"], cfg["id"])
                block = extract_block(run_text, case["id"])
                st = case_status(overall, block, case["id"])
                actual = summarize_block(block, case["id"], st)
                dur = (run_res["duration_s"] if run_res else compile_res["duration_s"])
                cmd = command_dict(run_argv if run_res else compile_argv, 30)
                logs = [compile_log, run_log] if run_res else [compile_log]
                waves = [vcd_path] if vcd_path.exists() else []
                rows.append(make_row(
                    cid, case["acceptance_id"], case["purpose"] + " Configuration %s." % cfg["id"],
                    case["expected"], st, actual, dur, cmd, logs, waves, plan_actual,
                ))

    # Defense in depth: the early return above already prevents this path.
    if not plan_ok:
        print("PLAN_CHECK=FAIL; auxiliary DUTs not run")
        return 1

    # Negative checker (separate TB, deliberately wrong expected value).
    neg_max_cycles = int((plan.get("negative", {}) or {}).get("tb_max_cycles", 20000))
    neg_compile_argv = [
        IVERILOG, "-B", IVL_LIB, "-g2012", "-Wall", "-s", "tb_uart_rx_neg",
        "-DTB_MAX_CYCLES=%d" % neg_max_cycles, "-I", "tb",
        "-o", "waves/%s/uart_rx_neg.vvp" % run_id,
        "src/uart_rx.v", "tb/rx_public_capture.sv", "tb/tb_uart_rx_neg.sv",
    ]
    neg_compile_log = log_dir / "compile_neg.log"
    neg_compile = run_cmd(neg_compile_argv, ROOT, 60, neg_compile_log)
    neg_run_argv = [VVP, "-N", "-M-", "-M" + str(IVL_LIB), "waves/%s/uart_rx_neg.vvp" % run_id]
    neg_run_log = log_dir / "run_neg.log"
    neg_run = None
    neg_status = "TOOL_ERROR"
    if neg_compile["ok"]:
        neg_run = run_cmd(neg_run_argv, ROOT, 30, neg_run_log)
        ntext = neg_run["combined"]
        if neg_run["returncode"] == 0 and not neg_run["timed_out"] \
                and not neg_run["log_truncated"] \
                and "TB_WATCHDOG_TIMEOUT" not in ntext \
                and "NEG_CONTROL_PASS" in ntext and "NEG_CHECKER_PASS" in ntext \
                and "NEG_EXTRA_VALID_DETECTED" in ntext \
                and "NEG_EXTRA_VALID_CONTROL_PASS" in ntext \
                and "NEG_MISSING_DETECTED" in ntext \
                and "NEG_ORDER_DETECTED" in ntext \
                and "NEG_WRONG_BYTE_DETECTED" in ntext \
                and "NEG_TWO_EVENT_CONTROL_PASS" in ntext \
                and "NEG_CAPTURE_SAME_EDGE_CONTROL_PASS" in ntext \
                and "NEG_CAPTURE_DROP_CONTROL_PASS" in ntext \
                and "NEG_CAPTURE_DROP_MISSING_DETECTED" in ntext \
                and "NEG_CAPTURE_DROP_WRONG_BYTE_DETECTED" in ntext \
                and "NEG_CAPTURE_CANCEL_CONTROL_PASS" in ntext \
                and "NEG_CAPTURE_CANCEL_MISSING_DETECTED" in ntext \
                and "NEG_CAPTURE_CANCEL_EXTRA_DETECTED" in ntext \
                and "NEG_CONTROL_FAIL" not in ntext and "NEG_CHECKER_MISSED" not in ntext \
                and "NEG_EXTRA_VALID_MISSED" not in ntext \
                and "NEG_EXTRA_VALID_CONTROL_FAIL" not in ntext \
                and "NEG_MISSING_MISSED" not in ntext \
                and "NEG_ORDER_MISSED" not in ntext and "NEG_WRONG_BYTE_MISSED" not in ntext \
                and "NEG_TWO_EVENT_CONTROL_FAIL" not in ntext \
                and "NEG_CAPTURE_SAME_EDGE_CONTROL_FAIL" not in ntext \
                and "NEG_CAPTURE_DROP_CONTROL_FAIL" not in ntext \
                and "NEG_CAPTURE_DROP_MISSING_MISSED" not in ntext \
                and "NEG_CAPTURE_DROP_WRONG_BYTE_MISSED" not in ntext \
                and "NEG_CAPTURE_CANCEL_CONTROL_FAIL" not in ntext \
                and "NEG_CAPTURE_CANCEL_MISSING_MISSED" not in ntext \
                and "NEG_CAPTURE_CANCEL_EXTRA_MISSED" not in ntext:
            neg_status = "PASS"
        else:
            neg_status = "FAIL"
    neg_actual = (
        "NEG_CONTROL_PASS; NEG_CHECKER_PASS; NEG_EXTRA/MISSING/ORDER/WRONG_BYTE_DETECTED; NEG_TWO_EVENT_CONTROL_PASS; NEG_CAPTURE_SAME_EDGE/DROP/CANCEL controls and missing/wrong/extra detection; public-stream capture plus shared ordered comparator"
        if neg_status == "PASS" else
        "negative checker did not report the expected control+detection markers"
    )
    rows.append(make_row(
        "COM-05", "RX-10/COM-05", "independent checker and ledger-capture negative proof at N=16",
        "Separate TB sends 0x55 but expects 0xAA; a public-stream capture source feeds the shared ordered comparator. Extra, missing, wrong-order and wrong-byte actual streams must be rejected, with one- and two-event controls passing.",
        neg_status, neg_actual,
        (neg_run["duration_s"] if neg_run else neg_compile["duration_s"]),
        command_dict(neg_run_argv if neg_run else neg_compile_argv, 30),
        [neg_compile_log, neg_run_log] if neg_run else [neg_compile_log],
        [], plan_actual,
    ))

    # Deliberate watchdog: expected TIMEOUT, not a functional failure.
    wd_compile_argv = [
        IVERILOG, "-B", IVL_LIB, "-g2012", "-Wall", "-s", "tb_uart_rx_watchdog",
        "-DTB_MAX_CYCLES=200",
        "-o", "waves/%s/uart_rx_watchdog.vvp" % run_id,
        "src/uart_rx.v", "tb/tb_uart_rx_watchdog.sv",
    ]
    wd_compile_log = log_dir / "compile_watchdog.log"
    wd_compile = run_cmd(wd_compile_argv, ROOT, 60, wd_compile_log)
    wd_run_argv = [VVP, "-N", "-M-", "-M" + str(IVL_LIB), "waves/%s/uart_rx_watchdog.vvp" % run_id]
    wd_run_log = log_dir / "run_watchdog.log"
    wd_run = None
    wd_status = "TOOL_ERROR"
    if wd_compile["ok"]:
        wd_run = run_cmd(wd_run_argv, ROOT, 30, wd_run_log)
        wd_status, wd_reason, wd_line = classify_watchdog(wd_run)
    else:
        wd_reason, wd_line = "watchdog compile failed", ""
    if wd_status == "TIMEOUT":
        wd_actual = wd_line + "; " + wd_reason + "; classified TIMEOUT not functional FAIL"
    else:
        wd_actual = wd_reason + "; classified " + wd_status + ", not mechanism success"
    rows.append(make_row(
        "COM-02", "COM-02", "bounded run and TB cycle watchdog",
        "Deliberate no-completion run with MAX_CYCLES=200 emits TB_WATCHDOG_TIMEOUT with rc=0 and is classified TIMEOUT; a process timeout is FAIL.",
        wd_status, wd_actual,
        (wd_run["duration_s"] if wd_run else wd_compile["duration_s"]),
        command_dict(wd_run_argv if wd_run else wd_compile_argv, 30),
        [wd_compile_log, wd_run_log] if wd_run else [wd_compile_log],
        [], plan_actual,
        limitations=["The deliberate watchdog test proves bounded termination, not functional correctness."],
    ))

    # Illegal N<8 configuration must be rejected.
    il_compile_argv = [
        IVERILOG, "-B", IVL_LIB, "-g2012", "-Wall", "-s", "tb_uart_rx_illegal",
        "-o", "waves/%s/uart_rx_illegal.vvp" % run_id,
        "src/uart_rx.v", "tb/tb_uart_rx_illegal.sv",
    ]
    il_compile_log = log_dir / "compile_illegal.log"
    il_compile = run_cmd(il_compile_argv, ROOT, 60, il_compile_log)
    il_run_argv = [VVP, "-N", "-M-", "-M" + str(IVL_LIB), "waves/%s/uart_rx_illegal.vvp" % run_id]
    il_run_log = log_dir / "run_illegal.log"
    il_run = None
    il_status = "TOOL_ERROR"
    if il_compile["ok"]:
        il_run = run_cmd(il_run_argv, ROOT, 30, il_run_log)
        if il_run["returncode"] == 0 and not il_run["timed_out"] \
                and not il_run["log_truncated"] \
                and "RX_ILLEGAL_CLKS_PER_BIT=4 minimum=8" in il_run["combined"] \
                and "RX_ILLEGAL_TEST_NO_REJECT" not in il_run["combined"]:
            il_status = "PASS"
        else:
            il_status = "FAIL"
    il_actual = (
        "RX_ILLEGAL_CLKS_PER_BIT=4 minimum=8; no silent clamp"
        if il_status == "PASS" else
        "illegal N=4 configuration was not explicitly rejected"
    )
    rows.append(make_row(
        "COM-06", "COM-06", "illegal N<8 configuration rejection",
        "N=4 must emit RX_ILLEGAL_CLKS_PER_BIT=4 minimum=8 at simulation start.",
        il_status, il_actual,
        (il_run["duration_s"] if il_run else il_compile["duration_s"]),
        command_dict(il_run_argv if il_run else il_compile_argv, 30),
        [il_compile_log, il_run_log] if il_run else [il_compile_log],
        [], plan_actual,
    ))

    # Meta rows: plan check, limits, fresh evidence.
    rows.insert(0, make_row(
        "COM-01", "COM-01", "frozen plan and artifact hash gate",
        "Plan SHA matches tests/rx-plan-1.3.5.sha256; RTL/TB/negative/watchdog/illegal/ledger-check hashes match the plan.",
        "PASS" if plan_ok else "FAIL",
        "PLAN_CHECK=PASS; %d artifact hashes match" % 7 if plan_ok else "PLAN_CHECK=FAIL; DUT not run",
        plan_duration, command_dict([PYTHON, "-c", "internal plan/artifact hash check"], 30),
        [plan_log], [], plan_actual,
    ))
    rows.insert(1, make_row(
        "COM-03", "COM-03", "bounded process and TB cycle limits",
        "Compile 60 s/item, run 30 s/item, TB_MAX_CYCLES selected per plan, hard cap 1,000,000.",
        "PASS" if plan_ok else "FAIL",
        "compile_timeout_s=60; run_timeout_s=30; per-config last_check+32 budgets=%s; tb_hard_cap=1000000; runner rejects >hard_cap; TB_HARD_CAP_REJECT on >1000000" % (
            ",".join("%s=%s(last=%s)" % (c["id"], c.get("tb_max_cycles", 0), c.get("last_check_cycle", "?")) for c in plan["configurations"])
        ),
        0.0, command_dict([PYTHON, "-c", "internal bounded-limit check"], 30),
        [plan_log], [], plan_actual,
    ))
    rows.insert(2, make_row(
        "COM-04", "COM-04", "fresh run evidence",
        "New run_id with new logs, results and VCDs; no old results or waves reused.",
        "PASS" if plan_ok else "FAIL",
        "run_id=%s; logs=%s; waves=%s" % (
            run_id, rel_pkg(log_dir), rel_pkg(wave_dir)
        ),
        0.0, command_dict([PYTHON, "-c", "internal fresh-evidence check"], 30),
        [plan_log], [], plan_actual,
    ))

    issues = []
    for r in rows:
        if r["status"] == "FAIL":
            issues.append("%s: FAIL" % r["id"])
        elif r["status"] == "TOOL_ERROR":
            issues.append("%s: TOOL_ERROR" % r["id"])
    if not issues:
        issues.append("No functional FAIL; COM-02 is an expected watchdog TIMEOUT, not a functional failure.")

    results = {
        "kind": "ACTUAL",
        "run_id": run_id,
        "generated_at": generated_at,
        "task_id": "B-UART-RX",
        "module_version": "1.0.0",
        "interface_version": "PERIPH-CORE-RX-1.0 / 1.0.0",
        "tools": tools,
        "tests": rows,
        "limitations": list(plan["limitations"]),
        "issues": issues,
    }
    write_text(RESULTS, json.dumps(results, ensure_ascii=False, indent=2) + "\n")

    # Schema validation is a separate structural check, not a DUT PASS.
    schema_log = log_dir / "schema_validate.log"
    schema_res = run_cmd(
        [PYTHON, str(PKG / "scripts" / "schema_validate.py"),
         "--schema", str(PKG / "templates" / "results.schema.json"),
         "--data", str(RESULTS)],
        PKG, 30, schema_log,
    )
    schema_ok = schema_res["ok"] and '"schema_check":"PASS"' in schema_res["combined"].replace(" ", "")

    manifest = {
        "run_id": run_id,
        "generated_at": generated_at,
        "plan": {
            "path": rel_pkg(PLAN),
            "expected_sha256": plan_expected,
            "actual_sha256": plan_actual,
            "hash_match": plan_hash_ok,
            "artifacts_ok": artifact_ok,
            "status": "PASS" if plan_ok else "FAIL",
            "log": rel_pkg(plan_log),
        },
        "tools": tools,
        "configs": {
            str(n): {
                "compile_command": [str(x) for x in c["compile_argv"]],
                "compile_log": rel_pkg(c["compile_log"]),
                "compile_rc": c["compile"]["returncode"],
                "compile_duration_s": c["compile"]["duration_s"],
                "run_command": [str(x) for x in c["run_argv"]],
                "run_log": rel_pkg(c["run_log"]),
                "run_rc": None if c["run"] is None else c["run"]["returncode"],
                "run_duration_s": None if c["run"] is None else c["run"]["duration_s"],
                "status": c["status"],
                "vcd": c["vcd"],
                "vcd_bytes": c["vcd_size"],
            }
            for n, c in config_runs.items()
        },
        "negative": {
            "compile_log": rel_pkg(neg_compile_log),
            "run_log": rel_pkg(neg_run_log),
            "status": neg_status,
        },
        "watchdog": {
            "compile_log": rel_pkg(wd_compile_log),
            "run_log": rel_pkg(wd_run_log),
            "status": wd_status,
        },
        "illegal_config": {
            "compile_log": rel_pkg(il_compile_log),
            "run_log": rel_pkg(il_run_log),
            "status": il_status,
        },
        "schema_validate": {
            "status": "PASS" if schema_ok else "FAIL",
            "log": rel_pkg(schema_log),
        },
    }
    write_text(log_dir / "run_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    print("RUN_ID=" + run_id)
    print("PLAN_CHECK=" + ("PASS" if plan_ok else "FAIL"))
    print("CONFIGS=" + ",".join("%s:%s" % (n, c["status"]) for n, c in config_runs.items()))
    print("NEGATIVE=" + neg_status)
    print("WATCHDOG=" + wd_status)
    print("ILLEGAL_CONFIG=" + il_status)
    print("SCHEMA=" + ("PASS" if schema_ok else "FAIL"))
    for r in rows:
        print("%s %s" % (r["status"], r["id"]))
    unexpected_timeouts = [r for r in rows if r["status"] == "TIMEOUT" and r["id"] != "COM-02"]
    return 0 if (plan_ok and schema_ok
                 and not any(r["status"] in ("FAIL", "TOOL_ERROR") for r in rows)
                 and not unexpected_timeouts) else 1


if __name__ == "__main__":
    sys.exit(main())
