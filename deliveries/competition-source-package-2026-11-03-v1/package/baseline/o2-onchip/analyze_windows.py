"""Analysis of real WDF samples. No simulation, DUT forcing or retirement claims."""
from pathlib import Path
import json, hashlib, importlib.util, csv, collections, sys
H=Path(__file__).resolve().parent
PC='soc/cpu_core/id_pc'; VALID='soc/cpu_core/id_valid'; ADV='soc/cpu_core/pipeline_advance'
HOLD='soc/cpu_core/eei_hold'; STALL='soc/cpu_core/stall_if'; FLUSH='soc/cpu_core/flush_id'
TAKEN='soc/cpu_core/branch_taken'; RESET='sys_rst_n'; TICK='soc/timer_ticks'
def need(v,m):
    if not v:raise ValueError(m)
def sext(v,bits):return (v^(1<<(bits-1)))-(1<<(bits-1))
def inst_at(program,pc):
    need(pc%4==0 and 0<=pc<=len(program)-4,'Active EX PC outside frozen image/alignment')
    return int.from_bytes(program[pc:pc+4],'little')
def srcs(w):
    op=w&127
    return ([w>>15&31] if op in [0x33,0x13,0x03,0x23,0x63,0x67] else [])+([w>>20&31] if op in [0x33,0x23,0x63] else [])
def direct_target(pc,w):
    op=w&127
    if op==0x63:
        imm=((w>>31&1)<<12)|((w>>7&1)<<11)|((w>>25&63)<<5)|((w>>8&15)<<1)
        return (pc+sext(imm,13))&0xffffffff
    if op==0x6f:
        imm=((w>>31&1)<<20)|((w>>12&255)<<12)|((w>>20&1)<<11)|((w>>21&1023)<<1)
        return (pc+sext(imm,21))&0xffffffff
    return None

def analyze(rows,program,functions,case,roi):
    need(len(rows)>=8,'Insufficient samples')
    need(all(r[RESET]==1 and r[HOLD]==0 and r['write_error']==0 for r in rows),'Reset/hold/write_error in algorithm window')
    need(all(((b[TICK]-a[TICK])&0xffffffff)==1 for a,b in zip(rows,rows[1:])),'Timer sample continuity')
    need(all(a[ADV]!=b[ADV] for a,b in zip(rows,rows[1:])),'Two-edge phase alternation')
    trigger=[r['sample'] for r in rows if r[PC]==case['pc'] and r[VALID] and r[ADV] and not r[HOLD] and r[RESET]]
    need(case['trigger_position'] in trigger,'Expected trigger point not observed; preserve original index')
    logical=[r for r in rows if r[ADV]]
    selected=[r for r in logical if roi[0]<r[TICK]<=roi[1]]
    active=[r for r in selected if r[VALID]]
    need(len(active)>0,'No active timed-window EX events')
    for r in active:inst_at(program,r[PC])
    owner=lambda pc:next((f['name'] for f in functions if f['pc']<=pc<f['pc']+f['bytes']),'UNCLASSIFIED')
    fn=collections.Counter(owner(r[PC]) for r in active)
    needs=[];flushes=[];checks=[];writes=[]
    for r in rows:
        if r['soc/wren']:
            writes.append(dict(sample=r['sample'],address=r['soc/address'],wdata=r['soc/wdata'],phase=r[ADV],timer=r[TICK],concurrent_EX_PC_not_store_origin=r[PC]))
    for i,r in enumerate(logical):
        if not (roi[0]<r[TICK]<=roi[1] and r[VALID]):continue
        w=inst_at(program,r[PC]);op=w&127
        need(not(r[STALL] and r[FLUSH]),'Unexpected simultaneous stall/flush')
        if r[STALL]:
            need(op==3 and (w>>7&31)!=0,'Stall without nonzero-rd EX load')
            e=dict(sample=r['sample'],pc=r[PC],rd=w>>7&31,fully_observed=i+2<len(logical))
            if e['fully_observed']:
                nxt=logical[i+1:i+3]
                need(nxt[0][VALID]==0 and nxt[1][VALID]==1,'Load-use one-bubble relation')
                cw=inst_at(program,nxt[1][PC]);need(e['rd'] in srcs(cw),'Load-use consumer source dependency')
                e.update(bubble_sample=nxt[0]['sample'],consumer_pc=nxt[1][PC],consumer_word=f'{cw:08x}')
            needs.append(e)
        if r[FLUSH]:
            need(op in [0x63,0x6f,0x67],'Flush without branch/jump EX opcode')
            if op==0x63:need(r[TAKEN]==1,'Branch flush without taken flag')
            else:need(r[TAKEN]==0,'Jump incorrectly labelled conditional branch')
            e=dict(sample=r['sample'],pc=r[PC],word=f'{w:08x}',kind='branch' if op==0x63 else 'jal' if op==0x6f else 'jalr',fully_observed=i+3<len(logical))
            if e['fully_observed']:
                nxt=logical[i+1:i+4];need([r[VALID] for r in nxt]==[0,0,1],'Control redirect two-bubble relation')
                target=direct_target(r[PC],w)
                if target is not None:need(nxt[2][PC]==target,'Direct branch/JAL target mismatch')
                e.update(bubble_samples=[nxt[0]['sample'],nxt[1]['sample']],next_valid_pc=nxt[2][PC],static_target=target,JALR_target_not_reconstructed=target is None)
            flushes.append(e)
    ticks=[r for r in rows if roi[0]<r[TICK]<=roi[1]]
    result=dict(samples=len(rows),nominal_clock_hz=27000000,ROI_physical_samples=len(ticks),logical_slots=len(selected),active_EX_events=len(active),invalid_EX_slots=sum(not r[VALID] for r in selected),EX_events_per_logical_slot=len(active)/len(selected),EX_events_per_physical_sample=len(active)/len(ticks),qualified_load_use_stalls=len(needs),qualified_control_flushes=len(flushes),function_EX_event_counts=dict(fn),function_counts_are_not_time_fraction=True,load_use_events=needs,control_flow_events=flushes,ordered_observed_writes=writes,EX_sample_indices=[r['sample'] for r in active],EX_intervals_physical_samples=dict(collections.Counter(b['sample']-a['sample'] for a,b in zip(active,active[1:]))),trigger_predicate_sample_indices=trigger,trigger_position=case['trigger_position'],all_signal_planes_binary=True,timer_adjacent_delta=1,phase_alternates=True,not_retirement_IPC=True,no_unified_commit_trace=True,JALR_full_target_and_data_forwarding_values_not_observed=True)
    need(result['active_EX_events']+result['invalid_EX_slots']==result['logical_slots'],'Slot accounting')
    return result

def run_case(caseid,rawpath):
    plan=json.loads((H/'WINDOW_PLAN_V2.json').read_text());case=next(c for c in plan['cases'] if c['id']==caseid)
    spec=importlib.util.spec_from_file_location('current_wdf',H/'read_wdf_current.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    raw=Path(rawpath);rows=m.decode(raw.read_bytes(),(H/'runtime-debug.fic').read_bytes());result=analyze(rows,(H/'firmware/program.bin').read_bytes(),json.loads((H/'ELF_FUNCTIONS.json').read_text()),case,plan['timer_ROI_preedge'])
    result.update(case=caseid,source='NEW_REAL_FPGA_WDF',wdf=str(raw),wdf_sha256=hashlib.sha256(raw.read_bytes()).hexdigest().upper(),limitations=plan['limitations'])
    with raw.with_suffix('.csv').open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    with raw.with_suffix('.analysis.json').open('x') as f:json.dump(result,f,indent=2)
    # Display scale is nominal only. Data are real sampled FPGA values, not RTL simulation.
    with raw.with_suffix('.vcd').open('x') as f:
        f.write('$comment Real FPGA WDF '+result['wdf_sha256']+'; nominal27MHz display scaling only $end\n$timescale 1ps $end\n$scope module FPGA $end\n')
        for i,(name,width) in enumerate(m.WIDTHS):f.write(f'$var wire {width} s{i} {name.replace("/","_")} $end\n')
        f.write('$upscope $end\n$enddefinitions $end\n')
        for r in rows:
            f.write('#'+str(round(r['sample']*1000000000000/27000000))+'\n')
            for i,(name,width) in enumerate(m.WIDTHS):f.write(f'b{r[name]:0{width}b} s{i}\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['load_use_events','control_flow_events','ordered_observed_writes','EX_sample_indices','trigger_predicate_sample_indices','limitations']}),flush=True)
if __name__=='__main__':run_case(*sys.argv[1:])
