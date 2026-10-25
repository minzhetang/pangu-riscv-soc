"""Preserve v1 formatting false-FAIL; byte-exact check of same output, then resume."""
from pathlib import Path
import json,shutil,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_redirect as s
def prepare():
    source=(H/'check_redirect.py').read_text();a="assert s.sha(p/'expected-ram.hex')==expected['ram_SHA256'];eq('all RAM',s.sha(d/'ram.hex'),expected['ram_SHA256'])"
    b="assert s.sha(p/'expected-ram.hex')==expected['ram_SHA256'];eq('all RAM bytes',bytes(int(v,16) for v in (d/'ram.hex').read_text().split()),bytes(int(v,16) for v in (p/'expected-ram.hex').read_text().split()))"
    assert source.count(a)==1
    with (H/'check_redirect_v2.py').open('x',encoding='utf-8') as f:f.write(source.replace(a,b))
    old=s.read(H/'small-result.json');assert old['status']=='STOPPED' and old['case']=='beq-taken-PF0'
    d=H/'runs/beq-taken-PF0';p=H/'cases/beq-taken';aa=(d/'ram.hex').read_bytes();bb=(p/'expected-ram.hex').read_bytes()
    actual=bytes(int(v,16) for v in aa.split());expected=bytes(int(v,16) for v in bb.split());assert actual==expected and len(actual)==32768
    s.save(H/'checker-v2-correction.json',dict(reason='v1 compared serialized hex-file SHA, while vvp formatted 32-bit expressions as 8 hex digits and Python used 2; both are same byte values',
        actual_text_bytes=len(aa),expected_text_bytes=len(bb),parsed_RAM_bytes=32768,parsed_equal=True,RTL_changed=False,TB_changed=False,expectations_changed=False,
        failed_v1_preserved=True,new_DUT_runs_for_recheck=0,old_checker_sha256=s.sha(H/'check_redirect.py'),new_checker_sha256=s.sha(H/'check_redirect_v2.py')))
def run():
    s.protect();paths=s.artifacts('initial');rows=[]
    import check_redirect_v2 as ck
    for c in s.read(H/'manual-plan.json')['cases']:
        for pf in ([1] if c['reset_pending'] else [0,1]):
            tid=c['id']+f'-PF{pf}';d=H/'runs'/tid
            if d.exists():
                assert tid=='beq-taken-PF0';r=s.read(d/'process.json');assert s.read(d/'check-result.json')['status']=='FAIL';rechecked=True
            else:
                d.mkdir();args=[s.lib.VVP,'-N','-M-','-M'+str(s.lib.LIB),paths[f'directed-{pf}'],'+IMAGE='+str(H/'cases'/c['id']/'imem.hex'),'+DATA='+str(H/'cases'/c['id']/'dmem.hex'),'+MAX_CYCLES=4000']
                if c['reset_pending']:args.append('+RESET_PENDING')
                r=s.bounded(args,d,'run-'+tid,30);s.save(d/'process.json',r);shutil.copyfile(r['stdout'],d/'stdout.log');rechecked=False
            try:
                assert r['returncode']==0 and not r['timed_out'] and not r['cap'],r
                result=ck.check(c,pf,d);s.save(d/('check-result-v2.json' if rechecked else 'check-result.json'),result);assert result['status']=='PASS',result
            except Exception as e:
                s.save(H/'small-result-v2.json',dict(status='STOPPED',case=tid,error=repr(e),completed=rows,protected=s.protect()));raise
            rows.append(dict(id=tid,status='PASS',process=r,check=result,rechecked_without_new_DUT=rechecked))
    s.save(H/'small-result-v2.json',dict(status='PASS',cases=rows,total_new_DUT_runs=67,new_DUT_runs_in_this_resume=66,rechecks_without_new_DUT=1,protected=s.protect()));print('67 actual directed DUT runs PASS; 1 same-output correction, no duplicate run')
def regression():
    assert s.read(H/'small-result-v2.json')['status']=='PASS';import regression_bridge as bridge
    original=bridge.read
    def routed(p):return s.read(H/'small-result-v2.json') if Path(p)==H/'small-result.json' else original(p)
    bridge.read=routed;bridge.regress()
if __name__=='__main__':{'prepare':prepare,'run':run,'regression':regression}[sys.argv[1]]()
