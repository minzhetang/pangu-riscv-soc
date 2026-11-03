from pathlib import Path
import sys
sys.dont_write_bytecode=True
H=Path('D:/A_FPGA_Comp/work/fpga/2026-10-26-coremark-stream-evidence-m1');sys.path.insert(0,str(H))
from host_supervisor import bounded
bounded([sys.executable,'-B',H/'host_worker.py','qualify-existing'],H,'replay-performance-qualification-v2',600)
bounded([sys.executable,'-B',H/'host_worker.py','replay','validation'],H,'replay-validation',600)
