from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from stream_io import Archiver,save
from run_capture_once import spool_budget
from stream_peripherals import SparseModel
rows=[]
def reject(label,fn):
    try:fn()
    except (AssertionError,ValueError,OSError) as exc:rows.append(dict(id=label,status='EXPECTED_REJECT',reason=str(exc)))
    else:raise AssertionError(label+' accepted')
d=H/'controls/spool-cap';d.mkdir();(d/'spool').mkdir();p=d/'spool/bus-000000.log'
with p.open('xb') as f:
    f.seek(32*1024*1024);f.write(b'X')
reject('unarchived spool >32MiB actual file',lambda:spool_budget(d));assert p.stat().st_size==33554433
# Ready event duplication or missing terminal close cannot become a complete archive.
d=H/'controls/ready-duplicate';d.mkdir();(d/'spool').mkdir();a=Archiver(d)
(d/'spool/trace-000000.log').write_bytes(b'EX|2|00000000\n');a.consume('SEGMENT|trace|0|1|spool/trace-000000.log')
reject('duplicate ready segment',lambda:a.consume('SEGMENT|trace|0|1|spool/trace-000000.log'))
reject('missing terminal receipt',lambda:a.finish())
reject('nonzero GPIO outside skip assumption',lambda:SparseModel(8).step(1,1,0,False,0,0))
save(H/'controls/capture-guards.json',dict(status='PASS',rows=rows,new_DUT=0,failed_spool_retained=True))
print(json.dumps(dict(status='CAPTURE_GUARDS_PASS',controls=len(rows),actual_overbudget_bytes=33554433)))
