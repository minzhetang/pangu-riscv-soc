from pathlib import Path
import hashlib,json,sys,re
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
    with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
r=read(H/'RESULT.json');notice=read(H/'LICENSE_NOTICE.json');old=read(H/'OLD_NOTICE_REPARSE.json')
assert r['GUI_launches']==1 and r['within_180_seconds'] and r['root_exited']
assert not r['remaining_own_visible_windows'] and r['control_invocations']==0
assert r['windows'][0]['title']=='Expiration Reminder'
assert notice['days']==old['days']==6
frozen=read(H/'FROZEN_INPUTS.json')['files']
assert all(sha(Path(x['path']))==x['SHA256'] for x in frozen)
protected=read(P/'work/fpga/2026-10-28-local-debug-insert-m1/PROTECTED_ORIGINALS.json')['files']
assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
d=P/'deliveries/mainline-local-debug-insert-r1-scope-2026-10-28-v1/IMPLEMENTATION_SCOPE.md'
save('SUMMARY.json',dict(date_client='2026-10-28',fact='F167',decisions=['D171','D172'],status='TITLE_AND_NATIVE_EXPIRY_NOTICE_VERIFIED_BODY_UNREAD',GUI_launches=1,GUI_seconds=r['elapsed_seconds'],window_title='Expiration Reminder',control_invocations=0,new_PDS=0,new_DUT=0,hardware='STOPPED',actual_native_days_notice=6,expiry_source='native stdout, not inferred from date; no license file read',license_feature_checkout='NOT_ESTABLISHED',old_F166_parser_correction='missed vendor invaild typo; same preserved old stdout already had six days',original_GUI_body_unread=True,UIA='unavailable rc1; original stderr not retained; minimal file helper later security exception, effective policy query unavailable',policy_changed=False,bypass_used=False,root_exited=True,remaining_own_visible_windows=0,protected_originals=len(protected),frozen_inputs=len(frozen),all_unchanged=True,upcoming_scope=dict(version='1.1.0',path=str(d),SHA256=sha(d),status='PENDING_SCOPE_APPROVAL')))
save('POSTFLIGHT.json',dict(status='READ_ONLY_GUI_SCOPE_COMPLETED_WITH_LIMITS',GUI_launches=1,GUI_budget_seconds=180,actual_GUI_seconds=r['elapsed_seconds'],root_exited=True,remaining_own_visible_windows=0,protected_originals=len(protected),frozen_inputs=len(frozen),unchanged=True,new_PDS=0,new_DUT=0,hardware='STOPPED'))
rows=[]
for p in sorted(H.rglob('*')):
    if p.is_file() and p.name!='SHA256SUMS.json':
        assert not p.is_symlink() and not getattr(p.lstat(),'st_file_attributes',0)&0x400
        rows.append(dict(path=p.relative_to(H).as_posix(),bytes=p.stat().st_size,SHA256=sha(p)))
save('SHA256SUMS.json',dict(files=rows,raw_native_and_security_logs='LOCAL_ONLY'))
print(json.dumps(dict(status='GUI_SCOPE_COMPLETED_WITH_LIMITS',days=6,protected=len(protected),GUI_seconds=r['elapsed_seconds'],R1_scope='PENDING',R1_SHA256=sha(d))))
