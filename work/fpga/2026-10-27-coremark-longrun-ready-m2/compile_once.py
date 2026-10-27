from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;R=H.parent/'2026-10-25-coremark-iter2-m1';M=H.parent/'2026-10-26-coremark-stream-evidence-m1'
sys.dont_write_bytecode=True
from stage_coremark import read,save,sha
from stage_budget import check
from host_supervisor import bounded
from preserve import protect
if __name__=='__main__':
 check();protect();assert read(H/'controls/container-results.json')['status']=='PASS_HOST_ONLY'
 for n in ['performance','validation']:assert read(H/'replays'/(n+'-N234')/'replay-result.json')['status']=='PASS_OLD_REPLAY_NOT_NEW_DUT'
 assert read(H/'oracle-freeze.json')['iterations']==8
 assert not (H/'compile-attempt.json').exists();assert not (H/'compile/performance8-N234.vvp').exists()
 target=read(R/'compile-plan.json')['targets'][0];args=[]
 for a in target['argv']:
  a=a.replace(str(R/'cases/performance-N234'),str(H/'cases/performance8-N234')).replace(str(R/'tests'),str(H/'tests')).replace(str(R/'compile/performance-N234.vvp'),str(H/'compile/performance8-N234.vvp'))
  args.append(a)
 assert sha(H/'block_codec.py')==sha(M/'block_codec.py')
 frozen=[p for p in H.rglob('*') if p.is_file() and (p.parent==H and p.suffix=='.py' or any(p.is_relative_to(H/x) for x in ['source','models','tests','cases/performance8-N234/source','oracles/performance8']))]
 save(H/'frozen-inputs.json',dict(status='BEFORE_COMPILE_AND_DUT',files=[dict(path=str(p.relative_to(H)),SHA256=sha(p)) for p in frozen]))
 save(H/'compile-plan.json',dict(maximum=1,targets=[dict(id='performance8-N234',argv=args)],timeout=120))
 save(H/'compile-attempt.json',dict(used=1,maximum=1,decision='D160'))
 r=bounded(args,H,'compile-performance8',120)
 p=H/'compile/performance8-N234.vvp';assert p.is_file() and p.stat().st_size>0
 save(H/'compile-result.json',dict(status='COMPILED_NOT_FUNCTIONAL_PASS',output=str(p),bytes=p.stat().st_size,SHA256=sha(p),process=r))
 print('ONE compile complete; process exited and fresh VVP verified; DUT not run')
