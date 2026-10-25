"""Mainline independent contract/VCD checks; no incoming code execution."""
from review import *
import types,importlib.util
def extract(p,names,ns):
    tree=ast.parse(p.read_text(encoding='utf-8-sig'));nodes=[x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name in names]
    assert {x.name for x in nodes}==set(names);exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns);return ns
def oracles():
    ns={'P':P,'s':types.SimpleNamespace(extract=extract)}
    spec=importlib.util.spec_from_file_location('owned_contract_2335',P/'work/system/2026-10-24-soc-txgpio-m1/peripheral_checker.py');mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);ns['ContractModel']=mod.ContractModel
    extract(P/'reports/progress/evidence/2026-10-24-increment-0030-alignment/review_0030.py',{'wrapper_wave'},ns)
    rx=extract(P/'deliveries/stage-return-review-2026-10-23-v01/scripts/audit_rx_wave.py',{'frames','audit'},{'SRC':P})
    groups=extract(P/'work/system/2026-10-23-memory-adapt-m1/audit_waves.py',{'groups'},{})['groups']
    return ns['wrapper_wave'],rx['audit'],groups
def run():
    wrap,rx,groups=oracles();summary=[]
    for n in [16,234]:
        wave=E/f'work/regif/txgpio-m1/waves/regif-m1-20261025-210743/regif_m1_N{n}.vcd';r=wrap(wave,n);save(H/f'wrapper-wave-N{n}.json',r)
        mark(wave.relative_to(E).as_posix(),'FULL_PARSE',dict(all_timestamps=True,checks=r['checks'],artifact=f'wrapper-wave-N{n}.json'))
        logs=[]
        for line in (E/f'work/regif/txgpio-m1/logs/regif-m1-20261025-210743/run_N{n}.log').read_text(encoding='utf-8-sig').splitlines():
            if line.startswith('REGIF_REQ '):logs.append({k:int(v,16 if k in ['addr','data'] else 2 if k=='strb' else 10) for k,v in re.findall(r'(\w+)=([^ ]+)',line)})
        actual=[];edge=0;serial=[]
        for t,b,a,ids in groups(wave):
            def g(v,k):
                x=v.get(ids.get('tb_local_regif_txgpio_m1.'+k),'x');return None if any(z in x for z in 'xz') else int(x,2)
            if g(b,'clk')==0 and g(a,'clk')==1:
                edge+=1
                if g(b,'rst_n') and g(b,'io_sel') and g(b,'io_wr_en'):
                    actual.append(dict(seq=len(actual)+1,edge=edge,addr=g(b,'io_addr'),data=g(b,'io_wdata')&255,strb=g(b,'io_wstrb'),error=g(b,'io_wr_error'),ready=g(b,'dut.tx_ready'),busy=g(b,'dut.tx_busy'),tx_accept=g(b,'dut.tx_accept'),gpio_accept=g(b,'dut.gpio_accept')))
                serial.append(dict(time_ps=t,edge=edge,reset=g(b,'rst_n'),pin=g(b,'uart_tx')))
        save(H/f'wrapper-request-correlation-N{n}.json',dict(requests=len(actual),exact_match=logs==actual,logged=logs,actual=actual))
        save(H/f'wrapper-serial-samples-N{n}.json',serial)
        summary.append(dict(kind='wrapper',N=n,status=r['status'],checks=r['checks'],requests=len(actual),all_request_fields_and_edge_match=logs==actual))
    for n in [8,16,234]:
        wave=E/f'work/peripherals/rx/waves/rx-20261025-211013/uart_rx_N{n}.vcd';r=rx(wave,n);save(H/f'rx-wave-N{n}.json',r)
        mark(wave.relative_to(E).as_posix(),'FULL_PARSE',dict(all_timestamps=True,checks=r['port_checks'],artifact=f'rx-wave-N{n}.json'))
        events=[dict(type={'publish':1,'consume':2,'overflow':3}[x['kind']],data=x['data'],time_ps=x['time_ps']) for x in r['events'] if x['kind'] in ['publish','consume','overflow']]+[dict(type=4,data=0,time_ps=x['time_ps']) for x in r['cancelled']]
        events.sort(key=lambda x:(x['time_ps'],0 if x['type']==2 else 1))
        logs=[]
        for line in (E/f'work/peripherals/rx/logs/rx-20261025-211013/run_N{n}.log').read_text(encoding='utf-8-sig').splitlines():
            if line.startswith('RX_LEDGER_ACT '):
                row=dict(re.findall(r'(\w+)=([^ ]+)',line));logs.append({k:int(v,16) if k=='data' else v if k=='label' else int(v) for k,v in row.items()})
        ordered=[(x['type'],x['data']) for x in events]==[(x['type'],x['data']) for x in logs]
        wanted={x['time_ps'] for x in events};snaps={};edge=0
        for t,b,a,ids in groups(wave):
            def g(v,k):
                x=v.get(ids.get('tb_uart_rx.'+k),'x');return None if any(z in x for z in 'xz') else int(x,2)
            if g(b,'clk')==0 and g(a,'clk')==1:edge+=1
            if t in wanted:snaps[t]=dict(edge=edge,before={k:g(b,k) for k in ['rx_valid','rx_ready','clear_errors','overrun','frame_error']},after={k:g(a,k) for k in ['rx_valid','rx_ready','clear_errors','overrun','frame_error']})
        fields={'valid':'rx_valid','ready':'rx_ready','clear':'clear_errors','ov':'overrun','fe':'frame_error'};errors=collections.Counter();rows=[];offsets=collections.defaultdict(collections.Counter)
        for log,ev in zip(logs,events):
            snap=snaps[ev['time_ps']];mismatch=[]
            for prefix,part in [('pre','before'),('post','after')]:
                for k,port in fields.items():
                    if log[prefix+'_'+k]!=snap[part][port]:errors[prefix+'_'+k]+=1;mismatch.append(dict(field=prefix+'_'+k,expected=snap[part][port],actual=log[prefix+'_'+k]))
            offset=log['edge']-snap['edge'];offsets[log['label']][offset]+=1;rows.append(dict(log=log,oracle=ev,actual=snap,edge_offset=offset,mismatches=mismatch))
        timeline=dict(N=n,events=len(events),logs=len(logs),ordered_type_data_match=ordered,field_errors=dict(errors),edge_offsets={k:dict(v) for k,v in offsets.items()},rows=rows)
        save(H/f'rx-ledger-timeline-N{n}.json',timeline)
        summary.append(dict(kind='RX',N=n,status=r['status'],checks=r['port_checks'],events=len(events),ordered_type_data_match=ordered,ledger_field_errors=dict(errors),edge_offsets=timeline['edge_offsets']))
    save(H/'wave-summary.json',summary);print(json.dumps(summary))
if __name__=='__main__':run()
