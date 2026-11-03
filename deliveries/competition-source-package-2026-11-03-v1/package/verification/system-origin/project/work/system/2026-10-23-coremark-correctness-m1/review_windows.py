"""Independent post-run reading of saved ordinary VCD windows; no simulator."""
import json
from pathlib import Path
from prepare_and_build import HERE,save,sha

def review(case,run_name='dut-run-01'):
    directory=HERE/case/run_name; wave=directory/'wave.vcd'
    before=sha(wave)
    names={}; scope=[]; lines=wave.read_text().splitlines(); body=0
    for i,line in enumerate(lines):
        fields=line.split()
        if not fields: continue
        if fields[0]=='$scope': scope.append(fields[2])
        elif fields[0]=='$upscope': scope.pop()
        elif fields[0]=='$var': names['.'.join(scope+[fields[4]])]=fields[3]
        elif fields[0]=='$enddefinitions': body=i+1; break
    assert '$timescale\n\t1ps\n$end' in '\n'.join(lines[:body])
    prefix='tb_coremark.dut.'
    state={}; changes={}; tick=0; samples=[]; streams={'EX':[],'WB':[],'MEM':[]}; late_edges=[]
    def value(s,name):
        raw=s.get(names[prefix+name],'x')
        assert 'x' not in raw.lower() and 'z' not in raw.lower(),(name,raw)
        return int(raw,2)
    def hx(v): return f'{v:08x}'
    def group(t,update):
        previous=state.copy(); state.update(update)
        ck=names[prefix+'clk']
        if previous.get(ck)!='0' or state.get(ck)!='1' or previous.get(names[prefix+'rst_n'])!='1': return
        # First4095 cycles are continuously recorded; late restore is a separate window.
        if t<40995000:
            samples.append(t)
            if value(previous,'id_valid') and not value(previous,'eei_hold'):
                streams['EX'].append('EX|'+hx(value(previous,'id_pc')))
            if value(previous,'mem_valid') and value(previous,'mem_reg_write') and value(previous,'mem_rd'):
                streams['WB'].append('WB|'+str(value(previous,'mem_rd'))+'|'+hx(value(previous,'wb_write_data')))
            if value(previous,'ex_valid') and value(previous,'ex_mem_to_reg'):
                streams['MEM'].append('READ|'+'|'.join(hx(value(previous,n)) for n in ['ex_pc','mem_addr','mem_rdata','mem_load_data']))
            if value(previous,'mem_wren'):
                streams['MEM'].append('STORE|'+'|'.join(hx(value(previous,n)) for n in ['ex_pc','mem_addr','mem_wdata'])+'|'+f"{value(previous,'mem_wstrb'):x}")
        elif t>50000000:
            assert value(previous,'eei_stop_valid')==1
            assert value(previous,'eei_stop_kind')==2 and value(previous,'eei_stop_pc')==0x68
            assert not value(previous,'mem_wren')
            assert not (value(previous,'mem_valid') and value(previous,'mem_reg_write'))
            late_edges.append(t)
    for line in lines[body:]:
        if line.startswith('#'):
            group(tick,changes); changes={}; tick=int(line[1:])
        elif line and line[0] in 'bB':
            bits,code=line[1:].split(); changes[code]=bits
        elif line and line[0] in '01xXzZ': changes[line[1:]]=line[0].lower()
    group(tick,changes)
    actual={n:[] for n in streams}
    with (directory/'trace.log').open() as source:
        for line in source:
            line=line.strip(); kind=line.split('|',1)[0]
            channel='MEM' if kind in ('READ','STORE') else kind
            if len(actual[channel])<len(streams[channel]): actual[channel].append(line)
            if all(len(actual[n])==len(streams[n]) for n in streams): break
    assert streams==actual,'VCD prefix differs from actual ordered trace'
    assert len(samples)==4095,(len(samples),'initial window')
    assert sha(wave)==before
    return {'status':'PASS' if len(late_edges)>=2 else 'PARTIAL_MISSING_STOP_WINDOW','VCD_SHA256':before,'VCD_bytes':wave.stat().st_size,
            'time_unit':'1ps','last_tick':tick,'duration_ns':tick/1000,
            'continuous_initial_edges':len(samples),'prefix_event_counts':{n:len(v) for n,v in streams.items()},
            'observed_late_stop_edges_no_WB_STORE':late_edges,
            'limitation':'VCD initial4095 only if stop window missing; otherwise initial+stop windows. No full kernel timeline; full text streams separate.',
            'no_new_simulation':True}

if __name__=='__main__':
    result={case:review(case) for case in ['performance','validation']}
    save(HERE/'wave-window-review.json',result); print(json.dumps(result,indent=2))
