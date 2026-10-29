from pathlib import Path
import sys,json,time,shutil,difflib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2]
from stage_coremark import read,save,sha,table
from stage_budget import check,STAGE_DEADLINE
check();protected=read(H/'PROTECTED_INPUTS.json');assert all(sha(x['path'])==x['SHA256'] for x in protected)
for x in read(H/'SHORT_FROZEN_INPUTS.json')['files']:assert sha(H/x['path'])==x['SHA256']
host=read(H/'HOST_CONTROL_RESULTS.json');assert host['status']=='PASS_HOST_ONLY'
(H/'initialization').mkdir();rows=[]
for case in read(H/'FROZEN_PLAN.json')['cases']:
 tid=case['id'];o=read(H/'oracles-recovery'/tid/'expected.json');assert o['status']=='REFERENCE_ONLY_NOT_DUT'
 b=next(x for x in read(H/'BUILD_RESULTS.json') if x['id']==tid);assert sha(H/'build'/tid/'program.bin')==b['bin_SHA256']
 table((H/'build'/tid/'program.bin').read_bytes(),H/'initialization'/(tid+'.svh'))
 r=dict(id=tid,build='PASS',reference='PASS_REFERENCE_ONLY',steps=o['steps'],raw_ticks=o['raw_ticks'],nominal_seconds=o['raw_ticks']/27000000,crcfinal=o['crcfinal'],bin_SHA256=b['bin_SHA256'],ELF_SHA256=b['ELF_SHA256'],hardware_valid=False,formal_score_valid=False)
 if case['iterations']==2:
  d=H/'runs'/(tid+'-N234');f=read(d/'functional-result.json');assert f['status']=='PASS_FINITE_2_ITERATIONS_NOT_FORMAL_SCORE'
  result=read(d/'check-result.json');assert result['status']=='PASS';r.update(DUT='PASS_FINITE_TWO_ITERATIONS',functional=f,metrics=result['metrics'],trace_counts=result['trace_counts'])
 else:r.update(DUT='NOT_RUN',status='PROGRAM_BUILT_REFERENCE_ONLY_PENDING_TARGET_RUN')
 rows.append(r)
# Include own verification headers by identity for future portable packaging, not vendor models.
v=P/'work/fpga/2026-10-24-implementability-m0/verification';out=H/'verification';out.mkdir()
deps=[]
for p in v.glob('*.svh'):
 shutil.copy2(p,out/p.name);assert sha(p)==sha(out/p.name);deps.append(dict(source=str(p),copy=str((out/p.name).relative_to(H)),SHA256=sha(p)))
save(H/'DEPENDENCIES.json',dict(own_verification_headers=deps,licensed_models='Obtain GTP_DRM18K_E1.v and GTP_GRS.v from lawful PDS2022.2-SP6.4 installation; not copied',scripts='one-shot historical entries, absolute local argv recorded; do not rerun over artifacts',bitstream='NOT_GENERATED',previous_handoff='UNCHANGED'))
diff=[]
for rel in ['source','models','port']:
 for p in sorted((H/rel).rglob('*')):
  if not p.is_file():continue
  before=H/(rel+'-before')/p.relative_to(H/rel)
  if before.exists() and sha(before)!=sha(p):
   assert rel!='source','FUNCTIONAL_RTL_CHANGED'
   diff.extend(difflib.unified_diff(before.read_text().splitlines(True),p.read_text().splitlines(True),fromfile=str(before.relative_to(H)),tofile=str(p.relative_to(H))))
(H/'EXACT_SOURCE_DIFF.patch').write_text(''.join(diff),encoding='utf8')
save(H/'RESULTS-M1.json',dict(date='2026-10-29',status='PASS_SCOPED_SOFTWARE_NOT_FORMAL_SCORE',approval=['D194','D196'],C_builds=4,C_rebuilds_this_recovery=0,reference_invocations_total_including_preflight_failure=5,completed_references=4,RTL_compiles=2,new_DUT=2,rows=rows,host_controls=len(host['rows']),original_protected_unchanged=len(protected),hardware='STOPPED',PDS=0,clock=read(H/'RECOVERY_CLOCK.json'),remaining_absolute_seconds=STAGE_DEADLINE-time.monotonic(),limitations=['no hardware or long256 DUT','no true retirement PC or unified WB/STORE commit','fixed memory/initial state; finite inputs','nominal frequency only; VCD is not ILA','old preflight failure retained']))
files=[p for p in H.rglob('*') if p.is_file() and p.name!='SHA256SUMS-FINAL.txt'];assert sum(p.stat().st_size for p in files)<=2*1024**3
(H/'SHA256SUMS-FINAL.txt').write_text(''.join(sha(p)+'  '+p.relative_to(H).as_posix()+'\n' for p in sorted(files)),encoding='utf8')
print('Scoped software result frozen; no hardware/formal score; originals unchanged')
