"""Postflight evidence aggregation only; no tool compilation or DUT execution."""
from pathlib import Path
import collections,json,hashlib,sys,datetime
sys.dont_write_bytecode=True
import run_stage as s
H=s.HERE
def digest(p):return s.sha(p)
before=s.read(H/'frozen.json');count=s.frozen()
reg=s.read(H/'regression-result.json');programs=s.read(H/'programs-result.json');small=s.read(H/'small-result.json')
waves=s.read(H/'wave-audit.json');compile_result=s.read(H/'compile-result.json')
assert all(v['status']=='PASS' for v in [reg,programs,small,waves])
old={r['id']:r for r in s.read(s.OLD/'runs-v2/result.json')['cases']}
history=[];specified=collections.Counter();not_specified=collections.Counter()
for r in reg['cases']:
    for key in ['stall','flush']:
        c=r['checks'][key]
        if c['status']=='NOT_SPECIFIED':not_specified[key]+=1
        else:specified[key]+=1
        history.append(dict(id=r['id'],key=key,expected_independent=c['expected'],
            old=old[r['id']]['checks'][key]['actual'],new=c['actual'],
            equal=old[r['id']]['checks'][key]['actual']==c['actual']))
assert all(r['equal'] for r in history)
s.save(H/'history-counts.json',dict(status='PASS',checks=history,
    note='historical equality is not an independently frozen expectation'))
warning_rows=[]
for r in compile_result['rows']:
    text=Path(r['stderr']).read_text(encoding='utf-8',errors='replace')
    warning_rows.append(dict(id=r['id'],warnings=text,warning_lines=text.count('warning:'),
        errors=[line for line in text.splitlines() if 'error:' in line.lower()]))
assert not any(r['errors'] for r in warning_rows)
s.save(H/'compile-diagnostics.json',dict(targets=warning_rows))
sources=[]
for name in ['cpu.v','alu.v','control.v','regfile.v']:
    sources.append(dict(file=name,original=digest(s.OLD/'source'/name),before=digest(H/'source-before'/name),
        after=digest(H/'source'/name),changed=digest(H/'source-before'/name)!=digest(H/'source'/name)))
allruns=reg['cases']+small['cases']+programs['cases']
summary=dict(date_beijing='2026-10-24',stage_started='2026-10-23',stage='A-MEM-ADAPT-M1',status='LIMITED_SOFTWARE_ACCEPTED',
    sources=sources,frozen_files_rechecked=count,compile_count=len(compile_result['rows']),
    external_compile_permission='single maximum16 batch consumed; non-admin; no external simulation',
    compile_errors=0,compile_warnings_preserved=True,new_DUT_runs=len(allruns),
    PASS=sum(r['status']=='PASS' for r in allruns),FAIL=sum(r['status']=='FAIL' for r in allruns),
    TIMEOUT=sum(r['process']['timed_out'] for r in allruns),
    default_compatibility_cases=len(reg['cases']),small_cases=len(small['cases']),program_cases=len(programs['cases']),
    specified_expectation_checks=dict(specified),NOT_SPECIFIED_preserved=dict(not_specified),
    historical_count_checks=len(history),historical_count_equal=all(r['equal'] for r in history),
    independent_full_wave_checks=sum(r['checks'] for r in waves['cases']),
    programs=[{k:r[k] for k in ['id','sync','status','metrics','actual_streams','process']} for r in programs['cases']],
    limitations=['behavioral memory only; not full32K target DRM mapping/initialization/port collision or Fmax',
        'conservative two-clock phase correctness baseline; about2x physical clocks, not an efficiency improvement',
        '763 default-mode compatibility cases, NOT763 sync-mode cases',
        'finite CoreMark1-iteration CRC checks, no valid timer or official score',
        'no real retirement PC; EX and WB/STORE observations separate; fixed memory and reset state',
        'no peripherals integrated, no hardware/ILA; over_tempSTOP unchanged'])
s.save(H/'summary.json',summary)
with (H/'COMMANDS.md').open('x',encoding='utf-8') as f:
    f.write('# 本次实际执行命令\n\n16次编译经单批权限审批；781次仿真为普通权限。以下JSON argv不经shell拆分；cwd、限时、原生rc和墙时见对应process.json。\n\n')
    for r in compile_result['rows']+allruns:
        p=r if 'argv' in r else r['process']
        f.write('```json\n'+json.dumps(dict(argv=p['argv'],cwd=p['cwd'],timeout_seconds=p['timeout_seconds']),ensure_ascii=False)+'\n```\n\n')
with (H/'RESULT_MATRIX.md').open('x',encoding='utf-8') as f:
    f.write('# 逐例结果\n\n|用例|模式|结果|物理沿|推进沿|stall/flush|\n|---|---|---|---:|---:|---|\n')
    for r in small['cases']+programs['cases']:
        m=r['metrics'];f.write(f"|{r['id']}|{r['sync']}|{r['status']}|{m['physical']}|{m['advances']}|{m['stall']}/{m['flush']}|\n")
    f.write('\n## 默认模式旧763例\n\n|用例|结果|stall期望/实测|flush期望/实测|WB/STORE笔数|\n|---|---|---|---|---|\n')
    for r in reg['cases']:
        a,b=r['checks']['stall'],r['checks']['flush']
        f.write(f"|{r['id']}|{r['status']}|{a['expected'] if a['expected'] is not None else 'NOT_SPECIFIED'}/{a['actual']}|{b['expected'] if b['expected'] is not None else 'NOT_SPECIFIED'}/{b['actual']}|{r['ordered_WB_count']}/{r['ordered_STORE_count']}|\n")
# Only NEW stage artifacts; originals stay under frozen.json. This file excludes itself.
with (H/'SHA256SUMS.txt').open('x',encoding='utf-8') as f:
    for p in sorted(H.rglob('*')):
        if p.is_file() and p.name!='SHA256SUMS.txt':f.write(digest(p)+'  '+p.relative_to(H).as_posix()+'\n')
print(json.dumps(dict(status=summary['status'],DUT_runs=len(allruns),frozen_files=count,
    hashes=sources,independent_checks=summary['independent_full_wave_checks'],specified=specified,NOT_SPECIFIED=not_specified)))
