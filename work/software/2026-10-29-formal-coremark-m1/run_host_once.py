from pathlib import Path
import sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from stage_coremark import save
from host_supervisor import bounded
save(H/'host-control-attempt.json',dict(used=1,maximum=1))
bounded([sys.executable,'-B',H/'finalize_host.py'],H,'host-controls',60)
