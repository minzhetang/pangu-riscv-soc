"""One additional frozen unit compile: improve high-word/carry test coverage.
No production RTL changes, no repetition of system tests for this TB extension.
"""
import sys,ctypes
sys.dont_write_bytecode=True
import run_stage as s
def prepare():
    files=[s.H/'source/cycle_counter64.sv',s.H/'source/soc_data_adapter.sv',s.H/'tests/tb_timer_unit_v2.sv',s.H/'unit_boundary.py',s.IVL,s.VVP]
    out=s.H/'compile/unit-v2.vvp'
    argv=[s.IVL,'-B',s.LIB,'-g2012','-Wall','-s','tb_timer_unit_v2','-o',out,*files[:3]]
    s.save(s.H/'unit-v2-plan.json',dict(maximum=1,timeout=30,argv=list(map(str,argv)),output=str(out),
        files=[dict(path=str(p),sha256=s.sha(p)) for p in files],purpose='read nonzero high word through actual router, both words all write masks, held-read no side effects'))
def verify():
    p=s.read(s.H/'unit-v2-plan.json');assert all(s.sha(x['path'])==x['sha256'] for x in p['files']);s.frozen();return p
def compile_one():
    p=verify();assert not ctypes.windll.shell32.IsUserAnAdmin()
    r=s.bounded(p['argv'],s.H,'compile-unit-v2',30)
    ok=r['returncode']==0 and not r['timed_out'] and not r['cap']
    s.save(s.H/'unit-v2-compile-result.json',dict(status='PASS' if ok else 'FAIL',process=r,output=p['output'],sha256=s.sha(p['output']) if ok else None))
    print('unit-v2 compile',ok)
def run():
    p=verify();c=s.read(s.H/'unit-v2-compile-result.json');assert c['status']=='PASS' and s.sha(c['output'])==c['sha256']
    d=s.H/'runs/unit-v2';d.mkdir()
    r=s.bounded([s.VVP,'-N','-M-','-M'+str(s.LIB),c['output']],d,'run-unit-v2',20)
    raw=s.log(r['stdout']);ok=r['returncode']==0 and not r['timed_out'] and not r['cap'] and 'TIMER_UNIT_V2_PASS' in raw and 'FATAL' not in raw
    s.save(s.H/'unit-v2-result.json',dict(status='PASS' if ok else 'FAIL',process=r,stdout=raw))
    print(raw)
if __name__=='__main__':{'prepare':prepare,'compile':compile_one,'run':run}[sys.argv[1]]()
