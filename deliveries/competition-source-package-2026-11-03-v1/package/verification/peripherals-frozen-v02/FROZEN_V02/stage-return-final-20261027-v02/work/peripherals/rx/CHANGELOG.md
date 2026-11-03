# CHANGELOG

## v1.2.0 — 2026-10-23 — ordered ledger and budget hardening

### Added

- `tb/tb_uart_rx.sv`: ordered ACCEPT/CONSUME/DROP/CANCEL ledger with per-config expected counts; `RX_LAST_CHECK_CYCLE`; per-config `last_check_cycle + 32` budgets.
- `tb/rx_ledger_check.svh`: shared ordered comparator macro used by the formal TB and the negative extra-event proof.
- `tb/tb_uart_rx_neg.sv`: extra-ACCEPT negative and one-event control through the same comparator macro; watchdog/hard-cap protection retained.
- `tests/rx-plan-1.2.0.json`: frozen ledger counts, per-config last-check/budget evidence, watchdog process-timeout distinction.
- `scripts/run_rx.py`: log-truncation rejection; TB watchdog accepted only with native rc=0 and no process timeout; shared comparator/hard-cap gate.

### Historical

- v1.1.0 and v1.0.0 entries and runs remain preserved as history. Current local ACTUAL is `rx-20261023-192450`.

## v1.1.0 — 2026-10-23 — review-response contract boundary

### Added

- `tests/rx-plan-1.1.0.json` / `.sha256`: frozen plan for the review-response increment; old `1.0.0` plan preserved.
- `tb/tb_uart_rx.sv`: RX-05 5e clear+new overrun same-edge case; RX-09 DATA/START/STOP mid-frame reset and recovery; expected event ledger for valid/consume/overrun/frame-error counts; `TB_HARD_CAP_REJECT` above 1,000,000 cycles.
- `tb/tb_uart_rx_neg.sv`: `TB_MAX_CYCLES` watchdog and independent extra-valid/duplicate-event checker with `EXPECTED=1` negative and `EXPECTED=2` correct control.
- `scripts/run_rx.py`: shared file-backed bounded runner; fail-closed plan/artifact/path/cycle-budget gate; native rc classification; only COM-02 may be TIMEOUT; negative/illegal require rc=0.
- `results.json` / `logs/rx-20261023-180309/` / `waves/rx-20261023-180309/`: current local ACTUAL, 30 PASS + 1 expected TIMEOUT, schema PASS.

### Historical

- v1.0.0 entry below is preserved. Its `rx-20261023-115726` result, logs, VCDs and plan remain historical evidence, not the current 1.1.0 final local result.
- `rx-20261023-114340` and `rx-20261023-114355` remain preserved historical runs as described below.

## v1.0.0 — 2026-10-23 — B-UART-RX

### Added

- `src/uart_rx.v`: 8N1 UART RX core, `CLKS_PER_BIT=N>=8`, two-stage synchronizer, one-byte mailbox, sticky `frame_error`/`overrun`, async active-low reset, explicit `N<8` rejection.
- `tb/tb_uart_rx.sv`: self-checking directed TB; S_postNBA checks, four phases, true back-to-back frames, false start, mailbox/overrun, same-edge consume/replace, reset recovery, clear/new-error, bounded watchdog.
- `tb/tb_uart_rx_neg.sv`: independent checker negative proof with deliberately wrong expected value.
- `tb/tb_uart_rx_watchdog.sv`: deliberate bounded-watchdog test.
- `tb/tb_uart_rx_illegal.sv`: N=4 illegal-configuration rejection test.
- `tests/rx-plan-1.0.0.json` / `.sha256`: frozen execution plan; contract `PERIPH-CORE-RX-1.0` v1.0.0.
- `scripts/run_rx.py`: explicit-path bounded Icarus/Python runner; plan/artifact hash gate; compile 60 s/run 30 s; fresh logs/VCD/results; schema validation.
- `results.json`: ACTUAL, 30 PASS + 1 expected TIMEOUT (COM-02 watchdog).
- `logs/rx-20261023-115726/`: final logs, plan check, watchdog, illegal-config, schema, run manifest.
- `waves/rx-20261023-115726/`: N8/N16/N234 VCD and compiled VVPs.
- `docs/MAINLINE-RX-RECEIPT-20261023.md`: contract receipt and remaining-hours estimate.
- `docs/MIGRATION-0.1.0-to-1.0.0.md`: explicit migration from the draft plan.
- `STATUS.md`: acceptance matrix, evidence, boundaries and limitations.

### Changed / corrected before freeze

- `d` is E2, not E1; good stop publishes at S post-NBA, not S+1.
- Raw back-to-back is strictly 10NT; same-phase `d_next=d+10N`; no +1 and no extra idle.
- TB measurement/counter reset points were corrected so data/stop sampling aligns with the contract; debug prints were removed before freeze.
- `clear_errors` timing in the TB is deasserted after the S edge so the new-error priority is observable without clearing on the next edge.

### Preserved / superseded

- `tests/rx-plan.json`, `tests/rx-plan.sha256`, `docs/rx-sampling.md` and the old draft status content remain as history; not overwritten.
- `rx-20261023-114340`: initial full run; `RX-10-N16` was incorrectly treated as a per-config main-TB row and failed. Its logs/waves/manifest are preserved; the issue was fixed by moving RX-10 to the separate negative-proof row (`COM-05`).
- `rx-20261023-114355`: all functional checks passed before visible port-event counters were added; superseded by `rx-20261023-115726`. Its logs/waves/manifest are preserved.
- The old runs' `results.json` files were overwritten by subsequent runs; the final `results.json` is `rx-20261023-115726`. No old result is reused as final.

### Not done / not claimed

- No PDS synthesis/place-and-route/timing/resource/power run.
- No JTAG, power-up, download, Flash, SCBV, jumper or thermal change; hardware remains stopped.
- No B-REGIF, address map, CPU bus/adapter or SoC integration.
- No mainline reproduction, final acceptance, board-level baud/metastability/MTBF claim.

## v1.3.0 — 2026-10-24 — protocol event ledger correction

### Added

- `tests/rx-plan-1.3.0.json` / `.sha256`: frozen ledger counts N8/N16/N234 = 88/106/64, independent serial-decoded DROP data, protocol-derived CANCEL, and negative public-stream capture markers.
- `tb/tb_uart_rx.sv`: independent raw-serial decoder; DROP when a good frame completes with pre-edge valid=1/ready=0, including when OV was already 1 and clear_errors is simultaneous; per-event edge and pre/post public-port states; reset-derived CANCEL.
- `tb/tb_uart_rx_neg.sv`: `rx_public_capture` source plus extra/missing/wrong-order/wrong-byte negatives and one-/two-event controls.
- Formal run `rx-20261024-002409` logs/VCD/results; N16 5e actual DROP `edge=8081 data=0x44 pre_ov=1 post_ov=1`.

### Changed

- RX-05 5e expected ledger adds one DROP per configuration (old 87/105/63 -> 88/106/64); aggregate valid/consume/FE/OV counts remain unchanged.
- `scripts/run_rx.py`: plan 1.3.0 gate and required missing/order/wrong-byte/two-event-control negative markers.
- Removed the post-stimulus `actual_cancel()` task/calls; CANCEL now derives from reset while the independent decoder reports an active frame.

### Preserved / not done

- Old 1.2.0/1.1.0/1.0.0 plans, results, logs and counts retained as history.
- The ledger distinguishes protocol events from observable public state and does not claim a hidden physical write pulse.
- No RX core change, no mainline reproduction, no RX register packaging, no hardware.

## v1.3.1 — 2026-10-24 — edge pre/post state and capture negatives

### Added

- `tests/rx-plan-1.3.1.json` / `.sha256`: ledger 92/110/68; same-byte same-edge gap, pre_clear=1 for 5e, sampled CANCEL post-state, capture-path DROP/CANCEL negatives.
- `tb/tb_uart_rx.sv`: RX-08 A1/A1 same-byte replacement; 5e pre_clear uses stable prior clear; CANCEL post fields sampled from public ports after reset settles; `RX_LAST_CYCLE` for budget evidence.
- `tb/tb_uart_rx_neg.sv`: `rx_public_capture` now captures same-edge/DROP/CANCEL; controls and missing/wrong/extra negatives.
- Formal run `rx-20261024-173355`, logs/VCD/results; N16 5e `edge=8081 data=0x44 pre_clear=1 post_clear=0 pre/post_ov=1`.

### Changed

- Budgets updated to last_check+32: N8 5045, N16 11319, N234 110967.
- `run_rx.py` requires the new capture-path control/detection markers.
- RX core unchanged; 5e 0x44 DROP and 88/106/64 evidence remain historical, not reworked.

### Preserved / not done

- 1.3.0/1.2.0 plans, results, logs and 88/106/64 counts retained as history.
- No new DUT mainline run; original-waveform review is not a new DUT run.
- No RX packaging, CPU/SoC, PDS/timing/board or hardware.


## v1.3.3 — 2026-10-24 — shared public capture and edge state convergence

### Added

- `tb/rx_public_capture.sv`: shared by formal and negative TBs; formal crosschecks content-equivalence with inline ledger.
- `tests/rx-plan-1.3.3.json`: one-based CONSUME edges, stable pre/post states, shared capture hash, 92/110/68 and functional counts.
- `scripts/rx_status_selfcheck.py`: nonzero rc/truncated/global fail propagation controls.
- Formal run `rx-20261024-232514`; 5e pre_fe=1/pre_clear=1/post_fe=0.

### Changed

- `run_rx.py`: classify_config/case_status propagate global FAIL; negative markers require shared capture controls.
- `tb_uart_rx.sv`: CONSUME edge +1, pre fields from last settled state, crosscheck shared capture.
- RX core unchanged.

## v1.3.4 — 2026-10-25 — strict ordered shared capture and snapshots

- Added 1.3.4 plan; shared capture order/edge exact; post +1ps; 5e post_clear=1; formal run rx-20261025-191037.

## v1.3.5 — 2026-10-25 — true-edge pre/post snapshots

- Added 1.3.5 plan; inline ledger records pre at the true S/consume edge and post at +1 ps after the same NBA; ACCEPT, ACCEPT-REPLACE, DROP and CONSUME shapes checked; no DROP pre-copy special case; counts 92/110/68 and 41/41, 50/50, 29/29; formal run rx-20261025-211013.
