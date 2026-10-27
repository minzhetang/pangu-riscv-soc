from pathlib import Path
import sys,time,json
H=Path('D:/A_FPGA_Comp/work/fpga/2026-10-27-coremark-longrun-ready-m2');sys.path.insert(0,str(H));sys.dont_write_bytecode=True
from stage_coremark import read,save
from stage_budget import json_read,deadline,check
from stream_io import Archiver
check();rows=[]
p=H/'controls/extra-guard/oversized-index.json'
try:json_read(p)
except RuntimeError as e:assert str(e)=='JSON_CAP_BEFORE_READ';rows.append(dict(id='index cap before parse',status='EXPECTED_REJECT',error=str(e)))
else:raise RuntimeError('oversized index accepted')
r=read(H/'logs/negative-configured-memory/process.json');assert r['error']=='PARENT_MEMORY_CAP' and r['returncode']!=0;rows.append(dict(id='configured memory cap',status='EXPECTED_REJECT',process='logs/negative-configured-memory/process.json'))
d=H/'controls/extra-guard/callback-qualified';d.mkdir();(d/'spool').mkdir();(d/'spool/trace-000000.log').write_bytes(b'EX|2|00000000\n');a=Archiver(d,deadline=deadline(.04),poll=lambda:time.sleep(.06))
try:a.consume('SEGMENT|trace|0|1|spool/trace-000000.log')
except RuntimeError as e:assert str(e)=='ABSOLUTE_DEADLINE';rows.append(dict(id='deadline inside archive callback',status='EXPECTED_REJECT',error=str(e)))
else:raise RuntimeError('expired callback accepted')
assert (d/'spool/trace-000000.log').is_file();save(H/'controls/extra-guards.json',dict(status='PASS_HOST_ONLY',rows=rows,new_DUT=0,qualification_note='Initial auxiliary wrapper used lowercase deadline token; actual ABSOLUTE_DEADLINE correctly rejected but wrapper asserted. Original script/fixture retained; independent fresh callback confirmed exact rejection. No code/expected/DUT modification.'));print(json.dumps(rows))
