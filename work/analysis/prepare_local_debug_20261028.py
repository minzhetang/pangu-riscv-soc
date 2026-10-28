from pathlib import Path
import hashlib,json,shutil,time,sys,ctypes
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
P=Path('D:/A_FPGA_Comp');B=P/'work/fpga/2026-10-27-board-coremark8-bitstream-m1';H=P/'work/fpga/2026-10-28-local-debug-insert-m1'
D=P/'deliveries/mainline-local-debug-insert-scope-2026-10-28-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
assert not H.exists()
assert not ctypes.windll.shell32.IsUserAnAdmin()
assert shutil.disk_usage(P).free>=4*1024**3
assert sha(D/'IMPLEMENTATION_SCOPE.md')=='A93E2E610278DC6C723CE257DB253F8BD425A34F657B2D74321ACA5C67550DA0'
H.mkdir();start=time.monotonic()
def save(n,o):
    with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
save('STAGE_CLOCK.json',dict(started_monotonic=start,deadline_monotonic=start+3600,total_seconds=3600,date_client='2026-10-28'))
save('APPROVAL.json',dict(date_client='2026-10-28',decision='D169',user_reply='批准',scope='A-LOCAL-DEBUG-INSERT-M1 / 1.0.0',scope_actual_SHA256=sha(D/'IMPLEMENTATION_SCOPE.md'),max_Inserter_CLI=6,max_PDS_builds=1,max_new_C=0,max_new_DUT=0,GUI=False,hardware='STOPPED',external_tool_permission='SEPARATE_SYSTEM_REVIEW'))
for name in ['source','source-before','pds/source','ins-input','firmware','scripts','evidence']:(H/name).mkdir(parents=True,exist_ok=True)
protected=[]
def pin(p):
    if str(p) not in {r['path'] for r in protected}:protected.append(dict(path=str(p),SHA256=sha(p),bytes=p.stat().st_size))
def copy(p,q):
    pin(p);shutil.copyfile(p,q);assert sha(p)==sha(q)
for row in read(B/'SOURCE_RECEIPTS.json')['functional_RTL']:
    name=row['name'];assert sha(B/'source'/name)==row['SHA256']
    copy(B/'source'/name,H/'source'/name);copy(B/'source'/name,H/'source-before'/name)
    copy(B/'pds/source'/name,H/'pds/source'/name)
for name in ['board_pins.fdc','clock_27mhz.fdc']:copy(B/'pds'/name,H/'pds'/name)
copy(B/'pds/synthesize/board_top_syn.adf',H/'ins-input/board_top_syn.adf')
for name in ['program.bin','program.elf']:copy(B/'firmware'/name,H/'firmware'/name)
for n in ['SUMMARY.json','SOURCE_RECEIPTS.json','CONFIGURATION_AUDIT.json','TIMING_RESOURCE_AUDIT.json','WARNINGS_LICENSE_AUDIT.json','MEMORY_INIT_AUDIT.json','INIT_RECEIPT.json','pds/build.tcl','pds/generate_bitstream/board_top.sbit']:
    pin(B/n)
pin(D/'IMPLEMENTATION_SCOPE.md');pin(D/'SCOPE_STATUS.json')
for name in ['cdt_ins.exe','pds_shell.exe']:pin(Path('D:/PDS/PDS_2022.2-SP6.4/bin')/name)
for name in ['stage_budget.py','host_supervisor.py']:copy(B/name,H/name)
# Reuse the bounded runner, adding only own-process visible-window detection.
q=H/'host_supervisor.py';s=q.read_text(encoding='utf-8-sig')
old="if p.poll() is None:\n     value=peak(p.pid)"
new="if p.poll() is None:\n     require(not own_visible_window(p.pid),'UNEXPECTED_GUI_VISIBLE')\n     value=peak(p.pid)"
assert s.count(old)==1
guard='''
def own_visible_window(pid):
 found=[]
 u=ctypes.windll.user32
 callback_type=ctypes.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)
 @callback_type
 def visit(hwnd,lparam):
  owner=w.DWORD();u.GetWindowThreadProcessId(hwnd,ctypes.byref(owner))
  if owner.value==pid and u.IsWindowVisible(hwnd):found.append(True)
  return True
 u.EnumWindows.argtypes=[callback_type,w.LPARAM]
 require(bool(u.EnumWindows(visit,0)),'OWN_WINDOW_GUARD_UNAVAILABLE')
 return bool(found)
'''
s=s.replace('def bounded(',guard+'\ndef bounded(',1).replace(old,new)
q.write_text(s,encoding='utf-8')
save('RUNNER_CHANGE.json',dict(base=str(B/'host_supervisor.py'),change='Only check visible top-level windows belonging to the just-created Inserter/PDS process; stop own task on unexpected GUI',does_not_scan_hardware=True))
save('PROTECTED_ORIGINALS.json',dict(files=protected))
save('COUNTERS.json',dict(Inserter_CLI_used=0,PDS_used=0,first_failure=False))
save('PREPARATION.json',dict(status='INPUTS_PREPARED_NOT_NATIVE_VALIDATED',protected=len(protected),source13_same=True,new_C=0,new_DUT=0,hardware='STOPPED'))
assert all(sha(Path(r['path']))==r['SHA256'] for r in protected)
print(json.dumps(dict(stage=str(H),status='PREPARED',protected=len(protected),native_calls=0)))
