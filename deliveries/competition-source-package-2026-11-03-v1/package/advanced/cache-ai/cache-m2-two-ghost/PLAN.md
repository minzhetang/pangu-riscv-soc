# Frozen M2 two-entry ghost experiment ¡ª 2026-11-03

Keep all M0/M1 entries unchanged. Same isolation and original user's boundaries:
no CPU/SoC, Git/shared-memory/PDS/hardware/install/mainline-process actions.
One finite candidate, sequential below-normal short simulations only.

Problem: M1 uses one ghost tag per set, so alternating two cacheable lines in
one set cannot enter the two-way cache. Target: restore useful caching while
keeping first-touch stream traffic at bypass level. Retain small two-way data
cache (128B per I/D,4sets,16B), interfaces, write-through/no-write-allocate,
uncached bit31, errors, reset cancellation, data correctness and LRU unchanged.

Add parameter GHOST_TWO=0 to M1 RTL. ADMISSION=1,GHOST_TWO=1 selects M2;
defaults retain ADMISSION=0. For each set track two ghost tags with valid bits.
On unadmitted cacheable READ miss: use empty slot0 then empty slot1, otherwise
replace the slot chosen by FIFO bit, then point FIFO at the other slot.
A match in either slot causes full-line read. A match/fill/hit/write does not
change ghost slots/FIFO. Ghosts retain admission history after fills/evictions.
Uncached/illegal requests and writes must not add ghosts. Reset clears both
valid/tag slots and FIFO. First read remains one beat, no retained first-word data.

Expected added M2 ghost state: per set 2*(26+1)+1=55bits, 220/cache,440/I+D.
Compared to M1 108/cache, delta112/cache,224/I+D logical bits. No resource/STA proof.

Freeze data with independent byte-array oracle; separately list/FIFO/ghost oracle
for exact hit/backend transaction/byte counts. Retain all17 M1 workloads, add
same-set three-line cycle (known >ghost capacity), FIFO eviction/revisit, and
fixed seeded mixed traffic (64requests; read-only for I, read/write for D).
Run M0/M1/M2/bypass x I/D cases x delays0/3, same backend stalls and response stalls.
New MODE4 checks A,B,A,B admission, following hits and reset clearing both ghosts,
then fill cancellation/invalid partial line via inherited MODE3. Old MODE1/2 retain
write reset, dual-channel concurrency, held-valid and side-effect checks.
Negative data vector must fail. Checker must also reject correct-data but incorrect
traffic metrics, tested with a real M1 run against M2 adverse expected statistics.

Frozen target for each channel and delay: stream M2 bytes/cycles equal bypass;
adverse M2 cycles <=0.65*M1 and <=1.15*M0; locality/pollution M2 cycles <=1.05*M1.
Report other regressions honestly, especially three-line ghost-thrash and twoword.
Correctness PASS separate from performance target. No global replacement claim.
Stop after this candidate/matrix; no stress or further policy search.
Limits copied runner:20s/process,256MiB/process,384MiB/job,4child max;64MiB directory
and1MiB log sampled20ms, TB watchdog100000cycles. AI unchanged synthetic M0.
