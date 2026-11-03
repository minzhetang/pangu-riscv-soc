from native import *
P=H.parent/'2026-11-03-coremark-strict-m5'
for p in (H/'source').glob('*.v'):
 if sha(p)!=sha(P/'source'/p.name):raise RuntimeError('CPU RTL changed')
for mode in ['performance','validation']:
 if (H/'build'/f'{mode}-1/program.bin').read_bytes()!=(P/'build'/mode/'program.bin').read_bytes():raise RuntimeError('One-iteration build differs')
files=[]
for folder in ['source','firmware','port','upstream','vpi-deps','build']:
 files +=[p for p in(H/folder).rglob('*')if p.is_file()]
files +=[p for p in H.iterdir()if p.suffix in ['.cpp','.hpp','.py','.sv','.vpi','.exe']]
files +=[H/'HOST_CRC_ORACLE.json']
plan=dict(date='2026-11-03',scope='M6: 32-entry BTB CoreMark >=10 simulated target seconds; no new CPU RTL, no PDS or hardware',
 algorithm='Unchanged upstream CoreMark, GCC RV32I/ILP32 O2, TOTAL_DATA_SIZE=2000, ITERATIONS=192',
 order=['native reference replays 10 M5 full streams','six live VPI negative controls','one-iteration dual-seed streaming qualification','192-iteration 32-entry dual seeds','same-image BTB-off dual seeds if measured budget permits'],
 seed_modes=['performance:0/0/0x66','validation:0x3415/0x3415/0x66'],
 clock=dict(hz=27000000,simulator_half_period_fs=18518518519,timer='Counter increments every rising edge; one-edge registered memory read: actual read at edge N must equal N-2. No timer scaling, empty delay, or iteration-based time multiplication.'),
 reference='C++ independent sequential RV32I interpreter, own PC/registers/memory, advances from own instructions only. Each actual legal WB/STORE is checked immediately in its own ordered stream; bounded pending queues (32 each) handle pipeline-relative WB/STORE timing, not a real retirement stream. No dedup. Timer addresses must match independent reference read sequence; expected data from frozen N-2 clock equation, never DUT values. Full actual event stream gzip roundtrip checked and retained. Final state and exact UART also compared.',
 independent_CRC=json.loads((H/'HOST_CRC_ORACLE.json').read_text()),
 correctness=['all ordered legal WB and STORE; no dedup','32 regs and all 24576 ROM/RAM words','12 timer reads and phase-minus-mtime=4','main return 0 plus done600d600d; return alone insufficient','port_error/overflow/timer_error 0; seeds/iterations/start-stop counts exact','first algorithm CRCs and iteration-dependent final CRC agree unchanged native algorithm','192 runs require actual elapsed_ticks>=270000000 and no CoreMark ERROR, not host elapsed time'],
 budget=dict(case_seconds=21600,campaign_seconds=64800,process_memory_bytes=1073741824,log_bytes=1048576,raw_trace_per_case_bytes=8589934592,gzip_per_case_bytes=4294967296,trace_backlog_bytes=100663296,cycle_limit=900000000,reference_instruction_limit=700000000,initial_free_disk_bytes=shutil.disk_usage(H).free if False else 0),
 limits='One iteration qualifies mechanisms only, not >=10 seconds. No complete ISA/privilege proof, no hardware/ILA or formal FPGA score. No automatic unbounded retry. Initial qualification cost gates long runs; stop and preserve diagnostics if budget cannot fit.',
 sha256={p.relative_to(H).as_posix():sha(p)for p in sorted(files)})
import shutil
plan['budget']['initial_free_disk_bytes']=shutil.disk_usage(H).free
plan['revision_note']='v1 qualification overconstrained WB versus STORE relative timing, contrary to inherited separate-stream boundary. v1 failure, code and binaries preserved under history/checker-v1. This v2 changes checker queueing only, not CPU/program/expected CRC/timer rule. Negative controls must fail for their specific reason.'
save(H/'plans/FROZEN-v2.json',plan);print('FROZEN-v2',len(files))
