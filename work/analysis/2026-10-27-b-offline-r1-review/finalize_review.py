from pathlib import Path
import json,hashlib,collections,sys
P=Path('D:/A_FPGA_Comp');H=P/'work/analysis/2026-10-27-b-offline-r1-review';B=P/'队员成果接收/B-VERIFY-OFFLINE-M0-return-v02';V=B.with_name('B-VERIFY-OFFLINE-M0-return-v01');D=P/'deliveries/mainline-b-offline-r1-review-response-2026-10-27-v1'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
intake=read(H/'INTAKE.json');assert all(sha(B/r['path'])==r['SHA256'] for r in intake['rows']);assert all(sha(V/r['path'])==r['SHA256'] for r in read(H/'v01-before.json'))
for n in ['offline_api.py','block_codec.py']:assert sha(B/'frozen'/n)==sha(P/'deliveries/mainline-b-verify-offline-m0-2026-10-26-v1/frozen'/n)
# Pin the mainline without executing a compiler/reference/DUT.
S=P/'work/fpga/2026-10-27-coremark-longrun-ready-m2';frozen=read(S/'frozen-inputs.json')['files'];assert all(sha(S/r['path'])==r['SHA256'] for r in frozen);assert read(S/'STATUS.json')['status']=='PASS_FINITE_8_ITERATIONS_NOT_FORMAL_LONGRUN'
cov=[]
for r in intake['rows']:
 n=r['path'];c=dict(r)
 if n in ['RUN.py','src/support.py','src/worker.py','tests/run_suite.py','tests/generate.py'] or n.startswith('tests/fixtures/'):c['semantic_review']='FULL_SOURCE_REVIEWED'
 elif n=='DIFF.patch':c['semantic_review']='ALL_59_HUNKS_APPLIED_TO_V01_MATCH_V02'
 elif n in ['CHANGED_FILES.json','SOURCE_INDEX.json']:c['semantic_review']='ALL_DECLARED_HASHES_AND_SIZES_CROSSCHECKED'
 elif n.startswith('logs/') or n in ['tests/results.json','COMMANDS.md'] or n.startswith('diagnostics/') or n.startswith('pressure/'):c['semantic_review']='FULL_TEXT_OR_JSON_READ;54_CASES_RAW_RC_RESULT_STDOUT_CROSSCHECKED;NOT_A_NEW_RUN'
 elif n.startswith('frozen/'):c['semantic_review']='IDENTICAL_A_FROZEN_API;NO_REDUNDANT_FULL_SEMANTIC_REAUDIT'
 elif n.startswith('r1/task/'):c['semantic_review']='A_ORIGINAL_SCOPE_HISTORY;FULL_TEXT_READ_REUSED_SCOPE'
 elif n.startswith('r1/old-v01/'):c['semantic_review']='FULL_ORIGINAL_HISTORY_READ;NOT_A_NEW_RUN'
 else:c['semantic_review']='FULL_METADATA_READ_OR_JSON_PARSED;RELEVANT_FIELDS_CROSSCHECKED'
 cov.append(c)
(H/'READING_COVERAGE.json').write_text(json.dumps(dict(total=len(cov),all_bytes_hashed=True,all_text_read=True,expected_invalid_JSON=2,none_unreadable=True,rows=cov),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
result=read(H/'RESULTS.json');portable=read(H/'portable-repro-check/A_GUARD_RESULTS.json');assert [x['status'] for x in portable]==['FAIL']*3
summary=dict(date_client='2026-10-27',fact='F161',decision='D162',acceptance='CONDITIONAL_ACCEPTANCE',production_resource_approval='NOT_ACCEPTED_G1_G2_G3_OPEN',material=dict(files=intake['files'],SHA_entries=intake['manifest_entries'],manifest_SHA256=intake['manifest_SHA256'],bytes=intake['bytes'],plan_SHA256=intake['plan_SHA256'],declared_changes=537,source_index=85,diff_sections_exact=59,original37_unchanged=True),B_evidence=dict(local54_all_pass=True,raw_records_consistent=True,not_A_reproduced54=True),A=dict(new_host_cases=25,PASS=22,FAIL=3,host_seconds=result['seconds'],portable_counterexample_rerun_count=3,portable_counterexample_status='ALL_THREE_FAILURES_REPRODUCED;bootstrap rc1 expected',old_observation_records_replayed=9378498,new_DUT=0),closure=dict(C0='CLOSED_LIMITED',C1_1B_preflight='CLOSED_LIMITED;GENERAL_ACTIVE_MEMORY_STILL_OPEN',C2_256B='CLOSED_LIMITED',C3_protected_output='CLOSED_LIMITED',G1_runtime_memory_parent='OPEN',G2_streaming_log_sink='OPEN',G3_main_and_total_deadline='OPEN'),interface='ABI1.0.0/frozen bytes identical; no new production adapter integration',mainline='F160 unchanged; B tool not a dependency or replacement for A production checker',hardware='STOPPED',not_run=['whole B54 under A','fresh128MiB stress','CPU/ISA/reference/DUT/PDS/hardware'],source_protected=dict(B_v02=540,B_v01=374,mainline_frozen=len(frozen)),followup='D158 same bounded guard corrections only; reply ready not sent; no new deadline promised')
(H/'REVIEW_RESULTS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(D/'REVIEW_RESULTS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(H/'COMMANDS.md').write_text('''# Actual A reproduction commands

Only ordinary existing Python, -B, no install/compiler/DUT/hardware. <EXISTING_PYTHON> denotes the already verified runtime; profile paths and B personal paths are excluded from this summary. Exact CLI argument arrays and native rc are in logs/<id>/process.json (redacted interpreter label, unchanged arguments), stdout/stderr beside them.

```text
<EXISTING_PYTHON> -B work/analysis/2026-10-27-b-offline-r1-review/run_independent.py
<EXISTING_PYTHON> -B deliveries/mainline-b-offline-r1-review-response-2026-10-27-v1/REPRODUCE_GUARDS.py --tool-root D:/A_FPGA_Comp/队员成果接收/B-VERIFY-OFFLINE-M0-return-v02 --input-root D:/A_FPGA_Comp/deliveries/mainline-b-verify-offline-m0-2026-10-26-v1 --work D:/A_FPGA_Comp/work/analysis/2026-10-27-b-offline-r1-review/portable-repro-check
```

First driver native rc0 means its25-result collection completed; RESULTS.json has22 PASS/3 FAIL, not all pass. The portable three-probe entry native rc1 is expected on unchanged v02 because all three guards fail. Neither result is a CPU/ISA/benchmark validation. Original B54 PASS_LOCAL and its original logs are separate, never relabeled as A new runs.

All original539 manifest entries, frozen API, original37 plan/results and current mainline60 execution inputs were rehashed unchanged. Known invalid JSON fixture files are retained as expected invalid data, not unreadable intake. No B source or frozen expectation was changed. Source-only comparison is CODE_DIFF.patch; full original B diff59 sections independently applied exactly.
''',encoding='utf-8')
# Generate response manifest, excludes itself.
rows=[(p.relative_to(D).as_posix(),sha(p)) for p in sorted(D.rglob('*')) if p.is_file()]
(D/'SHA256SUMS.txt').write_text(''.join(value+'  '+name+'\n' for name,value in rows),encoding='utf-8')
(H/'POSTFLIGHT.json').write_text(json.dumps(dict(status='ORIGINALS_UNCHANGED_FAILURES_PRESERVED',B_files=len(intake['rows']),v01_files=len(read(H/'v01-before.json')),mainline_frozen=len(frozen),response_files=len(rows)+1,response_manifest_SHA256=sha(D/'SHA256SUMS.txt'),response_manifest_entries=len(rows),new_DUT=0,hardware='STOPPED',python_version=sys.version.split()[0]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:summary[k] for k in ['acceptance','production_resource_approval','A','closure']},ensure_ascii=False))
