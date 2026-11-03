#!/usr/bin/env python3
"""Bounded B-GPIO runner and ACTUAL results builder (correction 1.0.2).

Design rules:
  * Every plan/artifact hash is checked before any compile or DUT run.
  * Plan and artifact paths are normalized and must remain under the declared
    package/module roots; absolute paths, drive paths, ``..`` escapes and
    uncontrolled links are rejected.
  * A result is PASS only when the native return code is zero, no timeout
    occurred, the expected success marker is present, no failure marker is
    present, and exact write/compare counts agree.
  * Child processes are bounded.  On timeout the whole process tree is
    terminated, output is read with a bounded wait, and the cleanup duration
    is recorded.
  * Tool and package roots are explicit CLI arguments (or environment
    defaults); PATH is never modified and no shell is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path, PureWindowsPath
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent          # work/peripherals/gpio
DEFAULT_PKG = ROOT.parent.parent.parent                 # package root
sys.path.insert(0, str(ROOT.parent / "scripts"))
from runner_common import run_process, terminate_tree
DEFAULT_IVERILOG = Path(os.environ.get("GPIO_IVERILOG", r"D:\iverilog\bin\iverilog.exe"))
DEFAULT_VVP = Path(os.environ.get("GPIO_VVP", r"D:\iverilog\bin\vvp.exe"))
DEFAULT_IVL_LIB = Path(os.environ.get("GPIO_IVL_LIB", r"D:\iverilog\lib\ivl"))
DEFAULT_PLAN = "tests/gpio-plan.json"
DEFAULT_OUT_ROOT = None
PYTHON = Path(sys.executable).resolve()
CURRENT_PKG = DEFAULT_PKG

CONFIGS = (1, 8, 16)
MAIN_CASE_IDS = ("GPIO-01", "GPIO-02", "GPIO-03", "GPIO-04", "GPIO-05")
TB_HARD_CAP = 300000
MAX_LOG_CHARS = 4_000_000
TIMEOUT_CLEANUP_WAIT_S = 5
TIMEOUT_TREE_KILL_S = 5
BASE_LIMITS = [
    "Simulation-only: no PDS synthesis, place-and-route, timing analysis, JTAG, download, Flash, board pin test or temperature test was performed; hardware remains stopped.",
    "Only the public GPIO ports are observed; no claim is made about internal nodes or physical metastability.",
    "Icarus Verilog logical-cycle simulation does not prove physical metastability/MTBF, debounce, noise immunity or board-level input integrity.",
]


class RunnerError(Exception):
    """A bounded, user-visible runner/input error."""


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def rel_to_pkg(path: Path, pkg: Path) -> str:
    return path.resolve().relative_to(pkg.resolve()).as_posix()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _clip(text: str, limit: int = MAX_LOG_CHARS) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n[TRUNCATED %d chars]\n" % (len(text) - limit)


def _is_junction(path: Path) -> bool:
    try:
        return bool(hasattr(os.path, "isjunction") and os.path.isjunction(path))
    except OSError:
        return False


def resolve_under(root: Path, text: str, label: str, must_exist: bool = False) -> Path:
    """Resolve a relative path under root, rejecting escapes and links.

    The check is deliberately done on normalized components, not by string
    prefix matching.  Existing symlinks and Windows junctions are rejected
    before their targets can be used.
    """
    if not isinstance(text, str) or not text.strip():
        raise RunnerError("%s path is empty" % label)
    raw = PureWindowsPath(text)
    if raw.is_absolute() or raw.drive or raw.root:
        raise RunnerError("%s path is absolute or drive-qualified: %s" % (label, text))
    parts = raw.parts
    if not parts or any(part == ".." for part in parts):
        raise RunnerError("%s path escapes with '..': %s" % (label, text))
    root_res = root.resolve()
    current = root_res
    for part in parts:
        current = current / part
        if current.exists() and (current.is_symlink() or _is_junction(current)):
            raise RunnerError("%s path crosses an uncontrolled link: %s" % (label, text))
    candidate = (root_res / Path(*parts)).resolve()
    try:
        candidate.relative_to(root_res)
    except ValueError as exc:
        raise RunnerError("%s path escapes allowed root: %s" % (label, text)) from exc
    if must_exist and not candidate.exists():
        raise RunnerError("%s path does not exist: %s" % (label, text))
    return candidate


def _as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return str(value)


def _terminate_tree(pid: int) -> str:
    """Compatibility wrapper around the shared bounded tree terminator."""
    method, _error = terminate_tree(pid)
    return method


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


def extract_lines(block: str, prefix: str):
    return [line.strip() for line in block.splitlines() if line.strip().startswith(prefix)]


def extract_stats(log_text: str) -> str:
    lines = [line.strip() for line in log_text.splitlines() if line.strip().startswith("GPIO_STATS")]
    return lines[-1] if lines else ""


def classify_main(log_text: str, width: int, expected_writes: int,
                  expected_compares: int, returncode: Optional[int],
                  timed_out: bool, log_truncated: bool = False) -> tuple[str, str]:
    """Classify one formal run; native status and exact counts are mandatory."""
    if "TB_WATCHDOG_TIMEOUT" in log_text:
        return "TIMEOUT", "TB_WATCHDOG_TIMEOUT observed"
    if timed_out:
        return "TIMEOUT", "process timeout observed"
    if returncode is None:
        return "TOOL_ERROR", "no native return code"
    if returncode != 0:
        return "FAIL", "nonzero native return code %s" % returncode
    if "GPIO_SELFCHECK_FAIL" in log_text or "CHK_FAIL" in log_text or "TEST_FAIL" in log_text:
        return "FAIL", "failure marker present"
    if log_text.count("GPIO_SELFCHECK_PASS") != 1:
        return "FAIL", "success marker count is not exactly one"
    m = re.search(
        r"GPIO_STATS W=(\d+) writes=(\d+) expected_writes=(\d+) compares=(\d+) errors=(\d+)",
        log_text,
    )
    if not m:
        return "FAIL", "GPIO_STATS line missing"
    got_w = int(m.group(1))
    got_writes = int(m.group(2))
    got_expected_writes = int(m.group(3))
    got_compares = int(m.group(4))
    got_errors = int(m.group(5))
    if got_w != width:
        return "FAIL", "W mismatch got=%d expected=%d" % (got_w, width)
    if got_writes != expected_writes or got_expected_writes != expected_writes:
        return "FAIL", "write count mismatch got=%d expected_in_tb=%d expected_plan=%d" % (
            got_writes, got_expected_writes, expected_writes)
    if got_compares != expected_compares or got_errors != 0:
        return "FAIL", "compare/error mismatch compares=%d expected=%d errors=%d" % (
            got_compares, expected_compares, got_errors)
    return "PASS", "exact counts and success marker agree"


def classify_neg(log_text: str, returncode: Optional[int], timed_out: bool,
                 log_truncated: bool = False) -> tuple[str, str]:
    if "NEG_TB_WATCHDOG_TIMEOUT" in log_text:
        return "TIMEOUT", "negative TB watchdog observed"
    if timed_out:
        return "TIMEOUT", "process timeout observed"
    if returncode is None:
        return "TOOL_ERROR", "no native return code"
    if returncode != 0:
        return "FAIL", "nonzero native return code %s" % returncode
    if "GPIO_NEG_CONTROL_PASS" not in log_text:
        return "FAIL", "negative control marker missing"
    if "GPIO_NEG_CHECKER_PASS" not in log_text:
        return "FAIL", "negative checker marker missing"
    if any(x in log_text for x in ("GPIO_NEG_CONTROL_FAIL", "GPIO_NEG_SYNC_MISSED", "GPIO_NEG_HOLD_MISSED")):
        return "FAIL", "negative control/miss marker present"
    m = re.search(
        r"GPIO_NEG_CHECKER_PASS hold_errs=(\d+) sync_early_errs=(\d+) sync_late_errs=(\d+)",
        log_text,
    )
    if not m:
        return "FAIL", "negative checker count line missing"
    if int(m.group(1)) < 1 or int(m.group(2)) < 1 or int(m.group(3)) != 0:
        return "FAIL", "negative detection counts unexpected"
    return "PASS", "control and both deliberate errors are detected"


def classify_watchdog(log_text: str, returncode: Optional[int], timed_out: bool,
                      log_truncated: bool = False) -> tuple[str, bool, str]:
    if "TB_WATCHDOG_TIMEOUT" not in log_text:
        return "FAIL", False, "TB watchdog marker missing"
    if "limit=200" not in log_text:
        return "FAIL", False, "watchdog limit marker missing"
    # TIMEOUT remains the expected status even if the wrapper was killed, but
    # the mechanism is considered clean only when the TB self-terminated.
    mechanism_ok = (returncode == 0) and not timed_out and not log_truncated
    return "TIMEOUT", mechanism_ok, "watchdog marker observed; mechanism_ok=%s" % mechanism_ok


def command_dict(argv, timeout_s: int) -> dict:
    return {
        "argv": [str(x) for x in argv],
        "cwd": rel_to_pkg(ROOT, CURRENT_PKG),
        "executed": True,
        "timeout_s": timeout_s,
    }


def make_row(case_id: str, acceptance_id: str, purpose: str, expected: str,
             status: str, actual: str, duration_s: float, command: dict,
             log_paths, wave_paths, plan_sha: str, pkg: Path, limitations=None) -> dict:
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
        "log_paths": [rel_to_pkg(Path(x), pkg) for x in log_paths],
        "wave_paths": [rel_to_pkg(Path(x), pkg) for x in wave_paths],
        "limitations": list(limitations),
    }


def build_config_actual(case_id: str, width: int, log_text: str) -> str:
    block = extract_block(log_text, case_id)
    if not block:
        return "MISSING TEST_BEGIN/TEST_PASS block for " + case_id
    if case_id == "GPIO-01":
        obs = (extract_lines(block, "GPIO_WIDTH") + extract_lines(block, "GPIO01_RESET")
               + extract_lines(block, "GPIO01_RELEASE"))
        return "subcases=GPIO-01-RESET,GPIO-01-RELEASE; " + "; ".join(obs)
    if case_id == "GPIO-02":
        return "subcases=GPIO-02-ZERO,GPIO-02-ONES,GPIO-02-55,GPIO-02-AA,GPIO-02-WALK,GPIO-02-ISOLATION; " + "; ".join(extract_lines(block, "GPIO02_WRITES"))
    if case_id == "GPIO-03":
        return "subcases=GPIO-03-HOLD12; " + "; ".join(extract_lines(block, "GPIO03_HOLD"))
    if case_id == "GPIO-04":
        return "subcases=GPIO-04-AAB; " + "; ".join(extract_lines(block, "GPIO04_CONSEC"))
    if case_id == "GPIO-05":
        phases = extract_lines(block, "GPIO05_PHASE")
        reset_high = extract_lines(block, "GPIO05_RESET_HIGH")
        return "subcases=GPIO-05-PHASE2,GPIO-05-PHASE3,GPIO-05-PHASE7,GPIO-05-PHASE8,GPIO-05-RESET-HIGH; " + "; ".join(phases + reset_high)
    return block.strip().replace("\n", "; ")


def build_case_expected(case: dict, width: int) -> str:
    return case["expected"] + " Configuration W=" + str(width) + "."


def build_case_purpose(case: dict, width: int) -> str:
    return case["purpose"] + " Configuration W=" + str(width) + "."


def last_json_line(text: str):
    for line in reversed([x.strip() for x in text.splitlines() if x.strip()]):
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return None


def verify_plan_gate(plan_path: Path, hash_path: Path, pkg: Path, module_root: Path,
                     log_path: Path) -> dict:
    """Verify frozen plan and all three artifacts before any DUT command."""
    plan_expected = ""
    plan_actual = ""
    artifact_lines: list[str] = []
    plan = None
    ok = False
    reason = ""
    cap_line = ""
    try:
        plan_actual = sha256(plan_path)
        hash_text = hash_path.read_text(encoding="utf-8-sig").strip()
        parts = hash_text.split()
        if not parts:
            raise RunnerError("plan hash file is empty")
        plan_expected = parts[0].upper()
        if not re.fullmatch(r"[0-9A-F]{64}", plan_expected):
            raise RunnerError("plan hash file does not start with a SHA256")
        if plan_expected != plan_actual:
            raise RunnerError("PLAN_HASH_MISMATCH expected=%s actual=%s" % (plan_expected, plan_actual))
        plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
        if not isinstance(plan, dict):
            raise RunnerError("plan JSON is not an object")
        conf = plan.get("expected_per_configuration", {})
        max_cycles = int(conf.get("max_cycles", -1))
        hard_max = int(conf.get("hard_max_cycles", -1))
        cap_line = "PLAN_MAX_CYCLES=%d PLAN_HARD_MAX_CYCLES=%d TB_HARD_CAP=%d" % (
            max_cycles, hard_max, TB_HARD_CAP)
        if hard_max < 2 or max_cycles < 2 or max_cycles > hard_max:
            raise RunnerError("plan cycle limits are inconsistent")
        if hard_max > TB_HARD_CAP:
            raise RunnerError("plan hard_max_cycles exceeds TB hard cap")
        all_artifacts = True
        for key in ("rtl", "tb", "negative_tb"):
            info = plan.get("artifacts", {}).get(key)
            if not isinstance(info, dict) or not isinstance(info.get("path"), str):
                raise RunnerError("plan artifact %s is missing or malformed" % key)
            try:
                art_path = resolve_under(pkg, info["path"], "artifact " + key, must_exist=True)
                try:
                    art_path.relative_to(module_root.resolve())
                except ValueError as exc:
                    raise RunnerError("artifact %s is outside the GPIO module root" % key) from exc
                actual = sha256(art_path)
                match = actual == str(info.get("sha256", "")).upper()
                all_artifacts = all_artifacts and match
                artifact_lines.append(
                    "ARTIFACT key=%s path=%s resolved=%s expected=%s actual=%s match=%s"
                    % (key, info["path"], rel_to_pkg(art_path, pkg), info.get("sha256", ""), actual,
                       "YES" if match else "NO")
                )
            except Exception as exc:
                all_artifacts = False
                artifact_lines.append(
                    "ARTIFACT key=%s path=%s ERROR=%s match=NO"
                    % (key, info.get("path", "<missing>"), str(exc))
                )
        if not all_artifacts:
            raise RunnerError("ARTIFACT_HASH_OR_PATH_MISMATCH")
        ok = True
        reason = ""
    except Exception as exc:
        ok = False
        reason = str(exc)
    log_text = (
        "PLAN_PATH=" + (rel_to_pkg(plan_path, pkg) if plan_path.exists() else str(plan_path)) + "\n"
        + "PLAN_SHA256_EXPECTED=" + plan_expected + "\n"
        + "PLAN_SHA256_ACTUAL=" + plan_actual + "\n"
        + "PLAN_HASH_MATCH=" + ("YES" if plan_expected and plan_expected == plan_actual else "NO") + "\n"
        + cap_line + "\n"
        + "\n".join(artifact_lines) + "\n"
        + "DUT_STARTED=NO\n"
        + "PLAN_CHECK=" + ("PASS" if ok else "FAIL") + "\n"
        + "ABORT_REASON=" + reason + "\n"
    )
    write_text(log_path, log_text)
    return {
        "ok": ok,
        "reason": reason,
        "plan": plan,
        "expected": plan_expected,
        "actual": plan_actual,
        "hash_match": bool(plan_expected) and plan_expected == plan_actual,
        "artifacts_ok": bool(ok),
        "log": log_path,
        "dut_started": False,
        "cap_line": cap_line,
        "artifact_lines": artifact_lines,
    }


def archive_previous_results(results_path: Path, archive_dir: Path, pkg: Path) -> Optional[str]:
    if not results_path.exists():
        return None
    try:
        old = json.loads(results_path.read_text(encoding="utf-8-sig"))
        old_run = str(old.get("run_id", "previous")).replace("/", "_").replace("\\", "_")
    except Exception:
        old_run = "previous"
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / ("results-%s.json" % old_run)
    suffix = 0
    while dest.exists():
        suffix += 1
        dest = archive_dir / ("results-%s-%d.json" % (old_run, suffix))
    dest.write_bytes(results_path.read_bytes())
    return rel_to_pkg(dest, pkg)


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package-root", default=os.environ.get("GPIO_PACKAGE_ROOT", str(DEFAULT_PKG)),
                    help="explicit package root containing work/peripherals/gpio")
    ap.add_argument("--plan", default=DEFAULT_PLAN, help="relative plan path under the GPIO module")
    ap.add_argument("--plan-hash", default=None, help="relative plan hash path under the GPIO module")
    ap.add_argument("--out-root", default=DEFAULT_OUT_ROOT,
                    help="relative output root under the GPIO module (default: module root)")
    ap.add_argument("--iverilog", default=str(DEFAULT_IVERILOG), help="explicit iverilog executable")
    ap.add_argument("--vvp", default=str(DEFAULT_VVP), help="explicit vvp executable")
    ap.add_argument("--ivl-lib", default=str(DEFAULT_IVL_LIB), help="explicit Icarus ivl library directory")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    global CURRENT_PKG
    args = parse_args(argv)
    pkg = Path(args.package_root).resolve()
    CURRENT_PKG = pkg
    if not (pkg / "work" / "peripherals" / "gpio").is_dir():
        print("TOOL_ERROR package root does not contain work/peripherals/gpio: " + str(pkg))
        return 2

    try:
        plan_path = resolve_under(ROOT, args.plan, "plan", must_exist=True)
        default_hash = plan_path.with_suffix(".sha256").relative_to(ROOT.resolve()).as_posix()
        hash_path = resolve_under(ROOT, args.plan_hash or default_hash, "plan hash", must_exist=True)
        out_root = resolve_under(ROOT, args.out_root, "output root") if args.out_root else ROOT.resolve()
        out_root.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        print("TOOL_ERROR path preflight failed: " + str(exc))
        return 2

    run_id = datetime.now().strftime("gpio-%Y%m%d-%H%M%S")
    suffix = 0
    while (out_root / "logs" / run_id).exists() or (out_root / "waves" / run_id).exists():
        suffix += 1
        run_id = datetime.now().strftime("gpio-%Y%m%d-%H%M%S") + "-" + str(suffix)
    log_dir = out_root / "logs" / run_id
    wave_dir = out_root / "waves" / run_id
    log_dir.mkdir(parents=True, exist_ok=False)
    wave_dir.mkdir(parents=True, exist_ok=False)
    plan_log = log_dir / "plan_check.log"

    gate = verify_plan_gate(plan_path, hash_path, pkg, ROOT, plan_log)
    manifest = {
        "run_id": run_id,
        "generated_at": now(),
        "package_root": str(pkg),
        "plan_path": rel_to_pkg(plan_path, pkg),
        "plan_sha256": gate["actual"],
        "gate": {
            "status": "PASS" if gate["ok"] else "FAIL",
            "reason": gate["reason"],
            "hash_match": gate["hash_match"],
            "artifacts_ok": gate["artifacts_ok"],
            "dut_started": False,
            "log": rel_to_pkg(plan_log, pkg),
        },
        "tools": {},
        "configs": {},
        "negative": {},
        "watchdog": {},
        "schema_validate": {},
        "results": None,
        "archived_previous_results": None,
    }

    if not gate["ok"]:
        manifest["aborted"] = True
        manifest["abort_reason"] = gate["reason"]
        write_text(log_dir / "run_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        print("RUN_ID=" + run_id)
        print("PLAN_CHECK=FAIL")
        print("ABORTED_PLAN_CHECK=" + gate["reason"])
        print("DUT_STARTED=NO")
        print("MANIFEST=" + rel_to_pkg(log_dir / "run_manifest.json", pkg))
        return 2

    plan = gate["plan"]
    iverilog = Path(args.iverilog).resolve()
    vvp = Path(args.vvp).resolve()
    ivl_lib = Path(args.ivl_lib).resolve()
    tool_errors = []
    if not iverilog.is_file():
        tool_errors.append("iverilog missing: " + str(iverilog))
    if not vvp.is_file():
        tool_errors.append("vvp missing: " + str(vvp))
    if not ivl_lib.is_dir():
        tool_errors.append("ivl library missing: " + str(ivl_lib))
    if tool_errors:
        write_text(log_dir / "tool_preflight.log", "\n".join(tool_errors) + "\n")
        manifest["aborted"] = True
        manifest["abort_reason"] = "TOOL_PREFLIGHT_FAIL"
        manifest["tool_preflight"] = tool_errors
        manifest["tool_preflight_log"] = rel_to_pkg(log_dir / "tool_preflight.log", pkg)
        write_text(log_dir / "run_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        print("RUN_ID=" + run_id)
        print("PLAN_CHECK=PASS")
        print("TOOL_ERROR=" + "; ".join(tool_errors))
        print("DUT_STARTED=NO")
        return 2

    # Tool version queries are evidence only; they are not a compile/run PASS.
    tool_logs = []
    for name, qargv in (
        ("iverilog", [iverilog, "-V"]),
        ("vvp", [vvp, "-V"]),
        ("python", [PYTHON, "--version"]),
    ):
        p = log_dir / ("tool_" + name + ".log")
        r = run_cmd(qargv, ROOT, 10, p)
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
            "legal_source": "Existing lawful local Icarus installation; explicit path %s; PATH unchanged." % iverilog,
        },
        {
            "name": "Icarus Verilog (vvp)",
            "version": vvp_version,
            "legal_source": "Existing lawful local Icarus installation; explicit path %s; PATH unchanged." % vvp,
        },
        {
            "name": "Python (runner/results only)",
            "version": sys.version.split()[0],
            "legal_source": "Existing local Python; explicit executable %s; standard library only." % PYTHON,
        },
    ]
    manifest["tools"] = {
        "iverilog": str(iverilog),
        "vvp": str(vvp),
        "ivl_lib": str(ivl_lib),
        "python": str(PYTHON),
        "versions": {"iverilog": iverilog_version, "vvp": vvp_version, "python": sys.version.split()[0]},
        "version_logs": [rel_to_pkg(p, pkg) for _n, _r, p in tool_logs],
    }

    expected_by_width = {
        int(k): {"writes": int(v["writes"]), "compares": int(v["compares"])}
        for k, v in plan["expected_per_configuration"]["by_width"].items()
    }
    if set(expected_by_width) != set(CONFIGS):
        print("TOOL_ERROR plan does not define exactly W=1/8/16")
        return 2

    config_results = {}
    dut_started = False
    for width in CONFIGS:
        vvp_rel = "waves/%s/gpio_W%d.vvp" % (run_id, width)
        vcd_rel = "waves/%s/gpio_W%d.vcd" % (run_id, width)
        compile_argv = [
            iverilog, "-B", ivl_lib, "-g2012", "-Wall", "-s", "tb_gpio",
            "-DGPIO_W=%d" % width, "-o", vvp_rel,
            "src/gpio_core.v", "tb/tb_gpio.sv",
        ]
        compile_log = log_dir / ("compile_W%d.log" % width)
        compile_res = run_cmd(compile_argv, ROOT, 60, compile_log)
        run_argv = [vvp, "-N", "-M-", "-M" + str(ivl_lib), vvp_rel, "+WAVE_FILE=" + vcd_rel]
        run_log = log_dir / ("run_W%d.log" % width)
        run_res = None
        status = "TOOL_ERROR"
        reason = ""
        if compile_res["timed_out"]:
            reason = "compile timeout"
        elif not compile_res["ok"]:
            reason = "compile failed rc=%s" % compile_res["returncode"]
        else:
            run_res = run_cmd(run_argv, ROOT, 30, run_log)
            dut_started = True
            expected = expected_by_width[width]
            status, reason = classify_main(
                run_res["combined"], width, expected["writes"], expected["compares"],
                run_res["returncode"], run_res["timed_out"],
                run_res["log_truncated"],
            )
        vcd_path = ROOT / vcd_rel
        vcd_size = vcd_path.stat().st_size if vcd_path.exists() else 0
        config_results[width] = {
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
            "status": status,
            "reason": reason,
        }
        manifest["configs"][str(width)] = {
            "compile_command": [str(x) for x in compile_argv],
            "compile_log": rel_to_pkg(compile_log, pkg),
            "compile_rc": compile_res["returncode"],
            "compile_timed_out": compile_res["timed_out"],
            "compile_cleanup_s": compile_res["cleanup_s"],
            "compile_duration_s": compile_res["duration_s"],
            "run_command": [str(x) for x in run_argv],
            "run_log": rel_to_pkg(run_log, pkg),
            "run_rc": None if run_res is None else run_res["returncode"],
            "run_timed_out": None if run_res is None else run_res["timed_out"],
            "run_cleanup_s": None if run_res is None else run_res["cleanup_s"],
            "run_duration_s": None if run_res is None else run_res["duration_s"],
            "status": status,
            "reason": reason,
            "vcd": vcd_rel,
            "vcd_bytes": vcd_size,
            "expected_writes": expected_by_width[width]["writes"],
            "expected_compares": expected_by_width[width]["compares"],
        }

    # Negative checker is isolated from the formal TB.
    neg_vvp = "waves/%s/gpio_neg.vvp" % run_id
    neg_compile_argv = [
        iverilog, "-B", ivl_lib, "-g2012", "-Wall", "-s", "tb_gpio_neg",
        "-o", neg_vvp, "src/gpio_core.v", "tb/tb_gpio_neg.sv",
    ]
    neg_compile_log = log_dir / "compile_neg.log"
    neg_compile = run_cmd(neg_compile_argv, ROOT, 60, neg_compile_log)
    neg_run_argv = [vvp, "-N", "-M-", "-M" + str(ivl_lib), neg_vvp]
    neg_run_log = log_dir / "run_neg.log"
    neg_run = None
    neg_status = "TOOL_ERROR"
    neg_reason = ""
    if neg_compile["timed_out"]:
        neg_reason = "compile timeout"
    elif not neg_compile["ok"]:
        neg_reason = "negative compile failed rc=%s" % neg_compile["returncode"]
    else:
        neg_run = run_cmd(neg_run_argv, ROOT, 30, neg_run_log)
        dut_started = True
        neg_status, neg_reason = classify_neg(neg_run["combined"], neg_run["returncode"], neg_run["timed_out"], neg_run["log_truncated"])
    manifest["negative"] = {
        "compile_command": [str(x) for x in neg_compile_argv],
        "compile_log": rel_to_pkg(neg_compile_log, pkg),
        "compile_rc": neg_compile["returncode"],
        "run_command": [str(x) for x in neg_run_argv],
        "run_log": rel_to_pkg(neg_run_log, pkg),
        "run_rc": None if neg_run is None else neg_run["returncode"],
        "run_timed_out": None if neg_run is None else neg_run["timed_out"],
        "run_cleanup_s": None if neg_run is None else neg_run["cleanup_s"],
        "status": neg_status,
        "reason": neg_reason,
    }

    # Deliberate TB watchdog test on W=8; expected TIMEOUT, not PASS.
    wd_log = log_dir / "run_watchdog.log"
    wd_argv = [
        vvp, "-N", "-M-", "-M" + str(ivl_lib),
        "waves/%s/gpio_W8.vvp" % run_id, "+HANG", "+MAX_CYCLES=200",
    ]
    wd_res = None
    wd_status = "TOOL_ERROR"
    wd_mechanism_ok = False
    wd_reason = ""
    if config_results[8]["compile"]["ok"]:
        wd_res = run_cmd(wd_argv, ROOT, 30, wd_log)
        dut_started = True
        wd_status, wd_mechanism_ok, wd_reason = classify_watchdog(
            wd_res["combined"], wd_res["returncode"], wd_res["timed_out"], wd_res["log_truncated"])
    else:
        wd_reason = "W=8 compile failed; watchdog not executed"
    manifest["watchdog"] = {
        "command": [str(x) for x in wd_argv],
        "log": rel_to_pkg(wd_log, pkg),
        "status": wd_status,
        "mechanism_ok": wd_mechanism_ok,
        "reason": wd_reason,
        "rc": None if wd_res is None else wd_res["returncode"],
        "timed_out": None if wd_res is None else wd_res["timed_out"],
        "cleanup_s": None if wd_res is None else wd_res["cleanup_s"],
    }

    # Build result rows from actual logs only.
    plan_sha = gate["actual"]
    rows = []
    for width in CONFIGS:
        c = config_results[width]
        status = c["status"]
        log_paths = [c["compile_log"]]
        if c["run_log"].exists():
            log_paths.append(c["run_log"])
        wave_paths = [c["vcd_path"]] if c["vcd_size"] > 0 else []
        for case in plan["cases"]:
            if case["id"] not in MAIN_CASE_IDS:
                continue
            if ("W%d" % width) not in case.get("configs", []):
                continue
            case_id = case["id"]
            case_status = status
            if status == "PASS":
                actual = build_config_actual(case_id, width, c["run"]["combined"])
                if actual.startswith("MISSING"):
                    case_status = "FAIL"
            elif status == "TIMEOUT":
                actual = "watchdog/timeout observed before completion: " + (
                    extract_stats(c["run"]["combined"] if c["run"] else ""))
            elif status == "TOOL_ERROR":
                actual = "compile/tool failure; test case not executed: " + c["reason"]
            else:
                fails = [
                    x.strip() for x in (c["run"]["combined"] if c["run"] else "").splitlines()
                    if "CHK_FAIL" in x or "TEST_FAIL" in x or "GPIO_SELFCHECK_FAIL" in x
                ]
                actual = "failure markers: " + "; ".join(fails[:12]) + "; reason=" + c["reason"]
            cmd = command_dict(c["run_argv"] if c["run"] else c["compile_argv"], 30 if c["run"] else 60)
            dur = c["run"]["duration_s"] if c["run"] else c["compile"]["duration_s"]
            rows.append(make_row(
                case_id + "-W%d" % width, case_id,
                build_case_purpose(case, width), build_case_expected(case, width),
                case_status, actual, dur, cmd, log_paths, wave_paths, plan_sha, pkg,
            ))

    # GPIO-06 negative proof at W=8.
    if neg_status == "PASS":
        neg_actual = "; ".join([
            x.strip() for x in (neg_run["combined"] if neg_run else "").splitlines()
            if x.strip().startswith("NEG_") or x.strip().startswith("GPIO_NEG_")
        ])
    elif neg_status == "TIMEOUT":
        neg_actual = "negative TB timeout: " + neg_reason
    elif neg_compile["ok"]:
        neg_actual = "negative checker did not report the expected control+detection markers: " + neg_reason
    else:
        neg_actual = "negative TB compile failed; checker not executed: " + neg_reason
    neg_logs = [neg_compile_log]
    if neg_run_log.exists():
        neg_logs.append(neg_run_log)
    rows.append(make_row(
        "GPIO-06-W8", "GPIO-06",
        "independent checker negative proof at W=8",
        "Control expectation passes. A deliberately wrong hold expectation (A5 instead of 5A while wr_en=0) is detected, and a deliberately wrong one-edge synchronizer expectation is detected. Formal DUT expectations unchanged.",
        neg_status, neg_actual,
        (neg_run["duration_s"] if neg_run else neg_compile["duration_s"]),
        command_dict(neg_run_argv if neg_run else neg_compile_argv, 30 if neg_run else 60),
        neg_logs, [], plan_sha, pkg,
        limitations=[
            "Negative proof is isolated in tb_gpio_neg.sv and runs at W=8 only.",
            "It proves the external checker can reject a wrong hold value and a wrong one-edge sync expectation; it does not test every possible checker mutation.",
            "Simulation-only; no hardware/PDS/metastability proof.",
        ],
    ))

    rows.append(make_row(
        "COM-01-PLAN", "COM-01",
        "frozen expectation and artifact hash check before final DUT runs",
        "Plan SHA256 matches tests/gpio-plan.sha256; RTL, formal TB and negative TB hashes match the frozen plan; DUT is not started on mismatch.",
        "PASS" if gate["ok"] else "FAIL",
        "PLAN_SHA256_EXPECTED=%s; PLAN_SHA256_ACTUAL=%s; %s; PLAN_CHECK=%s; GATE_DUT_STARTED=NO" % (
            gate["expected"], gate["actual"], "; ".join(gate["artifact_lines"]),
            "PASS" if gate["ok"] else "FAIL"),
        time.monotonic() - time.monotonic(), command_dict([PYTHON, "scripts/run_gpio.py"], 120),
        [plan_log], [], plan_sha, pkg,
        limitations=["This row proves plan/artifact identity only; it does not prove DUT functionality."],
    ))

    if wd_status == "TIMEOUT":
        wd_line = "; ".join(
            x.strip() for x in (wd_res["combined"] if wd_res else "").splitlines()
            if "TB_WATCHDOG_TIMEOUT" in x
        )
        wd_actual = "%s; expected watchdog termination; mechanism_ok=%s; rc=%s; timed_out=%s; cleanup_s=%s" % (
            wd_line, wd_mechanism_ok, None if wd_res is None else wd_res["returncode"],
            None if wd_res is None else wd_res["timed_out"],
            None if wd_res is None else wd_res["cleanup_s"])
    elif wd_res is None:
        wd_actual = "W=8 compile failed; watchdog not executed"
    else:
        wd_actual = "watchdog marker not observed: " + wd_reason
    rows.append(make_row(
        "COM-02-WATCHDOG", "COM-02",
        "bounded run and TB cycle watchdog",
        "Compile/run process limits are 60 s/30 s; deliberate +HANG with MAX_CYCLES=200 emits TB_WATCHDOG_TIMEOUT on the 200th posedge and is classified TIMEOUT.",
        wd_status, wd_actual,
        (wd_res["duration_s"] if wd_res else config_results[8]["compile"]["duration_s"]),
        command_dict(wd_argv if wd_res else config_results[8]["compile_argv"], 30 if wd_res else 60),
        [wd_log] if wd_res else [config_results[8]["compile_log"]], [], plan_sha, pkg,
        limitations=["The deliberate watchdog test proves bounded termination, not functional correctness."],
    ))

    stats = []
    no_fail = True
    for width in CONFIGS:
        c = config_results[width]
        if c["run"] is not None:
            stats.append("W%d: %s" % (width, extract_stats(c["run"]["combined"])))
            if any(x in c["run"]["combined"] for x in ("CHK_FAIL", "TEST_FAIL", "GPIO_SELFCHECK_FAIL")):
                no_fail = False
    com3_status = "PASS" if all(config_results[w]["status"] == "PASS" for w in CONFIGS) and no_fail else "FAIL"
    com3_actual = "; ".join(stats) + (
        "; no X/Z or CHK_FAIL in completed runs" if com3_status == "PASS" else "")
    rows.append(make_row(
        "COM-03-TOPLEVEL", "COM-03",
        "public-port X/Z, comparison and write observations",
        "gpio_out and gpio_in_sync are checked for X/Z; writes and comparisons are counted; no CHK_FAIL is observed.",
        com3_status, com3_actual,
        (config_results[8]["run"]["duration_s"] if config_results[8]["run"] else config_results[8]["compile"]["duration_s"]),
        command_dict(config_results[8]["run_argv"] if config_results[8]["run"] else config_results[8]["compile_argv"], 30),
        [config_results[w]["run_log"] for w in CONFIGS if config_results[w]["run_log"].exists()],
        [], plan_sha, pkg,
        limitations=["Only public ports are observed; no internal-node X/Z claim is made."],
    ))

    vcd_lines = []
    all_vcd = True
    for width in CONFIGS:
        c = config_results[width]
        vcd_lines.append("W%d VCD=%s bytes=%d" % (width, rel_to_pkg(c["vcd_path"], pkg), c["vcd_size"]))
        all_vcd = all_vcd and c["vcd_size"] > 0
    com4_status = "PASS" if all_vcd and all(config_results[w]["status"] == "PASS" for w in CONFIGS) else "FAIL"
    com4_actual = "; ".join(vcd_lines) + "; GPIO_SELFCHECK_PASS markers require exact writes/compares and native exit 0"
    rows.append(make_row(
        "COM-04-ARTIFACTS", "COM-04",
        "fresh logs, non-empty VCDs and independent success markers",
        "New run directory contains new compile/run logs and non-empty VCDs; each configuration ends with GPIO_SELFCHECK_PASS and the exact expected write/compare counts.",
        com4_status, com4_actual,
        (config_results[8]["run"]["duration_s"] if config_results[8]["run"] else config_results[8]["compile"]["duration_s"]),
        command_dict(config_results[8]["run_argv"] if config_results[8]["run"] else config_results[8]["compile_argv"], 30),
        [config_results[w]["run_log"] for w in CONFIGS if config_results[w]["run_log"].exists()],
        [config_results[w]["vcd_path"] for w in CONFIGS if config_results[w]["vcd_size"] > 0],
        plan_sha, pkg,
        limitations=["VCDs are normal Icarus dumps of the testbench; they do not replace the frozen expected values or the checker."],
    ))

    com5_status = "PASS" if neg_status == "PASS" else neg_status
    rows.append(make_row(
        "COM-05-NEGATIVE", "COM-05",
        "negative checker isolation and expected detection",
        "A deliberately wrong held value and a wrong one-edge synchronizer expectation are rejected by the independent checker; formal DUT expectations are not changed.",
        com5_status, neg_actual,
        (neg_run["duration_s"] if neg_run else neg_compile["duration_s"]),
        command_dict(neg_run_argv if neg_run else neg_compile_argv, 30 if neg_run else 60),
        neg_logs, [], plan_sha, pkg,
        limitations=["Negative proof is separate from the formal TB and is intentionally expected to detect errors."],
    ))

    schema_log = log_dir / "schema_validate.log"
    schema_script = pkg / "scripts" / "schema_validate.py"
    schema_file = pkg / "templates" / "results.schema.json"
    schema_argv = [PYTHON, schema_script, "--schema", schema_file, "--data", out_root / "results.json"]
    com6_row = make_row(
        "COM-06-STATUS", "COM-06",
        "ACTUAL status, unique IDs, limitations and schema validation",
        "results.json is ACTUAL, schema-valid, uses PASS/FAIL/TIMEOUT/TOOL_ERROR/NOT_RUN, has unique IDs, and records finite coverage/limitations.",
        "PASS",
        "kind=ACTUAL; schema_check=PENDING; unique_ids=%d; limitations=%d" % (
            len(rows) + 1, len(plan.get("limitations", []))),
        0.0, command_dict(schema_argv, 30), [schema_log], [], plan_sha, pkg,
        limitations=["This row is filled only after the schema validator runs; the validator checks structure/semantics, not DUT functionality."],
    )
    rows.append(com6_row)
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate result IDs before writing")

    results = {
        "kind": "ACTUAL",
        "run_id": run_id,
        "generated_at": now(),
        "task_id": "B-GPIO",
        "module_version": "1.0.0",
        "interface_version": "PERIPH-CORE-0.1-DRAFT",
        "tools": tools,
        "tests": rows,
        "limitations": list(plan.get("limitations", [])),
        "issues": [
            "Hardware remains stopped; no PDS/JTAG/download/Flash/board pin/temperature work was performed.",
            "PERIPH-CORE-0.1-DRAFT is still not a mainline-approved interface; no B-REGIF work or address map is claimed.",
            "GPIO is kept under work/peripherals/gpio so the earlier B-UART-TX root snapshot and its hash manifest remain unchanged.",
            "Runner 1.0.2 gates plan/artifact hashes before DUT start, requires native exit status and exact counts, bounds process-tree cleanup, and makes tool/package roots explicit.",
            "The existing package has no Git repository; source/plan/log hashes and this ACTUAL result are the version identity.",
        ],
    }
    results_path = out_root / "results.json"
    manifest["archived_previous_results"] = archive_previous_results(results_path, ROOT / "tests" / "archive", pkg)
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def validate_once() -> tuple[bool, Optional[dict], dict]:
        write_text(schema_log, "")
        r = run_cmd(schema_argv, ROOT, 30, schema_log)
        parsed = last_json_line(r["stdout"])
        return (r["returncode"] == 0 and bool(parsed) and parsed.get("schema_check") == "PASS"), parsed, r

    pass1, parsed1, v1 = validate_once()
    if pass1:
        com6_row["status"] = "PASS"
        com6_row["actual"] = "kind=ACTUAL; schema_check=PASS; unique_ids=%d; limitations=%d; %s" % (
            len(rows), len(plan.get("limitations", [])), json.dumps(parsed1, ensure_ascii=False))
        com6_row["duration_s"] = v1["duration_s"]
    else:
        com6_row["status"] = "FAIL"
        com6_row["actual"] = "schema_check=FAIL; " + (
            json.dumps(parsed1, ensure_ascii=False) if parsed1 else (v1["stdout"] + v1["stderr"])[:2000])
        com6_row["duration_s"] = v1["duration_s"]
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pass2, parsed2, v2 = validate_once()
    if not pass2 and com6_row["status"] == "PASS":
        com6_row["status"] = "FAIL"
        com6_row["actual"] = "schema_check=FAIL after final write; " + (
            json.dumps(parsed2, ensure_ascii=False) if parsed2 else (v2["stdout"] + v2["stderr"])[:2000])
        results_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        pass3, parsed3, v3 = validate_once()
        if pass3:
            com6_row["status"] = "PASS"
            com6_row["actual"] = "kind=ACTUAL; schema_check=PASS; unique_ids=%d; limitations=%d; %s" % (
                len(rows), len(plan.get("limitations", [])), json.dumps(parsed3, ensure_ascii=False))
        pass2, parsed2, v2 = pass3, parsed3, v3
        results_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest["schema_validate"] = {
        "command": [str(x) for x in schema_argv],
        "log": rel_to_pkg(schema_log, pkg),
        "first": parsed1,
        "final": parsed2,
        "status": "PASS" if (pass2 and com6_row["status"] == "PASS") else "FAIL",
    }
    manifest["dut_started"] = dut_started
    manifest["results"] = rel_to_pkg(results_path, pkg)
    manifest["aborted"] = False
    write_text(log_dir / "run_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    print("RUN_ID=" + run_id)
    print("PLAN_CHECK=" + ("PASS" if gate["ok"] else "FAIL"))
    for width in CONFIGS:
        print("W%d_STATUS=%s" % (width, config_results[width]["status"]))
    print("NEG_STATUS=" + neg_status)
    print("WATCHDOG_STATUS=" + wd_status)
    print("WATCHDOG_MECHANISM_OK=" + str(wd_mechanism_ok))
    print("DUT_STARTED=" + str(dut_started))
    print("SCHEMA_CHECK=" + ("PASS" if pass2 and com6_row["status"] == "PASS" else "FAIL"))
    print("RESULTS=" + rel_to_pkg(results_path, pkg))
    print("MANIFEST=" + rel_to_pkg(log_dir / "run_manifest.json", pkg))
    return 0 if (
        gate["ok"]
        and all(config_results[w]["status"] == "PASS" for w in CONFIGS)
        and neg_status == "PASS"
        and wd_status == "TIMEOUT"
        and wd_mechanism_ok
        and pass2
        and com6_row["status"] == "PASS"
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
