# Actual A reproduction commands

Only ordinary existing Python, -B, no install/compiler/DUT/hardware. <EXISTING_PYTHON> denotes the already verified runtime; profile paths and B personal paths are excluded from this summary. Exact CLI argument arrays and native rc are in logs/<id>/process.json (redacted interpreter label, unchanged arguments), stdout/stderr beside them.

```text
<EXISTING_PYTHON> -B work/analysis/2026-10-27-b-offline-r1-review/run_independent.py
<EXISTING_PYTHON> -B deliveries/mainline-b-offline-r1-review-response-2026-10-27-v1/REPRODUCE_GUARDS.py --tool-root D:/A_FPGA_Comp/队员成果接收/B-VERIFY-OFFLINE-M0-return-v02 --input-root D:/A_FPGA_Comp/deliveries/mainline-b-verify-offline-m0-2026-10-26-v1 --work D:/A_FPGA_Comp/work/analysis/2026-10-27-b-offline-r1-review/portable-repro-check
```

First driver native rc0 means its25-result collection completed; RESULTS.json has22 PASS/3 FAIL, not all pass. The portable three-probe entry native rc1 is expected on unchanged v02 because all three guards fail. Neither result is a CPU/ISA/benchmark validation. Original B54 PASS_LOCAL and its original logs are separate, never relabeled as A new runs.

All original539 manifest entries, frozen API, original37 plan/results and current mainline60 execution inputs were rehashed unchanged. Known invalid JSON fixture files are retained as expected invalid data, not unreadable intake. No B source or frozen expectation was changed. Source-only comparison is CODE_DIFF.patch; full original B diff59 sections independently applied exactly.
