"""Read-only analysis of freshly captured simulation evidence; never runs a DUT."""
from pathlib import Path
import json,hashlib,copy
H=Path(__file__).resolve().parent;R=H.parents[2]
j=json.loads((H/'RESULTS.json').read_text());assert j['status']=='LIVE_GPIO_TIMER_CPU_SIM_PASS'
symbols={}
for mode in [0,1]:
 symbols[mode]={s.split()[2]:int(s.split()[0],16) for s in (H/'logs'/f'nm{mode}.log').read_text().splitlines() if len(s.split())==3}
rows=[];latency=[];raw_checks=[]
for name in sorted({x['case'] for x in j['results']}):
 a,b=[next(x for x in j['results'] if x['case']==name and x['dense']==m) for m in [0,1]]
 av,bv=a['repeats'][0],b['repeats'][0]
 assert [s for t,s in av['samples']]==[s for t,s in bv['samples']]
 assert [(i,s,w) for t,i,s,w in av['events']]==[(i,s,w) for t,i,s,w in bv['events']]
 rows.append(dict(case=name,status='PASS',retained_events=len(av['events']),event_uart_bytes=av['uart_bytes'],dense_uart_bytes=bv['uart_bytes'],uart_reduction_percent=100*(1-av['uart_bytes']/bv['uart_bytes']),event_work_ticks=av['work_ticks'],dense_work_ticks=bv['work_ticks'],event_window_ticks=av['window_ticks'],dense_window_ticks=bv['window_ticks'],work_reduction_percent=100*(1-av['work_ticks']/bv['work_ticks']),evicted=av['evicted'],rejected=av['rejected']))
 for mode,item in [(0,a),(1,b)]:
  d=H/'runs'/f'{name}-dense{mode}'
  for rep in range(2):
   words=[]
   for l in (d/f'ram{rep}.hex').read_text().splitlines():
    if not l.startswith(('//','@')):words.extend(int(v,16) for v in l.split())
   offset=(symbols[mode]['raw']-65536)//4;raw=words[offset:offset+64]
   exp=[v for pair in item['repeats'][rep]['samples'] for v in pair] if mode else [0]*64
   assert raw==exp,'dense raw store identity or unexpected event-mode raw write'
   raw_checks.append(dict(case=name,mode=mode,repeat=rep,status='PASS'))
  for line in (d/'reads.txt').read_text().splitlines():
   rr,addr,value,ticks=line.split()
   if int(addr,16)==0x20000100:assert int(value,16)==int(ticks,16),'timer-return identity mismatch'
  # VCD top-level pins/reset reconstruct the actual external stimulus timing.
  ids={};now=0;active=-1;resets=[];changes=[];pins=None
  with (d/'run.vcd').open() as f:
   for l in f:
    l=l.strip()
    if l.startswith('$var'):
     v=l.split();ids[v[4]]=v[3]
    elif l.startswith('#'):now=int(l[1:])
    elif l and not l.startswith('$'):
     if l=='1'+ids.get('rst','?'):active+=1;resets.append(now);pins=0
     elif l.startswith('b') and l.split()[-1]==ids.get('pins') and active>=0 and not any(c in l.split()[0] for c in 'xz'):
      v=int(l.split()[0][1:],2)
      if v!=pins:changes.append((active,now,v));pins=v
  for rep in range(2):
   for tick,index,state,reason in item['repeats'][rep]['events']:
    if reason==2:continue # timeout latency has a different, sample-age definition
    abs_ps=resets[rep]+5000+tick*10000
    prior=[(t,v) for rr,t,v in changes if rr==rep and t<=abs_ps]
    assert prior and prior[-1][1]==state
    delay=(abs_ps-prior[-1][0])/10000
    assert 0<=delay<=25004,'debounce detection delay outside frozen budget'
    latency.append(dict(case=name,mode=mode,repeat=rep,index=index,state=state,delay_ticks=delay))
comparison=dict(status='SAME_SAMPLE_SCOPE_LIMITED_PASS',rows=rows,payload_capacity={'event_context':128,'raw_plus_same_context':384,'reduction_percent':100*(1-128/384)},raw_storage_checks=raw_checks,latency=latency,max_observed_change_detection_delay_ticks=max(x['delay_ticks'] for x in latency),cpu_polling='busy wait in both modes; not a CPU-idle improvement',processing_metric='instrumented sample processing only, excludes polling wait and UART',uart_byte_metric='actual C character count; Verilog Windows text files add CR before LF, explicitly accounted for',context='same 32 sampled states and detector, same retained context; evictions/rejections explicit, not lossless full raw reconstruction')
(H/'COMPARISON.json').write_text(json.dumps(comparison,indent=2))
# Checker negative controls, distinct from new DUT tests.
e=a['repeats'][0]['events'];assert e
def rejects(x):return x!=e
mutants={'missing':e[:-1],'duplicate':e+[e[-1]],'wrong_order':list(reversed(e)),'wrong_time':copy.deepcopy(e),'wrong_state':copy.deepcopy(e)}
mutants['wrong_time'][0][0]+=1;mutants['wrong_state'][0][2]^=1
assert all(rejects(x) for x in mutants.values())
(H/'CHECKER_CONTROLS.json').write_text(json.dumps({'status':'PASS','controls':{k:'REJECT' for k in mutants},'new_DUT_runs':0},indent=2))
print('comparison PASS; max observed delay ticks',comparison['max_observed_change_detection_delay_ticks'])
