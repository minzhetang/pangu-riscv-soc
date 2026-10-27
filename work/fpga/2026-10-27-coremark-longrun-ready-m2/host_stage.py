from pathlib import Path
import sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from host_supervisor import bounded
from stage_budget import check
if __name__=='__main__':
 check();kind=sys.argv[1]
 if kind=='replay':
  for case in ['performance','validation']:bounded([sys.executable,'-B',H/'host_worker.py','replay',case],H,'replay-ready-'+case,600)
 elif kind=='oracle':bounded([sys.executable,'-B',H/'oracle.py'],H,'oracle-performance8',900)
 elif kind=='model':bounded([sys.executable,'-B',H/'host_worker.py','model'],H,'model-equivalence',60)
 else:raise RuntimeError('unknown stage')
