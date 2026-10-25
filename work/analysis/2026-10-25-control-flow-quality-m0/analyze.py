"""Parse existing validated O2 evidence; 0 compiler, 0 model replay, 0 DUT."""
from pathlib import Path
from bisect import bisect_right
from collections import Counter,defaultdict
import hashlib,json,re,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
B=P/'work/fpga/2026-10-25-board-coremark-m1';T=P/'work/system/2026-10-24-timed-coremark-m1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,o):
    with p.open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest().upper()
def sx(v,n):return ((v&((1<<n)-1))^(1<<(n-1)))-(1<<(n-1))
def decode(word,pc,nextpc,gap):
    op=word&127;rd=(word>>7)&31;rs1=(word>>15)&31;f3=(word>>12)&7
    if op==0x63:
        assert f3 in [0,1,4,5,6,7]
        imm=sx((word>>31)<<12|((word>>7)&1)<<11|((word>>25)&63)<<5|((word>>8)&15)<<1,13);target=(pc+imm)&0xffffffff
        assert nextpc in [target,(pc+4)&0xffffffff]
        same=target==((pc+4)&0xffffffff)
        if same:assert gap in [2,6];taken=gap==6
        else:taken=nextpc==target
        if gap is not None:assert gap==(6 if taken else 2),(hex(pc),gap,taken)
        return dict(kind={0:'BEQ',1:'BNE',4:'BLT',5:'BGE',6:'BLTU',7:'BGEU'}[f3],family='BRANCH',taken=taken,target=target,offset=imm,
            direction='backward' if imm<0 else 'forward' if imm>0 else 'self',PC_plus4_target=same)
    if op==0x6f:
        imm=sx((word>>31)<<20|((word>>12)&255)<<12|((word>>20)&1)<<11|((word>>21)&1023)<<1,21);target=(pc+imm)&0xffffffff
        assert nextpc==target
        if gap is not None:assert gap==6,(hex(pc),gap)
        return dict(kind='JAL_LINK' if rd in [1,5] else 'JAL_X0' if rd==0 else 'JAL_OTHER_LINK',family='JAL',taken=True,target=target,offset=imm,
            direction='backward' if imm<0 else 'forward' if imm>0 else 'self',PC_plus4_target=imm==4)
    if op==0x67:
        assert f3==0 and nextpc%4==0
        if gap is not None:assert gap==6,(hex(pc),gap)
        ret=rd==0 and rs1 in [1,5] and sx(word>>20,12)==0
        return dict(kind='JALR_RETURN' if ret else 'JALR_LINK' if rd in [1,5] else 'JALR_OTHER',family='JALR',taken=True,target=nextpc,
            offset=sx(word>>20,12),direction='indirect',PC_plus4_target=nextpc==((pc+4)&0xffffffff))
    return None
def selftest():
    cases=[(0x00000463,0x100,0x108,6,'BEQ',True),(0x00209263,0x100,0x104,2,'BNE',False),
        (0x00209263,0x100,0x104,6,'BNE',True),(0x008000ef,0x100,0x108,6,'JAL_LINK',True),(0x00008067,0x100,0x440,6,'JALR_RETURN',True)]
    for word,pc,n,g,k,t in cases:r=decode(word,pc,n,g);assert (r['kind'],r['taken'])==(k,t)
    rejected=0
    for word,pc,n,g in [(0x00000463,0x100,0x10c,6),(0x008000ef,0x100,0x108,2),(0x00209263,0x100,0x104,4)]:
        try:decode(word,pc,n,g)
        except AssertionError:rejected+=1
        else:raise AssertionError('invalid parser control accepted')
    return dict(status='PASS_PARSER_ONLY',synthetic_positive=5,synthetic_negative_rejected=rejected,new_DUT_runs=0)
def analyze(name):
    tid=name+'-N234';d=B/'runs'/tid;c=read(d/'check-result.json');assert c['status']=='PASS' and not c['errors']
    image=(B/'build'/name/'program.bin').read_bytes();art=next(a for a in read(T/'build-result.json')['artifacts'] if a['id']==name)
    assert sha(B/'build'/name/'program.bin')==art['bin_sha']
    start,end=c['detail']['stamps'][2:];old=next(r for r in read(T/'quality-window-analysis.json')['rows'] if r['program']==name)
    assert old['raw_physical_ticks']==end-start
    functions=sorted((int(pc,16),fn) for pc,fn in re.findall(r'^([0-9a-f]+) <([^>]+)>:',(T/'logs'/('build-'+name+'-objdump')/'stdout.log').read_text(),re.M));starts=[x[0] for x in functions]
    ex=[];window_digest=hashlib.sha256();all_counts=Counter()
    with (d/'trace.log').open(encoding='ascii') as f:
        for line in f:
            a=line.strip().split('|');cycle=int(a[1]);all_counts[a[0]]+=1
            if start+1<cycle<=end+1:window_digest.update(('|'.join(a)+'\n').encode())
            if a[0]=='EX':ex.append((cycle,int(a[2],16)))
    assert dict(all_counts)==c['trace_counts']
    prior=next(r for r in read(B/'quality-compare.json')['rows'] if r['program']==name)
    assert window_digest.hexdigest().upper()==prior['window']['sha256']
    stop=re.findall(r'^STOP\|2\|([0-9a-f]{8})$',(d/'stdout.log').read_text(),re.M);assert len(stop)==1
    stop_pc=int(stop[0],16);full=Counter();counts=Counter();gaps=Counter();by_fn=defaultdict(Counter);by_pc={};samples={};normal_gaps=Counter();load_gap=0;window_ex=0
    for i,(cycle,pc) in enumerate(ex):
        nxt=ex[i+1][1] if i+1<len(ex) else stop_pc;gap=ex[i+1][0]-cycle if i+1<len(ex) else None
        assert pc%4==0 and pc+4<=len(image);word=int.from_bytes(image[pc:pc+4],'little');r=decode(word,pc,nxt,gap)
        if r:
            full['control']+=1;full['redirect']+=r['taken'];full[r['family']]+=1
        if not start+1<cycle<=end+1:continue
        window_ex+=1
        if not r:
            assert gap in [2,4],(hex(pc),gap);normal_gaps[str(gap)]+=1
            if gap==4:assert word&127==3;load_gap+=1
            continue
        k=r['kind'];counts[k]+=1;counts['controls']+=1;counts['redirects']+=r['taken'];counts[r['family']+'_redirects']+=r['taken']
        counts['conditional_taken' if r['taken'] else 'conditional_not_taken']+=r['family']=='BRANCH'
        if r['family']=='BRANCH':counts[r['direction']+'_branch_'+('taken' if r['taken'] else 'not_taken')]+=1
        counts['PC_plus4_targets']+=r['PC_plus4_target']
        gaps[k+':'+str(gap)]+=1
        j=bisect_right(starts,pc)-1;fn=functions[j][1] if j>=0 else 'UNKNOWN';by_fn[fn][k]+=1
        key=f'{pc:08x}'
        if key not in by_pc:by_pc[key]=dict(pc=key,encoding=f'{word:08x}',function=fn,kind=k,executions=0,taken=0,not_taken=0,gaps=Counter(),targets=Counter(),offset=r['offset'])
        row=by_pc[key];row['executions']+=1;row['taken']+=r['taken'];row['not_taken']+=not r['taken'];row['gaps'][str(gap)]+=1;row['targets'][f'{nxt:08x}']+=1
        samplekey=k+':'+('taken' if r['taken'] else 'not_taken')
        samples.setdefault(samplekey,dict(cycle=cycle,pc=f'{pc:08x}',next_cycle=cycle+gap,next_pc=f'{nxt:08x}',gap=gap,function=fn,encoding=f'{word:08x}',**r))
    assert full['redirect']==c['metrics']['flush']
    assert window_ex==old['window_EX_observations'] and counts['redirects']==old['reference_redirect']
    assert load_gap==old['reference_load_use'],(load_gap,old['reference_load_use'])
    assert 2*window_ex+2*load_gap+4*counts['redirects']==end-start
    penalty=4*counts['redirects'];targeted=2*counts['redirects'];direct_only=2*counts['JAL_redirects']
    result=dict(program=name,status='PASS_EXISTING_TRACE_ANALYSIS',source_run=str(d),new_DUT_runs=0,model_replays=0,window=[start,end],raw_ticks=end-start,
        trace_SHA256=sha(d/'trace.log'),bin_SHA256=sha(B/'build'/name/'program.bin'),compute_window_event_SHA256=window_digest.hexdigest().upper(),
        total_EX=len(ex),whole_program_flush_from_control_decode=full['redirect'],whole_program_flush_verified=c['metrics']['flush'],
        window_EX=window_ex,window_load_use_from_successor_gaps=load_gap,control_counts=dict(counts),control_successor_gaps=dict(gaps),normal_successor_gaps=dict(normal_gaps),
        existing_redirect_ticks=penalty,existing_redirect_fraction=penalty/(end-start),
        conditional_hypothesis=dict(description='one fewer logical bubble for already-resolved redirects in two-clock mode, every event eligible, all else equal',
            ideal_ticks_saved=targeted,ideal_time_reduction=targeted/(end-start),ideal_speedup=(end-start)/(end-start-targeted),measured=False,guaranteed=False),
        direct_JAL_only_hypothesis=dict(ideal_ticks_saved=direct_only,ideal_time_reduction=direct_only/(end-start),measured=False),
        top_control_functions=sorted([dict(function=f,total=sum(v.values()),by_kind=dict(v)) for f,v in by_fn.items()],key=lambda x:-x['total'])[:12],
        examples=samples,limitations=['EX observation is not retirement','branch condition itself reused prior validated functional evidence, not re-executed','PC+4 target uses known baseline gap only; new candidate must not inherit that rule','timing estimate is static hypothesis; no new implementation/performance/timing proof'])
    save(H/(name+'-by-pc.json'),by_pc);return result
def main():
    inputs=set(B/'source'/r['file'] for r in read(B/'postflight.json')['source'])
    inputs.update([B/'quality-compare.json',T/'quality-window-analysis.json',T/'build-result.json',P/'work/fpga/2026-10-24-implementability-m0/verification/memory_protocol_checks.svh'])
    expected={str(p):r['sha256'] for p in [] for r in []}
    for line in (B/'SHA256SUMS-final.txt').read_text().splitlines():
        digest,n=line.split('  ',1);expected[str(B/n)]=digest
    for name in ['performance','validation']:
        inputs.add(B/'build'/name/'program.bin');inputs.add(T/'logs'/('build-'+name+'-objdump')/'stdout.log')
        for f in ['trace.log','check-result.json','stdout.log']:inputs.add(B/'runs'/(name+'-N234')/f)
    rows=[]
    for p in sorted(inputs):
        digest=sha(p)
        if str(p) in expected:assert digest==expected[str(p)]
        rows.append(dict(path=str(p),bytes=p.stat().st_size,sha256=digest))
    save(H/'INPUTS.json',dict(base_git='03850aa073afe2ff22001a17f9151e95067ce2a6',files=rows))
    result=dict(date_beijing='2026-10-25',decision='D137',status='PASS_READ_ONLY_ANALYSIS_NOT_NEW_DUT',parser=selftest(),rows=[analyze(n) for n in ['performance','validation']],
        RTL_changes=0,TB_changes=0,new_builds=0,new_DUT_runs=0,new_reference_replays=0,PDS_runs=0,hardware='STOPPED')
    assert all(sha(x['path'] if isinstance(x['path'],Path) else Path(x['path']))==x['sha256'] for x in rows)
    save(H/'SUMMARY.json',result);save(H/'postflight.json',dict(status='INPUTS_UNCHANGED',count=len(rows),new_DUT_runs=0,model_replays=0,hardware='STOPPED'))
    print(json.dumps([dict(program=r['program'],counts=r['control_counts'],redirect_ticks=r['existing_redirect_ticks'],hypothesis=r['conditional_hypothesis'],JAL_only=r['direct_JAL_only_hypothesis']) for r in result['rows']]))
if __name__=='__main__':main()
