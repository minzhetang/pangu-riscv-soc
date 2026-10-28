from pathlib import Path
import sys,json,time,hashlib,ctypes
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
from stage_budget import check,STAGE_DEADLINE
from host_supervisor import bounded
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def protect():
 rows=json.loads((H/'PROTECTED_ORIGINALS.json').read_text())['files'];assert all(sha(Path(x['path']))==x['SHA256'] for x in rows);return len(rows)
check();assert not ctypes.windll.shell32.IsUserAnAdmin();protect()
assert not (H/'PDS-attempt.json').exists();assert not (H/'pds/synthesize').exists();assert not list((H/'pds').rglob('*.sbit'))
exe=Path('D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe');assert sha(exe)=='631FFD8F14D6246872873C72025CBC2734C9F8C388075B7AFB0B042F3A684E6F'
files=[p for folder in ['source','source-before','pds/source','firmware','scripts'] for p in (H/folder).iterdir() if p.is_file()]+[H/'pds/build.tcl',H/'pds/board_pins.fdc',H/'pds/clock_27mhz.fdc',H/'gui_control.py',Path(__file__),H/'host_supervisor.py',H/'stage_budget.py']
save('FROZEN_INPUTS.json',dict(files=[dict(path=p.relative_to(H).as_posix(),SHA256=sha(p)) for p in files]))
save('PDS-attempt.json',dict(used=1,maximum=1,approval='D175',limit_seconds=1800,GUI_wait_limit=720,GUI_launches_separately_limited=1,hardware='STOPPED'))
start=time.time();argv=[str(exe),'-file',str(H/'pds/build.tcl')]
try:r=bounded(argv,H/'pds','pds-flow-once',1800,cap=4*1024**3)
except Exception as e:
 save('STATUS.json',dict(status='PDS_STOPPED',error_type=type(e).__name__,new_DUT=0,hardware='STOPPED'));raise
protect();assert all(sha(H/x['path'])==x['SHA256'] for x in json.loads((H/'FROZEN_INPUTS.json').read_text())['files'])
save('BUILD_EXIT_RECEIPT.json',dict(status='EXITED_AUDIT_PENDING',process=r,started_epoch=start,ended_epoch=time.time(),artifacts=[dict(path=str(p),bytes=p.stat().st_size,SHA256=sha(p),mtime_epoch=p.stat().st_mtime) for p in (H/'pds').rglob('*.sbit')],protected=protect()))
print('PDS exited; original sources unchanged; actual artifact audit pending')
