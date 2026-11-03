from pathlib import Path
import json,hashlib,difflib,ast
H=Path(__file__).resolve().parent;R=H.parents[2];M1=H.parent/'2026-11-03-btb-mmode-m1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tree=ast.parse((M1/'audit.py').read_text());fun=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='vcd_at');ns={};exec(compile(ast.Module(body=[fun],type_ignores=[]),str(M1/'audit.py'),'exec'),ns);vcd_at=ns['vcd_at']
waves=[]
def wave(stage,case,cycle,expected,post=False):
 p=H/'runs'/stage/case/'trace.vcd';ps=55000+10000*(cycle-1)+(1 if post else -1)
 snap=vcd_at(p,ps);actual={k:snap.get('tb.dut.'+k) for k in expected}
 waves.append(dict(run=stage,case=case,cycle=cycle,phase='after_rising_edge_1ps' if post else 'before_rising_edge',time_ps=ps,expected=expected,actual=actual,pass_=expected==actual))
wave('before-v2-s0-p1','jal_ifmiss',26,dict(id_pc=0xff8,id_valid=1,stall_all=1,i_hit=0,redirect=1))
wave('before-v2-s0-p1','jal_ifmiss',26,dict(id_valid=0),True)
wave('after-v2-s0-p1','jal_ifmiss',26,dict(id_pc=0xff8,id_valid=1,stall_all=1,i_hit=0,redirect=0))
wave('after-v2-s0-p1','jal_ifmiss',26,dict(id_pc=0xff8,id_valid=1),True)
wave('after-v2-s0-p1','jal_ifmiss',30,dict(id_pc=0xff8,stall_all=0,redirect=1,ex_alu_result_final=0xffc))
wave('after-v2-s0-p1','jal_ifmiss',30,dict(ex_rd=5,ex_reg_write=1,ex_alu_result=0xffc),True)
wave('after-trap-s0-p1','misaligned_jump_ifmiss',26,dict(stall_all=1,ex_exception=1,trap_valid=0,redirect=0,id_valid=1))
wave('after-trap-s0-p1','misaligned_jump_ifmiss',30,dict(stall_all=0,ex_exception=1,trap_valid=1,trap_epc=0xff8,trap_tval=0xffa))
protected=[]
for x in json.loads((R/'work/fpga/2026-11-03-event-recorder-m3/PROTECTED_INPUTS.json').read_text()):
 protected.append(dict(path=x['path'],unchanged=sha(R/x['path']).upper()==x['sha256']))
m1_manifest=json.loads((M1/'SHA256SUMS.json').read_text());m1bad=[x['path'] for x in m1_manifest if sha(M1/x['path'])!=x['sha256']]
copies=[];diff=[]
for p in sorted((H/'source-before').glob('*.v')):
 q=H/'source'/p.name
 copies.append(dict(file=p.name,m1_copy_matches=sha(p)==sha(M1/'source'/p.name),original_copy_matches=sha(H/'source-original-hl4'/p.name)==sha(M1/'source-before'/p.name),candidate_changed=sha(q)!=sha(p),before_sha256=sha(p),after_sha256=sha(q)))
 diff+=list(difflib.unified_diff(p.read_text().splitlines(True),q.read_text().splitlines(True),fromfile='M1/'+p.name,tofile='M2/'+p.name))
(H/'RTL_DIFF.patch').write_text(''.join(diff))
regressions=[]
modeltree=ast.parse((M1/'audit.py').read_text());modelcheck=next(x for x in modeltree.body if isinstance(x,ast.FunctionDef) and x.name=='check');modelns={};exec(compile(ast.Module(body=[modelcheck],type_ignores=[]),str(M1/'audit.py'),'exec'),modelns)
oldplans={t['name']:t for f in ['FROZEN_PLAN.json','FROZEN_EXTRA_PLAN.json'] for t in json.loads((H/f).read_text())['tests']}
independent_regression=[]
for stage in ['final-regression','final-regression-sync','final-extra-regression','final-extra-regression-sync']:
 rs=json.loads((H/(stage+'-RESULTS.json')).read_text())['results'];regressions+=rs
 for r in rs:
  lines=(H/'runs'/f'{stage}-p{r["pred"]}'/r['case']/'events.txt').read_text().splitlines()
  independent_regression.append(dict(stage=stage,case=r['case'],pred=r['pred'],pass_=modelns['check'](lines,oldplans[r['case']])))
before=json.loads((H/'before-v2-RESULTS.json').read_text())['results'];after=json.loads((H/'after-v2-RESULTS.json').read_text())['results'];original=json.loads((H/'original-v2-RESULTS.json').read_text())['results']
before+=json.loads((H/'before-trap-RESULTS.json').read_text())['results'];after+=json.loads((H/'after-trap-RESULTS.json').read_text())['results']
# Independent log observer: no dependence on run.py's PASS status for focus
# training/resolve, link visibility, each register or RAM word.
plan=json.loads((H/'PLAN-v2.json').read_text());plan['tests']+=json.loads((H/'PLAN-trap.json').read_text())['tests'];independent=[]
def verify(lines,t):
 def rows(tag):return [l.split()[1:] for l in lines if l.startswith(tag+' ')]
 actualwb=[[int(a),int(v,16)] for a,v in rows('WB')];actualstore=[[int(v,16) for v in r] for r in rows('STORE')]
 reg=[0]*32;mem=[0]*2048
 for a,v in t['wb']:reg[a]=v
 for a,v,mask in t['stores']:
  for b in range(4):
   if mask&(1<<b):mem[a//4]=(mem[a//4]&~(255<<(8*b)))|(v&(255<<(8*b)))
 focus=[r for r in rows('TRAIN') if int(r[1],16)==0xff8];resolve=[r for r in rows('RESOLVE') if int(r[1],16)==0xff8]
 return all([actualwb==t['wb'],actualstore==t['stores'],[[int(v,16) for v in r] for r in rows('TRAP')]==t['traps'],[[int(v,16) for v in r[1:]] for r in rows('TRAP_PRE')]==t['traps'],len(focus)==t.get('focus_train',1),len(resolve)==t.get('focus_resolve',1),all(r[2]=='0' for r in rows('TRAIN')),not rows('REDIRECT_HELD'),any(r[3]=='0' for r in rows('FOCUS_HOLD')),rows('END')==[['400']],rows('STATUS')==t.get('expected_status',[['00000080','1']]),not any(l.startswith('UNKNOWN') for l in lines),[[int(a),int(v,16)] for a,v in rows('REG')]==[[i,v] for i,v in enumerate(reg)],[[int(a),int(v,16)] for a,v in rows('MEM')]==[[i,v] for i,v in enumerate(mem)]])
for r in after:
 t=next(t for t in plan['tests'] if t['name']==r['case']);prefix='after-trap' if r['case'] in ['misaligned_jump_ifmiss','ebreak_ifmiss'] else 'after-v2';d=H/'runs'/f'{prefix}-s{r["sync"]}-p{r["pred"]}'/r['case']
 independent.append(dict(case=r['case'],sync=r['sync'],pred=r['pred'],pass_=verify((d/'events.txt').read_text().splitlines(),t)))
sample=(H/'runs/after-v2-s0-p1/jal_ifmiss/events.txt').read_text().splitlines();t=plan['tests'][0]
mutants={
 'drop_link':[x for x in sample if not x.startswith('WB 5 ')],
 'duplicate_link':sample+['WB 5 00000ffc'],
 'duplicate_training':sample+['TRAIN 99 00000ff8 0'],
 'stall_training':sample+['TRAIN 27 00000ff8 1'],
 'drop_resolve':[x for x in sample if not x.startswith('RESOLVE 30 ')],
 'lost_ifmiss_evidence':[x for x in sample if not x.startswith('FOCUS_HOLD')],
 'wrong_path_store':sample+['STORE 00000258 00000063 f'],
 'truncated':sample[:-1],
 'unknown':sample+['UNKNOWN accepted_fetch']}
controls=[dict(name=k,rejected=not verify(v,t)) for k,v in mutants.items()]
jobs=json.loads((H/'COMMANDS.json').read_text())
binding=[]
for j in jobs:
 if j['name'].startswith(('compile-after-v2','compile-after-trap','compile-final-')):
  binding.append(dict(job=j['name'],current_source_tb_matches=all(sha(Path(p))==v for p,v in j['input_sha256'].items())))
result=dict(wave_review=waves,protected=protected,m1_manifest_count=len(m1_manifest),m1_manifest_mismatch=m1bad,source_identity=copies,independent_new_cases=independent,independent_regression=independent_regression,checker_controls=controls,compile_binding=binding,
 summary=dict(new_pass=sum(x['status']=='PASS' for x in after),new_total=len(after),m1_before_pass=sum(x['status']=='PASS' for x in before),m1_before_fail=sum(x['status']=='FAIL' for x in before),original_pass=sum(x['status']=='PASS' for x in original),original_fail=sum(x['status']=='FAIL' for x in original),regression_pass=sum(x['status']=='PASS' for x in regressions),regression_total=len(regressions),hardware='NOT_RUN',pds='NOT_RUN',full_task2=False))
result['pass_']=all(x['pass_'] for x in waves+independent+independent_regression) and all(x['unchanged'] for x in protected) and not m1bad and all(x['m1_copy_matches'] and x['original_copy_matches'] for x in copies) and all(x['current_source_tb_matches'] for x in binding) and all(x['rejected'] for x in controls) and all(x['status']=='PASS' for x in after+regressions)
(H/'AUDIT.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(summary=result['summary'],waves=waves,controls=controls,pass_=result['pass_']),indent=2))
if not result['pass_']:raise SystemExit(1)
