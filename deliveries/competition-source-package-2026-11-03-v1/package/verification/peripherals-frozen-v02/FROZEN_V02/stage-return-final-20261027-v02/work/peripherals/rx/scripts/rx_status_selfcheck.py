#!/usr/bin/env python3
"""Failure-propagation controls for RX runner status."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import run_rx


def main() -> int:
    run_id = sys.argv[1] if len(sys.argv) > 1 else "rx-20261024-232048"
    log = ROOT / "logs" / run_id / "run_N16.log"
    text = log.read_text(encoding="utf-8", errors="replace")
    block = text[text.find("TEST_BEGIN RX-01"):]
    controls = []
    def add(name, actual, expected):
        controls.append({"case": name, "actual": actual, "expected": expected,
                         "status": "PASS" if actual == expected else "FAIL"})
    add("control_rc0_full_pass", run_rx.classify_config({"ok": True}, {"log_truncated": False, "timed_out": False, "returncode": 0, "combined": text}), "PASS")
    add("nonzero_rc", run_rx.classify_config({"ok": True}, {"log_truncated": False, "timed_out": False, "returncode": 1, "combined": text}), "FAIL")
    add("truncated_log", run_rx.classify_config({"ok": True}, {"log_truncated": True, "timed_out": False, "returncode": 0, "combined": text}), "FAIL")
    add("global_fail_with_case_pass", run_rx.classify_config({"ok": True}, {"log_truncated": False, "timed_out": False, "returncode": 0, "combined": text + "\nRX_SELFCHECK_FAIL errors=1\n"}), "FAIL")
    add("case_status_global_fail", run_rx.case_status("FAIL", block, "RX-01"), "FAIL")
    add("case_status_control", run_rx.case_status("PASS", block, "RX-01"), "PASS")
    all_pass = all(c["status"] == "PASS" for c in controls)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = ROOT / "logs" / ("rx-status-selfcheck-" + stamp)
    out.mkdir(parents=True, exist_ok=False)
    (out / "summary.json").write_text(json.dumps({
        "kind": "RX_STATUS_SELFCHECK", "source_log": str(log.relative_to(ROOT)),
        "all_pass": all_pass, "controls": controls,
        "note": "A per-case TEST_PASS cannot override nonzero rc, truncated log, or global RX_SELFCHECK_FAIL."
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"selfcheck": str(out), "all_pass": all_pass, "controls": controls}, ensure_ascii=False, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
