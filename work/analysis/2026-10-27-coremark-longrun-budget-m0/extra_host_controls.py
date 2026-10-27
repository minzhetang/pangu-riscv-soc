from pathlib import Path
import sys,json,time
H=Path('D:/A_FPGA_Comp/work/fpga/2026-10-27-coremark-longrun-ready-m2');sys.path.insert(0,str(H));sys.dont_write_bytecode=True
from stage_budget import json_read,deadline,check
from stage_coremark import save
from stream_io import Archiver
from host_supervisor import bounded
rows=[]
def reject(name,fn,token):
 try:fn()
 except Exception as e:
  assert token in str(e),(name,repr(e));rows.append(dict(id=name,status='EXPECTED_REJECT',reason=str(e)))
 else:raise RuntimeError(name+' accepted')
if __name__=='__main__':
 check();d=H/'controls/extra-guard';d.mkdir();p=d/'oversized-index.json'
 with p.open('xb') as f:f.seek(16*1024**2);f.write(b'X')
 reject('index cap before JSON parse',lambda:json_read(p),'JSON_CAP_BEFORE_READ')
 reject('configured memory cap enforced',lambda:bounded([sys.executable,'-B','-c','import time;time.sleep(1)'],H,'negative-configured-memory',2,cap=1),'PARENT_MEMORY_CAP')
 d=d/'callback';d.mkdir();(d/'spool').mkdir();(d/'spool/trace-000000.log').write_bytes(b'EX|2|00000000\n')
 a=Archiver(d,deadline=deadline(.04),poll=lambda:time.sleep(.06))
 reject('expiry inside archive processing callback',lambda:a.consume('SEGMENT|trace|0|1|spool/trace-000000.log'),'deadline')
 assert (d/'spool/trace-000000.log').is_file(),'failed input must remain'
 save(H/'controls/extra-guards.json',dict(status='PASS_HOST_ONLY',rows=rows,new_DUT=0));print(json.dumps(rows))
