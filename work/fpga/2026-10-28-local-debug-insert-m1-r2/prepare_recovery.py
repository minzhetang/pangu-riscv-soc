"""Prepare controls only. Never start vendor software or change frozen R2 inputs."""
from pathlib import Path
import json,re,hashlib,ast
H=Path(__file__).resolve().parent;D=H/'prepared'
original=(H/'gui_control.py').read_text(encoding='utf-8')
fixed=original.replace('from PIL import Image,ImageDraw','from PIL import Image,ImageDraw\nfrom window_policy import decide')
fixed=fixed.replace("if row['minimized'] or not(500<=width<=4096 and 250<=height<=2160)","if row['minimized'] or not(300<=width<=4096 and 80<=height<=2160)")
old="""    seen.add(q.name);a=json.loads(q.read_text(encoding='utf-8-sig'))
    current=windows(p.pid);matches=[r for r in current if r['role']==a['role']]
    if len(matches)!=1:raise RuntimeError('OWN_WINDOW_ROLE_NOT_UNIQUE')
    row=matches[0];op=a['op'];hwnd=row['hwnd']"""
new="""    a=json.loads(q.read_text(encoding='utf-8-sig'))
    current=windows(p.pid);decision=decide(a,current)
    if decision.startswith('WAIT_'):
     save('GUI_PENDING.json',dict(command=q.name,decision=decision,elapsed=time.monotonic()-start));continue
    if decision!='EXECUTE':raise RuntimeError(decision)
    matches=[r for r in current if r['role']==a['role']]
    row=matches[0];op=a['op'];hwnd=row['hwnd'];seen.add(q.name)"""
assert original.count(old)==1;fixed=fixed.replace(old,new)
ast.parse(fixed)
with (D/'gui_control_fixed.py').open('x',encoding='utf-8') as f:f.write(fixed)
build=(H/'pds/build.tcl').read_text(encoding='utf-8')
oldwait='''set wait_deadline [expr {[clock seconds]+720}]
while {![file exists [file join $project_dir .. FIC_READY.json]]} {
    if {[file exists [file join $project_dir .. GUI_ABORT.json]]} {error "A_GUI_ABORT"}
    if {[clock seconds]>$wait_deadline} {error "A_FIC_WAIT_DEADLINE"}
    after 200
}'''
newwait='''set a_wait_count 0
while {![file exists [file join $project_dir .. FIC_READY.json]]} {
    if {[file exists [file join $project_dir .. GUI_ABORT.json]]} {error "A_GUI_ABORT"}
    if {$a_wait_count>=3600} {error "A_FIC_WAIT_DEADLINE"}
    after 200
    incr a_wait_count
}'''
assert build.count(oldwait)==1
with (D/'build_fixed.tcl').open('x',encoding='utf-8') as f:f.write(build.replace(oldwait,newwait))
assert 'clock seconds' not in (D/'build_fixed.tcl').read_text()
logs='\n'.join(p.read_text(errors='replace') for p in [H/'logs/pds-flow-once/stdout.log',H/'logs/readonly-help/stdout.log',H/'logs/readonly-wait-query/stdout.log',H/'gui-stdout.log'])
days=sorted(set(map(int,re.findall(r'will\s+(?:invalid|invaild)\s+in\s+(\d+)\s+days',logs,flags=re.I))))
assert days==[6]
with (H/'LICENSE_NOTICE_CORRECTION.json').open('x',encoding='utf-8') as f:json.dump(dict(actual_days=days,initial_auditor_regex_miss=True,correction='invalid and invaild explicitly matched; original logs and preliminary SUMMARY retained',not_exact_expiration_date=True),f,indent=2)
summary=json.loads((H/'SUMMARY.json').read_text())
summary.update(license_days_actual=days,readonly_help_processes=2,readonly_queries_total=6,wait_replacement='BOUNDED_AFTER_WHILE_INCR_NATIVE_QUERY_PASS',window_policy='13_SYNTHETIC_CASES_AND_STARTUP_SEQUENCE_PASS_NOT_NEW_GUI',recovery_files='PREPARED_NOT_EXECUTED',initial_summary_superseded_only_for_license_and_final_query_counts=True)
with (H/'SUMMARY_FINAL.json').open('x',encoding='utf-8') as f:json.dump(summary,f,ensure_ascii=False,indent=2);f.write('\n')
with (D/'PREPARATION_RECEIPT.json').open('x',encoding='utf-8') as f:json.dump(dict(status='PREPARED_NOT_RUN',files=[dict(name=p.name,SHA256=hashlib.sha256(p.read_bytes()).hexdigest().upper()) for p in sorted(D.iterdir()) if p.is_file()],remaining_gate='No new GUI/build budget in R2. Next execution must verify native PDS is still alive before consuming the GUI launch, not only SYNTH_READY presence.'),f,indent=2)
print('Prepared corrections; 6-day native notice parsed; no vendor execution')
