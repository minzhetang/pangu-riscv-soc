# Frozen Cache M1 admission experiment

All M0 files/expectations/logs remain immutable. New work only here. No CPU, PDS,
hardware, installations, Git or shared memory writes; CoreMark untouched.

Candidate optional parameter ADMISSION=1: retain M0 default=0. For each of 4 sets,
keep a ghost-valid/tag (26 tag bits + valid) of last unadmitted cacheable read miss.
First miss for a different tag: one-word bypass, remember tag; subsequent miss
matching ghost: 4-beat fill. Cache hits use normal LRU. Writes do not create ghost
entries. Already admitted misses do not overwrite ghost. Reset clears all ghosts.
Capacity/line/ways, write-through/no-allocate, errors/MMIO/response/reset contract
unchanged; no extra ports or CPU ISA. Ghost state is 108 logical bits/cache,
216 for I+D, not a synthesis resource estimate.

Problem: M0 delay3 stream 357 uncached vs 918 cached cycles, 4x read bytes.
Target: candidate single-use stream read bytes equal bypass; cycles <= bypass+5%%.
Locality must remain faster than bypass, but may regress vs M0. Do not require
universal improvement; record alternating same-set adverse case. Stop after one
candidate and finite matrix; no long stress. Keep as optional candidate unless
universal improvement established (not expected).

Freeze golden responses independently from admission policy: M0 byte-memory oracle.
New separate cache-list/ghost oracle supplies expected hit/command/byte counts.
Original workloads + per-mask readback, 2-word reuse, alternating same-set adverse
case, hot set plus pollution. I/D, delay0/3, baseline/admission/bypass. New TB mode3
checks ghost reset, second-miss fill, following hit, reset during second-touch fill.
Retain original reset/concurrent/held-valid and wrong-data negative checks.
Every response/error and traffic/hit count must exactly match frozen expectation.
Single sequential process via copied bounded runner, below-normal; 20s/process,
256MiB/process 384MiB/job, directory64MiB/log1MiB sampled limits, TB watchdog.
No AI change this stage; AI remains synthetic M0, no real-model/accuracy claim.
