from pathlib import Path
import json,hashlib,re,collections,time
H=Path(__file__).resolve().parent;B=H.parent/'2026-10-27-board-coremark8-bitstream-m1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
new=(H/'build/flow.log').read_text(errors='replace').splitlines();old=(B/'pds/flow.log').read_text(errors='replace').splitlines()
delta=collections.Counter(x for x in new if x.startswith('W: Public-4008'))-collections.Counter(x for x in old if x.startswith('W: Public-4008'))
lines=list(delta.elements())
save('WARNING_DETAIL.json',dict(new_Public4008_messages=lines,count=len(lines),debug_namespace=sum('u_CORES/' in x for x in lines),not_automatically_waived=True))
audit=json.loads((H/'AUDIT_RESULT.json').read_text());fic=json.loads((H/'FIC_AUDIT.json').read_text())
pre=json.loads((H/'PRE_EXIT_RECEIPT.json').read_text());build=json.loads((H/'BUILD_EXIT_RECEIPT.json').read_text());gui=json.loads((H/'GUI_RESULT.json').read_text())
assert pre['process']['returncode']==build['process']['returncode']==gui['rc']==0
assert gui['root_exited'] and not gui['remaining_own_windows']
assert gui['seconds']<600 and pre['process']['elapsed_seconds']<180 and build['process']['elapsed_seconds']<1800
protected=json.loads((H/'PROTECTED_ORIGINALS.json').read_text())['files'];assert all(sha(Path(x['path']))==x['SHA256'] for x in protected)
frozen={}
for phase in ['pre','build']:
 rows=json.loads((H/(phase+'-FROZEN_INPUTS.json')).read_text())['files'];frozen[phase]=len(rows)
 assert all(sha(H/x['path'])==x['SHA256'] for x in rows)
stage=time.monotonic()-json.loads((H/'STAGE_CLOCK.json').read_text())['start_monotonic'];assert stage<3600
save('POSTFLIGHT.json',dict(protected_original_entries=len(protected),protected_unchanged=True,frozen_files=frozen,frozen_unchanged=True,scope_version='1.4.0',PDS_entries=2,PDS_rc=[0,0],PDS_seconds=[pre['process']['elapsed_seconds'],build['process']['elapsed_seconds']],GUI_entries=1,GUI_rc=0,GUI_seconds=gui['seconds'],stage_seconds=stage,extra_native_queries=0,new_DUT=0,hardware='STOPPED'))
save('SUMMARY.json',dict(date_client='2026-10-28',fact='F171',approval='D179',result_decision='D180',stage='A-LOCAL-DEBUG-INSERT-M1-R4',status=audit['status'],bitstream=audit['artifact'],FIC=dict(path='debug.fic',SHA256=fic['FIC_SHA256'],data_channels=140,depth=1024,clock='nt_clk physical rising',filter=False,multi_window=False),clock27=audit['main_27MHz'],minimum_setup_ns=audit['minimum_setup_ns'],minimum_hold_ns=audit['minimum_hold_ns'],resources=audit['resources'],resource_delta=audit['resource_delta'],functional_INIT_same=1792,critical_open=4,constant_probe_open=7,new_Public4008=len(lines),optional_user_reset_port='DISABLED_DOCUMENTED_DEFAULT; NOT_BOARD_RESET_CONNECTED; sys_rst_n observed channel38',CPU_functional_changes=0,source_comments=7,new_DUT=0,license_actual_days=[6],hardware='STOPPED',next='Read-only review of four tool-generated debug/JTAG clock critical warnings; no automatic rebuild/hardware clearance'))
save('SHA256SUMS.json',dict(scope='LOCAL_ONLY_FINAL_SNAPSHOT_NO_VENDOR_OR_BINARY_CONTENT_UPLOAD',files=[dict(path=p.relative_to(H).as_posix(),bytes=p.stat().st_size,SHA256=sha(p)) for p in sorted(H.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json']))
print(json.dumps(json.loads((H/'SUMMARY.json').read_text()),ensure_ascii=False))
