from pathlib import Path
from collections import Counter
import ast,datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
M0=HERE.parent
sys.path.insert(0,str(M0))
import run as old
old.verify()
result=old.read(HERE/'result.json');wave=old.read(HERE/'wave-audit.json')
assert result['model_selftest']['status']=='PASS' and wave['status']=='PASS'
tree=ast.parse((HERE/'audit_waves.py').read_text(encoding='utf-8'))
ns={}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='frames'],type_ignores=[]),'frames','exec'),ns)
model_samples=[]
for t,b,a,ids in ns['frames'](HERE/'runs/model-selftest/wave.vcd'):
    if t in [45000,65000,85000]:
        def v(key):return int(a[ids[key]],2)
        model_samples.append(dict(time_ps=t,async_data=v('async_data'),registered_data=v('dq'),legacy_data=v('legacy_function_data')))
assert model_samples[0]['async_data']==0x11223344 and model_samples[0]['legacy_data']==0xa5a5a5a5
groups=[]
for f,d in [(0,0),(1,0),(0,1),(1,1)]:
    rows=[x for x in result['cpu'] if x['if_sync']==f and x['data_sync']==d]
    groups.append(dict(if_sync=f,data_sync=d,counts=dict(Counter(x['status'] for x in rows))))
summary=dict(date_beijing=datetime.datetime.now().astimezone().isoformat(),groups=groups,
    counts=dict(Counter(x['status'] for x in result['cpu'])),all_process_native_zero=all(x['process']['returncode']==0 for x in result['cpu']),
    process_timeouts=sum(x['process']['timeout'] for x in result['cpu']),
    cycles_min=min(x['actual']['cycles'] for x in result['cpu']),cycles_max=max(x['actual']['cycles'] for x in result['cpu']),
    sim_time_ps_min=min(x['actual']['time_ps'] for x in result['cpu']),sim_time_ps_max=max(x['actual']['time_ps'] for x in result['cpu']),
    CPU_wall_seconds_total=round(sum(x['process']['elapsed_seconds'] for x in result['cpu']),6),
    CPU_wall_seconds_min=min(x['process']['elapsed_seconds'] for x in result['cpu']),
    CPU_wall_seconds_max=max(x['process']['elapsed_seconds'] for x in result['cpu']),
    memory_model_wave_samples=model_samples,wave_consistency_checks=wave['total_checks'],
    key_counterexamples={x['id']:x for x in wave['audits'] if x['id'] in ['P01-i1-d0','P05-i0-d1','P02-i0-d0']},
    E1='LIMITED_CHARACTERIZATION_COMPLETE',E2='NOT_IMPLEMENTED_NOT_APPROVED',hardware='STOP')
old.save(HERE/'summary.json',summary)
lines=['# M0 v2完整CPU逐例结果\n','|程序|组合IF/组合DATA|同步IF/组合DATA|组合IF/同步DATA|同步IF/同步DATA|\n','|---|---|---|---|---|\n']
for case in old.read(M0/'inputs/cases.json'):
    row=[]
    for f,d in [(0,0),(1,0),(0,1),(1,1)]:
        x=next(x for x in result['cpu'] if x['id']==case['id'] and x['if_sync']==f and x['data_sync']==d)
        row.append(f"{x['status']} / {x['actual']['cycles']}周期 / stall{x['actual']['stall']},flush{x['actual']['flush']}")
    lines.append('|'+case['id']+'|'+'|'.join(row)+'|\n')
with (HERE/'RESULT_MATRIX.md').open('x',encoding='utf-8') as f:f.writelines(lines)
paths=[p for p in HERE.rglob('*') if p.is_file()]
paths += [Path(x['process']['stdout']) for x in result['cpu']]+[Path(x['process']['stderr']) for x in result['cpu']]
paths += [M0/'logs'/name for name in ['v2-compile-01.command.json','v2-compile-01.stderr.log','v2-compile-01.stdout.log','v2-run-model-selftest.stdout.log']]
with (HERE/'SHA256SUMS.txt').open('x',encoding='utf-8') as f:
    for p in sorted(set(paths)):f.write(f'{old.sha(p)}  {p}\n')
print(json.dumps({k:v for k,v in summary.items() if k!='key_counterexamples'},ensure_ascii=False))
