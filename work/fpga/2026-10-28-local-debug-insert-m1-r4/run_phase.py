from pathlib import Path
import sys,json,time,hashlib,ctypes
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
from host_supervisor import bounded
from stage_budget import check
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
phase=sys.argv[1];assert phase in ['pre','build'];check();assert not ctypes.windll.shell32.IsUserAnAdmin()
protected=json.loads((H/'PROTECTED_ORIGINALS.json').read_text())['files'];assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
exe=Path('D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe');assert sha(exe)=='631FFD8F14D6246872873C72025CBC2734C9F8C388075B7AFB0B042F3A684E6F'
assert not (H/(phase+'-attempt.json')).exists();assert not (H/phase/'synthesize').exists()
if phase=='build':
 g=json.loads((H/'FIC_AUDIT.json').read_text());assert g['status']=='PASS_FULL_140_CONNECTIONS'
 gui=json.loads((H/'GUI_RESULT.json').read_text());assert gui['rc']==0 and gui['root_exited'] and not gui['remaining_own_windows']
 assert sha(H/'debug.fic')==g['FIC_SHA256']
files=[p for root in ['source','source-before','firmware',phase+'/source','scripts'] for p in (H/root).iterdir() if p.is_file()]+[H/phase/'flow.tcl',H/phase/'board_pins.fdc',H/phase/'clock_27mhz.fdc',H/'gui_control.py',H/'process_guard.py',H/'host_supervisor.py',H/'stage_budget.py',H/'window_policy.py',Path(__file__)]
if phase=='build':files.append(H/'debug.fic')
save(phase+'-FROZEN_INPUTS.json',dict(files=[dict(path=p.relative_to(H).as_posix(),SHA256=sha(p)) for p in files]))
seconds=180 if phase=='pre' else 1800;save(phase+'-attempt.json',dict(used=1,maximum=1,approval='D179',timeout_seconds=seconds,hardware='STOPPED'))
start=time.time()
try:r=bounded([str(exe),'-file',str(H/phase/'flow.tcl')],H/phase,phase+'-once',seconds,cap=4*1024**3)
except Exception as e:
 save(phase+'-STOP.json',dict(status='STOPPED',error=type(e).__name__,no_retry=True));raise
assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
assert all(sha(H/x['path'])==x['SHA256'] for x in json.loads((H/(phase+'-FROZEN_INPUTS.json')).read_text())['files'])
names=['synthesize/board_top_syn.adf','synthesize/board_top_syn.vm'] if phase=='pre' else ['generate_bitstream/board_top.sbit']
artifacts=[]
for name in names:
 p=H/phase/name;assert p.is_file() and p.stat().st_size>0 and p.stat().st_mtime>=start-2
 artifacts.append(dict(path=p.relative_to(H).as_posix(),bytes=p.stat().st_size,SHA256=sha(p),mtime_epoch=p.stat().st_mtime))
save('PRE_EXIT_RECEIPT.json' if phase=='pre' else 'BUILD_EXIT_RECEIPT.json',dict(status='PROCESS_EXITED_REAL_ARTIFACTS_PRESENT_FULL_AUDIT_PENDING',process=r,started_epoch=start,ended_epoch=time.time(),artifacts=artifacts))
print(phase+' exited; fresh artifacts verified; next audit pending')
