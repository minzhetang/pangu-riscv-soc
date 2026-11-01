# Technical snapshot — paused, 1 November 2026

Project: Pangu100Pro+ MES2L676-100HP / PG2L100H-6IFBG676, nominal27MHz.
This is an evidence-backed snapshot, not a release or blanket CPU/ISA acceptance.

| Directory | Exact status |
|---|---|
| accepted-o2 | Previously accepted limited O2 reliability source baseline; recoverable artifacts remain local with original SHA. |
| alignment-baseline | New minimum EEI alignment-fatal repair plus board QA; standard software multiply; board run538539600ticks. |
| candidate-sm2 | Same repaired RTL plus signed-magnitude two-bit software multiply; first valid report496232016ticks. Adoption pending. |
| candidate-validation-not-run | Standard validation seed image compiled/implemented/INIT/STA checked; **not run on FPGA**. |
| verification |24 directed new alignment passes and763 frozen regression passes; finite scopes, not full RV32I proof. |
| evidence/onchip-prior-debug-image | Real earlier FPGA captures' audit/results, a different fixed debug bitstream. Not newly captured candidate data. |
| checkpoint | Current pause, user-reported power-off, unresolved serial Overrun, and resume steps. |

H66 accepted actual four-key input sequence, SRAM byte/halfword/sign handling and80 manual products. H67 user observed reset all-off, all8 LEDs individually lit, then A5 (LED0/2/5/7 on). Optical observation is a user receipt, not a calibrated electrical test.

The single SM2 candidate reduces cycles7.85598% versus the same-CPU baseline, costs60 extra program bytes, and has identical1810LUT/1527FF/14DRM36/15IO and passing27MHz STA. A repeat report has the same cycle count but records serial **Overrun**; clean repetition and second-seed target validation remain open. No final adoption or certified CoreMark score is claimed. Clock frequency is nominal and not independently calibrated. QA and UART formatting are outside the measured compute interval.

New alignment behavior uses the existing fatal EEI stop/drain path, not a privileged trap implementation. Reserved/illegal encoding coverage, full exceptions, asynchronous external timing/MTBF, and debug clock routing remain limited. Earlier debug image has4 Critical warnings and qualified CDC/I/O usage; current non-debug0Critical does not close those findings.

PDS flow.tcl uses sibling source/ and constraints under each pds/ directory. The supplied owned ROM binding includes the exact embedded image for that variant. Vendor primitive definitions, proprietary databases, bitstreams, huge waves, installers and private machine identifiers are excluded. Follow UPSTREAM_DEPENDENCIES.json for legal external inputs. Existing workspace scripts/reports may cite local evidence not shipped here; such references are provenance, not claims of standalone reproduction. SHA256SUMS.json records every copied original's path and exact bytes.

The old pending README/CONTRIBUTION documentation review is intentionally not part of this commit. No hardware work or tests were performed during this synchronization. The project remains paused and the board was reported powered off.
