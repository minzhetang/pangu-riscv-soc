from pathlib import Path
import hashlib,json,shutil,time,sys,re
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
B=H.parent/'2026-10-27-board-coremark8-bitstream-m1'
R=H.parent/'2026-10-28-local-debug-insert-m1-r1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
scope=P/'deliveries/mainline-local-debug-insert-r2-scope-2026-10-28-v1/IMPLEMENTATION_SCOPE.md'
assert sha(scope)=='C67EC98CBE52B27132D6EAA173D9630F16BEF543FCBAB0854038F385F6020B15'
assert not (H/'STAGE_CLOCK.json').exists()
start=time.monotonic();save('STAGE_CLOCK.json',dict(start_monotonic=start,deadline_monotonic=start+3600,budget_seconds=3600))
save('APPROVAL.json',dict(date_client='2026-10-28',decision='D175',scope='A-LOCAL-DEBUG-INSERT-M1-R2 / 1.2.0',scope_SHA256=sha(scope),user_reply='均批准',GUI_launch_limit=1,GUI_seconds=600,PDS_build_limit=1,PDS_seconds=1800,hardware='STOPPED'))
old=json.loads((R/'PROTECTED_ORIGINALS.json').read_text(encoding='utf-8-sig'))['files']
assert all(sha(Path(x['path']))==x['SHA256'] for x in old)
save('PROTECTED_ORIGINALS.json',dict(files=old))
for name in ['source','source-before']:shutil.copytree(R/name,H/name)
receipts=json.loads((R/'SOURCE_RECEIPTS.json').read_text())
for x in receipts['files']:
 assert sha(H/'source'/x['name'])==x['candidate_SHA256']
 assert sha(H/'source-before'/x['name'])==x['baseline_SHA256']
shutil.copy2(R/'SOURCE_RECEIPTS.json',H/'SOURCE_RECEIPTS.json')
shutil.copy2(R/'DEBUG_METADATA.patch',H/'DEBUG_METADATA.patch')
(H/'logs').mkdir();(H/'scripts').mkdir();(H/'pds').mkdir()
shutil.copytree(B/'pds/source',H/'pds/source')
for n in ['cpu.v','soc_top.sv','board_top.sv']:shutil.copy2(H/'source'/n,H/'pds/source'/n)
for n in ['board_pins.fdc','clock_27mhz.fdc']:shutil.copy2(B/'pds'/n,H/'pds'/n)
shutil.copytree(B/'firmware',H/'firmware')
for n in ['stage_budget.py','host_supervisor.py']:shutil.copy2(B/n,H/n)
original=(B/'pds/build.tcl').read_text()
head,tail=original.split('dev_map',1)
pause='''
set f [open [file join $project_dir .. SYNTH_READY.json] w]
puts $f {"status":"SYNTHESIS_FINISHED_AWAITING_FIC"}
close $f
set wait_deadline [expr {[clock seconds]+720}]
while {![file exists [file join $project_dir .. FIC_READY.json]]} {
    if {[file exists [file join $project_dir .. GUI_ABORT.json]]} {error "A_GUI_ABORT"}
    if {[clock seconds]>$wait_deadline} {error "A_FIC_WAIT_DEADLINE"}
    after 200
}
add_fic [file join $project_dir .. debug.fic]
puts {A_FIC_ATTACHED_BEFORE_MAP}
dev_map'''
(H/'pds/build.tcl').write_text(head+pause+tail,encoding='utf-8')
probe='''set h [file normalize [file join [file dirname [info script]] ..]]
ins_new [file join $h debug.fic]
ins_set_file -input [file join $h pds synthesize board_top_syn.adf]
ins_add_core 1
ins_set_core -core 0 -data_depth 1024 -clock_edge 1 -multi_windows 0 -enable_sq 0
puts {A_R2_NETS_BEGIN}
ins_list_nets
puts {A_R2_NETS_END}
ins_save [file join $h debug.fic]
'''
(H/'scripts/gui-probe.tcl').write_text(probe,encoding='utf-8')
print('R2 frozen candidates prepared; 13 input hashes agree; no vendor process yet')
