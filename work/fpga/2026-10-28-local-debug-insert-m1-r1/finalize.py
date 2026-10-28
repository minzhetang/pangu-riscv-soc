"""Read-only postflight and safe receipts. Do not start vendor executables."""
from pathlib import Path
import hashlib,json,re,time
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
old=json.loads((H/'PROTECTED_ORIGINALS.json').read_text(encoding='utf-8-sig'))['files']
assert all(sha(Path(r['path']))==r['SHA256'] for r in old)
r1=json.loads((H/'gui-attempt1/GUI_RESULT.json').read_text());r2=json.loads((H/'GUI_RESULT.json').read_text())
gui_seconds=r1['seconds']+r2['seconds'];assert gui_seconds<600
assert r1['root_exited'] and r2['root_exited']
assert not r1['remaining_own_windows'] and not r2['remaining_own_windows']
source=json.loads((H/'SOURCE_RECEIPTS.json').read_text())
for r in source['files']:
 assert sha(H/'source-before'/r['name'])==r['baseline_SHA256']
 assert sha(H/'source'/r['name'])==r['candidate_SHA256']
fic=(H/'partial.fic').read_text(encoding='utf-8-sig');assert 'dataDepth=1024' in fic
assert 'clockEdge=Rising' in fic and 'enableStorageQualification=false' in fic and 'enableMultiWindow=false' in fic
assert not re.search(r'\.triggerChannel<',fic)
logs='\n'.join(p.read_text(errors='replace') for p in [H/'gui-attempt1/gui-stdout.log',H/'gui-stdout.log'])
days=[int(x) for x in re.findall(r'will\s+invaild\s+in\s+(\d+)\s+days',logs)]
save('SAFE_TOOL_RESULT.json',dict(license_checkout_observed='fabric_inserter',actual_expiry_notice_days=days,ADF_compile_success='Compiling file' in logs and 'successfully' in logs,net_recovery_message='All signals have been recovered' in logs,net_listing_success='Executing : ins_list_nets successfully.' in logs,FIC_save_success='Executing : ins_save' in logs and 'partial.fic successfully.' in logs,license_paths_or_machine_identifiers_not_copied=True))
save('POSTFLIGHT.json',dict(protected_originals=len(old),protected_originals_unchanged=True,source_before_13_unchanged=True,metadata_stripping_restores_original_13=True,new_PDS=0,new_DUT=0,new_Flash=0,hardware='STOPPED',gui_launches=2,gui_seconds=gui_seconds,both_own_roots_exited=True,remaining_own_visible_windows=0,partial_FIC_SHA256=sha(H/'partial.fic'),partial_FIC_bytes=(H/'partial.fic').stat().st_size,stage_seconds=time.monotonic()-json.loads((H/'STAGE_CLOCK.json').read_text())['start_monotonic']))
mapping=json.loads((H/'NET_MAPPING.json').read_text())
save('SUMMARY.json',dict(date_client='2026-10-28',stage='A-LOCAL-DEBUG-INSERT-M1-R1',scope_version='1.1.0',approval='D173',fact='F168',decision='D174',status='PARTIAL_GUI_CONFIGURATION_SAVED_STOPPED_NO_BUILD',gui_launches=2,gui_seconds=gui_seconds,actual_listed_nets=mapping['net_count'],planned_data_bits=140,name_matched_bits=126,unresolved_mapping_bits=14,actual_connected_data_bits=0,partial_FIC='partial.fic',partial_FIC_SHA256=sha(H/'partial.fic'),depth=1024,clock_edge='Rising',qualification=False,multi_window=False,device_settings_new_FIC='NOT_VERIFIED',new_PDS=0,new_Inserter_CLI=0,new_DUT=0,new_debug_bitstream='NOT_GENERATED',new_timing='NOT_RUN',new_INIT_audit='NOT_RUN',new_metadata_candidate='PREPARED_NOT_SYNTHESIZED',stop_reason='A GUI supervisor required a fixed title; ins_save changed it. No tool design failure established; GUI two-launch limit now exhausted.',root_exit_codes=[r1['rc'],r2['rc']],license_notice_days=days,hardware='STOPPED',limitations=['126 names matched are not proof of connected FIC channels','14 unmatched exact names do not establish absent logical functions','No bitstream or hardware capture acceptance','Next GUI use requires new bounded authorization; unused PDS budget is not a third GUI launch']))
exclude={'SHA256SUMS.json'}
rows=[dict(path=p.relative_to(H).as_posix(),bytes=p.stat().st_size,SHA256=sha(p)) for p in sorted(H.rglob('*')) if p.is_file() and p.name not in exclude]
save('SHA256SUMS.json',dict(status='LOCAL_ONLY_INCLUDES_VENDOR_INPUT_AND_RAW_LOG_HASHES',files=rows))
print(json.dumps(json.loads((H/'SUMMARY.json').read_text()),ensure_ascii=False))
