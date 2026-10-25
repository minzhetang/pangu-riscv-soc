"""Native sparse VCD: derive physical ticks from time, mark every off interval."""
from pathlib import Path
import re,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_coremark as s
def snapshots(path):
    scope=[];names={};values={};time=0;started=False;header=True;recording=True
    with path.open(encoding='ascii') as f:
        for line in f:
            a=line.split()
            if not a:continue
            if header:
                if a[0]=='$scope':scope.append(a[2])
                elif a[0]=='$upscope':scope.pop()
                elif a[0]=='$var' and scope==['tb_board_coremark']:names.setdefault(a[3],[]).append(a[4])
                elif a[0]=='$enddefinitions':header=False
                continue
            if a[0].startswith('#'):
                if started:yield time,dict(values),recording
                stamp=int(a[0][1:]);assert stamp>=time;time=stamp;started=True
            elif a[0]=='$dumpoff':recording=False
            elif a[0]=='$dumpon':recording=True
            elif a[0][0] in ['b','B'] and len(a)==2:
                for n in names.get(a[1],[]):values[n]=a[0][1:]
            elif a[0][0] in '01xz':
                for n in names.get(a[0][1:],[]):values[n]=a[0][0]
    if started:yield time,dict(values),recording
def audit(tid):
    d=H/'runs'/tid;path=d/'wave.vcd';assert '$timescale\n\t1ps\n$end' in path.read_text(encoding='ascii')[:2000]
    releases=[]
    for line in (d/'uart-pins.log').read_text().splitlines():
        a=line.split('|')
        if int(a[2])==0 and a[4]=='1':releases.append(int(a[1]))
    assert len(releases)==1;first_edge=releases[0]-1+37037
    visible=set();pretimer=set();checks=0;settled_reads=0;off=0;intervals=[];last=None;last_time=0
    required=['clk','rst_n','monitor_ticks','monitor_advance','key_n','gpio_in_async','uart_tx','gpio_out']
    for t,v,recording in snapshots(path):
        last_time=t
        if not recording:off+=1;continue
        if t<first_edge:continue
        assert all(n in v and not re.search('[xz]',v[n],re.I) for n in required),(tid,t,'unknown visible critical signal')
        if v['clk']!='1':continue
        c=(t-first_edge)//37037+1
        assert int(v['monitor_ticks'],2)==c and int(v['monitor_advance'],2)==c%2,(tid,t,c,'post-edge counter/phase')
        assert int(v['key_n'],2)==31 and int(v['gpio_in_async'],2)==0 and int(v['gpio_out'],2)==0
        assert int(v['pre_ticks'],2)==c-1
        if all(k in v and not re.search('[xz]',v[k],re.I) for k in ['monitor_address','monitor_read']):
            addr=int(v['monitor_address'],2)
            if addr in [0x20000100,0x20000104]:
                assert int(v['monitor_read'],2)==(c>>(32 if addr==0x20000104 else 0))&0xffffffff;settled_reads+=1
        if all(k in v and not re.search('[xz]',v[k],re.I) for k in ['pre_addr','pre_io_data']):
            addr=int(v['pre_addr'],2)
            if addr in [0x20000100,0x20000104]:
                assert int(v['pre_io_data'],2)==((c-1)>>(32 if addr==0x20000104 else 0))&0xffffffff
                pretimer.add(c)
        if c!=last:
            if intervals and c==intervals[-1][1]+1:intervals[-1][1]=c
            elif not intervals or c!=intervals[-1][1]:intervals.append([c,c])
            last=c
        visible.add(c);checks+=1
    result=s.read(d/'check-result.json');assert result['status']=='PASS'
    timer_cycles={r['cycle'] for r in result['timer_reads']}
    assert checks>=1000 and timer_cycles<=pretimer,(tid,checks,timer_cycles-pretimer)
    assert result['metrics']['physical'] in visible and off>0
    return dict(id=tid,status='PASS',VCD_sha256=s.sha(path),bytes=path.stat().st_size,stable_post_checks=checks,
        distinct_visible_cycles=len(visible),intervals=intervals,explicit_off_timestamp_groups=off,
        timer_LOAD_pre_capture_cycles=sorted(timer_cycles),settled_timer_address_samples=settled_reads,
        first_active_posedge_ps=first_edge,last_timestamp_ps=last_time,
        scope='native VCD windows; captured pre-edge variables + independent physical-time/post-edge checks',
        full_algorithm_wave=False,hardware_ILA=False,retirement_PC=False)
if __name__=='__main__':
    rows=[audit(t) for t in ['performance-N234','validation-N234']]
    s.save(H/'wave-audit.json',dict(status='PASS',rows=rows,new_DUT_runs=0,protected=s.protect()))
    print('Native window waveform/timer pre-post audit PASS; skipped regions explicit; no new DUT')
