from pathlib import Path
import json,hashlib,importlib.util
R=Path(__file__).resolve().parent
M=json.loads((R/'SHA256_MANIFEST.json').read_text(encoding='utf-8'))
for x in M['files']:
 p=(R/x['path']).resolve()
 if not p.is_relative_to(R) or hashlib.sha256(p.read_bytes()).hexdigest().upper()!=x['sha256']:raise SystemExit('Hash mismatch: '+x['path'])
s=importlib.util.spec_from_file_location('snapshot_checker',R/'host-tools/validate_capture.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
e=json.loads((R/'EXPECTED_FIELDS.json').read_text());count=0
for h in sorted((R/'evidence').iterdir()):
 mode='validation' if 'validation' in h.name else 'performance';raw=(h/'uart-raw.txt').read_bytes();serial=json.loads((h/'SERIAL_RESULT.json').read_text(encoding='utf-8-sig'));run=json.loads((h/'CONTROLLER_RESULT.json').read_text());result=c.validate(raw,serial,e[mode]['expected'],e[mode]['flags'])
 if run['error'] is not None or not all(x['job_empty'] and not x['forced_cleanup'] and x['root_exit_code']==0 for x in run['cleanup']):raise SystemExit('Controller/cleanup failure')
 print(h.name,result['ticks'],'RECORDED_REPORT_REPLAY_PASS');count+=1
if count!=3:raise SystemExit('Expected three recorded captures')
print('Snapshot integrity and3 old-report replays PASS; new DUT/hardware runs=0')
