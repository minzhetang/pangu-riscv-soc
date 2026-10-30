from pathlib import Path
import sys,json,time,hashlib,ctypes,re
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from stage_budget import check
from host_supervisor import bounded
from host_checks import selftest,tree_bytes
from audit_case import audit
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(p,o):
 with p.open('x',encoding='utf8') as f:json.dump(o,f,ensure_ascii=False,indent=2)
def protect():
 for x in read(H/'PROTECTED_INPUTS.json')['files']:assert sha(Path(x['path']))==x['SHA256']
 return True
check();assert not ctypes.windll.shell32.IsUserAnAdmin();protect()
save(H/'HOST_PREFLIGHT.json',selftest())
frozen=[p for root in ['performance256','validation256'] for p in (H/root).rglob('*') if p.is_file()]+list(H.glob('*.py'))+[H/'PLAN.json']
save(H/'FROZEN_INPUTS.json',dict(before_native=True,files=[dict(path=str(p.relative_to(H)),SHA256=sha(p)) for p in frozen]))
def frozen_ok():
 for x in read(H/'FROZEN_INPUTS.json')['files']:assert sha(H/x['path'])==x['SHA256'],x['path']
last=[0.0]
def probe():
 check()
 if time.monotonic()-last[0]<.5:return
 last[0]=time.monotonic();assert tree_bytes(H)<=2*1024**3,'STAGE_BYTES_CAP'
 for tid in ['performance256','validation256']:
  assert tree_bytes(H/tid)<=512*1024**2,'CASE_BYTES_CAP'
  p=H/tid/'pds/flow.log'
  if p.exists():
   try:
    assert p.stat().st_size<=16*1024**2,'FLOW_LOG_CAP'
    pool=[int(x.replace(',','')) for x in re.findall(r'Peak memory pool usage is ([\d,]+) MB',p.read_text(encoding='utf-8-sig',errors='strict'))]
   except FileNotFoundError:continue
   assert not pool or max(pool)<=2048,'REPORTED_POOL_CAP'
rows=[]
try:
 for c in read(H/'PLAN.json')['cases']:
  check();protect();frozen_ok();d=H/c['id'];assert not list((d/'pds').rglob('*.sbit')) and not (d/'pds/compile').exists()
  save(d/'PDS_ATTEMPT.json',dict(used=1,max_case=1,max_stage=2,approval='D200',argv=c['argv'],cwd=c['cwd'],max_seconds=1800))
  started=time.time();r=bounded(c['argv'],c['cwd'],'pds-'+c['id'],1800,cap=1024**3,resource_probe=probe);ended=time.time()
  protect();frozen_ok();save(d/'BUILD_EXIT_RECEIPT.json',dict(status='EXITED_NOT_YET_ACCEPTED',process=r,started_epoch=started,ended_epoch=ended))
  rows.append(audit(c['id']))
 protect();frozen_ok();check()
 save(H/'RESULTS.json',dict(date='2026-10-30',status='SOFTWARE_BITSTREAMS_GENERATED_WITH_KNOWN_LIMITS',cases=rows,PDS=2,new_GCC=0,new_reference=0,new_DUT=0,protected=True,hardware='STOPPED',formal_score=False))
 print('Two nondebug software bitstreams accepted with known limits; hardware STOPPED',flush=True)
except Exception as exc:
 save(H/'STOPPED.json',dict(status='STOPPED_PRESERVE_EVIDENCE_NO_RETRY',exception_type=type(exc).__name__,message=str(exc)[:400],completed_audits=[x['id'] for x in rows],attempts=[p.parent.name for p in H.glob('*/PDS_ATTEMPT.json')],hardware='STOPPED'))
 print('Stopped; original error and local logs retained; no follow-on case',flush=True)
 raise
