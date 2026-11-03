#!/usr/bin/env python3
"""Fixed fixture: emit a valid-looking result with no self memory measurement."""
import json
import sys
from pathlib import Path

out = None
for i, arg in enumerate(sys.argv):
    if arg == "--out":
        out = Path(sys.argv[i + 1])
if out is None:
    raise SystemExit(2)
result = {
    "kind": "B_VERIFY_OFFLINE_WORKER",
    "case_id": "R1-MEM-MEASURE",
    "ABI": "B-VERIFY-OFFLINE-ABI/1.0.0",
    "CPU_function_proven": False,
    "new_DUT": 0,
    "limits": {},
    "expected_input": None,
    "actual_input": None,
    "status": "MATCH",
    "native_rc": 0,
    "fully_consumed": True,
    "checked": 8,
    "expected_records": 8,
    "actual_records": 8,
    "mismatch_count": 0,
    "differences": [],
    "neighbors": [],
    "first_difference": None,
    "termination": "normal",
    "worker_reported_peak_bytes": None,
}
(out / "worker-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                        encoding="utf-8", newline="\n")
print(json.dumps({"status": "MATCH", "native_rc": 0, "case": "R1-MEM-MEASURE"}))
raise SystemExit(0)
