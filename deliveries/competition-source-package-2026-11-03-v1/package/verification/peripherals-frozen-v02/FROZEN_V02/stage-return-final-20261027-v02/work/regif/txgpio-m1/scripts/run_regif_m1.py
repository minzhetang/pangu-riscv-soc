#!/usr/bin/env python3
"""Bounded runner for LOCAL-REGIF-TXGPIO-M1 packaging tests."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # work/regif/txgpio-m1
PKG = ROOT.parent.parent.parent                        # package root
sys.path.insert(0, str(PKG / "work" / "peripherals" / "scripts"))
from runner_common import run_process

IVERILOG = Path(r"D:\iverilog\bin\iverilog.exe")
VVP = Path(r"D:\iverilog\bin\vvp.exe")
IVL_LIB = Path(r"D:\iverilog\lib\ivl")
PYTHON = Path(sys.executable)

PLAN = ROOT / "tests" / "w01-w10-plan-1.0.5.json"
PLAN_HASH = ROOT / "tests" / "w01-w10-plan-1.0.5.sha256"
RESULTS = ROOT / "results.json"
WRAPPER = ROOT / "src" / "local_regif_txgpio_m1.v"
TB = ROOT / "tb" / "tb_local_regif_txgpio_m1.sv"
TX = PKG / "work" / "peripherals" / "src" / "uart_tx.v"
GPIO = PKG / "work" / "peripherals" / "gpio" / "src" / "gpio_core.v"
HARD_CAP = 1_000_000
CONFIGS = (16, 234)
ALL_CASES = ("W01", "W02", "W03", "W04", "W05", "W06", "W07", "W08", "W09", "W10")
N234_CASES = ("W05", "W06", "W09")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper() if path.exists() else "MISSING"


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def command_dict(argv, timeout_s: int) -> dict:
    return {"argv": [str(x) for x in argv], "cwd": str(ROOT.relative_to(PKG)), "executed": True, "timeout_s": timeout_s}


def expected_markers(n: int):
    cases = N234_CASES if n == 234 else ALL_CASES
    return tuple(case + ("-N234" if n == 234 else "") for case in cases)


def analyze_markers(text: str, n: int):
    """Require the exact, unique TEST_BEGIN/TEST_PASS set and one global PASS."""
    text = text.lstrip("\ufeff")
    errors = []
    expected = list(expected_markers(n))
    begins = re.findall(r"^TEST_BEGIN ([^ \r\n]+)\s*$", text, re.MULTILINE)
    passes = re.findall(r"^TEST_PASS ([^ \r\n]+)\s*$", text, re.MULTILINE)
    for marker in expected:
        if begins.count(marker) != 1:
            errors.append("TEST_BEGIN %s count=%d expected=1" % (marker, begins.count(marker)))
        if passes.count(marker) != 1:
            errors.append("TEST_PASS %s count=%d expected=1" % (marker, passes.count(marker)))
        if marker in begins and marker in passes:
            if text.find("TEST_BEGIN " + marker) > text.find("TEST_PASS " + marker):
                errors.append("TEST_PASS %s appears before TEST_BEGIN" % marker)
    for marker in sorted(set(begins) | set(passes)):
        if marker not in expected:
            errors.append("unexpected TEST marker %s" % marker)
    if len(begins) != len(expected):
        errors.append("TEST_BEGIN total=%d expected=%d" % (len(begins), len(expected)))
    if len(passes) != len(expected):
        errors.append("TEST_PASS total=%d expected=%d" % (len(passes), len(expected)))
    global_pass = re.findall(r"^REGIF_M1_SELFCHECK_PASS\b.*$", text, re.MULTILINE)
    if len(global_pass) != 1:
        errors.append("REGIF_M1_SELFCHECK_PASS count=%d expected=1" % len(global_pass))
    if re.search(r"^REGIF_M1_SELFCHECK_FAIL\b", text, re.MULTILINE):
        errors.append("REGIF_M1_SELFCHECK_FAIL present")
    for bad in ("CHK_FAIL", "TEST_FAIL", "REGIF_TB_WATCHDOG_TIMEOUT"):
        if bad in text:
            errors.append("%s present" % bad)
    return errors


REQ_RE = re.compile(
    r"^REGIF_REQ seq=(\d+) edge=(\d+) addr=([0-9a-fA-F]+) data=([0-9a-fA-F]+) "
    r"strb=([01]+) error=([01]) ready=([01]) busy=([01]) tx_accept=([01]) gpio_accept=([01])\s*$",
    re.MULTILINE,
)

# Manually frozen request-field sequence (not derived from a DUT run).  Edge is
# checked for the first request anchor and strict monotonic uniqueness; the
# field sequence is checked for every request.
EXPECTED_EDGES = {
    16: [9, 26, 29, 30, 37, 202, 203, 365, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 546, 554, 724, 794, 964, 1116],
    234: [6, 2349, 2350, 4692, 7040, 7048, 9398, 10340, 12690, 14804],
}

EXPECTED_REQUESTS = {
    16: [
        ("00", "5a", "1111", "1", "0", "reject"),
        ("0c", "a5", "1111", "0", "1", "gpio"),
        ("0c", "a5", "1111", "0", "1", "gpio"),
        ("0c", "5a", "1111", "0", "1", "gpio"),
        ("00", "5a", "1111", "0", "1", "tx"),
        ("00", "a5", "1111", "0", "1", "tx"),
        ("00", "3c", "1111", "1", "0", "reject"),
        ("00", "a5", "1111", "0", "1", "tx"),
        ("04", "01", "1111", "1", "1", "reject"),
        ("14", "02", "1111", "1", "1", "reject"),
        ("08", "03", "1111", "1", "1", "reject"),
        ("10", "04", "1111", "1", "1", "reject"),
        ("02", "05", "1111", "1", "1", "reject"),
        ("0c", "06", "0000", "1", "1", "reject"),
        ("0c", "07", "0001", "1", "1", "reject"),
        ("0c", "08", "0011", "1", "1", "reject"),
        ("00", "09", "1100", "1", "1", "reject"),
        ("0c", "11", "1111", "0", "1", "gpio"),
        ("0c", "11", "1111", "0", "1", "gpio"),
        ("0c", "22", "1111", "0", "1", "gpio"),
        ("00", "96", "1111", "0", "1", "tx"),
        ("00", "6a", "1111", "0", "1", "tx"),
        ("00", "96", "1111", "0", "1", "tx"),
        ("00", "6a", "1111", "0", "1", "tx"),
        ("00", "96", "1111", "0", "1", "tx"),
        ("00", "6a", "1111", "0", "1", "tx"),
    ],
    234: [
        ("00", "5a", "1111", "0", "1", "tx"),
        ("00", "a5", "1111", "0", "1", "tx"),
        ("00", "3c", "1111", "1", "0", "reject"),
        ("00", "a5", "1111", "0", "1", "tx"),
        ("00", "96", "1111", "0", "1", "tx"),
        ("00", "6a", "1111", "0", "1", "tx"),
        ("00", "96", "1111", "0", "1", "tx"),
        ("00", "6a", "1111", "0", "1", "tx"),
        ("00", "96", "1111", "0", "1", "tx"),
        ("00", "6a", "1111", "0", "1", "tx"),
    ],
}
TX_RE = re.compile(r"^REGIF_TX_FRAME event=(START|COMPLETE|CANCEL)(?: idx=\d+)? edge=(\d+)(?: data=([0-9a-fA-F]+))?(?: observed_edge=(\d+))?\s*$", re.MULTILINE)
GPIO_RE = re.compile(r"^REGIF_GPIO_ACCEPT seq=(\d+) edge=(\d+) data=([0-9a-fA-F]+)\s*$", re.MULTILINE)


def analyze_events(text: str, n: int):
    """Validate the actual public request/TX/GPIO ledger parsed from the run log."""
    text = text.lstrip("\ufeff")
    errors = []
    expected = {
        "N16": {
            "requests": 26, "tx_accept": 9, "gpio_accept": 6, "reject": 11,
            "complete": 6, "cancel": 3, "frames": 6,
            "tx_data": ["5a", "a5", "a5", "96", "6a", "96", "6a", "96", "6a"],
            "gpio_data": ["a5", "a5", "5a", "11", "11", "22"],
            "complete_data": ["5a", "a5", "a5", "6a", "6a", "6a"],
        },
        "N234": {
            "requests": 10, "tx_accept": 9, "gpio_accept": 0, "reject": 1,
            "complete": 6, "cancel": 3, "frames": 6,
            "tx_data": ["5a", "a5", "a5", "96", "6a", "96", "6a", "96", "6a"],
            "gpio_data": [],
            "complete_data": ["5a", "a5", "a5", "6a", "6a", "6a"],
        },
    }["N%d" % n]
    reqs = REQ_RE.findall(text)
    req_total = len(reqs)
    tx_accepts = [r[3].lower() for r in reqs if r[8] == "1"]
    gpio_accepts = [r[3].lower() for r in reqs if r[9] == "1"]
    rejects = [r for r in reqs if r[8] == "0" and r[9] == "0"]
    tx_events = TX_RE.findall(text)
    starts = [e for e in tx_events if e[0] == "START"]
    completes = [e for e in tx_events if e[0] == "COMPLETE"]
    cancels = [e for e in tx_events if e[0] == "CANCEL"]
    gpio_logs = GPIO_RE.findall(text)
    expected_rows = EXPECTED_REQUESTS[n]
    if req_total != expected["requests"]:
        errors.append("request ledger total=%d expected=%d" % (req_total, expected["requests"]))
    if req_total != len(expected_rows):
        errors.append("request rows=%d expected frozen=%d" % (req_total, len(expected_rows)))
    seen_edges = []
    expected_busy = {"N16": {7}, "N234": {3}}["N%d" % n]
    for idx, row in enumerate(reqs[:len(expected_rows)]):
        seq, edge, addr, data, strb, err, ready, busy, tx_accept, gpio_accept = row
        kind = "tx" if tx_accept == "1" else ("gpio" if gpio_accept == "1" else "reject")
        exp = expected_rows[idx]
        got = (addr.lower(), data.lower(), strb, err, ready, kind)
        if got != exp:
            errors.append("request seq=%s fields=%s expected=%s" % (seq, got, exp))
        expected_busy_bit = "1" if (idx + 1) in expected_busy else "0"
        if busy != expected_busy_bit:
            errors.append("request seq=%s busy=%s expected=%s" % (seq, busy, expected_busy_bit))
        if int(seq) != idx + 1:
            errors.append("request seq=%s expected=%d" % (seq, idx + 1))
        seen_edges.append(int(edge))
    first_edge_expected = 9 if n == 16 else 6
    if not seen_edges or seen_edges[0] != first_edge_expected:
        errors.append("first request edge=%s expected=%d" % (seen_edges[0] if seen_edges else "?", first_edge_expected))
    if seen_edges != EXPECTED_EDGES[n]:
        errors.append("request edge timeline=%s expected=%s" % (seen_edges, EXPECTED_EDGES[n]))
    if seen_edges != sorted(set(seen_edges)):
        errors.append("request edges not strictly increasing/unique")
    if "REGIF_TX_FRAME event=BAD_STOP" in text:
        errors.append("serial monitor detected BAD_STOP")
    if len(tx_accepts) != expected["tx_accept"]:
        errors.append("TX accept ledger=%d expected=%d" % (len(tx_accepts), expected["tx_accept"]))
    if tx_accepts != expected["tx_data"]:
        errors.append("TX accept data=%s expected=%s" % (",".join(tx_accepts), ",".join(expected["tx_data"])))
    if len(gpio_accepts) != expected["gpio_accept"]:
        errors.append("GPIO accept ledger=%d expected=%d" % (len(gpio_accepts), expected["gpio_accept"]))
    if gpio_accepts != expected["gpio_data"]:
        errors.append("GPIO accept data=%s expected=%s" % (",".join(gpio_accepts), ",".join(expected["gpio_data"])))
    if len(rejects) != expected["reject"]:
        errors.append("reject ledger=%d expected=%d" % (len(rejects), expected["reject"]))
    if len(starts) != expected["tx_accept"]:
        errors.append("TX START ledger=%d expected=%d" % (len(starts), expected["tx_accept"]))
    if len(completes) != expected["complete"]:
        errors.append("TX COMPLETE ledger=%d expected=%d" % (len(completes), expected["complete"]))
    if len(cancels) != expected["cancel"]:
        errors.append("TX CANCEL ledger=%d expected=%d" % (len(cancels), expected["cancel"]))
    if [e[2].lower() for e in completes] != expected["complete_data"]:
        errors.append("TX COMPLETE data=%s expected=%s" % (",".join(e[2].lower() for e in completes), ",".join(expected["complete_data"])))
    # Event edge and observe edge are distinct: event is the real accept/end
    # edge; observed is the next posedge where the public pin was sampled.
    for e in tx_events:
        if not e[3]:
            errors.append("TX %s edge=%s missing observed_edge" % (e[0], e[1]))
        elif int(e[3]) != int(e[1]) + 1:
            errors.append("TX %s event_edge=%s observed_edge=%s expected observed=edge+1" %
                          (e[0], e[1], e[3]))
    # START event edges must equal the accepted request edges, in order.
    tx_accept_rows = [(int(r[1]), r[3].lower()) for r in reqs if r[8] == "1"]
    start_rows = [(int(e[1]), e[3]) for e in starts]
    if len(start_rows) != len(tx_accept_rows):
        errors.append("TX START rows=%d accepted requests=%d" % (len(start_rows), len(tx_accept_rows)))
    else:
        for (sedge, _), (redge, rdata) in zip(start_rows, tx_accept_rows):
            if sedge != redge:
                errors.append("TX START edge=%d expected accept edge=%d data=%s" % (sedge, redge, rdata))
    # COMPLETE event edge must be exactly 10N after the START event edge.
    start_edges = {int(e[1]) for e in starts}
    for e in completes:
        if int(e[1]) - 10 * n not in start_edges:
            errors.append("TX COMPLETE event_edge=%s has no START at event_edge-10N" % e[1])
    # GPIO log seq/edge/data must match the accepted request ledger, one-to-one.
    accepted_gpio_rows = [(i + 1, int(r[1]), r[3].lower())
                          for i, r in enumerate([x for x in reqs if x[9] == "1"])]
    gpio_log_rows = [(int(g[0]), int(g[1]), g[2].lower()) for g in gpio_logs]
    if accepted_gpio_rows != gpio_log_rows:
        errors.append("GPIO log seq/edge/data=%s expected request-aligned=%s" % (gpio_log_rows, accepted_gpio_rows))
    m = re.search(r"REGIF_M1_SELFCHECK_PASS accepted_tx=(\d+) accepted_gpio=(\d+) rejected=(\d+) frames=(\d+) requests=(\d+) complete=(\d+) cancel=(\d+) bad_stop=(\d+)", text)
    if not m:
        errors.append("missing detailed REGIF_M1_SELFCHECK_PASS counters")
    else:
        got = dict(zip(("tx", "gpio", "reject", "frames", "requests", "complete", "cancel", "bad_stop"), map(int, m.groups())))
        if got != {"tx": expected["tx_accept"], "gpio": expected["gpio_accept"],
                   "reject": expected["reject"], "frames": expected["frames"],
                   "requests": expected["requests"], "complete": expected["complete"],
                   "cancel": expected["cancel"], "bad_stop": 0}:
            errors.append("summary counters=%s expected=%s" % (got, expected))
    return errors


def analyze_run(res, text: str, n: int):
    errors = []
    if res is None:
        return ["no run result"]
    if res.get("returncode") != 0:
        errors.append("native returncode=%s expected=0" % res.get("returncode"))
    if res.get("timed_out"):
        errors.append("process timed out")
    if res.get("log_truncated"):
        errors.append("log truncated")
    errors.extend(analyze_markers(text, n))
    errors.extend(analyze_events(text, n))
    return errors


def main() -> int:
    run_id = datetime.now().strftime("regif-m1-%Y%m%d-%H%M%S")
    log_dir = ROOT / "logs" / run_id
    wave_dir = ROOT / "waves" / run_id
    log_dir.mkdir(parents=True, exist_ok=True)
    wave_dir.mkdir(parents=True, exist_ok=True)
    plan = json.loads(PLAN.read_text(encoding="utf-8-sig"))
    plan_actual = sha256(PLAN)
    plan_expected = PLAN_HASH.read_text(encoding="ascii").split()[0].upper() if PLAN_HASH.exists() else ""
    plan_hash_ok = bool(plan_expected) and plan_expected == plan_actual
    artifacts = {
        "wrapper": WRAPPER,
        "tx": TX,
        "gpio": GPIO,
        "tb": TB,
        "tx_public_monitor": ROOT / "tb" / "regif_tx_public_monitor.sv",
    }
    expected_hashes = {
        "wrapper": plan["baseline"]["wrapper"]["sha256"],
        "tx": plan["baseline"]["tx_rtl"]["sha256"],
        "gpio": plan["baseline"]["gpio_rtl"]["sha256"],
        "tb": plan["baseline"]["tb"]["sha256"],
        "tx_public_monitor": plan["baseline"]["tx_public_monitor"]["sha256"],
    }
    artifact_lines = []
    artifact_ok = True
    for key, path in artifacts.items():
        actual = sha256(path)
        match = actual == expected_hashes[key]
        artifact_ok = artifact_ok and match
        artifact_lines.append("ARTIFACT %s path=%s expected=%s actual=%s match=%s" %
                              (key, path.relative_to(PKG), expected_hashes[key], actual, "YES" if match else "NO"))
    hard_cap = int(plan["limits"].get("hard_max_cycles", HARD_CAP))
    tb_max = int(plan["limits"].get("tb_max_cycles", 300000))
    plan_ok = plan_hash_ok and artifact_ok and 1 <= hard_cap <= HARD_CAP and 1 <= tb_max <= hard_cap
    plan_log = log_dir / "plan_check.log"
    plan_log.write_text(
        "PLAN_PATH=%s\nPLAN_SHA256_EXPECTED=%s\nPLAN_SHA256_ACTUAL=%s\nPLAN_HASH_MATCH=%s\n%s\nPLAN_CHECK=%s\n" %
        (PLAN.relative_to(PKG), plan_expected, plan_actual, "YES" if plan_hash_ok else "NO",
         "\n".join(artifact_lines), "PASS" if plan_ok else "FAIL"),
        encoding="utf-8", newline="\n")
    if not plan_ok:
        print("PLAN_CHECK=FAIL; no DUT compile/run")
        return 1

    tools = []
    for name, argv in (("iverilog", [IVERILOG, "-V"]), ("vvp", [VVP, "-V"]), ("python", [PYTHON, "--version"])):
        p = log_dir / ("tool_%s.log" % name)
        r = run_process(argv, ROOT, 10, p)
        m = re.search(r"Icarus Verilog (?:runtime )?version\s+([^\r\n]+)", r["combined"])
        if m:
            version = m.group(1).strip()
        else:
            m = re.search(r"Python\s+([^\r\n]+)", r["combined"])
            version = m.group(1).strip() if m else "UNVERIFIED"
        tools.append({"name": name, "version": version,
                      "legal_source": "Existing lawful local tool; explicit path, PATH unchanged."})

    rows = []
    config_results = {}
    for n in CONFIGS:
        vvp_rel = "waves/%s/regif_m1_N%d.vvp" % (run_id, n)
        vcd_rel = "waves/%s/regif_m1_N%d.vcd" % (run_id, n)
        compile_argv = [IVERILOG, "-B", IVL_LIB, "-g2012", "-Wall", "-s", "tb_local_regif_txgpio_m1",
                        "-DCLKS_PER_BIT=%d" % n, "-DTB_MAX_CYCLES=%d" % tb_max,
                        "-o", vvp_rel, "src/local_regif_txgpio_m1.v",
                        "../../peripherals/src/uart_tx.v", "../../peripherals/gpio/src/gpio_core.v",
                        "tb/regif_tx_public_monitor.sv", "tb/tb_local_regif_txgpio_m1.sv"]
        compile_log = log_dir / ("compile_N%d.log" % n)
        compile_res = run_process(compile_argv, ROOT, 60, compile_log)
        run_argv = [VVP, "-N", "-M-", "-M" + str(IVL_LIB), vvp_rel, "+WAVE_FILE=" + vcd_rel]
        run_log = log_dir / ("run_N%d.log" % n)
        run_res = None
        status = "TOOL_ERROR"
        text = ""
        analysis_errors = []
        if compile_res["ok"]:
            run_res = run_process(run_argv, ROOT, 30, run_log)
            text = run_res["combined"]
            analysis_errors = analyze_run(run_res, text, n)
            status = "PASS" if not analysis_errors else "FAIL"
        vcd = ROOT / vcd_rel
        config_results[n] = {"status": status, "text": text, "run": run_res,
                             "compile": compile_res, "compile_log": compile_log, "run_log": run_log,
                             "run_argv": run_argv, "compile_argv": compile_argv,
                             "analysis_errors": analysis_errors,
                             "vcd": vcd, "vcd_size": vcd.stat().st_size if vcd.exists() else 0}
        cases = N234_CASES if n == 234 else ALL_CASES
        for case in cases:
            marker_case = case + ("-N234" if n == 234 else "")
            begin_count = len(re.findall(r"^TEST_BEGIN " + re.escape(marker_case) + r"\s*$", text, re.MULTILINE))
            pass_count = len(re.findall(r"^TEST_PASS " + re.escape(marker_case) + r"\s*$", text, re.MULTILINE))
            passed = (begin_count == 1 and pass_count == 1)
            frame_counts = re.search(r"REGIF_M1_SELFCHECK_PASS accepted_tx=(\d+) accepted_gpio=(\d+) rejected=(\d+) frames=(\d+) requests=(\d+) complete=(\d+) cancel=(\d+) bad_stop=(\d+)", text)
            actual = "BEGIN=%d PASS=%d; %s" % (begin_count, pass_count,
                                               "counters " + "/".join(frame_counts.groups()) if frame_counts else "no detailed counters")
            if analysis_errors:
                actual += "; errors: " + "; ".join(analysis_errors[:6])
            rows.append({
                "id": "%s-N%d" % (case, n),
                "acceptance_id": case,
                "purpose": "W01-W10 wrapper contract check at N=%d" % n,
                "expected": plan["manual_expectations"].get(case, ""),
                "expected_sha256": plan_actual,
                "actual": actual,
                "status": "PASS" if (status == "PASS" and passed) else status,
                "duration_s": (run_res["duration_s"] if run_res else compile_res["duration_s"]),
                "command": command_dict(run_argv if run_res else compile_argv, 30),
                "log_paths": [str(compile_log.relative_to(PKG)), str(run_log.relative_to(PKG))] if run_res else [str(compile_log.relative_to(PKG))],
                "wave_paths": [str(vcd.relative_to(PKG))] if vcd.exists() else [],
                "limitations": ["Simulation-only; no hardware/PDS/timing evidence."],
            })
    count_ok = all(not c.get("analysis_errors") for c in config_results.values())
    status_all = "PASS" if (plan_ok and count_ok and all(c["status"] == "PASS" for c in config_results.values())) else "FAIL"
    results = {
        "kind": "ACTUAL",
        "run_id": run_id,
        "generated_at": now(),
        "task_id": "B-REGIF",
        "module_version": "1.0.0",
        "interface_version": "LOCAL-REGIF-TXGPIO-M1/1.0.0",
        "tools": tools,
        "tests": rows,
        "limitations": plan["limitations"],
        "issues": ["Packaging only; not A SoC integration, formal timing, RX packaging or hardware."],
    }
    RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("RUN_ID=" + run_id)
    print("PLAN_CHECK=" + ("PASS" if plan_ok else "FAIL"))
    print("COUNTS_OK=" + str(count_ok))
    for n in CONFIGS:
        print("N%d_STATUS=%s" % (n, config_results[n]["status"]))
        for err in config_results[n].get("analysis_errors", []):
            print("N%d_ERROR=%s" % (n, err))
    print("SCHEMA_CHECK=PENDING")
    print("RESULTS=" + str(RESULTS.relative_to(PKG)))
    print("STATUS=" + status_all)
    return 0 if status_all == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
