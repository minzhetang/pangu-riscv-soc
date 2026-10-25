"""Read-only existing CoreMark artifacts and resource arithmetic; no native tools/DUT."""
from pathlib import Path
import hashlib,json,re,struct,sys,math,collections
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
P=Path('D:/A_FPGA_Comp');H=Path(__file__).resolve().parent
B=P/'work/fpga/2026-10-25-board-coremark-m1';T=P/'work/system/2026-10-24-timed-coremark-m1'
O=P/'work/system/2026-10-23-coremark-correctness-m1/upstream-direct/files'
F=27000000;CAP=256*1024*1024
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest().upper()
def save(n,o):
    with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def elf_initial_word(p,address):
    data=p.read_bytes();assert data[:7]==b'\x7fELF\x01\x01\x01'
    off=struct.unpack_from('<I',data,28)[0];size,count=struct.unpack_from('<HH',data,42)
    for i in range(count):
        typ,foff,virtual,physical,filesz,memsz,flags,align=struct.unpack_from('<8I',data,off+i*size)
        if typ==1 and virtual<=address and address+4<=virtual+filesz:
            return struct.unpack_from('<I',data,foff+address-virtual)[0]
    raise AssertionError('No initial file-backed word at '+hex(address))
def stream_partition(p,start,end):
    counts=collections.Counter();sizes=collections.Counter();h=hashlib.sha256();lines=0
    with p.open('rb') as f:
        for line in f:
            h.update(line);parts=line.split(b'|',2);assert len(parts)==3
            kind=parts[0].decode('ascii');cycle=int(parts[1]);phase='compute' if start<cycle<=end else 'outside'
            counts[phase+':'+kind]+=1;sizes[phase]+=len(line);lines+=1
    return dict(path=str(p),SHA256=h.hexdigest().upper(),bytes=p.stat().st_size,lines=lines,counts=dict(counts),bytes_by_region=dict(sizes))
def run():
    inputs=[]
    def protect(p):
        p=Path(p);inputs.append(dict(path=str(p),SHA256=sha(p)));return p
    receipts=read(protect(P/'work/analysis/2026-10-25-prefetch-warning-m0/INPUTS.json'))['source']
    assert len(receipts)==26
    for r in receipts:
        assert sha(Path(r['path']))==r['SHA256'];protect(r['path'])
    source_integrity=read(protect(P/'work/system/2026-10-23-coremark-correctness-m1/source-integrity-review.json'))
    official={Path(r['path']).name:r['sha256'] for r in source_integrity['verified_local_vs_archive']}
    for name in ['core_main.c','core_list_join.c','core_matrix.c','core_state.c','core_util.c','coremark.h']:
        assert sha(T/'upstream'/name)==sha(O/name)==official[name];protect(T/'upstream'/name);protect(O/name)
    for name in ['README.md','barebones_porting.md']:protect(O/name)
    for rel in ['port/core_portme.c','port/core_portme.h','firmware/timer.h','firmware/start.S','firmware/link.ld','check_timed_v2.py','build-result.json']:protect(T/rel)
    for rel in ['tests/tb_board_coremark.sv','stage_coremark.py','check_coremark.py','models/cpu_program_reference.py','RESULTS.json','frozen-case-plan.json']:protect(B/rel)
    protect(P/'work/fpga/2026-10-24-implementability-m0/stage.py')
    port=(T/'port/core_portme.c').read_text(encoding='utf-8-sig');hdr=(T/'port/core_portme.h').read_text(encoding='utf-8-sig');util=(T/'upstream/core_util.c').read_text(encoding='utf-8-sig')
    assert 'seed4_volatile=1' in port and not re.search(r'\bITERATIONS\b',port)
    assert 'retval = seed4_volatile;' in util and '#define SEED_METHOD SEED_VOLATILE' in hdr
    assert 'return ticks/27000000u;' in port and 'elapsed_ticks>UINT32_MAX' in port
    builds=read(T/'build-result.json')['artifacts'];rows=[];streams=[]
    for name in ['performance','validation']:
        d=B/'runs'/(name+'-N234');check=read(protect(d/'check-result.json'));proc=read(protect(d/'process.json'));assert check['status']=='PASS' and proc['returncode']==0
        art=next(r for r in builds if r['id']==name);elf=protect(B/'build'/name/'program.elf');binary=protect(B/'build'/name/'program.bin')
        assert sha(elf)==art['ELF_sha'] and sha(binary)==art['bin_sha']
        seed4=elf_initial_word(elf,art['symbols']['seed4_volatile']);assert seed4==1
        stamps=check['detail']['stamps'];raw=check['detail']['raw_ticks'];assert raw==stamps[3]-stamps[2]
        rs=[]
        for n in ['trace.log','bus.log']:
            s=stream_partition(d/n,stamps[2],stamps[3]);streams.append(s);inputs.append(dict(path=str(d/n),SHA256=s['SHA256']));rs.append(s)
        counts=collections.Counter({k.split(':',1)[1]:v for k,v in rs[0]['counts'].items() if k.startswith('compute:')})
        assert counts['EX']>0 and counts['WB']>0 and counts['READ']>0 and counts['STORE']>0
        rate=proc['elapsed_seconds']/check['metrics']['physical'];factor=10*F/raw;linear_iterations=math.ceil(factor)
        forecasts=[]
        for iterations in [2,linear_iterations,160]:
            ticks=iterations*raw;physical=check['metrics']['physical']-raw+ticks
            forecasts.append(dict(iterations=iterations,linear_compute_ticks=ticks,linear_seconds_at_nominal=ticks/F,estimated_physical=physical,estimated_DUT_host_seconds=physical*rate,artifact_bytes={Path(s['path']).name:s['bytes_by_region'].get('outside',0)+iterations*s['bytes_by_region'].get('compute',0) for s in rs},not_a_measurement=True,per_iteration_state_variation_not_calibrated=True))
        rows.append(dict(seed=name,elf_seed4_initial=seed4,raw_ticks=raw,nominal_seconds=raw/F,start=stamps[2],end=stamps[3],physical=check['metrics']['physical'],old_DUT_host_seconds=proc['elapsed_seconds'],within_window_counts=dict(counts),iteration_floor_from_single_run=linear_iterations,forecasts=forecasts))
    save('STREAM_PARTITIONS.json',dict(rows=streams,source='F143 original byte streams read once; no DUT/reference replay'))
    rules=dict(commit='1f483d5b8316753a742cbf5590caf5bd0a4e4777',source_urls=['https://github.com/eembc/coremark/blob/1f483d5b8316753a742cbf5590caf5bd0a4e4777/README.md','https://github.com/eembc/coremark/blob/1f483d5b8316753a742cbf5590caf5bd0a4e4777/barebones_porting.md'],actually_opened=True,minimum_seconds=10,required_seed_sets=['0,0,0x66','0x3415,0x3415,0x66'],data_bytes=2000,profile_seeds_only_for_PGO=True,iteration_and_port_changes_allowed=True,upstream_six_unchanged=True)
    selfchecks=[]
    for ticks,want_seconds,want_valid in [(F-1,0,False),(F,1,False),(10*F-1,9,False),(10*F,10,True),(11*F-1,10,True)]:
        got=ticks//F;assert got==want_seconds and (got>=10)==want_valid
        selfchecks.append(dict(ticks=ticks,integer_seconds=got,raw_threshold_accepts=want_valid,host_arithmetic_only=True))
    save('CALCULATOR_SELFTEST.json',dict(status='PASS',rows=selfchecks,new_DUT=0))
    findings=[dict(id='M1',status='VERIFIED_STATIC_AND_OLD_ELF',finding='seed4 is literal1 in SEED_VOLATILE path; changing only -DITERATIONS does not parameterize this port'),dict(id='M2',status='VERIFIED_STATIC',finding='time_in_secs integer division supported by HAS_FLOAT0 path but report is coarse; retain raw ticks and do exact rational host calculation separately, not a formal score'),dict(id='M3',status='VERIFIED_LIMIT',finding='64bit physical counter read, but CORE_TICKS32 and explicit UINT32_MAX delta guard limit accepted interval to <159.08s at nominal27MHz; >=10s fits, wrap path not newly proven'),dict(id='M4',status='VERIFIED_VALIDATION_COUPLING',finding='checker requires short-warning presence, exact single run/start-stop, phase and 1iteration manual plan; cannot label longer program passed without new pre-frozen oracle/iterations/finalCRC and error policy'),dict(id='M5',status='VERIFIED_BUDGET_CONFLICT',finding='6M total clocks/360s/256MiB each logs cannot be reused unchanged for >=270M compute clocks; projections conditional, no long run executed'),dict(id='M6',status='HARDWARE_STOP_RETAINED',finding='27MHz nominal constraint/config is not external time calibration; software duration cannot replace FPGA run, formal measurement or ILA')]
    save('SUMMARY.json',dict(date_beijing='2026-10-25',stage='A-COREMARK-MEASUREMENT-READINESS-M0',decision='NOT_READY_FOR_FORMAL_LONG_RUN_RECOMMEND_TWO_ITERATION_CALIBRATION',rules=rules,frequency_nominal=F,minimum_compute_ticks=10*F,current_bounds=dict(physical_cycles=6000000,host_seconds_per_case=360,each_log_bytes=CAP),MAX_CORE_TICKS_seconds=(2**32-1)/F,rows=rows,findings=findings,compile_DUT_GCC_PDS_runs=0,hardware='STOPPED',stable='F143_O2',candidate='F146_HELD',limitations=['linear forecasts are neither verified next-iteration behavior nor host runtime commitments','original EX/WB/MEM classes remain split, no actual retirementPC/unified commit','no formal score or hardware-frequency calibration','B receipt is user-reported sent; no teammate ACK inferred']))
    # Actual per-source lines for report references, not summaries from chat.
    excerpts=[]
    for rel,needles in [('port/core_portme.c',['seed4_volatile','time_in_secs','elapsed_ticks>UINT32_MAX','SIM ONLY','timing_phase=3']),('port/core_portme.h',['CORE_TICKS','HAS_FLOAT','SEED_METHOD']),('upstream/core_main.c',['res->iterations','i == 0','iterations == 0','Must execute','crcfinal']),('firmware/timer.h',['counter_read','while(a!=b)'])]:
        for i,l in enumerate((T/rel).read_text(encoding='utf-8-sig').splitlines(),1):
            if any(x in l for x in needles):excerpts.append(dict(path=str(T/rel),line=i,text=l))
    save('CODE_ANCHORS.json',excerpts)
    unique={r['path']:r for r in inputs};save('INPUTS.json',dict(files=list(unique.values()),count=len(unique),native_tool_execution=False))
    for r in unique.values():assert sha(Path(r['path']))==r['SHA256']
    save('postflight.json',dict(status='READ_ONLY_INPUTS_UNCHANGED',inputs=len(unique),native_compiler_DUT_PDS_GCC_runs=0,algorithm_or_port_or_RTL_TB_changes=False,hardware='STOPPED',stable='F143',candidate_promoted=False))
    print(json.dumps(dict(status='READ_ONLY_AUDIT_COMPLETE',inputs=len(unique),rows=[dict(seed=r['seed'],floor=r['iteration_floor_from_single_run'],forecast2=r['forecasts'][0],forecast_long=r['forecasts'][1]) for r in rows],hardware='STOPPED')))
if __name__=='__main__':run()
