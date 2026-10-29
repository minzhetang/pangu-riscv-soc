from pathlib import Path
import shutil,sys,json
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;S=H.parents[2]/'work/fpga/2026-10-27-coremark-longrun-ready-m2'
shutil.copy2(S/'stage_coremark.py',H/'stage_coremark.py')
p=H/'models/cpu_program_reference.py';s=p.read_text();assert s.count('25000000')==1;p.write_text(s.replace('25000000','250000000'),encoding='utf-8',newline='\n')
s=(S/'oracle.py').read_text();s=s[:s.index('def run(case):')];assert s.count('25000000')==1;s=s.replace('25000000','250000000').replace('self.start<900','self.start<1200')
(H/'reference_schedule.py').write_text(s,encoding='utf-8')
(H/'oracles').mkdir()
