from pathlib import Path
from stage_coremark import read,sha
H=Path(__file__).resolve().parent;B=H.parent/'2026-10-26-coremark-stream-evidence-m1';R=H.parent/'2026-10-25-coremark-iter2-m1'
def protect():
 rows=read(H/'protected-originals.json')['files']
 for x in rows:assert sha(x['path'])==x['SHA256'],x['path']
 for root in ['source','source-before']:
  for p in (H/root).iterdir():
   if p.is_file():assert sha(p)==sha(B/'source'/p.name),str(p)
 for p in (H/'cases/performance8-N234/source').iterdir():
  if p.suffix in ['.v','.sv']:assert sha(p)==sha(R/'cases/performance-N234/source'/p.name)
 assert sha(H/'models/peripheral_checker.py')==sha(B/'models/peripheral_checker.py')
 a=(H/'models/cpu_program_reference.py').read_text(encoding='utf-8-sig');b=(B/'models/cpu_program_reference.py').read_text(encoding='utf-8-sig')
 assert a.replace('self.steps<25000000','self.steps<5000000')==b
 for root in ['port','firmware','upstream']:
  for p in (H/root).iterdir():
   if p.is_file():assert sha(p)==sha(R/root/p.name)
 return len(rows)
