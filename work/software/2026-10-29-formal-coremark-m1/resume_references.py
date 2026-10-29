from pathlib import Path
import sys,json,time,hashlib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
def save(p,o):
 with p.open('x',encoding='utf8') as f:json.dump(o,f,indent=2)
old=json.loads((H/'STAGE_CLOCK.json').read_text());now=time.monotonic()
save(H/'RECOVERY_CLOCK.json',dict(start=now,deadline_monotonic=max(now,old['deadline_monotonic']) if now<old['deadline_monotonic'] else now+7200,old_clock=old,old_expired=now>old['deadline_monotonic'],approval='2026-10-29 user 批准，继续; replacement preflight and remaining tests; old clock retained'))
worker=(H/'reference_worker-r1-PENDING.py').read_text().replace("H/'oracles'/tid","H/'oracles-recovery'/tid")
(H/'reference_worker-r1.py').write_text(worker,encoding='utf8')
(H/'oracles-recovery').mkdir()
from host_supervisor import bounded
for tid in ['performance2','validation2','performance256','validation256']:
 save(H/(tid+'-recovery-attempt.json'),dict(used=1,maximum=1,worker_sha256=hashlib.sha256(worker.encode()).hexdigest()))
 bounded([sys.executable,'-B',H/'reference_worker-r1.py',tid],H,'reference-recovery-'+tid,300 if tid.endswith('2') else 1200)
