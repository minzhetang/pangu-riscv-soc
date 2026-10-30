"""Repair absent log parent only, preserving pre-Popen failure and original deadline."""
from pathlib import Path
import sys,json,hashlib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
old=json.loads((H/'STOPPED.json').read_text(encoding='utf8'));assert old['exception_type']=='FileNotFoundError' and old['completed_audits']==[]
assert not (H/'logs').exists() and not list(H.glob('*/pds/compile')) and not list(H.rglob('*.sbit'))
(H/'logs').mkdir()
s=(H/'run_stage.py').read_text();s=s.replace("H/'HOST_PREFLIGHT.json'","H/'HOST_PREFLIGHT-r1.json'").replace("H/'FROZEN_INPUTS.json'","H/'FROZEN_INPUTS-r1.json'").replace("d/'PDS_ATTEMPT.json'","d/'PDS_ATTEMPT-r1.json'").replace("H/'STOPPED.json'","H/'STOPPED-r1.json'")
(H/'run_stage-r1.py').write_text(s,encoding='utf8')
with (H/'PRELAUNCH_RECOVERY.json').open('x',encoding='utf8') as f:json.dump(dict(reason='missing logs parent, FileNotFoundError at bounded mkdir before subprocess.Popen; native PDS0',original_error='STOPPED.json',native_attempts_consumed=0,maximum_native=2,original_clock_retained=True,source_inputs_modified=False,repair='create logs and r1 metadata/entry paths only',frozen_original_entry_SHA256=hashlib.sha256((H/'run_stage.py').read_bytes()).hexdigest().upper()),f,indent=2)
print('Prelaunch error retained; log parent created; no PDS executed; original two-CLI budget retained')
