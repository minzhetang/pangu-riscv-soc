from pathlib import Path
import ast,json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[2];M2=H.parent/'2026-11-03-btb-mmode-m2';M1=H.parent/'2026-11-03-btb-mmode-m1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tree=ast.parse((M1/'audit.py').read_text());f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='vcd_at');ns={};exec(compile(ast.Module(body=[f],type_ignores=[]),'vcd_parser','exec'),ns);vcd_at=ns['vcd_at']
plan=json.loads((H/'PLAN-v2.json').read_text());results=json.loads((H/'after-v2-RESULTS.json').read_text())['results']
def check(lines,t):
 def rows(tag):return [l.split()[1:] for l in lines if l.startswith(tag+' ')]
 def hx(tag):return [[int(v,16) for v in r] for r in rows(tag)]
 wb=[[int(a),int(v,16)] for a,v in rows('WB')];regs=[0]*32;mem=[0]*2048
 for a,v in t['wb']:regs[a]=v
 for a,v,s in t['stores']:mem[a//4]=v
 vec=rows('VECTOR');expected_vec=[] if t['entry'] is None else [t['entry']]
 return all([wb==t['wb'],hx('STORE')==t['stores'],hx('TRAP')==t['traps'],[[int(v,16) for v in r[1:]] for r in rows('TRAP_PRE')]==t['traps'],[int(r[1],16) for r in vec]==expected_vec,[int(r[0],16) for r in rows('REDIRECT_POST')]==expected_vec,rows('STATUS')==[t['status']],rows('TRAP_STATUS')==([] if not t['traps'] else [['00001880','3']]),[[int(a),int(v,16)] for a,v in rows('REG')]==[[i,v] for i,v in enumerate(regs)],[[int(a),int(v,16)] for a,v in rows('MEM')]==[[i,v] for i,v in enumerate(mem)],rows('END')==[['400','0']],not any(l.startswith('UNKNOWN') for l in lines)])
independent=[];response=[]
for r in results:
 t=next(t for t in plan['tests'] if t['name']==r['case']);p=H/'runs'/f'after-v2-s{r["sync"]}-p{r["pred"]}'/r['case']/'events.txt';lines=p.read_text().splitlines()
 independent.append(dict(case=r['case'],sync=r['sync'],pred=r['pred'],pass_=check(lines,t)))
 if r['actual']['trap_pre']:response.append(dict(case=r['case'],sync=r['sync'],pred=r['pred'],cycles=int(r['actual']['trap_pre'][0][0])-int(r['actual']['csr_enable'][0][0])))
t=next(t for t in plan['tests'] if t['name']=='irq_7_vector1');sample=(H/'runs/after-v2-s0-p1/irq_7_vector1/events.txt').read_text().splitlines()
mutants={
 'wrong_vector':[('VECTOR 10 00000100 00000008' if s.startswith('VECTOR ') else s) for s in sample],
 'wrong_epc':[('TRAP 00000020 80000007 00000000' if s.startswith('TRAP ') else s) for s in sample],
 'wrong_status':[('TRAP_STATUS 00000008 3' if s.startswith('TRAP_STATUS ') else s) for s in sample],
 'duplicate_trap':sample+['TRAP 0000001c 80000007 00000000'],
 'duplicate_wb':sample+['WB 4 0000005b'],
 'missing_store':[s for s in sample if not s.startswith('STORE ')],
 'wrong_register':[('REG 4 00000000' if s.startswith('REG 4 ') else s) for s in sample],
 'wrong_memory':[('MEM 128 00000000' if s.startswith('MEM 128 ') else s) for s in sample],
 'unknown':sample+['UNKNOWN_CONTROL 100'],
 'truncated':sample[:-1]}
controls=[dict(name=n,rejected=not check(lines,t)) for n,lines in mutants.items()]
waves=[]
for sync in [0,1]:
 case='irq_7_vector1';r=next(r for r in results if r['case']==case and r['sync']==sync and r['pred']==1);cycle=int(r['actual']['trap_pre'][0][0]);p=H/'runs'/f'after-v2-s{sync}-p1'/case/'trace.vcd'
 for post in [False,True]:
  ps=55000+10000*(cycle-1)+(1 if post else -1);snap=vcd_at(p,ps)
  expect=dict(id_pc=28,interrupt_taken=1,trap_vector=284,trap_epc=28,trap_cause=0x80000007,pipeline_advance=1) if not post else dict(pc_reg=284,mepc=28,mcause=0x80000007,mstatus=0x1880,priv=3)
  actual={k:snap.get('tb.dut.'+k) for k in expect};waves.append(dict(sync=sync,cycle=cycle,time_ps=ps,phase='post_1ps' if post else 'pre_edge',expected=expect,actual=actual,pass_=actual==expect))
for cycle,expected in [(10,dict(id_pc=28,ex_is_csr=1,interrupt_taken=1,csr_commit_eff=0,trap_epc=28)),(19,dict(id_pc=28,ex_is_csr=1,interrupt_taken=0,csr_commit_eff=1))]:
 snap=vcd_at(H/'runs/after-v2-s0-p1/adjacent_disable_precise/trace.vcd',55000+10000*(cycle-1)-1)
 actual={k:snap.get('tb.dut.'+k) for k in expected};waves.append(dict(case='adjacent_disable_precise',cycle=cycle,phase='pre_edge',expected=expected,actual=actual,pass_=actual==expected))
protected=[dict(path=x['path'],unchanged=sha(R/x['path']).upper()==x['sha256']) for x in json.loads((R/'work/fpga/2026-11-03-event-recorder-m3/PROTECTED_INPUTS.json').read_text())]
source=[dict(file=p.name,copy_matches_M2=sha(H/'source-before'/p.name)==sha(M2/'source'/p.name),candidate_unchanged=sha(p)==sha(H/'source-before'/p.name),sha256=sha(p)) for p in sorted((H/'source').glob('*.v'))]
m2items=json.loads((M2/'SHA256SUMS.json').read_text());m2bad=[x['path'] for x in m2items if sha(M2/x['path'])!=x['sha256']]
jobs=json.loads((H/'COMMANDS.json').read_text());binding=[dict(job=j['name'],matches=all(sha(Path(p))==s for p,s in j['input_sha256'].items())) for j in jobs if j['name'].startswith(('compile-after-v2','compile-final-regression','compile-final-extra-regression','compile-after-if'))]
result=dict(independent_ledgers=independent,checker_controls=controls,vcd_review=waves,csr_to_trap_cycles=response,protected=protected,source_identity=source,m2_manifest_count=len(m2items),m2_manifest_mismatch=m2bad,compile_binding=binding)
regression=[r for stage in ['final-regression','final-regression-sync','final-extra-regression','final-extra-regression-sync','after-if-v2','after-if-trap'] for r in json.loads((H/(stage+'-RESULTS.json')).read_text())['results']]
result['regression_count']=len(regression);result['regression_nonpass']=[r for r in regression if r['status']!='PASS']
result['pass_']=len(results)==44 and all(x['status']=='PASS' for x in results) and all(x['pass_'] for x in independent+waves) and all(x['rejected'] for x in controls) and all(x['unchanged'] for x in protected) and all(x['copy_matches_M2'] for x in source) and [x['file'] for x in source if not x['candidate_unchanged']]==['cpu_hl4.v'] and not m2bad and all(x['matches'] for x in binding) and len(regression)==108 and not result['regression_nonpass']
(H/'AUDIT.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(pass_=result['pass_'],runs=len(results),wave_review=waves,response_cycles=sorted(set(x['cycles'] for x in response)),negative_controls=len(controls)),indent=2))
if not result['pass_']:raise SystemExit(1)
