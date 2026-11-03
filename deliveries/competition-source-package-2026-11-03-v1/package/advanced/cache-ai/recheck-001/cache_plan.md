# CACHE-ISOLATED-M0 frozen v1 — 2026-11-03

Freeze this plan and generated vectors before writing/running RTL. No CPU or shared files.
Two independent blocking caches: I read-only and D read/write. Each 128 data bytes,
2 ways x 4 sets x 16 bytes (4 little-endian 32-bit words). True per-set LRU,
invalid way first. D write-through/no-write-allocate, byte enables; zero strobe
is a successful no-op. I writes and unaligned requests return error without traffic.
Addresses bit31=1 bypass cache; test backend uses low 12 bits, with special read
0x80000ffc returning/incrementing a counter. This map is a prototype contract,
not the current SoC memory map. No coherence/self-modifying-code support.

Requests accepted only on valid && ready at rising edge; payload held until then.
Exactly one outstanding; response valid/data/error held until ready. Holding valid
after acceptance means another request when ready next asserts, including identical
requests. No deduplication by address. Completion is response handshake; writes are
already committed at backend command handshake. Reset synchronously cancels protocol,
invalidates tags/LRU, suppresses new acceptance; backend memory/side effects already
committed survive. Reset must include backend (no transaction IDs/draining).

Backend command valid/ready: address, write, wdata, strobe, len (beats minus one).
Reads use len=3 for fill, len=0 bypass; writes len=0 and an acknowledgment beat.
Response valid/ready/rdata/last; no error bus in this bounded memory model.
Each I/D channel has a separate backend; concurrent operation must be checked.

Frozen tests: locality (64 repeated reads across 4 lines); stream (32 single-use
lines); LRU conflict (A,B,A,C,B same set); D byte lanes/all 16 masks, write miss,
zero strobe; uncached alias avoidance, repeated MMIO side effects; unaligned/I-write
rejection; deterministic mixed reads/writes. Independent byte-array reference supplies
every response. Cache-model oracle supplies hit and backend transaction/byte counts.
Run both channels cached/uncached, backend delays 0 and 3 plus command/beat stalls,
response backpressure 0..3 cycles and repeated identical requests. Test reset idle,
during fill, response pending and after accepted write. Verify no ghost response,
no repeated side effect under stalls. Short concurrent I/D test too.

Acceptance: exact all responses/errors, command count, transferred bytes, hit count,
no stalled payload change, no stray/duplicated responses, bounded completion.
Compare identical traces including testbench overhead; report cycles, eligible read
hit rate, transactions, payload bytes (write enabled bytes; read 4 bytes/beat).
No minimum speedup assumption: stream fills may waste bandwidth/cycles.
Finite checks only, not exhaustive/formal/synthesis/board validation.
