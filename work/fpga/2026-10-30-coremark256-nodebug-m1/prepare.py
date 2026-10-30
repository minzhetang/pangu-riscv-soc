"""Freeze two approved image-only production cases, no native execution."""
from pathlib import Path
import sys,time,json,hashlib,shutil,difflib,re
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2];F=P/'work/fpga/2026-10-27-board-coremark8-bitstream-m1';S=P/'work/software/2026-10-29-formal-coremark-m1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf8') as f:json.dump(o,f,ensure_ascii=False,indent=2)
scope=P/'deliveries/mainline-coremark256-nodebug-scope-2026-10-30-v1/IMPLEMENTATION_SCOPE.md'
assert sha(scope)=='4C6E5A61DFFB882F378883926D098364EDF8FB16C6150A01B193DE47A67C0A46'
save('APPROVAL.json',dict(date='2026-10-30',decision='D200',source='user 批准',version='1.0.0',scope_SHA256=sha(scope),max_PDS=2,hardware='STOPPED'))
start=time.monotonic();save('STAGE_CLOCK.json',dict(start=start,deadline_monotonic=start+4800))
for n in ['stage_budget.py','host_supervisor.py']:shutil.copy2(F/n,H/n)
s=(H/'host_supervisor.py').read_text().replace('32*1024**2-count','16*1024**2-count').replace("require(own<=cap,'PARENT_MEMORY_CAP')","require(own<=512*1024**2,'PARENT_MEMORY_CAP')")
(H/'host_supervisor.py').write_text(s,encoding='utf8')
baseline_init=(F/'pds/source/init_tables.svh').read_text();baseline_memory=(F/'pds/source/memory_model.sv').read_text();assert baseline_memory.count(baseline_init)==1
protected=read(F/'PROTECTED_ORIGINALS.json')['files']+read(S/'PROTECTED_INPUTS.json')
protected += [dict(path=str(p),SHA256=sha(p)) for root in [F/'source-before',F/'pds/source'] for p in root.iterdir() if p.is_file()]
protected += [dict(path=str(scope),SHA256=sha(scope))]
plan=[]
for tid in ['performance256','validation256']:
 d=H/tid;d.mkdir();(d/'pds').mkdir();shutil.copytree(F/'source-before',d/'source-before');shutil.copytree(F/'pds/source',d/'production-before');shutil.copytree(F/'pds/source',d/'pds/source');shutil.copytree(S/'build'/tid,d/'firmware')
 newinit=(S/'initialization'/(tid+'.svh')).read_text();newmemory=baseline_memory.replace(baseline_init,newinit)
 (d/'pds/source/init_tables.svh').write_text(newinit,encoding='utf8');(d/'pds/source/memory_model.sv').write_text(newmemory,encoding='utf8')
 for n in ['build.tcl','board_pins.fdc','clock_27mhz.fdc']:shutil.copy2(F/'pds'/n,d/'pds'/n)
 for n in [p.name for p in (F/'source-before').iterdir() if p.suffix in ['.sv','.v']]:
  if n!='memory_model.sv':assert sha(d/'pds/source'/n)==sha(S/'source'/n)
 assert newmemory.replace(newinit,'<INIT>')==baseline_memory.replace(baseline_init,'<INIT>')
 (d/'INIT_DIFF.patch').write_text(''.join(difflib.unified_diff(baseline_memory.splitlines(True),newmemory.splitlines(True),fromfile='production-before/memory_model.sv',tofile='pds/source/memory_model.sv')),encoding='utf8')
 entry=next(x for x in read(S/'RESULTS-M1.json')['rows'] if x['id']==tid)
 assert sha(d/'firmware/program.bin')==entry['bin_SHA256'] and sha(d/'firmware/program.elf')==entry['ELF_SHA256']
 plan.append(dict(id=tid,bin_SHA256=entry['bin_SHA256'],ELF_SHA256=entry['ELF_SHA256'],init_SHA256=sha(d/'pds/source/init_tables.svh'),argv=['D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe','-file',str(d/'pds/build.tcl')],cwd=str(d/'pds'),seconds=1800,compile_seed4=256))
 protected += [dict(path=str(p),SHA256=sha(p)) for p in (S/'build'/tid).iterdir() if p.is_file()]
assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
save('PROTECTED_INPUTS.json',dict(files=protected));save('PLAN.json',dict(before_PDS=True,cases=plan,all_stage_seconds=4800,source_RTL_changes='none; production INIT substitution only',hardware='STOPPED'))
print('D200 two image-only production cases prepared; 0 PDS')
