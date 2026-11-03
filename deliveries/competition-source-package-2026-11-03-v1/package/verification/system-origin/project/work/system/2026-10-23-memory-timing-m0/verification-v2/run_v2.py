"""One permission-gated compilation; ordinary bounded model/CPU runs afterwards."""
from pathlib import Path
import argparse, datetime, difflib, hashlib, json, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
M0=HERE.parent
sys.path.insert(0,str(M0))
import run as old

def save(name,obj):old.save(HERE/name,obj)
def stamp():return datetime.datetime.now().astimezone().isoformat()
def verify():
    old.verify()
    rows=old.read(HERE/'frozen.json')['files']
    bad=[r['path'] for r in rows if old.sha(r['path'])!=r['sha256']]
    assert not bad,bad
    return dict(checked=len(rows),changed=[])

def prepare():
    old.verify()
    argv=[str(old.IVL),'-B',str(old.LIB),'-g2012','-Wall','-s','tb_cpu_timing',
        '-o',str(HERE/'cpu-v2.vvp'),str(HERE/'tb_cpu_timing.sv')]
    argv += [str(M0/'source'/name) for name in old.CPU_HASH]
    save('compile-command.json',dict(argv=argv,cwd=str(HERE),timeout_seconds=60,max_attempts=1,
        scope='third distinct M0 target; CPU unchanged; no simulation outside sandbox'))
    before=(M0/'tb_cpu_timing.sv').read_text(encoding='utf-8')
    after=(HERE/'tb_cpu_timing.sv').read_text(encoding='utf-8')
    with (HERE/'testbench.diff').open('x',encoding='utf-8') as f:
        f.writelines(difflib.unified_diff(before.splitlines(True),after.splitlines(True),
            fromfile=str(M0/'tb_cpu_timing.sv'),tofile=str(HERE/'tb_cpu_timing.sv')))
    paths=[Path(r['path']) for r in old.read(M0/'frozen-inputs.json')['files']]
    paths += [M0/name for name in ['results.json','result-after-external.json','stage-status-recovered.json',
        'logs/external-run-P02-i0-d0.stdout.log','external-compile/result.json']]
    paths += [HERE/name for name in ['PLAN.md','tb_cpu_timing.sv','run_v2.py','compile-command.json','testbench.diff']]
    save('frozen.json',dict(date_beijing=stamp(),files=[dict(path=str(p),sha256=old.sha(p)) for p in sorted(set(paths))]))
    print(json.dumps(dict(prepared=True,files=len(set(paths)),source_changed=False,inputs_changed=False)))

def compile_once():
    verify()
    save('compile-attempt.json',dict(date_beijing=stamp(),limit=1,simulation_allowed_here=False))
    command=old.read(HERE/'compile-command.json')
    r=old.bounded(command['argv'],HERE,'v2-compile-01',60)
    good=r['returncode']==0 and not r['timeout'] and not r['log_cap']
    output=HERE/'cpu-v2.vvp'
    r.update(status='COMPILED_NOT_RUN' if good and output.is_file() and output.stat().st_size>0 else 'TOOL_ERROR',
        output=str(output),output_sha256=old.sha(output) if output.is_file() else None,postflight=verify())
    save('compile-result.json',r)
    print(json.dumps(r,ensure_ascii=False))

def strict_ifid(text):
    fetches={};pairs=[];errors=[]
    for line in text.splitlines():
        t=line.split()
        if not t:continue
        if t[0]=='FETCH':fetches[int(t[1])]=t[2:4]
        elif t[0]=='IFID' and int(t[1]) in fetches:
            ok=t[2:4]==fetches[int(t[1])]
            pairs.append(dict(cycle=int(t[1]),match=ok))
            if not ok:errors.append(line)
    if len(pairs)!=len(fetches):errors.append('missing accepted FETCH -> IFID pair')
    return dict(checked=len(pairs),errors=errors)

def sim_all():
    verify()
    c=old.read(HERE/'compile-result.json')
    assert c['status']=='COMPILED_NOT_RUN'
    assert old.sha(c['output'])==c['output_sha256']
    save('simulation-attempt.json',dict(date_beijing=stamp(),compiler_executions=0,max_cpu_cycles=2000,timeout_seconds=30))
    def job(name,program='P02',f=0,d=0,extra=()):
        directory=HERE/'runs'/name;directory.mkdir(exist_ok=False)
        argv=[old.VVP,'-N','-M-','-M'+str(old.LIB),c['output'],
            '+PROGRAM='+str(M0/'inputs'/f'{program}.program.hex'),
            '+DATA='+str(M0/'inputs'/f'{program}.data.hex'),f'+IF_SYNC={f}',f'+DATA_SYNC={d}']+list(extra)
        r=old.bounded(argv,directory,'v2-run-'+name,30)
        return r,old.bounded_text(r['stdout']),directory/'wave.vcd'
    r,text,wave=job('model-selftest',extra=['+MEMORY_SELFTEST'])
    good=r['returncode']==0 and not r['timeout'] and not r['log_cap'] and 'MODEL_SELFTEST_PASS checks=7 CPU_active_cycles=0' in text and wave.is_file()
    result=dict(date_beijing=stamp(),scope='M0 verification v2, not a CPU fix or physical memory mapping',
        model_selftest=dict(status='PASS' if good else 'FAIL',process=r,wave=str(wave)),cpu=[])
    if good:
        # Run the complete control group before any latency characterization.
        cases=old.read(M0/'inputs/cases.json')
        for f,d in [(0,0),(1,0),(0,1),(1,1)]:
            for case in cases:
                name=f"{case['id']}-i{f}-d{d}"
                r,text,wave=job(name,case['id'],f,d)
                checked=old.check_log(text,case['expected'])
                pairing=strict_ifid(text)
                checked['ifid_pairing']=pairing
                if pairing['errors']:
                    checked['status']='FAIL';checked['issues']+=pairing['errors']
                if r['timeout']:checked['status']='TIMEOUT'
                elif r['returncode']!=0:checked['status']='TOOL_ERROR'
                if not wave.is_file():checked['status']='FAIL';checked['issues'].append('no new VCD')
                checked.update(id=case['id'],if_sync=f,data_sync=d,process=r,wave=str(wave),
                    expected=case['expected'])
                save(f'{name}.json',checked)
                result['cpu'].append(checked)
            if f==0 and d==0 and any(x['status']!='PASS' for x in result['cpu']):
                result['control_group_failed']=True
                break
    result['postflight']=verify()
    result['status']='MODEL_CHECK_FAILED' if not good else ('CONTROL_GROUP_FAILED' if result.get('control_group_failed') else 'PROBE_RUNS_COMPLETED_NOT_ADAPTATION_ACCEPTANCE')
    save('result.json',result)
    print(json.dumps(dict(status=result['status'],model=result['model_selftest']['status'],
        cases=[dict(id=x['id'],if_sync=x['if_sync'],data_sync=x['data_sync'],status=x['status'],issues=x['issues'][:3]) for x in result['cpu']]),ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','compile','simulate','verify'])
    a=p.parse_args().action
    if a=='prepare':prepare()
    elif a=='compile':compile_once()
    elif a=='simulate':sim_all()
    else:print(json.dumps(verify()))
