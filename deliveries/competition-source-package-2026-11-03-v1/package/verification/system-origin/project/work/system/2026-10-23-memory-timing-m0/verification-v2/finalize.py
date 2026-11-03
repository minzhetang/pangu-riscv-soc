from pathlib import Path
import datetime,json,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import run_v2 as v
v.verify()
ROOT=HERE.parents[3]
rows=[]
for line in (HERE/'SHA256SUMS.txt').read_text(encoding='utf-8-sig').splitlines():
    if not line.strip():continue
    expected,name=line.split(maxsplit=1)
    assert v.old.sha(name)==expected.upper(),name
    rows.append(name)
for name in ['CURRENT.md','INDEX.md','DECISIONS.md','FACTS.md','TODO.md','COLLABORATION.md']:
    text=(ROOT/'.project-memory'/name).read_text(encoding='utf-8-sig')
    assert 'F129' in text or 'F-129' in text,name
    assert 'D117' in text or 'D-117' in text,name
report=ROOT/'reports/verification/2026-10-23-memory-timing-m0-v2.md'
result=dict(date_beijing=datetime.datetime.now().astimezone().isoformat(),
    frozen_inputs=v.verify(),artifact_checks=len(rows),
    status='E1_LIMITED_CHARACTERIZATION_COMPLETE_E2_NOT_APPROVED',
    no_CPU_source_edits=True,original_inputs_and_expectations_unchanged=True,
    report_sha256=v.old.sha(report),hardware='STOP',next_scope='A-MEM-ADAPT-M1_PROPOSED_ONLY')
v.save('postflight.json',result)
print(json.dumps(result,ensure_ascii=False))
