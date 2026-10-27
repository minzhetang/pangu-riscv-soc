# Actual read-only analysis

Existing Python, ordinary user, no tools installed. The executed source was work/analysis/2026-10-27-b-offline-r1-dispatch/analyze_mainline.py; run_analysis.py is its exact-byte mirror. Source has a fixed exclusive output path; do not overwrite or rerun against the existing directory. For reproduction, select a unique independent output path first.

```text
<EXISTING_PYTHON> -B work/analysis/2026-10-27-b-offline-r1-dispatch/analyze_mainline.py
```

Native rc0, 39 pinned inputs unchanged; 11557928 existing trace rows classified. No compiler/DUT/ISA/reference model execution. Numeric extrapolations are conditional planning, not observed test or oracle output.
