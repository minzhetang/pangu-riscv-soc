"""Replays already-validated reference for timer-window classification; 0 DUT runs.
EX timestamp is an observation point, not a real retirement interface.
"""
from pathlib import Path
from collections import Counter
from bisect import bisect_right
import sys,re,json
sys.dont_write_bytecode=True
import run_stage as s
import check_timed_v2 as ck
from cpu_program_reference import Reference as Base
H=Path(__file__).resolve().parent
def analyze(name):
    tid=name+'-N16';d=H/'runs'/tid;result=s.read(d/'check-result-v2.json');assert result['status']=='PASS'
    start,end=result['detail']['stamps'][2:];cycles=[]
    with (d/'trace.log').open() as f:
        for line in f:
            if line.startswith('EX|'):cycles.append(int(line.split('|',2)[1]))
    dis=s.log(H/'logs'/('build-'+name+'-objdump')/'stdout.log')
    functions=sorted((int(a,16),b) for a,b in re.findall(r'^([0-9a-f]+) <([^>]+)>:',dis,re.M))
    starts=[a for a,b in functions];by_fn=Counter();by_op=Counter();counts=Counter()
    class Profile(Base):
        def step(self):
            old_steps=self.steps;old_stall=self.stall;old_flush=self.flush;pc=self.pc
            super().step()
            if self.steps==old_steps:return
            c=cycles[old_steps]
            if start+1<c<=end+1:
                counts['EX']+=1;counts['load_use']=self.stall-old_stall+counts['load_use'];counts['redirect']=self.flush-old_flush+counts['redirect']
                word=int.from_bytes(self.rom[pc:pc+4],'little');op=word&127
                by_op[{3:'LOAD',0x23:'STORE',0x63:'BRANCH',0x6f:'JAL',0x67:'JALR',0x33:'ALU_R',0x13:'ALU_I',0x37:'LUI',0x17:'AUIPC'}.get(op,'OTHER')]+=1
                i=bisect_right(starts,pc)-1;by_fn[functions[i][1] if i>=0 else 'UNKNOWN']+=1
    ck.Reference=Profile
    try:replay=ck.check(tid)
    finally:ck.Reference=Base
    assert replay['status']=='PASS' and replay['streams']==result['streams']
    raw=end-start
    return dict(program=name,window_start_tick=start,window_end_tick=end,raw_physical_ticks=raw,
        minimum_empty_read_window=result['detail']['empty_window'],window_EX_observations=counts['EX'],
        reference_load_use=counts['load_use'],reference_redirect=counts['redirect'],
        fixed_two_clock_EX_component=2*counts['EX'],fixed_two_clock_load_use_component=2*counts['load_use'],
        fixed_two_stage_redirect_component=4*counts['redirect'],
        boundary_residual=raw-2*counts['EX']-2*counts['load_use']-4*counts['redirect'],
        instruction_groups=dict(by_op),top_function_EX_observations=by_fn.most_common(12),
        non_compute_intervals=dict(reset_release_to_start_sample=start,
            stop_sample_to_UART_phase=result['detail']['phases'][3][0]-end,
            UART_phase_to_finished=result['detail']['phases'][4][0]-result['detail']['phases'][3][0]),
        correct_replay=True,new_DUT_runs=0,
        limitations=['not retired CPI; reference classifies load-use and redirect, not independent full-wave bubble audit',
            'window includes timer-call boundary code; empty read cost is not blindly subtracted',
            'frequency setting not measured hardware frequency; no valid formal score or optimization benefit'])
if __name__=='__main__':
    rows=[analyze(n) for n in ['performance','validation']]
    s.save(H/'quality-window-analysis.json',dict(status='PASS_ANALYSIS_ONLY',rows=rows,new_DUT_runs=0));print(json.dumps(rows))
