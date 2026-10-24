"""Stable post-edge samples, independently computed from VCD physical time.
Not CPU retirement evidence; sparse dumpoff sections are explicitly excluded.
"""
from pathlib import Path
import sys,re,json
sys.dont_write_bytecode=True
import run_stage as s
def snapshots(path,top):
    scope=[];names={};values={};tick=0;started=False;scale=[];header=True
    with path.open(encoding='ascii') as f:
        for line in f:
            a=line.strip().split()
            if not a:continue
            if header:
                if a[0]=='$scope':scope.append(a[2])
                elif a[0]=='$upscope':scope.pop()
                elif a[0]=='$var' and scope==[top]:names[a[3]]=a[4]
                elif a[0]=='$enddefinitions':header=False
                continue
            if a[0][0]=='#':
                if started:yield tick,dict(values)
                tick=int(a[0][1:]);started=True
            elif a[0][0] in ['b','B'] and len(a)==2:
                if a[1] in names:values[names[a[1]]]=a[0][1:]
            elif a[0][0] in '01xz' and a[0][1:] in names:values[names[a[0][1:]]]=a[0][0]
    if started:yield tick,dict(values)
def main(tid):
    path=s.H/'runs'/tid/'wave.vcd';checks=reads=0;covered=[];last=None
    assert '$timescale\n\t1ps\n$end' in path.read_text(encoding='ascii')[:2000]
    for t,v in snapshots(path,'tb_timed_system'):
        keys=['clk','rst_n','monitor_ticks','monitor_address','monitor_read','monitor_advance']
        if not all(k in v and not re.search('[xz]',v[k],re.I) for k in keys):continue
        if v['rst_n']!='1' or v['clk']!='1' or t<45000:continue
        c=(t-35000)//10000
        assert int(v['monitor_ticks'],2)==c,('post-edge counter',t,c,v['monitor_ticks'])
        assert int(v['monitor_advance'],2)==c%2,('post-edge phase, NOT consuming phase',t,c)
        addr=int(v['monitor_address'],2)
        if addr in [0x20000100,0x20000104]:
            expected=(c>>(32 if addr==0x20000104 else 0))&0xffffffff
            assert int(v['monitor_read'],2)==expected,('settled post-edge read',t,addr)
            reads+=1
        checks+=1
        if c!=last:covered.append(c);last=c
    assert checks>=1000
    result=dict(status='PASS',stable_post_edge_checks=checks,timer_address_samples=reads,
      distinct_visible_cycles=len(set(covered)),visible_cycle_min=min(covered),visible_cycle_max=max(covered),
      VCD_sha=s.sha(path),scope='sampled VCD windows only; CPU LOAD consumes pre-edge value separately checked in trace',
      full_algorithm_wave=False,retirement_PC=False)
    s.save(s.H/'runs'/tid/'wave-review.json',result);print(json.dumps(result))
if __name__=='__main__':main(sys.argv[1])
