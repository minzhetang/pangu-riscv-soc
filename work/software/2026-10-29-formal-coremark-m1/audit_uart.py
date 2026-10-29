"""Full actual UART transitions + separate centre decoding, independent of VCD windows."""
from pathlib import Path
from bisect import bisect_right
import sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_coremark as s
def expected_changes(starts,data,n):
    assert len(starts)==len(data);out=[];last=1;end=0
    for start,byte in zip(starts,data):
        assert start>=end
        for bit,value in enumerate([0]+[(byte>>b)&1 for b in range(8)]+[1]):
            if value!=last:out.append((start+bit*n,value));last=value
        end=start+10*n
    return out
def decode(changes,n,last_cycle):
    cycles=[c for c,v in changes];assert cycles==sorted(set(cycles))
    def value(c):
        i=bisect_right(cycles,c)-1;return changes[i][1] if i>=0 else 1
    frames=[];end=0;old=1
    for c,v in changes:
        if old==1 and v==0 and c>=end:
            end=c+10*n;assert end<=last_cycle
            assert value(c+n//2)==0 and value(c+9*n+n//2)==1
            byte=sum(value(c+(b+1)*n+n//2)<<b for b in range(8));frames.append((c,byte))
        old=v
    assert value(last_cycle)==1
    return frames
def audit(tid,path=None,directory=None):
    d=Path(directory) if directory is not None else H/'runs'/tid;p=d/'uart-pins.log' if path is None else path
    check=s.read(d/'check-result.json');assert check['status']=='PASS'
    plan=s.read(H/'frozen-case-plan.json')['cases'][tid]
    frozen=H/'oracles-recovery'/tid.split('-N')[0]/'expected-report.txt';assert s.sha(frozen)==plan['expected_report_sha256'];expected=frozen.read_bytes()
    stores=[]
    with __import__('contextlib').closing(__import__('stream_io').open_stream(d,'trace')) as f:
        for line in f:
            a=line.strip().split('|')
            if a[0]=='STORE' and a[3]=='20000000':stores.append((int(a[1]),int(a[4],16)&255))
    assert bytes(v for c,v in stores)==expected
    changes=[];last_time=-1;last_bit=1;epoch=None;rows=0;releases=0;reset_rows=0
    with p.open(encoding='ascii') as f:
        for line in f:
            a=line.strip().split('|');assert len(a)==6 and a[0]=='PIN'
            assert all(x in '01' for x in a[3:]);time,c,clk,rst,bit=map(int,a[1:]);assert time>last_time;last_time=time;rows+=1
            if not rst:
                assert c==0 and bit==1;last_bit=1;reset_rows+=1;continue
            if c==0:
                releases+=1;assert bit==1 and clk==1
                # Actual rst release captured one ps after the third clock edge.
                first_active_ps=time-1+37037;continue
            assert clk==1 and bit!=last_bit and 1<=c<=check['metrics']['physical']
            candidate=time-(c-1)*37037
            if epoch is None:epoch=candidate
            assert epoch==candidate==first_active_ps+1,'actual timestamps must agree with physical-cycle log'
            changes.append((c,bit));last_bit=bit
    assert releases==1 and reset_rows>=1
    assert changes==expected_changes([c for c,v in stores],expected,234),'wrong/missing/extra/reordered pin transition'
    frames=decode(changes,234,check['metrics']['physical'])
    assert frames==stores and len(frames)==plan['expected_UART_bytes']
    assert frames[-1][0]+2340<check['metrics']['physical']-32
    return dict(id=tid,status='PASS',pin_log_sha256=s.sha(p),records=rows,actual_transitions=len(changes),frames=len(frames),
        first_frame_cycle=frames[0][0],last_frame_cycle=frames[-1][0],last_frame_end_cycle=frames[-1][0]+2340,
        data_sha256=plan['expected_report_sha256'],CLKS_PER_BIT=234,clock_period_ps=37037,first_active_posedge_ps=epoch-1,
        actual_transition_timestamps_match_cycles=True,separate_centre_decode=True,ordinary_native_VCD_is_windowed=True)
def selftest():
    data=b'AA';starts=[2,83];good=expected_changes(starts,data,8);assert decode(good,8,170)==list(zip(starts,data))
    probes={'missing_frame':good[:len(good)//2],
        'extra_repeated_frame':good+[(c+170,v) for c,v in good[:len(good)//2]],
        'wrong_byte':expected_changes(starts,b'BA',8),
        'order_bytes':expected_changes(starts,b'AB',8)}
    for name,bad in probes.items():
        try:passed=decode(bad,8,400)==list(zip(starts,data)) and bad==good
        except AssertionError:passed=False
        assert not passed,name
    return dict(status='PASS',synthetic_only=True,new_DUT_runs=0,control=1,negative=list(probes))
if __name__=='__main__':
    rows=[audit(t) for t in ['performance-N234','validation-N234']]
    negative=[];d=H/'uart-negative';d.mkdir()
    # Mutate a complete small actual-pin log, never the DUT input/expected report.
    tid='performance-N234';original=(H/'runs'/tid/'uart-pins.log').read_text();lines=original.splitlines()
    i=next(i for i,l in enumerate(lines) if int(l.split('|')[2])>0)
    for name in ['missing_change','wrong_bit','wrong_timestamp','duplicate_change']:
        copy=lines.copy()
        if name=='missing_change':copy.pop(i)
        elif name=='duplicate_change':copy.insert(i+1,copy[i])
        else:
            a=copy[i].split('|');j=5 if name=='wrong_bit' else 1;a[j]=str(int(a[j])+(1 if j==1 else 1-2*int(a[j])));copy[i]='|'.join(a)
        p=d/(name+'.log');p.write_text('\n'.join(copy)+'\n',encoding='ascii')
        try:audit(tid,p)
        except AssertionError as err:negative.append(dict(id=name,status='EXPECTED_REJECTION',detail=str(err)[:120]))
        else:raise AssertionError('corrupt log accepted '+name)
    s.save(H/'uart-audit.json',dict(status='PASS',rows=rows,actual_log_negative=negative,decoder_selftest=selftest(),new_DUT_runs=0,
        scope='entire actual output pin transition timeline + frozen bytes; not hardware/ILA',protected=s.protect()))
    print('Complete UART pin timeline/centre decode and 4 real-log corruptions rejected; no new DUT')
