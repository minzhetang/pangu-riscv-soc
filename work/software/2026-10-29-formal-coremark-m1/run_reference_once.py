from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from host_supervisor import bounded
tid=sys.argv[1];assert tid in ['performance2','validation2','performance256','validation256']
with (H/(tid+'-reference-attempt.json')).open('x') as f:json.dump(dict(used=1,maximum=1),f)
bounded([sys.executable,'-B',str(H/'reference_worker.py'),tid],H,'reference-'+tid,300 if tid.endswith('2') else 1200)
