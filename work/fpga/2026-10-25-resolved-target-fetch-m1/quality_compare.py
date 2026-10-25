"""Same image/workload old/new calculation windows; 0 new reference/DUT runs."""
from pathlib import Path
import hashlib,json,sys
from collections import Counter
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_redirect as s
def collect(trace,image,start,end):
    digest=hashlib.sha256();counts=Counter();previous=None;loaduse=0;EX=0
    with trace.open(encoding='ascii') as f:
        for line in f:
            a=line.strip().split('|');cy=int(a[1])
            if start+1<cy<=end+1:counts[a[0]]+=1
            if a[0]!='EX':continue
            pc=int(a[2],16)
            if previous:
                c,p=previous
                if start+1<c<=end+1:
                    op=int.from_bytes(image[p:p+4],'little')&127
                    if op==3 and cy-c==4:loaduse+=1
            if start+1<cy<=end+1:digest.update((a[2]+'\n').encode('ascii'));EX+=1
            previous=(cy,pc)
    return dict(EX=EX,load_use=loaduse,EX_PC_SHA256=digest.hexdigest().upper(),counts=dict(counts))
def main():
    assert s.read(H/'core-result.json')['status']=='PASS';rows=[]
    for name in ['performance','validation']:
        tid=name+'-N234';old=s.read(s.B/'runs'/tid/'check-result.json');new=s.read(H/'runs'/tid/'check-result.json')
        image=(H/'build'/name/'program.bin').read_bytes();assert image==(s.B/'build'/name/'program.bin').read_bytes()
        before=collect(s.B/'runs'/tid/'trace.log',image,*old['detail']['stamps'][2:]);after=collect(H/'runs'/tid/'trace.log',image,*new['detail']['stamps'][2:])
        assert (before['EX'],before['load_use'],before['EX_PC_SHA256'])==(after['EX'],after['load_use'],after['EX_PC_SHA256'])
        start,end=new['detail']['stamps'][2:];redirects=hits=0
        for line in (H/'runs'/tid/'fetch.log').open(encoding='ascii'):
            a=line.split('|')
            if a[0]=='REDIR' and start+1<int(a[1])<=end+1:redirects+=1;hits+=int(a[4])
        old_class=next(r for r in s.read(s.T/'quality-window-analysis.json')['rows'] if r['program']==name)
        assert redirects==hits==old_class['reference_redirect']
        parts=dict(EX=2*after['EX'],load_use=2*after['load_use'],redirects=4*redirects-2*hits)
        assert sum(parts.values())==new['detail']['raw_ticks']
        a=old['detail'];b=new['detail'];saving=a['raw_ticks']-b['raw_ticks'];assert saving==2*hits
        # Main and stack return remain checked against the independent ISA model.
        minimum=0x18000
        for line in (H/'runs'/tid/'trace.log').open(encoding='ascii'):
            p=line.split('|')
            if p[0]=='WB' and p[2]=='2':v=int(p[3],16);assert 0x16000<=v<=0x18000;minimum=min(minimum,v)
        rows.append(dict(id=tid,status='PASS_FINITE_COMPARABLE_BENEFIT',O2_before_ticks=a['raw_ticks'],O2_candidate_ticks=b['raw_ticks'],ticks_saved=saving,
            time_reduction=saving/a['raw_ticks'],speedup=a['raw_ticks']/b['raw_ticks'],compute_benefit=saving>0,unchanged_image_SHA256=s.sha(H/'build'/name/'program.bin'),
            program_bytes=len(image),same_workload_EX_sequence=True,window_EX_PC_SHA256=after['EX_PC_SHA256'],window_EX=after['EX'],window_load_use=after['load_use'],window_redirects=redirects,window_hits=hits,
            physical_window_parts=parts,boundary_residual=0,old_window_counts=before['counts'],new_window_counts=after['counts'],
            empty_window_before=a['empty_window'],empty_window_after=b['empty_window'],empty_subtracted=False,
            formatting_ticks_before=a['phases'][3][0]-a['stamps'][3],formatting_ticks_after=b['phases'][3][0]-b['stamps'][3],
            UART_phase_ticks_before=a['phases'][4][0]-a['phases'][3][0],UART_phase_ticks_after=b['phases'][4][0]-b['phases'][3][0],
            UART_bytes_before=old['UART_frames'],UART_bytes_after=new['UART_frames'],minimum_SP=minimum,observed_stack_depth=0x18000-minimum,
            whole_metrics_before=old['metrics'],whole_metrics_after=new['metrics'],formal_score=False,
            caveat='finite simulation tick benefit at same nominal clock; no hardware/Fmax/energy or novelty claim; host runtime and UART polling are separate'))
    result=dict(status='PASS_ANALYSIS_ONLY',all_seeds_benefit=all(r['compute_benefit'] for r in rows),rows=rows,new_DUT_runs=0,new_reference_replays=0,protected=s.protect())
    s.save(H/'quality-compare.json',result);print(json.dumps(rows,ensure_ascii=False))
if __name__=='__main__':main()
