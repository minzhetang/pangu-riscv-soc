from pathlib import Path
import ast
H=Path('work/fpga/2026-10-27-coremark-longrun-ready-m2');R=H.parent/'2026-10-25-coremark-iter2-m1';M=H.parent/'2026-10-26-coremark-stream-evidence-m1'
p=H/'build_once.py';s=p.read_text();s=s.replace(" table(image,H/'cases/performance8-N234/source/init_tables.svh') if not (H/'cases/performance8-N234/source/init_tables.svh').exists() else None\n",'');p.write_text(s)
s=(R/'precompute.py').read_text();tree=ast.parse(s)
parts=[ast.get_source_segment(s,n) for n in tree.body if isinstance(n,ast.ClassDef)]
classes='\n'.join(parts).replace('self.ref.steps<5000000','self.ref.steps<25000000').replace('time.monotonic()-self.start<600','time.monotonic()-self.start<900')
run=ast.get_source_segment(s,next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run'))
run=run.replace("baseline=case.startswith('old-');name=case.removeprefix('old-');assert name in ['performance','validation'];expected_iterations=1 if baseline else 2","baseline=False;name=case;assert name=='performance8';expected_iterations=8")
run=run.replace("old=read(H/'oracles'/('old-'+name)/'expected.json');assert old['calibration'].startswith('PASS')\n        result['calibration_source_SHA256']=sha(H/'oracles'/('old-'+name)/'expected.json')","old=read(R/'oracles'/'performance'/'expected.json');result['calibration_source_SHA256']=sha(R/'oracles'/'performance'/'expected.json')")
header='from stage_coremark import *\nimport sys,time,re\nfrom stage_budget import check\nR=H.parent/"2026-10-25-coremark-iter2-m1"\nsys.path.insert(0,str(H/"models"))\nfrom cpu_program_reference import Reference\n'
(H/'oracle.py').write_text(header+classes+'\n'+run+'\nif __name__=="__main__":check();run("performance8");check()\n')
s=(M/'host_worker.py').read_text();a=s.index('\ndef qualify_existing');b=s.index("\nif __name__=='__main__':");s=s[:a]+s[b:];s=s[:s.index("    elif sys.argv[1]=='qualify-existing':")];(H/'host_worker.py').write_text(s)
(H/'host_stage.py').write_text('''from pathlib import Path
import sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from host_supervisor import bounded
from stage_budget import check
if __name__=='__main__':
 check();kind=sys.argv[1]
 if kind=='replay':
  for case in ['performance','validation']:bounded([sys.executable,'-B',H/'host_worker.py','replay',case],H,'replay-'+case,600)
 elif kind=='oracle':bounded([sys.executable,'-B',H/'oracle.py'],H,'oracle-performance8',900)
 elif kind=='model':bounded([sys.executable,'-B',H/'host_worker.py','model'],H,'model-equivalence',60)
 else:raise RuntimeError('unknown stage')
''')
for p in H.glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
print('All candidate Python syntax parsed; no native build or DUT')
