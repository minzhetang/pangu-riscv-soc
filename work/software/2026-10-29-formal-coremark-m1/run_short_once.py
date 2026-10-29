from pathlib import Path
import sys,time,shutil
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2]
from stage_coremark import read,save,sha
from stage_budget import check,deadline
from host_supervisor import bounded
from stream_io import Archiver,require
tid=sys.argv[1];assert tid in ['performance2','validation2'];check()
for x in read(H/'SHORT_FROZEN_INPUTS.json')['files']:assert sha(H/x['path'])==x['SHA256']
target=next(x for x in read(H/'SHORT_COMPILE_PLAN.json')['targets'] if x['id']==tid)
save(H/(tid+'-compile-attempt.json'),dict(used=1,maximum=1))
comp=bounded(target['argv'],H,'compile-'+tid,120)
vvpfile=H/'compile'/(tid+'.vvp');assert vvpfile.is_file() and vvpfile.stat().st_size>0
save(H/(tid+'-compile-result.json'),dict(status='COMPILED_NOT_FUNCTIONAL_PASS',process=comp,SHA256=sha(vvpfile)))
save(H/(tid+'-DUT-attempt.json'),dict(used=1,maximum=1,physical_limit=12000000))
run=H/'runs'/(tid+'-N234');run.mkdir();(run/'spool').mkdir();end=deadline(900)
state=dict(offset=0,pending=b'',ready_events=0,peak_spool=0);last_probe=[0.0]
def probe():
 check(end)
 size=0
 for p in (run/'spool').iterdir():
  try:size+=p.stat().st_size
  except FileNotFoundError:pass
 state['peak_spool']=max(size,state['peak_spool']);require(size<=32*1024**2,'SPOOL_CAP')
 for n,cap in [('wave.vcd',256*1024**2),('uart-pins.log',8*1024**2)]:
  p=run/n
  if p.exists():require(p.stat().st_size<=cap,n+'_CAP')
 if time.monotonic()-last_probe[0]>1:
  size=0
  for p in H.rglob('*'):
   try:
    if p.is_file():size+=p.stat().st_size
   except FileNotFoundError:pass
  require(size<=2*1024**3,'TOTAL_STAGE_EVIDENCE_CAP');last_probe[0]=time.monotonic()
arch=Archiver(run,deadline=end,poll=probe)
def collect(logdir,exitcode):
 probe();p=logdir/'stdout.log'
 if not p.exists():return
 with p.open('rb') as f:f.seek(state['offset']);data=f.read(8*1024**2+1)
 state['offset']+=len(data);state['pending']+=data;require(len(state['pending'])<=8*1024**2,'STDOUT_PENDING_CAP')
 parts=state['pending'].split(b'\n');state['pending']=parts.pop()
 for line in parts:
  text=line.rstrip(b'\r').decode('utf-8-sig')
  if text.startswith(('SEGMENT|','END_STREAM|')):arch.consume(text);state['ready_events']+=text.startswith('SEGMENT|')
 if exitcode is not None:require(not state['pending'],'TRUNCATED_STDOUT')
lib=P/'tools/iverilog-13.0-msys2-ucrt64/ucrt64/lib/ivl';vvp=lib.parents[1]/'bin/vvp.exe'
r=bounded([vvp,'-N','-M-','-M'+str(lib),vvpfile,'+MAX_CYCLES=12000000'],run,'run-'+tid,max(.001,end-time.monotonic()),while_running=collect,resource_probe=probe)
specs=arch.finish();save(run/'process.json',r);shutil.copyfile(r['stdout'],run/'stdout.log');save(run/'capture-result.json',dict(status='CAPTURE_ONLY_NOT_FUNCTIONAL_PASS',streams=specs,supervisor={k:v for k,v in state.items() if k!='pending'}))
bounded([sys.executable,'-B',H/'check_short_worker.py',tid],H,'final-check-'+tid,300)
