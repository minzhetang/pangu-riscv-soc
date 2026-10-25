"""Independent complete VCD port/reset reconstruction, no new DUT execution."""
from pathlib import Path
import sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));sys.path.insert(0,str(H/'models'))
import stage_board as s
from peripheral_checker import decode_frames
def audit(tid):
    p=H/'runs'/tid/'wave.vcd';scope=[];names={};widths={};states={};wanted={};time=0;previous={};checks=0;groups=0;pipe=0;rises=[];samples=[1];leds=[0]
    rows=s.read(H/'simulation-result.json')['rows'];result=next(r for r in rows if r['id']==tid)
    unit=tid=='reset';top='tb_reset' if unit else 'tb_board_system'
    selected={'clk':top+'.clk','key':top+('.key0_n' if unit else '.key_n'),'reset':top+('.sys_rst_n' if unit else '.board_dut.sys_rst_n')}
    if not unit:selected.update(uart=top+'.uart_tx',led=top+'.gpio_out',gpio=top+'.board_dut.gpio_keys')
    stores=[]
    if not unit:
        for line in (p.parent/'trace.log').read_text().splitlines():
            a=line.split('|')
            if a[0]=='STORE' and a[3] in ['20000000','2000000c']:stores.append((int(a[1]),int(a[3],16),int(a[4],16)&255))
    gp={c:v for c,a,v in stores if a==0x2000000c};expected_led=0
    def group():
        nonlocal previous,checks,groups,pipe,expected_led
        if not wanted or not states:return
        current={k:states.get(code) for k,code in wanted.items()};groups+=1
        clk=current['clk'];key=current['key'];reset=current['reset']
        assert clk in [0,1] and key is not None and reset in [0,1],(tid,time,current)
        rise=previous.get('clk',0)==0 and clk==1
        key0=key&1
        if not key0:pipe=0
        elif rise:pipe=((pipe<<1)|1)&7
        assert reset==(pipe>>2),(tid,time,'release differs',pipe,current);checks+=1
        if not unit:
            assert current['gpio']==((~(key>>1))&15),(tid,time,'physical key mapping');checks+=1
        if rise:
            rises.append(time)
            if not unit and previous.get('reset')==1:
                c=len(samples);assert current['uart'] in [0,1] and current['led'] is not None
                if c in gp:expected_led=gp[c]
                assert current['led']==expected_led,(tid,c,current['led'],expected_led)
                samples.append(current['uart']);leds.append(current['led']);checks+=2
        previous=current
    with p.open('r',encoding='ascii') as f:
        header=True
        for line in f:
            a=line.split()
            if header:
                if line.startswith('$scope'):scope.append(a[2])
                elif line.startswith('$upscope'):scope.pop()
                elif line.startswith('$var'):
                    name='.'.join(scope+[a[4]]);names[name]=a[3];widths[name]=int(a[2])
                elif line.startswith('$enddefinitions'):
                    assert all(v in names for v in selected.values()),(tid,set(selected.values())-set(names))
                    wanted={k:names[v] for k,v in selected.items()};header=False
                continue
            if line.startswith('#'):
                group();stamp=int(line[1:]);assert stamp>=time;time=stamp
            elif line.startswith(('b','B')):
                value,code=line[1:].split()
                if code in wanted.values():states[code]=None if any(v in value.lower() for v in 'xz') else int(value,2)
            elif line and line[0] in '01xXzZ':
                code=line[1:].strip()
                if code in wanted.values():states[code]=int(line[0]) if line[0] in '01' else None
        group()
    assert groups>0 and len(rises)>2
    row=dict(id=tid,status='PASS',wave_sha256=s.sha(p),bytes=p.stat().st_size,complete_timestamp_groups=groups,
             checked_conditions=checks,last_ps=time,reset_three_edge_model=True)
    if not unit:
        metrics=result['check']['metrics'];assert len(samples)-1==metrics['physical'],(tid,len(samples),metrics)
        assert set(b-a for a,b in zip(rises,rises[1:]))=={37037}
        frames=decode_frames(samples,234);expected=[(c,v) for c,a,v in stores if a==0x20000000]
        assert frames==expected and [v for c,v in frames]==s.read(H/'manual-plan.json')['cases'][tid]['UART_bytes']
        row.update(active_cycles=len(samples)-1,clock_period_ps=37037,UART_frames=frames,
                   accepted_GPIO_writes=[(c,v) for c,a,v in stores if a==0x2000000c],final_LED=leds[-1])
    return row
rows=[audit(tid) for tid in ['reset','board5-N234','board12-N234']]
s.save(H/'wave-audit.json',dict(status='PASS',rows=rows,new_DUT_runs=0,
    limitation='logical waveform and explicit requests only, not physical metastability/MTBF/analog timing; no arbitrary warm restart',protected=s.protect()))
print('All 3 fresh VCDs fully parsed; reset, real pin mapping, clock, complete UART and LED timeline PASS')
