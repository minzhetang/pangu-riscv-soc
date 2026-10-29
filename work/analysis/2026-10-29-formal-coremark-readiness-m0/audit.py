"""Read existing code/results; compute conditional budgets, no model/tool/DUT run."""
from pathlib import Path
from fractions import Fraction
import json,hashlib,re,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
S=P/'work/fpga/2026-10-27-coremark-longrun-ready-m2'
R=P/'work/fpga/2026-10-25-coremark-iter2-m1'
O=P/'work/system/2026-10-23-coremark-correctness-m1/upstream-direct/files'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest().upper()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,o):
    with (H/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
paths=[S/'port/core_portme.c',S/'port/core_portme.h',S/'firmware/timer.h',S/'firmware/start.S',S/'firmware/link.ld',S/'check_coremark.py',S/'oracle.py',S/'frozen_checks.py',S/'manual-plan.json',S/'build_once.py',S/'SUMMARY.json',S/'runs/performance8-N234/ram-output.txt',S/'runs/performance8-N234/check-result.json',S/'models/cpu_program_reference.py',S/'models/peripheral_checker.py',S/'tests/tb_board_coremark.sv',S/'build/performance8/program.bin',S/'build/performance8/program.elf',O/'README.md',O/'barebones_porting.md',P/'work/system/2026-10-23-coremark-correctness-m1/source-integrity-review.json',R/'runs/performance-N234/check-result.json',R/'runs/validation-N234/check-result.json',P/'work/fpga/2026-10-25-board-coremark-m1/runs/performance-N234/check-result.json',P/'work/fpga/2026-10-25-board-coremark-m1/runs/validation-N234/check-result.json',P/'deliveries/full-project-technical-handoff-2026-10-29-v01/MANIFEST.json',P/'deliveries/full-project-technical-handoff-2026-10-29-v01/SHA256SUMS.txt']
paths+=sorted((S/'source').iterdir())+sorted((S/'upstream').iterdir())
baseline=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,SHA256=sha(p)) for p in paths];save('INPUTS.json',baseline)
old=read(P/'work/system/2026-10-23-coremark-correctness-m1/source-integrity-review.json')
official={Path(x['path']).name:x['sha256'] for x in old['verified_local_vs_archive']}
assert all(sha(p)==official[p.name] for p in (S/'upstream').iterdir())
assert all(sha(O/n)==official[n] for n in ['README.md','barebones_porting.md'])
anchors=[]
for p,needles in [(S/'port/core_portme.c',['ITERATIONS','UINT32_MAX','time_in_secs','SIM ONLY','timing_phase=3']), (S/'port/core_portme.h',['HAS_FLOAT','COMPILER_FLAGS','MEM_LOCATION','CORE_TICKS']), (S/'upstream/core_main.c',['iterations == 0','start_time();','stop_time();','list_known_crc','matrix_known_crc','state_known_crc','time_in_secs(total_time) < 10','HAS_FLOAT','MAIN_RETURN_VAL']), (S/'check_coremark.py',['short run validity warning','formal_score_valid=False','timer_start_calls']), (S/'oracle.py',['expected_iterations=8','25000000','delta<270000000']), (S/'upstream/coremark.h',['secs_ret','MAIN_RETURN_VAL'])]:
    for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
        if any(n in line for n in needles):anchors.append(dict(path=p.relative_to(P).as_posix(),line=i,text=line.strip()))
save('CODE_ANCHORS.json',anchors)
measure=[]
for stage,n,seed in [('2026-10-25-board-coremark-m1',1,'performance'),('2026-10-25-board-coremark-m1',1,'validation'),('2026-10-25-coremark-iter2-m1',2,'performance'),('2026-10-25-coremark-iter2-m1',2,'validation'),('2026-10-27-coremark-longrun-ready-m2',8,'performance8')]:
    q=P/'work/fpga'/stage/'runs'/(seed+'-N234')/'check-result.json';o=read(q);assert o['status']=='PASS'
    measure.append(dict(seed='performance' if seed=='performance8' else seed,iterations=n,raw_ticks=o['detail']['raw_ticks'],physical=o['metrics']['physical'],source=q.relative_to(P).as_posix(),nominal_hz=27000000,hardware=False))
hz=27000000;models=[]
for seed in ['performance','validation']:
    pts=[x for x in measure if x['seed']==seed];a,b=pts[-2:];slope=Fraction(b['raw_ticks']-a['raw_ticks'],b['iterations']-a['iterations']);intercept=Fraction(b['raw_ticks'])-slope*b['iterations'];rows=[]
    for n in [128,160,192,256]:
        ticks=slope*n+intercept;seconds=ticks/hz
        rows.append(dict(iterations=n,predicted_ticks_exact=str(ticks),nominal_seconds_exact=str(seconds),nominal_seconds_display=float(seconds),candidate_over_10_nominal_seconds=seconds>=10,official_32bit_range_if_estimate_holds=ticks<=0xffffffff,NOT_EXECUTED=True))
    models.append(dict(seed=seed,source_points=pts[-2:],slope_ticks_exact=str(slope),intercept_exact=str(intercept),rows=rows,interpretation='CONDITIONAL_EXTRAPOLATION_NOT_FROZEN_EXPECTED_NOT_HW_TIME'))
save('MEASURED_AND_FORECAST.json',dict(measured_old_only=measure,models=models,choice=dict(proposed_iterations=256,reason='about20s at fixed27MHz conditional estimate, margin over10s without port/CPU width changes; real time gate remains mandatory',NOT_APPROVED_OR_EXECUTED=True),timer=dict(hardware_counter_bits=64,port_tick_bits=32,ten_second_threshold=10*hz,max_accepted_delta=0xffffffff,max_nominal_seconds_exact=str(Fraction(0xffffffff,hz)),max_nominal_seconds_display=float(Fraction(0xffffffff,hz)),core_clock_basis='physical original clock; do not divide MHz by2 for two-phase pipeline')))
rules=(O/'README.md').read_text(encoding='utf-8');assert all(x in rules for x in ['at least 10 seconds','0,0,0x66','0x3415,0x3415,0x66','2000 bytes total','same flags'])
save('OFFICIAL_RULES.json',dict(commit='1f483d5b8316753a742cbf5590caf5bd0a4e4777',source='local previously authenticated upstream files, rehashed against receipt; no network this task',source_SHA256={n:sha(O/n) for n in ['README.md','barebones_porting.md']},required=['>=10s real target timed workload','both performance and validation seeds','2000 total bytes','uniform compilation flags/data types','no changes to six official algorithm/header sources'],allowed=['core_portme implementation/configuration','fixed iteration count','build options'],HAS_FLOAT0='explicitly permitted in barebones guide; integer seconds precision is a reporting limitation, not ISA or timer failure',timing_reference='barebones guide requires test of time measurement against external reference; not yet hardware validated',all_benchmark_success_paths='core_main return0 independent of total_errors; require success/CRC/error evidence, not main return alone',source_URLs=['https://github.com/eembc/coremark/blob/1f483d5b8316753a742cbf5590caf5bd0a4e4777/README.md#run-rules','https://github.com/eembc/coremark/blob/1f483d5b8316753a742cbf5590caf5bd0a4e4777/barebones_porting.md']))
# Read-only tool identity comparison, not version command/installation/execution.
manifest=read(P/'work/toolchain-readiness/2026-10-22-xpack-rv32i/installed-files.json');expected={Path(x['path']):x['sha256'] for x in manifest};tools=[]
for name in ['gcc','objcopy','objdump','readelf','nm']:
    q=P/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin'/('riscv-none-elf-'+name+'.exe');got=sha(q);assert got==expected[q];tools.append(dict(path=q.relative_to(P).as_posix(),SHA256=got,matches_previously_verified_install=True,executed=False))
save('TOOL_IDENTITIES.json',dict(version_record='xPack15.2.0-1 GCC15.2.0; bytes same as existing verified install',tools=tools,new_native_version_queries=0))
assert all(sha(P/x['path'])==x['SHA256'] for x in baseline)
save('POSTFLIGHT.json',dict(protected_inputs=len(baseline),unchanged=True,RTL_modifications=0,new_C_builds=0,new_RTL_compiles=0,new_reference_or_DUT_runs=0,hardware='STOPPED',B_receipt='PENDING_USER_WILL_FORWARD',handoff_manifest_unchanged=True))
save('SUMMARY.json',dict(date='2026-10-29',stage='A-FORMAL-COREMARK-READINESS-M0',status='READONLY_EVIDENCE_AND_NEXT_SCOPE_ONLY',facts='F179',decision='D193',inputs=len(baseline),official_sources_rehashed=True,existing_tools_five_SHA_match=True,new_execution=0,hardware='STOPPED',recommendation='propose bounded software-only 2+2 short DUT regression and two256 build-only candidates; no long RTL run or PDS',pending_scope='deliveries/mainline-formal-coremark-software-scope-2026-10-29-v1/IMPLEMENTATION_SCOPE.md'))
print(json.dumps(dict(status='READONLY_COMPLETE',inputs=len(baseline),old_results=len(measure),forecast_NOT_EXECUTED=models,timer_max_nominal_seconds=float(Fraction(0xffffffff,hz))),ensure_ascii=False))
