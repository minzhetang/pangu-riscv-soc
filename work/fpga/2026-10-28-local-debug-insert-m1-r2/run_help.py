from pathlib import Path
import sys,json,hashlib
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
from host_supervisor import bounded
H=Path(__file__).resolve().parent
assert not (H/'HELP-attempt.json').exists()
script=H/'scripts/help-only.tcl'
(H/'HELP-attempt.json').write_text(json.dumps(dict(type='READONLY_TCL_INTERFACE_AND_OFFICIAL_HELP',queries=4,maximum=6,timeout_seconds=30,compile=0,synthesize=0,GUI=0,hardware='STOPPED',script_SHA256=hashlib.sha256(script.read_bytes()).hexdigest().upper()),indent=2),encoding='utf-8')
r=bounded(['D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe','-file',str(script)],H/'pds','readonly-help',30,cap=1024**3)
(H/'HELP_EXIT.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
