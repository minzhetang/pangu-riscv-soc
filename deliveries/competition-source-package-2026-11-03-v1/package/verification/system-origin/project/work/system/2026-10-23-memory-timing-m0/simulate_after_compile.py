"""Ordinary-user simulation only; never invokes a compiler or a historical VVP."""
import datetime, json, sys
sys.stdout.reconfigure(encoding='utf-8')
import run as m

m.verify()
compile_result=m.read(m.ROOT/'external-compile/result.json')
assert compile_result['status']=='COMPILED_NOT_SIMULATED'
assert len(compile_result['compiles'])==2 and all(x['returncode']==0 for x in compile_result['compiles'])
outputs={r['target']:r['output'] for r in compile_result['compiles']}
m.save(m.ROOT/'external-compile/outputs-sha256.json',dict(files=[dict(path=p,sha256=m.sha(p)) for p in outputs.values()]))
result=dict(scope='M0 characterization, no RTL modifications',cpu=[],drm=None,
            historical_failure='results.json',compile_result='external-compile/result.json')
d=m.ROOT/'runs/drm'; d.mkdir(exist_ok=False)
rr=m.bounded([m.VVP,'-N','-M-','-M'+str(m.LIB),outputs['drm']],d,'external-run-drm',30)
text=m.bounded_text(rr['stdout'])
passed=rr['returncode']==0 and 'DRM_PASS checks=13' in text and (d/'wave.vcd').is_file()
result['drm']=dict(status='PASS' if passed else 'FAIL',process=rr,wave=str(d/'wave.vcd'))
if passed:
    for c in m.read(m.ROOT/'inputs/cases.json'):
        for f,dm in [(0,0),(1,0),(0,1),(1,1)]:
            name=f"{c['id']}-i{f}-d{dm}"
            d=m.ROOT/'runs'/name; d.mkdir(exist_ok=False)
            rr=m.bounded([m.VVP,'-N','-M-','-M'+str(m.LIB),outputs['cpu'],
                '+PROGRAM='+str(m.ROOT/'inputs'/f"{c['id']}.program.hex"),
                '+DATA='+str(m.ROOT/'inputs'/f"{c['id']}.data.hex"),f'+IF_SYNC={f}',f'+DATA_SYNC={dm}'],d,'external-run-'+name,30)
            checked=m.check_log(m.bounded_text(rr['stdout']),c['expected'])
            if rr['timeout']: checked['status']='TIMEOUT'
            elif rr['returncode']!=0: checked['status']='TOOL_ERROR'
            if not (d/'wave.vcd').is_file(): checked['status']='FAIL'; checked['issues'].append('no new VCD')
            checked.update(id=c['id'],if_sync=f,data_sync=dm,process=rr,wave=str(d/'wave.vcd'))
            result['cpu'].append(checked)
result['status']='CHARACTERIZATION_COMPLETED' if passed else 'MODEL_CHECK_FAILED_CPU_NOT_RUN'
result['postflight']=m.verify()
result['date_beijing']=datetime.datetime.now().astimezone().isoformat()
m.save(m.ROOT/'result-after-external.json',result)
print(json.dumps(dict(status=result['status'],drm=result['drm']['status'],
    cases=[dict(id=x['id'],if_sync=x['if_sync'],data_sync=x['data_sync'],status=x['status'],issues=x['issues'][:4]) for x in result['cpu']]),ensure_ascii=False))
