from pathlib import Path
import sys,time
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from stage_coremark import save
import check_coremark,audit_uart,audit_wave
tid=sys.argv[1]+'-N234';d=H/'runs'/tid;t=time.monotonic()
r=check_coremark.check(tid);save(d/'check-result.json',r);assert r['status']=='PASS',r['errors']
u=audit_uart.audit(tid);save(d/'uart-audit.json',u)
w=audit_wave.audit(tid);save(d/'wave-audit.json',w)
save(d/'functional-result.json',dict(status='PASS_FINITE_2_ITERATIONS_NOT_FORMAL_SCORE',seconds=time.monotonic()-t,UART=u,VCD=w))
print(tid,'strict per-event RF RAM UART VCD PASS',flush=True)
