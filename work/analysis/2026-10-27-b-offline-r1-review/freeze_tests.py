from pathlib import Path
import json,shutil,hashlib
P=Path('D:/A_FPGA_Comp');H=P/'work/analysis/2026-10-27-b-offline-r1-review';B=P/'队员成果接收/B-VERIFY-OFFLINE-M0-return-v02'
shutil.copytree(B,H/'tool-copy');(H/'outputs').mkdir();(H/'cases').mkdir();(H/'logs').mkdir();(H/'fixtures').mkdir()
p=json.loads((B/'tests/PLAN.json').read_text(encoding='utf-8-sig'));selected=[]
for x in p['cases']:
 if x['id'].startswith(('P01-','P02-','C0-','C1-','C2-')) or x['id'] in ['R1-RESULT-ENOUGH','R1-LOG-FLOOD','R1-WORKER-RC','R1-MISSING-RESULT','R1-PASS-TEXT']:
  selected.append(dict(id=x['id'],kind='CLI',expected=x['expected'],fixture_worker=x.get('fixture_worker'),case=x.get('case')))
selected += [dict(id='C3-O-protected',kind='protected',expected=dict(rc=3,no_tree_changes=True)),dict(id='C3-OO-protected',kind='protected',expected=dict(rc=3,no_tree_changes=True)),dict(id='invalid-JSON-protected',kind='protected',expected=dict(rc=7,no_tree_changes=True)),dict(id='oversized-CASE',kind='input',expected=dict(rc=3,no_output=True)),dict(id='active-memory-guard',kind='resource_fixture_internal',expected=dict(active_kill=True,rc=5,cap_bytes=16777216,allocation_bytes=33554432)),dict(id='main-deadline',kind='resource_fixture_internal',expected=dict(main_seconds=1,cleanup_seconds=1,kill_called_by_seconds=1.1,total_by_seconds=2.1,rc=6))]
plan=dict(stage='A independent B-R1 scoped review',date='2026-10-27',source_manifest_SHA256=hashlib.sha256((B/'SHA256SUMS.txt').read_bytes()).hexdigest().upper(),frozen_before_execution=True,scope='Host only; no B code/model/expected edits, no DUT/CPU/ISA/PDS/hardware',per_CLI_seconds=120,stage_seconds=900,parent_working_set_cap=536870912,log_cap=8388608,cases=selected,not_run=['B whole54 suite or fresh128MiB stress; targeted P0 failures suffice to withhold production acceptance'])
(H/'FROZEN_PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Frozen',len(selected),'bounded independent cases; all B original bytes retained')
