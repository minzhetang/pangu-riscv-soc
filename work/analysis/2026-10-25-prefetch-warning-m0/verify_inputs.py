"""Read-only end-of-analysis input and verdict check, zero tool executions."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent;P=Path('D:/A_FPGA_Comp')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
i=load(H/'INPUTS.json');checked=[]
for row in i['source']+i['pds_inventory']+i['help']:
    p=Path(row['path']);assert sha(p)==row['SHA256'];checked.append(str(p))
library={}
for p in H.glob('*-graph*.json'):
    g=load(p);assert sha(Path(g['path']))==g['SHA256'] and g['unsupported_syntax_skipped']==0
    for v in g['library'].values():library[v['path']]=v['SHA256']
    if 'constrained' in p.name:assert g['graph']['acyclic'] and g['with_async_FF_control_arcs']['acyclic']
for p,expected in library.items():assert sha(Path(p))==expected
r=P/'reports/verification/2026-10-25-prefetch-warning-m0.md'
out=dict(status='READ_ONLY_REVIEW_COMPLETE_ROOT_CAUSE_OPEN',source_and_PDS_help_inputs=len(checked),source_files=len(i['source']),primitive_models=len(library),all_input_hashes_unchanged=True,report_SHA256=sha(r),SUMMARY_SHA256=sha(H/'SUMMARY.json'),warning_count=dict(old=7,new=8),candidate_promoted=False,stable_baseline='F143 O2',new_compiler_runs=0,new_DUT_runs=0,new_PDS_runs=0,hardware='STOPPED')
with (H/'postflight.json').open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(out))
