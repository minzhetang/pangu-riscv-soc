"""Postflight/receipt generation only. No native compilers or DUT execution."""
from pathlib import Path
import sys,json,difflib,re
sys.dont_write_bytecode=True
import run_stage as s
H=s.H
def main():
    protected=s.verify_originals();frozen=s.frozen();correction=s.read(H/'checker-v2-correction.json')
    assert all(s.sha(x['path'])==x['sha256'] for x in correction['files']+correction['raw_performance'])
    old=s.read(s.OLD/'frozen.json')['files'];assert all(s.sha(x['path'])==x['sha256'] for x in old)
    unit=s.read(H/'unit-v2-result.json');assert unit['status']=='PASS'
    first=s.log(H/'runs/unit/stdout.log');assert re.search(r'TIMER_UNIT_PASS checks=171 carry_retries=1',first)
    assert s.read(H/'checker-negative-result-v2.json')['status']=='PASS'
    ids=['baseline-N16','baseline-N234','smoke-N16','performance-N16','validation-N16'];cases=[]
    for tid in ids:
        d=H/'runs'/tid;v='check-result-v2.json' if tid.startswith(('performance','validation')) else 'check-result.json'
        result=s.read(d/v);assert result['status']=='PASS'
        cases.append(dict(id=tid,result_file=str(d/v),process=s.read(d/'process.json'),functional=result))
        if tid.startswith('baseline'):
            old_run=s.OLD/'runs'/tid.replace('baseline','system')
            assert all(s.sha(d/n)==s.sha(old_run/n) for n in ['trace.log','registers.hex','ram.hex'])
    waves=[s.read(H/'runs'/tid/'wave-review.json') for tid in ['smoke-N16','performance-N16','validation-N16']]
    assert all(w['status']=='PASS' for w in waves)
    quality=s.read(H/'quality-window-analysis.json');assert quality['status']=='PASS_ANALYSIS_ONLY'
    builds=s.read(H/'build-result.json');compiles=s.read(H/'compile-result.json');assert compiles['status']=='PASS_COMPILE_ONLY'
    commands=[];diagnostics=[]
    for a in builds['artifacts']:
        for p in a['commands']:commands.append(p)
    for x in compiles['rows']:
        commands.append(x['process']);diagnostics.append(dict(id=x['id'],native_rc=x['process']['returncode'],seconds=x['process']['elapsed_seconds'],stderr=s.log(x['process']['stderr'])))
    extra=s.read(H/'unit-v2-compile-result.json');commands.append(extra['process']);diagnostics.append(dict(id='unit-v2',native_rc=extra['process']['returncode'],seconds=extra['process']['elapsed_seconds'],stderr=s.log(extra['process']['stderr'])))
    commands.append(s.read(H/'runs/unit/process.json'));commands.extend(x['process'] for x in cases);commands.append(unit['process'])
    with (H/'COMMANDS.md').open('x',encoding='utf-8') as f:
        f.write('# Actual native commands and limits\n\n')
        for p in commands:f.write('```json\n'+json.dumps(p,ensure_ascii=False)+'\n```\n\n')
        f.write('## Ordinary Python evidence checks (no DUT)\n\n')
        for tid in ids:
            checker='check_timed_v2.py' if tid.startswith(('performance','validation')) else 'check_timed.py'
            f.write('`python.exe -B '+str(H/checker)+' '+tid+'`\n\n')
        f.write('Original performance check_timed.py FAIL is preserved in check-result.json; v2 explicitly includes the mandatory BSS STORE, not event filtering.\n')
        for name in ['checker_negative_tests.py','checker_negative_tests_v2.py','analyze_windows.py','finalize.py']:f.write('`python.exe -B '+str(H/name)+'`\n\n')
        for tid in ['smoke-N16','performance-N16','validation-N16']:f.write('`python.exe -B '+str(H/'wave_review.py')+' '+tid+'`\n\n')
    with (H/'SOURCE_DIFF.patch').open('x',encoding='utf-8') as f:
        for n in ['soc_data_adapter.sv','soc_top.sv']:
            f.writelines(difflib.unified_diff((H/'source-before'/n).read_text(encoding='utf-8-sig').splitlines(True),(H/'source'/n).read_text().splitlines(True),fromfile='source-before/'+n,tofile='source/'+n))
        for n in ['core_portme.c','core_portme.h']:
            f.writelines(difflib.unified_diff((H/'port-before'/n).read_text(encoding='utf-8-sig').splitlines(True),(H/'port'/n).read_text().splitlines(True),fromfile='port-before/'+n,tofile='port/'+n))
        f.writelines(difflib.unified_diff((H/'models-before/cpu_program_reference.py').read_text().splitlines(True),(H/'cpu_program_reference.py').read_text().splitlines(True),fromfile='models-before/cpu_program_reference.py',tofile='cpu_program_reference.py'))
    s.save(H/'compile-diagnostics.json',diagnostics)
    summary=dict(date='2026-10-24',stage='A-TIMED-COREMARK-M1',authorization='D123',
      status='FINITE_TIMED_SOFTWARE_SYSTEM_ACCEPTED_NO_FORMAL_SCORE_OR_HARDWARE',
      CPU_B_and_official_algorithms_unchanged=True,protected_originals=protected,stage_frozen_files=frozen,old_system_protected=len(old),
      fresh_compiles=7,fresh_DUT_runs=7,external_compile_permissions='fixed6+fixed1 separately approved and consumed',
      native_builds=builds['artifacts'],cases=cases,unit_current_checks=296,unit_initial_checks=171,
      carry_retry_coverage='unit/router near-carry seed only; production reset zero; CPU retry branch not dynamically reached',
      checker_selftest=dict(correct=1,negative_rejections=8,extra_DUT_runs=0),
      waveform_stable_post_edge_checks=sum(w['stable_post_edge_checks'] for w in waves),
      quality=quality['rows'],prior_checker_error='v1 omitted legitimate BSS zero STORE; raw FAIL preserved, exact startup PC54 required in v2; no DUT rerun or source/input changes',
      hardware='STOP',formal_CoreMark_score=False,limits=['not full ISA or all timer/IO cases','no real retirement PC/unified commit order','fixed memory/initial state',
        'integer seconds display floors short duration; raw ticks exact, no >32bit delta certification',
        'no PDS synthesis/resource/Fmax/physical clock measurement/ILA evidence','two-clock storage throughput cost remains; no optimization benefit claimed'])
    s.save(H/'summary.json',summary)
    s.save(H/'postflight.json',dict(status='PASS',protected_originals=protected,stage_frozen_files=frozen,old_system_protected=len(old),
       source_SHA=[dict(file=n,sha256=s.sha(H/'source'/n)) for n in ['cpu.v','alu.v','control.v','regfile.v','memory_model.sv','local_regif_txgpio_m1.v','uart_tx.v','gpio_core.v']],new_DUT_runs=0))
    with (H/'SHA256SUMS.txt').open('x',encoding='utf-8') as f:
        for p in sorted(H.rglob('*')):
            if p.is_file() and p.name!='SHA256SUMS.txt':f.write(s.sha(p)+'  '+p.relative_to(H).as_posix()+'\n')
    print(json.dumps(dict(status=summary['status'],protected=protected,frozen=frozen,old_protected=len(old),wave_checks=summary['waveform_stable_post_edge_checks'],compiles=7,DUT_runs=7)))
if __name__=='__main__':main()
