"""Fixed permission-gated compiler target; ordinary isolated routing unit run."""
import sys,ctypes,json,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2]
spec=importlib.util.spec_from_file_location('helpers',P/'work/system/2026-10-23-memory-adapt-m1/run_stage.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);s.HERE=H
def prepare():
    argv=[s.IVL,'-B',s.LIB,'-g2012','-Wall','-s','tb_data_adapter','-o',H/'build/adapter.vvp',
        H/'source/soc_data_adapter.sv',H/'tests/tb_data_adapter.sv']
    paths=[s.IVL,s.VVP,H/'source/soc_data_adapter.sv',H/'tests/tb_data_adapter.sv',H/'verify_adapter.py']
    s.save(H/'adapter-compile-plan.json',dict(maximum=1,timeout_seconds=60,only_compile=True,argv=list(map(str,argv)),
        protected=[dict(path=str(p),sha256=s.sha(p)) for p in paths]))
def check():
    plan=s.read(H/'adapter-compile-plan.json')
    assert all(s.sha(r['path'])==r['sha256'] for r in plan['protected'])
    return plan
def compile_one():
    plan=check();assert not ctypes.windll.shell32.IsUserAnAdmin()
    s.save(H/'adapter-compile-attempt.json',dict(maximum=1,non_admin=True))
    r=s.bounded(plan['argv'],H/'build','adapter-compile',60)
    output=H/'build/adapter.vvp';ok=r['returncode']==0 and not r['timed_out'] and output.is_file()
    s.save(H/'adapter-compile-result.json',dict(status='PASS_NOT_RUN' if ok else 'FAIL',process=r,
        sha256=s.sha(output) if output.exists() else None))
    print('adapter compile',ok)
def run():
    check();c=s.read(H/'adapter-compile-result.json');assert c['status']=='PASS_NOT_RUN'
    assert s.sha(H/'build/adapter.vvp')==c['sha256']
    folder=H/'tests/adapter-run';folder.mkdir()
    r=s.bounded([s.VVP,'-N','-M-','-M'+str(s.LIB),H/'build/adapter.vvp'],folder,'adapter-run',30)
    text=s.text_log(r['stdout']);ok=r['returncode']==0 and not r['timed_out'] and 'ADAPTER_UNIT_PASS checks=9792' in text and 'FATAL' not in text
    s.save(H/'adapter-result.json',dict(status='PASS' if ok else 'FAIL',process=r,checks=9792,
        scope='CPU-side address/data routing unit only, no CPU, RAM primitive or B module instantiated',complete_system='NOT_RUN'))
    print('adapter unit',ok)
if __name__=='__main__':{'prepare':prepare,'compile':compile_one,'run':run}[sys.argv[1]]()
