from pathlib import Path
import json,hashlib,collections,re
P=Path('D:/A_FPGA_Comp');B=P/'队员成果接收/B-VERIFY-OFFLINE-M0-return-v02';V=B.with_name('B-VERIFY-OFFLINE-M0-return-v01');H=P/'work/analysis/2026-10-27-b-offline-r1-review'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
p=read(B/'tests/PLAN.json');old=read(V/'tests/PLAN.json');r=read(B/'tests/results.json');plans={c['id']:c for c in p['cases']};declared=read(B/'CHANGED_FILES.json')['files'];mismatch=[]
for d in declared:
 if d.get('new_sha256') is not None and sha(B/d['path'])!=d['new_sha256']:mismatch.append(d['path']+' new')
 if d.get('old_sha256') is not None and (not (V/d['path']).is_file() or sha(V/d['path'])!=d['old_sha256']):mismatch.append(d['path']+' old')
for d in read(B/'SOURCE_INDEX.json')['entries']:
 if sha(B/d['path'])!=d['sha256'] or (B/d['path']).stat().st_size!=d['bytes']:mismatch.append(d['path']+' source index')
assert all(x==plans[x['id']] for x in old['cases']);assert sha(B/'tests/history/PLAN-v01.json')==sha(V/'tests/PLAN.json');assert sha(B/'tests/history/results-v01.json')==sha(V/'tests/results.json')
checks=[]
for x in r['cases']:
 cid=x['id'];e=plans[cid]['expected'];res=x.get('result',{});cmd=x.get('command');issues=[]
 if x['test_status']!='PASS':issues.append('B reported nonpass')
 if cmd is not None and cmd['rc']!=e['native_rc']:issues.append('parent native rc')
 for k in ['checked','expected_records','actual_records']:
  if k in e and res.get(k)!=e[k]:issues.append(k)
 if res.get('status')!=e['run_status']:issues.append('status')
 d=B/'logs'/cid
 if (d/'result.json').exists():
  raw=read(d/'result.json')
  for k in ['status','native_rc','checked','worker_rc','elapsed_s']:
   if raw.get(k)!=res.get(k):issues.append('raw result '+k)
 if (d/'worker-result.json').exists():
  worker=read(d/'worker-result.json')
  if res.get('worker_rc')!=worker.get('native_rc'):issues.append('worker real rc mismatch')
 if (d/'suite.stdout.log').exists() and cmd is not None:
  if (d/'suite.stdout.log').read_text(encoding='utf-8-sig')!=cmd.get('stdout',''):issues.append('original stdout differs')
 checks.append(dict(id=cid,B_status=x['test_status'],kind=plans[cid]['kind'],issues=issues))
# Read every diff hunk and match declared source changes independently.
patch=(B/'DIFF.patch').read_text(encoding='utf-8-sig');sections=re.findall(r'^diff --git a/(.+?) b/(.+)$',patch,re.M);assert all(a==b for a,b in sections)
summary=dict(status='MATERIAL_REVIEW_NOT_A_RUNTIME_PASS',original37_plan_identical=True,history_original_files_identical=True,metadata_mismatches=mismatch,source_index_entries=len(read(B/'SOURCE_INDEX.json')['entries']),changed_entries=len(declared),diff_sections=len(sections),diff_bytes=len(patch.encode()),B_results=checks,B_test_count=len(checks),B_RAW_log_inconsistencies=[x for x in checks if x['issues']],known_contract_gaps=['RUN.execute_case lacks in-loop memory threshold/fail-closed/parent budget checks','worker stdout/stderr written directly then truncated, not bounded sink','parent enforces hard_deadline after cleanup instead of main deadline, then fresh waits','R1-TIMEOUT frozen max_elapsed2.6 exceeds authorized total2+0.1 observation tolerance'])
(H/'MATERIAL_AUDIT.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k!='B_results'},ensure_ascii=False))
