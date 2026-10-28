from pathlib import Path
import json,hashlib,time,re,sys
sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
old=json.loads((H/'PROTECTED_ORIGINALS.json').read_text())['files']
frozen=json.loads((H/'FROZEN_INPUTS.json').read_text())['files']
assert all(sha(Path(x['path']))==x['SHA256'] for x in old)
assert all(sha(H/x['path'])==x['SHA256'] for x in frozen)
assert not list((H/'pds').rglob('*.sbit')) and not (H/'debug.fic').exists()
assert json.loads((H/'GUI_RESULT.json').read_text())['root_exited']
assert json.loads((H/'WAIT_QUERY_RESULT.json').read_text())['status']=='PASS'
assert json.loads((H/'prepared/POLICY_SELFTEST.json').read_text())['status']=='PASS'
final=json.loads((H/'POSTFLIGHT.json').read_text())
final.update(PDS_readonly_help_processes=2,help_queries=6,stage_seconds=time.monotonic()-json.loads((H/'STAGE_CLOCK.json').read_text())['start_monotonic'],remaining_own_GUI_windows=0,license_actual_days=[6],completion='PARTIAL_SYNTHESIS_ONLY_NO_FIC_OR_BITSTREAM')
assert final['stage_seconds']<3600
with (H/'POSTFLIGHT_FINAL.json').open('x',encoding='utf-8') as f:json.dump(final,f,indent=2);f.write('\n')
files=[dict(path=p.relative_to(H).as_posix(),bytes=p.stat().st_size,SHA256=sha(p)) for p in sorted(H.rglob('*')) if p.is_file() and p.name!='SHA256SUMS-final.json']
with (H/'SHA256SUMS-final.json').open('x',encoding='utf-8') as f:json.dump(dict(scope='LOCAL_ONLY_FINAL_SNAPSHOT_INCLUDES_VENDOR_ARTIFACT_HASHES_NOT_CONTENT_UPLOAD',files=files),f,indent=2);f.write('\n')
print(json.dumps(final))
