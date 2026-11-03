from pathlib import Path
import json
from execute import H,compile_sw,simulate,save
plan=json.loads((H/'FROZEN_PLAN.json').read_text())
# Additional expectations frozen before these builds/runs; old cases unchanged.
newplan={
 'normal128':dict(input=plan['cases']['normal']['input']+[0]*96,events=plan['cases']['normal']['events'],fault=0,evicted=0,rejected=0,frozen=0),
 'wrap_fault128':dict(input=plan['cases']['wrap_fault_window']['input']+[0]*96,events=plan['cases']['wrap_fault_window']['events'],fault=1,evicted=5,rejected=1,frozen=1),
 'timeout20':dict(input=[0]*2+[1]*126,events=[[3,1,0],[23,1,2]],fault=2,evicted=0,rejected=0,frozen=0)
}
if (H/'EXTENDED_PLAN.json').exists():assert json.loads((H/'EXTENDED_PLAN.json').read_text())==newplan
else:save(H/'EXTENDED_PLAN.json',newplan)
def check(d,c,repeat):
 cfg=json.loads((H/'build'/json.loads((d/'INPUTS.json').read_text())['build']/'BUILD.json').read_text());sy=cfg['symbols']
 accepted=(d/'accepted.txt').read_bytes();assert accepted==(d/'serial.txt').read_bytes();parts=accepted.decode().split('~');assert len(parts)==repeat+1 and parts[-1]==''
 results=[]
 for rep in range(repeat):
  ram=[]
  for l in (d/f'ram{rep}.hex').read_text().splitlines():
   if not l.startswith(('//','@')):ram.extend(int(v,16) for v in l.split())
  def w(k,n=1):q=(sy[k][0]-65536)//4;return ram[q:q+n]
  obs=[l.split() for l in (d/'observe.txt').read_text().splitlines() if l.split()[0]==str(rep)]
  g=[(int(x[2]),int(x[3],16)&7) for x in obs if x[1]=='G'];t=[(int(x[2]),int(x[3],16)) for x in obs if x[1]=='T']
  assert g==list(enumerate(c['input']));assert [i for i,v in t]==list(range(cfg['count']))
  assert all(x[3]==x[4] for x in obs if x[1]=='T');ts=[v for i,v in t];start=w('start_tick')[0]
  assert all(cfg['period']*(i+1)<=v-start<=cfg['period']*(i+1)+1000 for i,v in enumerate(ts))
  for k in ['fault','evicted','rejected','frozen']:assert w(k)==[c[k]],(k,w(k),c[k])
  assert w('complete')==[1] and w('done_samples')==[cfg['count']] and w('late')==[0]
  head=w('head')[0];n=w('count')[0];ev=w('events',32)
  actual=[ev[4*((head+8-n+k)&7):4*((head+8-n+k)&7)+4] for k in range(n)]
  expected=[[ts[i],i,s,r] for i,s,r in c['events']];assert actual==expected
  hx=lambda vs:''.join(f'{v:08x} ' for v in vs)
  out='REC2 '+hx([cfg['period'],cfg['count'],cfg['wait'],cfg['count'],0,start,w('end_tick')[0],w('work_ticks')[0],0,n,c['evicted'],c['rejected'],c['fault'],c['frozen']])+'\n'
  for e in expected:out+='E '+hx(e)+'\n'
  out+='END\n';assert parts[rep]==out.replace('\n','\r\n')
  results.append(dict(status='PASS',events=actual,samples=cfg['count'],period=cfg['period'],window_ticks=w('end_tick')[0]-start))
 if repeat==2:assert results[0]==results[1]
 return results
if __name__=='__main__':
 b=compile_sw('shape128',12000,128,20,0);result=[]
 for name,c in newplan.items():
  d=simulate(name,b,c['input'],repeat=1,limit=90,maxcycles=1800000)
  result.append(dict(case=name,results=check(d,c,1)))
  save(H/'EXTENDED_RESULTS.json',dict(status='IN_PROGRESS',results=result))
 save(H/'EXTENDED_RESULTS.json',dict(status='PASS_SHORTENED_PERIOD_PRODUCTION_SHAPE',results=result,full_12_8_seconds='NOT_RUN'))
 print('PASS production-shape count128/wait20 at shortened period, three cases')
