from pathlib import Path
import sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from host_supervisor import bounded
bounded([sys.executable,'-B',H/'final_check_worker.py'],H,'final-functional-check',600)
