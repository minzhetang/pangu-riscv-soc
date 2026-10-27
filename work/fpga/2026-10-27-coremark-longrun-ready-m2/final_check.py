from pathlib import Path
import sys
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from host_supervisor import bounded
if __name__=='__main__':bounded([sys.executable,'-B',H/'final_worker.py'],H,'final-functional-performance8',1800)
