# Pre-run fixture correction
Frozen cache_tb.sv retained. Its inherited MODE1 reset-after-write used absolute
transaction count4, valid only for M0's earlier hit. Admission changes that earlier
hit into a fill. Before any M1 execution, execution_tb.sv changes this one wait to
the current transaction count +1. The requirement (wait for committed write) and
all expected data remain unchanged. Both designs use the SAME corrected fixture.
FROZEN_SHA256.txt stays unchanged; EXECUTION_SHA256.txt freezes this correction,
candidate, baseline, backend and bounded runner before execution.
