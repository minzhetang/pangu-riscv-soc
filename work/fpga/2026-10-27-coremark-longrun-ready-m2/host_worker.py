"""Host-only bounded stage entry. No compiler/DUT is reachable here."""
from pathlib import Path
import sys,json,time,hashlib
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;B=H.parent/'2026-10-25-coremark-iter2-m1'
from stage_coremark import read,sha
import check_coremark as c
import stream_peripherals as peripheral
import audit_uart

def save_new(p,o):
    with p.open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')

def replay(name):
    tid=name+'-N234';d=H/'replays'/tid;start=time.monotonic()
    result=c.check(tid,d);save_new(d/'check-result.json',result)
    old=read(B/'runs'/tid/'check-result.json')
    assert json.loads(json.dumps({k:v for k,v in result.items() if k!='streaming'}))==old,'not identical to F151 strict result'
    assert result['status']=='PASS'
    uart=audit_uart.audit(tid,directory=d);save_new(d/'uart-audit.json',uart)
    save_new(d/'replay-result.json',dict(status='PASS_OLD_REPLAY_NOT_NEW_DUT',old_result_identical=True,host_seconds=round(time.monotonic()-start,6),streaming=result['streaming'],UART=uart,trace_counts=result['trace_counts'],new_DUT=0))
    print(json.dumps(dict(id=tid,status='OLD_REPLAY_PASS',host_seconds=round(time.monotonic()-start,6),streaming=result['streaming']),ensure_ascii=False))
if __name__=='__main__':
    assert not sys.flags.optimize
    if sys.argv[1]=='model':
        result=peripheral.selftest();save_new(H/'controls/model-equivalence.json',result);print(json.dumps(result))
    elif sys.argv[1]=='replay':replay(sys.argv[2])
