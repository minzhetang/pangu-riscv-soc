"""Comparable short-window compiler experiment, actual new evidence only."""
from pathlib import Path
from bisect import bisect_right
from collections import Counter
import json,re,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_coremark as s
def analyze():
    assert s.read(H/'simulation-result.json')['status']=='PASS';rows=[]
    for name in ['performance','validation']:
        tid=name+'-N234';d=H/'runs'/tid;before=s.read(s.B/'runs'/tid/'check-result.json');after=s.read(d/'check-result.json')
        assert before['status']==after['status']=='PASS'
        a=next(a for a in s.read(H/'build-result.json')['artifacts'] if a['id']==name)
        original=next(a for a in s.read(s.T/'build-result.json')['artifacts'] if a['id']==name)
        b=before['detail'];c=after['detail'];start,end=c['stamps'][2:];groups=Counter();functions=Counter();minimum=0x18000;sp_updates=0
        image=(H/'build'/name/'program.bin').read_bytes();dis=s.log(H/'logs'/('build-'+name+'-objdump')/'stdout.log')
        boundaries=sorted((int(pc,16),fn) for pc,fn in re.findall(r'^([0-9a-f]+) <([^>]+)>:',dis,re.M));starts=[x[0] for x in boundaries]
        nops=0
        with (d/'trace.log').open(encoding='ascii') as f:
            for line in f:
                p=line.strip().split('|')
                if p[0]=='WB' and p[2]=='2':
                    sp=int(p[3],16);assert 0x16000<=sp<=0x18000,('stack range',sp);minimum=min(minimum,sp);sp_updates+=1
                if p[0]=='EX' and start+1<int(p[1])<=end+1:
                    pc=int(p[2],16);word=int.from_bytes(image[pc:pc+4],'little');op=word&127
                    groups[{3:'LOAD',0x23:'STORE',0x63:'BRANCH',0x6f:'JAL',0x67:'JALR',0x33:'ALU_R',0x13:'ALU_I',0x37:'LUI',0x17:'AUIPC'}.get(op,'OTHER')]+=1
                    i=bisect_right(starts,pc)-1;functions[boundaries[i][1] if i>=0 else 'UNKNOWN']+=1
                    nops+=word==0x13
        assert sp_updates>0
        assert (H/'firmware/start.S').read_bytes()==(H/'firmware-before/start.S').read_bytes()
        assert s.sha(H/'tests/tb_board_coremark.sv')==s.sha(s.B/'tests/tb_board_coremark.sv')
        row=dict(id=tid,status='PASS_SHORT_COMPARABLE_EXPERIMENT',O2_ticks=b['raw_ticks'],O3_ticks=c['raw_ticks'],
            tick_reduction=(b['raw_ticks']-c['raw_ticks'])/b['raw_ticks'],speedup=b['raw_ticks']/c['raw_ticks'],
            compute_benefit=c['raw_ticks']<b['raw_ticks'],O2_bytes=original['bytes'],O3_bytes=a['bytes'],bytes_delta=a['bytes']-original['bytes'],
            O2_empty_window=b['empty_window'],O3_empty_window=c['empty_window'],empty_cost_subtracted=False,
            formatting_ticks_O2=b['phases'][3][0]-b['stamps'][3],formatting_ticks_O3=c['phases'][3][0]-end,
            UART_phase_ticks_O2=b['phases'][4][0]-b['phases'][3][0],UART_phase_ticks_O3=c['phases'][4][0]-c['phases'][3][0],
            UART_bytes_O2=before['UART_frames'],UART_bytes_O3=after['UART_frames'],
            stack_min_SP=minimum,observed_stack_depth=0x18000-minimum,reserved_stack=8192,remaining_to_stack_bottom=minimum-0x16000,SP_WB_checked=sp_updates,
            total_metrics=after['metrics'],window_EX_groups=dict(groups),top_function_EX_observations=functions.most_common(12),window_architectural_nops=nops,
            caveats=['finite seeds/one iteration, not official score or hardware','SP minimum is observed finite execution, not static worst-case proof','EX is not true retirement; WB/MEM separately ordered','changed image addresses/layout mean old full RF/RAM/PC equality is not a valid expectation','no UART speed change; report metadata/timestamps may differ','compiler optimization is not architecture innovation'])
        rows.append(row)
    result=dict(status='PASS_ANALYSIS_NOT_HARDWARE',rows=rows,all_seeds_benefit=all(r['compute_benefit'] for r in rows),
        decision='PDS_CANDIDATE_COST_CHECK_ELIGIBLE' if all(r['compute_benefit'] for r in rows) else 'STOP_O3_KEEP_O2_NO_PDS',new_DUT_runs=0,protected=s.protect())
    s.save(H/'quality-compare.json',result);print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':analyze()
