from pathlib import Path
import json
from window_policy import decide
H=Path(__file__).resolve().parent
main=dict(role='main',minimized=False,client_size=[1723,1004],title='Fabric Inserter')
saved=dict(main,title='Fabric Inserter - D:/saved.fic')
reminder=dict(role='reminder',minimized=False,client_size=[500,106])
req=dict(role='main',op='source',expected_client_size=[1723,1004])
cases=[
 ('startup_main_absent',req,[],'WAIT_ROLE'),
 ('reminder_before_main',req,[reminder],'WAIT_REMINDER'),
 ('reminder_over_main_blocks_typing',req,[main,reminder],'WAIT_REMINDER'),
 ('main_after_reminder',req,[main],'EXECUTE'),
 ('save_title_change_same_role',req,[saved],'EXECUTE'),
 ('duplicate_main',req,[main,saved],'STOP_AMBIGUOUS_ROLE'),
 ('unknown_dialog',req,[dict(role='REJECT')],'STOP_UNKNOWN_DIALOG'),
 ('minimized_prevents_typing',req,[dict(main,minimized=True)],'WAIT_RESTORE'),
 ('resized_prevents_typing',req,[dict(main,client_size=[1000,700])],'STOP_GEOMETRY_CHANGED'),
 ('restore_allowed_minimized',dict(role='main',op='restore'),[dict(main,minimized=True)],'EXECUTE'),
 ('reminder_capture_explicit',dict(role='reminder',op='capture'),[reminder],'EXECUTE'),
 ('reminder_click_exact_geometry',dict(role='reminder',op='click',expected_client_size=[500,106]),[reminder],'EXECUTE'),
 ('reminder_wrong_geometry',dict(role='reminder',op='click',expected_client_size=[600,106]),[reminder],'STOP_GEOMETRY_CHANGED'),
]
results=[]
for name,request,rows,expected in cases:
 actual=decide(request,rows);results.append(dict(name=name,expected=expected,actual=actual,PASS=actual==expected))
 if actual!=expected:raise RuntimeError(name)
# The previously failing sequence must wait twice and execute once, never send to the reminder.
sequence=[decide(req,s) for s in [[],[reminder],[main]]]
assert sequence==['WAIT_ROLE','WAIT_REMINDER','EXECUTE']
(H/'POLICY_SELFTEST.json').write_text(json.dumps(dict(status='PASS',tests=results,startup_sequence=sequence,scope='PURE_HOST_SYNTHETIC_METADATA_NOT_GUI_OR_DUT'),indent=2)+'\n',encoding='utf-8')
print('13 policy tests and startup sequence PASS; no GUI/vendor/DUT run')
