from pathlib import Path
import json,hashlib,shutil,time,ast
H=Path(__file__).resolve().parent;R=H.parent/'2026-10-28-local-debug-insert-m1-r2';P=H.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
scope=P/'deliveries/mainline-local-debug-insert-r3-scope-2026-10-28-v1/IMPLEMENTATION_SCOPE.md'
assert sha(scope)=='2DF97E37D6151A44BBEEE792BDBA741455CEA9E62E470B18BEC1D60812221917'
assert not (H/'STAGE_CLOCK.json').exists()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
start=time.monotonic();save('STAGE_CLOCK.json',dict(start_monotonic=start,deadline_monotonic=start+3600,budget_seconds=3600))
save('APPROVAL.json',dict(date_client='2026-10-28',decision='D177',scope='1.3.0',scope_SHA256=sha(scope),user_reply='批准 继续',GUI_max_launches=1,GUI_max_seconds=600,PDS_max_builds=1,PDS_max_seconds=1800,hardware='STOPPED'))
rows=json.loads((R/'PROTECTED_ORIGINALS.json').read_text())['files']
assert all(sha(Path(x['path']))==x['SHA256'] for x in rows)
# Also freeze the previous attempt's 50 execution inputs; never edit old evidence.
prev=json.loads((R/'FROZEN_INPUTS.json').read_text())['files']
rows+= [dict(path=str(R/x['path']),SHA256=x['SHA256']) for x in prev]
assert all(sha(Path(x['path']))==x['SHA256'] for x in rows)
save('PROTECTED_ORIGINALS.json',dict(files=rows))
for n in ['source','source-before','firmware']:shutil.copytree(R/n,H/n)
(H/'pds').mkdir();shutil.copytree(R/'pds/source',H/'pds/source')
for n in ['board_pins.fdc','clock_27mhz.fdc']:shutil.copy2(R/'pds'/n,H/'pds'/n)
shutil.copy2(R/'prepared/build_fixed.tcl',H/'pds/build.tcl')
for n in ['SOURCE_RECEIPTS.json','DEBUG_METADATA.patch','stage_budget.py']:shutil.copy2(R/n,H/n)
(H/'logs').mkdir();(H/'scripts').mkdir();(H/'gui-commands').mkdir()
shutil.copy2(R/'scripts/gui-probe.tcl',H/'scripts/gui-probe.tcl')
shutil.copy2(R/'prepared/window_policy.py',H/'window_policy.py')
shutil.copy2(R/'prepared/test_window_policy.py',H/'test_window_policy.py')
gui=(R/'prepared/gui_control_fixed.py').read_text(encoding='utf-8')
gui=gui.replace(" selfcheck();assert not c.windll.shell32.IsUserAnAdmin();assert not (H/'GUI-attempt.json').exists()"," selfcheck();assert not c.windll.shell32.IsUserAnAdmin();assert not (H/'GUI-attempt.json').exists()\n from process_guard import verify_waiting_pds\n verify_waiting_pds(H)")
ast.parse(gui);(H/'gui_control.py').write_text(gui,encoding='utf-8')
host=(R/'host_supervisor.py').read_text(encoding='utf-8')
old=' p=subprocess.Popen(list(map(str,argv)),cwd=cwd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)'
new=old+'''
 birth=[FT() for _ in range(4)]
 if not k.GetProcessTimes(p._handle,*[ctypes.byref(t) for t in birth]):
  p.terminate();p.wait(timeout=3);raise RuntimeError('OWN_PROCESS_IDENTITY_UNAVAILABLE')
 save(d/'own-process.json',dict(pid=p.pid,creation_ticks=(birth[0].high<<32)|birth[0].low,argv=list(map(str,argv))))'''
assert host.count(old)==1;host=host.replace(old,new);ast.parse(host)
(H/'host_supervisor.py').write_text(host,encoding='utf-8')
run=(R/'run_pds.py').read_text(encoding='utf-8').replace("'D175'","'D177'")
run=run.replace("H/'stage_budget.py']","H/'stage_budget.py',H/'window_policy.py',H/'process_guard.py']")
(H/'run_pds.py').write_text(run,encoding='utf-8')
assert 'clock seconds' not in (H/'pds/build.tcl').read_text()
receipt=json.loads((H/'SOURCE_RECEIPTS.json').read_text())
for r in receipt['files']:
 assert sha(H/'source'/r['name'])==r['candidate_SHA256']
 assert sha(H/'source-before'/r['name'])==r['baseline_SHA256']
print('R3 prepared; 96 protected originals; unchanged 13-source metadata candidate; no vendor launch')
