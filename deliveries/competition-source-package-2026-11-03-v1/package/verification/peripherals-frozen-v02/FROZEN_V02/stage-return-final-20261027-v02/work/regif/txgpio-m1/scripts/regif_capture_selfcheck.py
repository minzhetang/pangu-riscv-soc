#!/usr/bin/env python3
"""Run the synthetic public uart_tx capture-path controls."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent.parent.parent / "work/peripherals/scripts"))
from runner_common import run_process

IVERILOG = Path(r"D:\iverilog\bin\iverilog.exe")
VVP = Path(r"D:\iverilog\bin\vvp.exe")
IVL_LIB = Path(r"D:\iverilog\lib\ivl")


def main() -> int:
    run_id = datetime.now().strftime("regif-capture-%Y%m%d-%H%M%S")
    log_dir = ROOT / "logs" / run_id
    wave_dir = ROOT / "waves" / run_id
    log_dir.mkdir(parents=True, exist_ok=False)
    wave_dir.mkdir(parents=True, exist_ok=True)
    vvp = "waves/%s/regif_tx_capture_neg.vvp" % run_id
    compile_argv = [IVERILOG, "-B", IVL_LIB, "-g2012", "-Wall", "-s", "tb_regif_tx_capture_neg",
                    "-o", vvp, "tb/regif_tx_public_monitor.sv", "tb/tb_regif_tx_capture_neg.sv"]
    c = run_process(compile_argv, ROOT, 60, log_dir / "compile_capture.log")
    status = "TOOL_ERROR"
    text = ""
    run = None
    if c["ok"]:
        run = run_process([VVP, "-N", "-M-", "-M" + str(IVL_LIB), vvp], ROOT, 30, log_dir / "run_capture.log")
        text = run["combined"]
        required = [
            "REGIF_CAP_GOOD_PASS", "REGIF_CAP_BAD_STOP_DETECTED",
            "REGIF_CAP_EXTRA_DETECTED", "REGIF_CAP_MISSING_DETECTED",
            "REGIF_CAP_LAST_HALF_STOP_CANCEL",
            "REGIF_CAP_CONTROL_PASS", "REGIF_CAP_SELFCHECK_PASS",
        ]
        forbidden = ["REGIF_CAP_GOOD_FAIL", "REGIF_CAP_BAD_STOP_MISSED",
                     "REGIF_CAP_EXTRA_MISSED", "REGIF_CAP_MISSING_MISSED",
                     "REGIF_CAP_LAST_HALF_STOP_FAIL",
                     "REGIF_CAP_CONTROL_FAIL", "REGIF_CAP_SELFCHECK_FAIL", "CHK_FAIL"]
        status = "PASS" if (run["returncode"] == 0 and not run["timed_out"] and not run["log_truncated"]
                            and all(x in text for x in required)
                            and not any(x in text for x in forbidden)) else "FAIL"
    result = {
        "kind": "REGIF_CAPTURE_SELFCHECK", "run_id": run_id,
        "compile_rc": c["returncode"], "run_rc": None if run is None else run["returncode"],
        "timed_out": None if run is None else run["timed_out"],
        "log_truncated": None if run is None else run["log_truncated"],
        "status": status,
        "required_markers": ["REGIF_CAP_GOOD_PASS", "REGIF_CAP_BAD_STOP_DETECTED",
                             "REGIF_CAP_EXTRA_DETECTED", "REGIF_CAP_MISSING_DETECTED",
                             "REGIF_CAP_LAST_HALF_STOP_CANCEL",
                             "REGIF_CAP_CONTROL_PASS", "REGIF_CAP_SELFCHECK_PASS"],
        "note": "Same shared regif_tx_public_monitor as the formal wrapper TB; synthetic public uart_tx only.",
    }
    (log_dir / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8", newline="\n")
    print(json.dumps({"result": result, "log_dir": str(log_dir)}, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
