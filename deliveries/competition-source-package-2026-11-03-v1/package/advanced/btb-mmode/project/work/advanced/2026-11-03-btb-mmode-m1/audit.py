"""Offline independent ledger checks, fault controls and edge-qualified VCD review."""
from pathlib import Path
import json,hashlib,difflib
H=Path(__file__).resolve().parent;R=H.parents[2]
plans={t['name']:t for f in ['FROZEN_PLAN.json','FROZEN_EXTRA_PLAN.json'] for t in json.loads((H/f).read_text())['tests']}
def check(lines,t):
 def rows(tag):return [l.split()[1:] for l in lines if l.startswith(tag+' ')]
 wb=[[int(a),int(b,16)] for a,b in rows('WB')];stores=[[int(v,16) for v in r] for r in rows('STORE')]
 traps=[[int(v,16) for v in r] for r in rows('TRAP')];pre=[[int(v,16) for v in r[1:]] for r in rows('TRAP_PRE')]
 regs=[0]*32;mem=[0]*2048
 for a,v in t['wb']:regs[a]=v
 for a,v,s in t['stores']:
  for b in range(4):
   if s&(1<<b):mem[a//4]=(mem[a//4]&~(255<<(b*8)))|(v&(255<<(b*8)))
 return all([wb==t['wb'],stores==t['stores'],traps==t['traps'],pre==t['traps'],[[int(a),int(v,16)] for a,v in rows('REG')]==[[i,v] for i,v in enumerate(regs)],[[int(a),int(v,16)] for a,v in rows('MEM')]==[[i,v] for i,v in enumerate(mem)],len(rows('END'))==1,not any(l.startswith('UNKNOWN') for l in lines),not any(r[-1]!='0' for r in rows('TRAIN'))])
independent=[]
for stage in ['final-r2','final-r2-sync','final-extra-r2','final-extra-r2-sync']:
 for r in json.loads((H/(stage+'-RESULTS.json')).read_text())['results']:
  p=H/'runs'/f'{stage}-p{r["pred"]}'/r['case']/'events.txt'
  independent.append(dict(stage=stage,pred=r['pred'],case=r['case'],pass_=check(p.read_text().splitlines(),plans[r['case']])))
sample=(H/'runs/final-r2-p1/jal/events.txt').read_text().splitlines();t=plans['jal'];controls=[]
def control(name,lines):
 try:accepted=check(lines,t)
 except (ValueError,IndexError):accepted=False
 controls.append(dict(name=name,rejected=not accepted))
control('duplicate_wb',[sample[0]]+sample)
control('missing_store',[l for l in sample if not l.startswith('STORE')])
control('wrong_store',[('STORE 00000200 00000001 f' if l.startswith('STORE') else l) for l in sample])
control('wrong_epc',[('TRAP 0000000c 00000000 0000000a' if l.startswith('TRAP ') else l) for l in sample])
control('wrong_precise_origin',[('TRAP_PRE 5 0000000a 00000000 0000000a' if l.startswith('TRAP_PRE') else l) for l in sample])
control('truncated',sample[:-1])
control('unknown_control',sample+['UNKNOWN_CONTROL 50'])
control('training_while_held',sample+['TRAIN 50 00000008 1'])
control('wrong_reg',[('REG 5 0000000c' if l.startswith('REG 5 ') else l) for l in sample])
control('wrong_memory',[('MEM 128 00000001' if l.startswith('MEM 128 ') else l) for l in sample])
control('duplicate_end',sample+[sample[-1]])
def vcd_at(p,time_ps):
 scope=[];names={};values={};now=0;header=True
 for line in p.open():
  a=line.split()
  if not a:continue
  if header:
   if a[0]=='$scope':scope.append(a[2])
   elif a[0]=='$upscope':scope.pop()
   elif a[0]=='$var':names['.'.join(scope+[a[4]])]=a[3]
   elif a[0]=='$enddefinitions':header=False
  elif line.startswith('#'):
   now=int(line[1:])
   if now>time_ps:break
  elif line[0] in 'bBrR':
   if len(a)==2:values[a[1]]=a[0][1:]
  elif line[0] in '01xXzZ':values[line[1:].strip()]=line[0]
 out={}
 for n,code in names.items():
  v=values.get(code,'x')
  try:out[n]=int(v,2)
  except ValueError:out[n]=v
 return out
waves=[]
def wave(case,cycle,expect,post=False):
 p=H/'runs/final-r2-p1'/case/'trace.vcd';ps=50000+5000+10000*(cycle-1)+(1 if post else -1)
 snap=vcd_at(p,ps);actual={k:snap.get('tb.dut.'+k) for k in expect}
 waves.append(dict(case=case,cycle=cycle,phase='after_commit_1ps' if post else 'before_rising_edge',time_ps=ps,expected=expect,actual=actual,pass_=actual==expect))
wave('jal',5,dict(id_pc=8,ex_target_misaligned=1,trap_epc=8,trap_tval=10,trap_cause=0,trap_valid=1,redirect_pc=256))
wave('jal',5,dict(mepc=8,mcause=0,mtval=10),True)
wave('mprv_store_hold',21,dict(stall_all=1,mem_wren=1,store_consumed=0,ex_alu_result=512))
wave('mprv_store_hold',22,dict(stall_all=1,mem_wren=0,store_consumed=1,ex_alu_result=512))
wave('irq_timer',81,dict(id_pc=28,id_jump=1,interrupt_taken=1,trap_epc=28,trap_cause=0x80000007,trap_valid=1))
metrics=[]
for sync,stage in [(0,'final-r2'),(1,'final-r2-sync')]:
 for pred in [0,1]:
  p=H/'runs'/f'{stage}-p{pred}'/'branch_loop'/'trace.vcd'
  # At each actual rising edge, before NBA, identify the externally accepted signature store.
  signature=[]
  for cycle in range(1,80):
   snap=vcd_at(p,50000+5000+10000*(cycle-1)-1)
   if snap.get('tb.we')==1 and snap.get('tb.addr')==512:signature.append(cycle)
  metrics.append(dict(sync=sync,pred=pred,signature_store_cycles=signature))
protected=[]
for item in json.loads((R/'work/fpga/2026-11-03-event-recorder-m3/PROTECTED_INPUTS.json').read_text()):
 p=R/item['path'];sha=hashlib.sha256(p.read_bytes()).hexdigest().upper();protected.append(dict(path=item['path'],expected=item['sha256'],actual=sha,unchanged=sha==item['sha256']))
copies=[];diff=[]
old=R/'work/advanced/2026-11-03-hl4-precise-target-m0/source-before'
for p in sorted((H/'source-before').glob('*.v')):
 copies.append(dict(file=p.name,copy_matches_original=p.read_bytes()==(old/p.name).read_bytes(),candidate_changed=p.read_bytes()!=(H/'source'/p.name).read_bytes()))
 diff+=list(difflib.unified_diff(p.read_text().splitlines(True),(H/'source'/p.name).read_text().splitlines(True),fromfile='source-before/'+p.name,tofile='source/'+p.name))
(H/'RTL_DIFF.patch').write_text(''.join(diff))
result=dict(independent_ledgers=independent,fault_controls=controls,wave_review=waves,cycle_metrics=metrics,protected=protected,source_identity=copies,
 pass_=all(x['pass_'] for x in independent+waves) and all(x['rejected'] for x in controls) and all(x['unchanged'] for x in protected) and all(x['copy_matches_original'] for x in copies))
(H/'AUDIT.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['independent_ledgers','protected']},indent=2))
