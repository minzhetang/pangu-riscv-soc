"""Strict finite-board-report check. Does not claim unseen GPIO edges or retirement."""
from pathlib import Path
import json,re,sys,hashlib
ROOT=Path(__file__).resolve().parent
def need(ok,why):
 if not ok:raise ValueError(why)
def check(raw,case,transport):
 need(transport['transport_clean'] and transport['end_marker_seen'],'UART transport incomplete/error')
 text=raw.decode('ascii',errors='strict');lines=text.splitlines()
 need(lines and re.fullmatch(r'REC2 (?:[0-9a-f]{8} ){14}',lines[0]),'Header framing/field count')
 need(lines[-1]=='END' and raw.endswith(b'\nEND\n'),'Complete END and no trailing bytes')
 h=[int(x,16) for x in lines[0].split()[1:]]
 period,count,wait,done,dense,start,end,work,late,retained,evicted,rejected,fault,frozen=h
 need((period,count,wait,done,dense,late)==(2700000,128,20,128,0,0),'Fixed production parameters/sample completion/overload')
 need(0<work<period*count,'Plausible nonzero processing time')
 duration=(end-start)&0xffffffff
 need(period*count<=duration<=period*count+2000,'Full batch target timer interval')
 ev=[]
 for row in lines[1:-1]:
  need(bool(re.fullmatch(r'E (?:[0-9a-f]{8} ){4}',row)),'Malformed/extra event/duplicate report')
  t,i,s,r=[int(x,16) for x in row.split()[1:]]
  need(i<128 and s<=7 and r<=3,'Event range')
  offset=(t-start)&0xffffffff
  need(0<=offset-(i+1)*period<=2000,'Software observation time vs fixed sample index')
  if ev:need(i>ev[-1][1] and offset>((ev[-1][0]-start)&0xffffffff),'Ordered nonduplicate event/index/tick')
  ev.append([t,i,s,r])
 need(len(ev)==retained and retained<=8 and evicted==0,'Exact retained ledger/eviction')
 expected=json.loads((ROOT/'PLAN.json').read_text())['scenarios'][case]
 need([x[2] for x in ev]==expected['states'],'Exact observed state sequence')
 need([x[3] for x in ev]==expected.get('reasons',[]),'Exact event reason sequence')
 need(fault==expected['fault'] and frozen==expected['frozen'],'Fault/freeze state')
 if case in ['idle','normal']:need(rejected==0,'Unexpected rejected event')
 if case=='timeout':need(ev[1][1]-ev[0][1]==wait,'Timeout age exactly WAIT_SAMPLES')
 return dict(status='PASS_LIMITED_BOARD_LEDGER',case=case,header=h,events=ev,elapsed_target_ticks=duration,nominal_seconds=duration/27000000,source_SHA256=hashlib.sha256(raw).hexdigest().upper(),limits=['Human input timing not independently edge-captured','No physical pulse completeness or internal WB/STORE/stop-status claim','Nominal 27MHz, no oscillator calibration'])
if __name__=='__main__':
 H=Path(sys.argv[1]);case=sys.argv[2]
 try:result=check((H/'uart-raw.bin').read_bytes(),case,json.loads((H/'SERIAL_RESULT.json').read_text()))
 except Exception as e:result=dict(status='FAIL',case=case,error=type(e).__name__+': '+str(e))
 with (H/'REPORT_CHECK.json').open('x',encoding='utf8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
 print(json.dumps(result,ensure_ascii=False))
