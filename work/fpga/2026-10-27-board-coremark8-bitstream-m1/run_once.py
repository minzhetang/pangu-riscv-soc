from pathlib import Path
import sys,json,time,hashlib,ctypes
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
from stage_budget import check,STAGE_DEADLINE
from host_supervisor import bounded
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def protect():
 rows=read(H/'PROTECTED_ORIGINALS.json')['files'];assert all(sha(Path(r['path']))==r['SHA256'] for r in rows);return len(rows)
if __name__=='__main__':
 check();assert not ctypes.windll.shell32.IsUserAnAdmin();protect();assert not (H/'PDS-attempt.json').exists();assert not (H/'pds/compile').exists();assert not list((H/'pds').rglob('*.sbit'))
 files=[p for root in ['source','source-before','firmware','pds/source'] for p in (H/root).iterdir() if p.is_file()]+[H/'pds/build.tcl',H/'pds/board_pins.fdc',H/'pds/clock_27mhz.fdc',H/'host_supervisor.py',H/'stage_budget.py',Path(__file__)]
 save('FROZEN_INPUTS.json',dict(files=[dict(path=str(p.relative_to(H)),SHA256=sha(p)) for p in files]))
 budget=min(1800,STAGE_DEADLINE-time.monotonic());assert budget>60
 save('PDS-attempt.json',dict(used=1,maximum=1,approval='D164',timeout_seconds=budget,max_logs_each=32*1024**2,shell_parent_memory_limit_bytes=4*1024**3,hardware='STOPPED'))
 start=time.time();argv=['D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe','-file',str(H/'pds/build.tcl')]
 try:
  r=bounded(argv,H/'pds','pds-flow-once',budget,cap=4*1024**3)
 except Exception as exc:
  save('STATUS.json',dict(status='PDS_EXECUTION_STOPPED_PENDING_DIAGNOSIS',error_type=type(exc).__name__,PDS_attempts_used=1,new_DUT=0,hardware='STOPPED'));print('PDS stopped; original diagnostics retained; no retry');raise
 end=time.time();check();protect();assert all(sha(H/x['path'])==x['SHA256'] for x in read(H/'FROZEN_INPUTS.json')['files'])
 artifacts=[dict(path=str(p),bytes=p.stat().st_size,SHA256=sha(p),mtime_epoch=p.stat().st_mtime) for p in (H/'pds').rglob('*.sbit')]
 save('BUILD_EXIT_RECEIPT.json',dict(status='PROCESS_EXITED_NOT_YET_ARTIFACT_ACCEPTANCE',process=r,started_epoch=start,ended_epoch=end,artifacts=artifacts,protected=protect(),hardware='STOPPED'))
 print(json.dumps(dict(status='PDS_EXITED_ARTIFACT_AUDIT_PENDING',native_rc=r['returncode'],seconds=r['elapsed_seconds'],sbit_count=len(artifacts)),ensure_ascii=False))
