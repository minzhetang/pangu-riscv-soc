#!/usr/bin/env python3
"""Entry-marker and actual-event negative controls for the packaging runner."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import run_regif_m1 as runner


def mutate_remove(text: str, pattern: str) -> str:
    return re.sub(pattern, "", text, count=1, flags=re.MULTILINE)


def mutate_duplicate(text: str, pattern: str) -> str:
    return re.sub(pattern, lambda m: m.group(0) + "\n" + m.group(0), text, count=1, flags=re.MULTILINE)


def result_case(name: str, text: str, n: int, expected_ok: bool):
    errors = runner.analyze_markers(text, n) + runner.analyze_events(text, n)
    actual_ok = len(errors) == 0
    return {
        "case": name,
        "expected": "PASS" if expected_ok else "REJECT",
        "actual": "PASS" if actual_ok else "REJECT",
        "status": "PASS" if actual_ok == expected_ok else "FAIL",
        "errors": errors[:8],
    }


def main() -> int:
    run_id = sys.argv[1] if len(sys.argv) > 1 else None
    if run_id is None:
        candidates = sorted((ROOT / "logs").glob("regif-m1-*"), key=lambda p: p.stat().st_mtime)
        if not candidates:
            print("NO_RUN_LOG")
            return 1
        run_id = candidates[-1].name
    log_dir = ROOT / "logs" / run_id
    n16 = (log_dir / "run_N16.log").read_text(encoding="utf-8", errors="replace")
    n234 = (log_dir / "run_N234.log").read_text(encoding="utf-8", errors="replace")
    n16 = n16.lstrip("\ufeff")
    n234 = n234.lstrip("\ufeff")
    rows = []
    rows.append(result_case("N16_control", n16, 16, True))
    rows.append(result_case("N234_control", n234, 234, True))

    # Marker negatives on the actual N16 result log.
    rows.append(result_case("missing_TEST_PASS_W01",
                            mutate_remove(n16, r"^TEST_PASS W01\s*$"), 16, False))
    rows.append(result_case("duplicate_TEST_PASS_W01",
                            mutate_duplicate(n16, r"^TEST_PASS W01\s*$"), 16, False))
    rows.append(result_case("wrong_TEST_PASS_W99",
                            n16.replace("TEST_PASS W10", "TEST_PASS W99", 1), 16, False))
    rows.append(result_case("TEST_FAIL_present",
                            n16 + "TEST_FAIL W10 injected\n", 16, False))
    first_req = re.search(r"^REGIF_REQ seq=1 edge=9 addr=00 .*$", n16, re.MULTILINE)
    if not first_req:
        print("MISSING_FIRST_REQUEST_LINE")
        return 1
    first_req_line = first_req.group(0)
    rows.append(result_case("wrong_first_request_address",
                            n16.replace(first_req_line, first_req_line.replace("addr=00", "addr=01"), 1), 16, False))
    rows.append(result_case("wrong_first_request_edge",
                            n16.replace(first_req_line, first_req_line.replace("edge=9 ", "edge=8 "), 1), 16, False))
    rows.append(result_case("bad_stop_monitor_event",
                            n16 + "REGIF_TX_FRAME event=BAD_STOP idx=1 edge=9999 data=33\n", 16, False))
    req_lines = re.findall(r"^REGIF_REQ .*$", n16, re.MULTILINE)
    if len(req_lines) < 2:
        print("INSUFFICIENT_REQUEST_LINES")
        return 1
    second = req_lines[1]
    second_bad_edge = re.sub(r"edge=\d+", "edge=999", second, count=1)
    rows.append(result_case("nonfirst_request_edge",
                            n16.replace(second, second_bad_edge, 1), 16, False))
    second_bad_busy = second.replace("busy=0", "busy=1", 1) if "busy=0" in second else second.replace("busy=1", "busy=0", 1)
    rows.append(result_case("busy_field",
                            n16.replace(second, second_bad_busy, 1), 16, False))
    comp = re.search(r"^REGIF_TX_FRAME event=COMPLETE .*$", n16, re.MULTILINE)
    if not comp:
        print("MISSING_COMPLETE")
        return 1
    comp_line = comp.group(0)
    comp_bad = re.sub(r"edge=\d+", "edge=99999", comp_line, count=1)
    rows.append(result_case("complete_frame_edge",
                            n16.replace(comp_line, comp_bad, 1), 16, False))
    gp = re.search(r"^REGIF_GPIO_ACCEPT .*$", n16, re.MULTILINE)
    if not gp:
        print("MISSING_GPIO_ACCEPT")
        return 1
    gp_line = gp.group(0)
    gp_bad = re.sub(r"seq=\d+ edge=\d+", "seq=99 edge=999999", gp_line, count=1)
    rows.append(result_case("gpio_seq_edge",
                            n16.replace(gp_line, gp_bad, 1), 16, False))

    # Actual-event negatives on the actual N16 result log.
    first_complete = re.search(r"^REGIF_TX_FRAME event=COMPLETE idx=1 edge=\d+ data=5a observed_edge=\d+\s*$", n16, re.MULTILINE)
    if not first_complete:
        print("MISSING_ACTUAL_TX_COMPLETE_LINE")
        return 1
    tx_complete_line = first_complete.group(0)
    rows.append(result_case("wrong_tx_complete_byte",
                            n16.replace(tx_complete_line, tx_complete_line.replace("data=5a", "data=5b"), 1), 16, False))
    rows.append(result_case("extra_tx_frame",
                            n16 + "REGIF_TX_FRAME event=COMPLETE idx=99 edge=9999 data=6a\n", 16, False))
    rows.append(result_case("missing_tx_frame",
                            n16.replace(tx_complete_line + "\n", "", 1), 16, False))

    first_gpio = re.search(r"^REGIF_GPIO_ACCEPT seq=\d+ edge=\d+ data=a5\s*$", n16, re.MULTILINE)
    if not first_gpio:
        print("MISSING_ACTUAL_GPIO_LINE")
        return 1
    gpio_line = first_gpio.group(0)
    rows.append(result_case("extra_gpio_accept",
                            n16 + "REGIF_GPIO_ACCEPT seq=99 edge=9999 data=a5\n", 16, False))
    rows.append(result_case("missing_gpio_accept",
                            n16.replace(gpio_line + "\n", "", 1), 16, False))
    rows.append(result_case("duplicate_gpio_accept",
                            n16.replace(gpio_line, gpio_line + "\n" + gpio_line, 1), 16, False))

    # Runner-level negatives: native rc / truncation are outside marker text.
    for name, fake in (
        ("nonzero_native_rc", {"returncode": 1, "timed_out": False, "log_truncated": False}),
        ("truncated_log", {"returncode": 0, "timed_out": False, "log_truncated": True}),
    ):
        errs = runner.analyze_run(fake, n16, 16)
        rows.append({"case": name, "expected": "REJECT", "actual": "REJECT" if errs else "PASS",
                     "status": "PASS" if errs else "FAIL", "errors": errs[:8]})

    all_pass = all(r["status"] == "PASS" for r in rows)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = ROOT / "logs" / ("regif-entry-selfcheck-" + stamp)
    out_dir.mkdir(parents=True, exist_ok=False)
    summary = {
        "kind": "REGIF_ENTRY_SELFCHECK",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_run_id": run_id,
        "source_logs": [str((log_dir / "run_N16.log").relative_to(ROOT)),
                        str((log_dir / "run_N234.log").relative_to(ROOT))],
        "all_pass": all_pass,
        "cases": rows,
        "note": "Control and negative controls use the same analyze_markers/analyze_events/analyze_run path as the official runner; actual inputs are the formal N16/N234 logs.",
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8", newline="\n")
    print(json.dumps({"run_id": run_id, "selfcheck": str(out_dir.relative_to(ROOT)),
                      "all_pass": all_pass, "cases": rows}, ensure_ascii=False, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
