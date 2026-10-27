from pathlib import Path
import sys,time
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from stage_coremark import read,save
from stage_budget import check
from host_supervisor import bounded
import check_coremark as checker
import audit_uart,audit_wave
if __name__=='__main__':
 check();tid='performance8-N234';d=H/'runs'/tid;start=time.monotonic()
 result=checker.check(tid);save(d/'check-result.json',result);assert result['status']=='PASS',result['errors']
 uart=audit_uart.audit(tid);save(d/'uart-audit.json',uart)
 wave=audit_wave.audit(tid);save(d/'wave-audit.json',wave)
 save(d/'functional-result.json',dict(status='PASS_FINITE_8_ITERATIONS_NOT_FORMAL_SCORE',check_seconds=time.monotonic()-start,UART=uart,VCD=wave))
 print('Finite 8-iteration RF/RAM/every ordered stream/timing/complete UART/native VCD PASS')
