# SM2 accepted technical evidence — 2 November 2026

This supplements the 1 November source snapshot. The historical `candidate-sm2` and `candidate-validation-not-run` names remain unchanged; the evidence here now supports limited acceptance under decision D300. It is not full RV32I, privileged-ISA, physical CDC or safety certification.

Performance256: 496,232,016 target cycles, 18.378963556 nominal seconds. Compared with 538,539,600 baseline cycles: 7.855984% fewer cycles and 8.525767% higher throughput. Code +60 bytes; identical LUT1810/FF1527/DRM36=14 at the same nominal27MHz. Validation256: two new reports at522,673,286 cycles /19.358269852 nominal seconds, matching five CRCs. Computation timing excludes GPIO waits and UART reporting.

Read REPORT.md and RESULTS.json. SOURCE_MAP.json links the existing tracked RTL/software snapshot and the newly archived evidence. Sbit/SVF/ELF binaries and tool/vendor models remain local; hashes and configuration provenance are retained. The current board image at stage end was the validation image, not the performance image. No Flash operation occurred.

The three evidence directories contain full raw UART text, all-error ledgers and controller outcomes. The generic report-check fields do not make adoption decisions; the combined identity/resource/correctness decision is RESULTS.json. Old RXOver and cleanup failures remain under diagnostics; they were not retrospectively relabeled PASS. UART-only USB reconnection preceded recovery, but its unique root cause remains unresolved.

Old baseline ILA captures are not optimized-SM2 ILA captures. The old debug-clock Critical findings, external IO/CDC limits, independent clock/temperature measurement and full-retirement-trace limitations remain. Final competition documents/media and third-party software dependency closure are separate pending work.

`host-tools` records the actual Windows capture/checking implementations and dependencies. Some original controllers intentionally retain absolute paths to the original workspace; do not treat them as portable launchers or execute them to inspect this snapshot. Only the offline verifier is portable:

```
python -B verify_evidence.py
```

It checks snapshot hashes and replays the three already-recorded serial reports. This is not a new DUT/hardware run. CoreMark upstream source, its copyright/license materials, GNU tools and PDS legal environment remain external, as documented in the prior snapshot. No project-wide open-source license is added.
