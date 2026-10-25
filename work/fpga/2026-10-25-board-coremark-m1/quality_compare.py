"""Compare new actual compute windows with F136; no replay/DUT or optimization."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_coremark as s
def window(path,start,end):
    digest=hashlib.sha256();counts=Counter()
    with path.open(encoding='ascii') as f:
        for line in f:
            a=line.strip().split('|');c=int(a[1])
            if start+1<c<=end+1:
                digest.update(('|'.join(a)+'\n').encode('ascii'));counts[a[0]]+=1
    return dict(sha256=digest.hexdigest().upper(),event_counts=dict(counts))
def analyze():
    assert s.read(H/'simulation-result.json')['status']=='PASS'
    old_analysis=s.read(s.T/'quality-window-analysis.json');rows=[]
    for tid,plan in s.read(H/'frozen-case-plan.json')['cases'].items():
        name=tid.split('-N')[0];d=H/'runs'/tid;new=s.read(d/'check-result.json');old=s.read(Path(plan['old_run'])/'check-result-v2.json')
        assert new['status']==old['status']=='PASS'
        start,end=new['detail']['stamps'][2:];before=window(Path(plan['old_run'])/'trace.log',*old['detail']['stamps'][2:]);now=window(d/'trace.log',start,end)
        assert before==now,'compute-window event/time differs from prior baseline'
        classification=next(r for r in old_analysis['rows'] if r['program']==name)
        assert now['event_counts']['EX']==classification['window_EX_observations'] and end-start==classification['raw_physical_ticks']
        parts={k:classification[k] for k in ['fixed_two_clock_EX_component','fixed_two_clock_load_use_component','fixed_two_stage_redirect_component','boundary_residual']}
        assert parts['boundary_residual']==0 and sum(parts.values())==end-start
        np=new['detail']['phases'];op=old['detail']['phases']
        assert [v for c,v in np]==[0,1,2,3,4]
        row=dict(program=name,status='PASS_IDENTICAL_COMPUTE_WINDOW',raw_ticks_new=end-start,raw_ticks_old=old['detail']['raw_ticks'],
            actual_speedup=1.0,optimized=False,window=now,
            old_classification_reused_only_after_identical_actual_window=True,parts=parts,
            component_fraction={k:v/(end-start) for k,v in parts.items() if k!='boundary_residual'},
            soft_multiply_hotspot=next((dict(function=f,EX_observations=n) for f,n in classification['top_function_EX_observations'] if f=='__mulsi3'),None),
            formatting_ticks_new=np[3][0]-end,formatting_ticks_old=op[3][0]-old['detail']['stamps'][3],
            output_phase_ticks_new=np[4][0]-np[3][0],output_phase_ticks_old=op[4][0]-op[3][0],
            full_physical_ticks_new=new['metrics']['physical'],full_physical_ticks_old=old['metrics']['physical'],
            UART_bytes_new=new['UART_frames'],UART_bytes_old=old['UART_frames'],
            final_state_byte_equal_to_old={f:s.sha(d/f)==s.sha(Path(plan['old_run'])/f) for f in ['registers.hex','ram.hex']},
            limitation='classification is the earlier validated reference under an identical new observed window, not new full-wave bubble audit/retired CPI; frequency remains nominal, no formal score')
        rows.append(row)
    result=dict(status='PASS_ANALYSIS_ONLY',rows=rows,new_DUT_runs=0,algorithm_or_RTL_changes=0,
        recommendation='quality work should use comparable compute ticks, correctness, code size and mapped timing/resources; UART wait must be separated, no automatic M/cache/prediction expansion',
        protected=s.protect())
    s.save(H/'quality-compare.json',result)
    print(json.dumps(rows,ensure_ascii=False))
if __name__=='__main__':analyze()
