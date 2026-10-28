from pathlib import Path
import json,hashlib,shutil,time,difflib,ast
H=Path(__file__).resolve().parent;P=H.parents[2];R=H.parent/'2026-10-28-local-debug-insert-m1-r3';B=H.parent/'2026-10-27-board-coremark8-bitstream-m1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
scope=P/'deliveries/mainline-local-debug-insert-r4-scope-2026-10-28-v1/IMPLEMENTATION_SCOPE.md'
assert sha(scope)=='133BA9BB7BA890EE3DFD792B486DCFCA6899092D25BA62335C22676634DA9484'
assert not (H/'STAGE_CLOCK.json').exists()
now=time.monotonic();save('STAGE_CLOCK.json',dict(start_monotonic=now,deadline_monotonic=now+3600,budget_seconds=3600))
save('APPROVAL.json',dict(date_client='2026-10-28',decision='D179',scope_version='1.4.0',scope_SHA256=sha(scope),user_reply='批准',PDS_entries=2,pre_seconds=180,build_seconds=1800,GUI_launches=1,GUI_seconds=600,hardware='STOPPED'))
protected=json.loads((R/'PROTECTED_ORIGINALS.json').read_text())['files']
for x in json.loads((R/'FROZEN_INPUTS.json').read_text())['files']:protected.append(dict(path=str(R/x['path']),SHA256=x['SHA256']))
assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
save('PROTECTED_ORIGINALS.json',dict(files=protected))
for n in ['source','source-before','firmware']:shutil.copytree(R/n,H/n)
mark=b' /* synthesis PAP_MARK_DEBUG="true" */'
p=H/'source/cpu.v';raw=p.read_bytes();old=b'wire eei_hold =';assert raw.count(old)==1
p.write_bytes(raw.replace(old,b'wire eei_hold'+mark+b' =',1))
assert sum(p.read_bytes().count(mark) for p in (H/'source').iterdir() if p.is_file())==7
rows=[];diff=[]
for p in sorted((H/'source').iterdir()):
 if not p.is_file():continue
 before=(H/'source-before'/p.name).read_bytes();after=p.read_bytes();assert after.replace(mark,b'')==before
 rows.append(dict(name=p.name,baseline_SHA256=hashlib.sha256(before).hexdigest().upper(),candidate_SHA256=sha(p),stripped_equals_baseline=True))
 if before!=after:diff.extend(difflib.unified_diff(before.decode('utf-8-sig').splitlines(True),after.decode('utf-8-sig').splitlines(True),fromfile='source-before/'+p.name,tofile='source/'+p.name))
save('SOURCE_RECEIPTS.json',dict(status='SEVEN_COMMENT_ONLY_CANDIDATE',files=rows,comments=7))
(H/'DEBUG_METADATA.patch').write_bytes(''.join(diff).encode('utf-8'))
flow=(B/'pds/build.tcl').read_text()
pre=flow.split('dev_map',1)[0]
full=flow.replace('dev_map','add_fic [file normalize [file join $project_dir .. debug.fic]]\ndev_map',1)
for n,tcl in [('pre',pre),('build',full)]:
 (H/n).mkdir();shutil.copytree(R/'pds/source',H/n/'source')
 for name in ['cpu.v','soc_top.sv','board_top.sv']:shutil.copy2(H/'source'/name,H/n/'source'/name)
 for name in ['board_pins.fdc','clock_27mhz.fdc']:shutil.copy2(B/'pds'/name,H/n/name)
 (H/n/'flow.tcl').write_text(tcl,encoding='utf-8')
 assert 'clock seconds' not in tcl and 'while ' not in tcl
(H/'scripts').mkdir();(H/'logs').mkdir();(H/'gui-commands').mkdir()
for n in ['stage_budget.py','host_supervisor.py','window_policy.py','test_window_policy.py']:shutil.copy2(R/n,H/n)
gui=(R/'gui_control.py').read_text(encoding='utf-8')
gui=gui.replace('from process_guard import verify_waiting_pds','from process_guard import verify_completed_synthesis').replace('verify_waiting_pds(H)','verify_completed_synthesis(H)')
ast.parse(gui);(H/'gui_control.py').write_text(gui,encoding='utf-8')
root=H.as_posix()
probe=f'''ins_new {{{root}/debug.fic}}
ins_set_file -input {{{root}/pre/synthesize/board_top_syn.adf}}
ins_add_core 1
ins_set_core -core 0 -data_depth 1024 -clock_edge 1 -multi_windows 0 -enable_sq 0
puts {{A_R4_NETS_BEGIN}}
ins_list_nets
puts {{A_R4_NETS_END}}
ins_save {{{root}/debug.fic}}
'''
(H/'scripts/gui-probe.tcl').write_text(probe,encoding='utf-8')
print('R4 prepared: 7 comments stripped restore all 13 originals; two nonwaiting PDS scripts')
