"""Postflight and Q02 observed-workflow metrics, no native or DUT execution."""
from pathlib import Path
from collections import Counter
import sys,json
sys.dont_write_bytecode=True
import run_integration as r
h=r.H;s=r.s
result=r.read(h/'result.json');assert result['status']=='PASS_LIMITED_SYSTEM'
neg=r.read(h/'checker-negative-result.json');assert neg['status']=='PASS'
sources=r.read(h/'source-receipts.json');assert all(s.sha(x['original'])==s.sha(h/'source'/x['copy'])==x['sha256'] for x in sources)
compiled=r.read(h/'compile-result.json');assert compiled['status']=='ALL_COMPILED_NOT_SIMULATED'
quality=[]
for n in [16,234]:
    d=h/'runs'/f'system-N{n}';check=r.read(d/'checker-result.json')
    reads=Counter();writes=Counter()
    with (d/'trace.log').open(encoding='ascii') as f:
        for line in f:
            a=line.strip().split('|')
            if a[0] in ['READ','STORE']:
                addr=int(a[3],16)
                if 0x20000000<=addr<=0x200000ff:(reads if a[0]=='READ' else writes)[f'{addr:08x}']+=1
    starts=[c for c,b in check['public_UART_frames']];last_complete=starts[-1]+10*n
    quality.append(dict(N=n,physical_cycles=check['metrics']['physical'],pipeline_advances=check['metrics']['advances'],
        first_TX_accept=starts[0],last_TX_complete=last_complete,TX_starts=starts,
        start_gaps=[b-a for a,b in zip(starts,starts[1:])],core_earliest_gap=10*n+1,
        UART_line_active_clock_count=12*10*n,IO_READ_count=dict(reads),IO_STORE_count=dict(writes),
        GPIO_actual_accepts=check['GPIO_actual_events'],
        interpretation='testbench GPIO input intentionally changes atE4096; N16 completion includes deliberate input wait, not an application-compute benchmark',
        limitations='physical simulation clocks only, includes startup/drain/tail, not real retirement CPI or CoreMark score'))
r.save(h/'quality-metrics.json',quality)
diagnostics=[]
for x in compiled['rows']:
    diagnostics.append(dict(id=x['id'],stderr=s.text_log(x['process']['stderr']),elapsed_seconds=x['process']['elapsed_seconds']))
r.save(h/'compile-diagnostics.json',diagnostics)
summary=dict(stage='A-SOC-TXGPIO-M1',date_beijing='2026-10-24',authorization='D120',
    status='FINITE_SOFTWARE_SYSTEM_ACCEPTED_NOT_HARDWARE_OR_FINAL_PACKAGE',
    baseline_CPU='F130 whole group unchanged',baseline_memory='F131 functional primitive binding unchanged',
    received_wrapper_sha256='5C81EE8F01372D33D4173A34BB095B3D6E649541E4716C933AF11A2390D264FA',
    CPU_and_B_sources_unchanged=True,protected_files=r.frozen(),new_fixed_compiles=4,
    external_compile_permission='separately approved maximum4 fixed non-admin compile-only targets, consumed',
    ordinary_new_DUT_runs=4,wrapper_positive_configs=2,system_positive_configs=2,
    whole_system_cases=[x for x in result['cases'] if x['id'].startswith('system')],
    wrapper_original_TB_results=[x for x in result['cases'] if x['id'].startswith('wrapper')],
    live_checker_selftest=dict(total=8,correct_control=1,negative_rejections=7,DUT_runs=0),
    quality=quality,teammate_package_final_acceptance='CONDITIONAL; incoming runner/TB/metadata/RX-ledger gaps remain',
    hardware='STOP over_temp unchanged',CoreMark_formal_score='NOT_MEASURED',
    limitations=['only fixed12bytes/3GPIOwrites, N16/N234, fixed memory/reset/inputs',
        'not full ISA/CPU correctness, no true retirement PC or unified WB-STORE commit stream',
        'not synthesis/mapping/resource/Fmax/FPGA/ILA or formal benchmark',
        'two-clock CPU advance cost remains; no efficiency innovation claimed'])
r.save(h/'summary.json',summary)
with (h/'COMMANDS.md').open('x',encoding='utf-8') as f:
    f.write('# Actual fixed compiles and ordinary simulations\n\n')
    for x in compiled['rows']+result['cases']:
        p=x['process'];f.write('```json\n'+json.dumps({k:p[k] for k in ['argv','cwd','timeout_seconds','returncode','elapsed_seconds']},ensure_ascii=False)+'\n```\n\n')
with (h/'SHA256SUMS.txt').open('x',encoding='utf-8') as f:
    for p in sorted(h.rglob('*')):
        if p.is_file() and p.name!='SHA256SUMS.txt':f.write(s.sha(p)+'  '+p.relative_to(h).as_posix()+'\n')
print(json.dumps(dict(status=summary['status'],protected=summary['protected_files'],quality=quality)))
