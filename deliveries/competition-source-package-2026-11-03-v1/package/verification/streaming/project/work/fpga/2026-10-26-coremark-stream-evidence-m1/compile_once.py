"""Exactly one compiler invocation; business scope D156, tool permission separate."""
from pathlib import Path
import sys,json,ctypes
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
from stage_coremark import read,sha
from stream_io import save
from host_supervisor import bounded

def protect():
    rows=read(H/'protected-originals.json')['files']
    for row in rows:assert sha(row['path'])==row['SHA256'],row['path']
    B=H.parent/'2026-10-25-coremark-iter2-m1'
    for root in ['source','cases/performance-N234/source']:
        for p in (H/root).iterdir():
            if p.is_file():assert sha(p)==sha(B/root/p.name),str(p)
    for name in ['cpu_program_reference.py','peripheral_checker.py']:assert sha(H/'models'/name)==sha(B/'models'/name)
    return len(rows)
if __name__=='__main__':
    assert not sys.flags.optimize and not ctypes.windll.shell32.IsUserAnAdmin()
    assert read(H/'controls/negative-results.json')['status']=='PASS'
    assert read(H/'controls/model-equivalence.json')['status']=='PASS'
    for name in ['performance','validation']:assert read(H/'replays'/(name+'-N234')/'replay-result.json')['old_result_identical']
    plan=read(H/'compile-plan.json');assert plan['maximum']==1 and len(plan['targets'])==1
    row=plan['targets'][0];out=Path(row['output']);assert not out.exists()
    frozen=[dict(path=str(p),SHA256=sha(p)) for root in ['source','models','tests','cases/performance-N234/source','build','oracles'] for p in (H/root).rglob('*') if p.is_file()]
    for name in ['check_coremark.py','frozen_checks.py','stream_io.py','stream_peripherals.py','audit_uart.py','audit_wave.py']:frozen.append(dict(path=str(H/name),SHA256=sha(H/name)))
    save(H/'frozen-live-inputs.json',dict(files=frozen))
    save(H/'compile-attempt.json',dict(maximum=1,used=1,decision='D156',before_originals=protect(),scope='logging-only TB; same 13RTL/initialization/images; no GCC'))
    r=bounded(row['argv'],H,'compile-performance-N234',120)
    assert out.is_file() and out.stat().st_size>0
    save(H/'compile-result.json',dict(status='PASS_COMPILE_ONLY_NOT_DUT',rows=[dict(id=row['id'],output=str(out),SHA256=sha(out),process=r)],protected=protect()))
    print('Single compiler exited; new VVP verified; DUT has not been executed',flush=True)
