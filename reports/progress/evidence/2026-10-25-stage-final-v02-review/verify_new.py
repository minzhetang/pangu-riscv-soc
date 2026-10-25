"""Actual new mainline runs: independent public-wave and exact ledger checks."""
from final_waves import *
W=P/'work/peripheral-review/2026-10-25-stage-final-v02'
def runner_functions():
    src=resolve('work/regif/txgpio-m1/scripts/run_regif_m1.py');tree=ast.parse(src.read_text(encoding='utf-8-sig'));ns=dict(re=re)
    names={'ALL_CASES','N234_CASES','REQ_RE','EXPECTED_EDGES','EXPECTED_REQUESTS','TX_RE','GPIO_RE'}
    nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in {'expected_markers','analyze_markers','analyze_events','analyze_run'} or isinstance(x,ast.Assign) and any(isinstance(y,ast.Name) and y.id in names for y in x.targets)]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    return ns

def requests(wave,groups):
    rows=[];edge=0
    for t,b,a,ids in groups(wave):
        def g(v,k):
            x=v.get(ids.get('tb_local_regif_txgpio_m1.'+k),'x');return None if any(z in x for z in 'xz') else int(x,2)
        if g(b,'clk')==0 and g(a,'clk')==1:
            edge+=1
            if g(b,'rst_n') and g(b,'io_sel') and g(b,'io_wr_en'):
                rows.append(dict(seq=len(rows)+1,edge=edge,addr=g(b,'io_addr'),data=g(b,'io_wdata')&255,strb=g(b,'io_wstrb'),error=g(b,'io_wr_error'),ready=g(b,'dut.tx_ready'),busy=g(b,'dut.tx_busy'),tx_accept=g(b,'dut.tx_accept'),gpio_accept=g(b,'dut.gpio_accept')))
    return rows

def tx_boundary(text,n,accepts):
    events=[];idx=-1
    for typ,edge,data,observed in re.findall(r'^REGIF_TX_FRAME event=(START|COMPLETE|CANCEL)(?: idx=\d+)? edge=(\d+)(?: data=([0-9a-f]+))? observed_edge=(\d+)\s*$',text,re.M):
        if typ=='START':idx+=1
        source=accepts[idx];edge=int(edge);observed=int(observed)
        assert observed==edge+1
        if typ=='START':assert edge==source['edge']
        elif typ=='COMPLETE':assert edge==source['edge']+10*n and int(data,16)==source['data']
        else:assert source['edge']<edge<source['edge']+10*n
        events.append(dict(kind=typ,event_edge=edge,observed_edge=observed,data=int(data,16) if data else None,accept_edge=source['edge']))
    assert idx==8 and len(accepts)==9 and len(events)==18
    assert [e['kind'] for e in events].count('COMPLETE')==6 and [e['kind'] for e in events].count('CANCEL')==3
    assert [(e['kind'],e['event_edge']) for e in events[:2]]==[('START',37 if n==16 else 6),('COMPLETE',197 if n==16 else 2346)]
    return dict(status='PASS',events=events,first_start=events[0]['event_edge'],first_complete=events[1]['event_edge'],counts=dict(start=9,complete=6,cancel=3,bad_stop=0),exact_all_START_accept=True,exact_all_COMPLETE_E_plus_10N=True,observed_plus1=True)

def rx_timeline(wave,text,n,a,groups):
    exp=[dict(type={'publish':1,'consume':2,'overflow':3}[e['kind']],data=e['data'],time_ps=e['time_ps']) for e in a['events'] if e['kind'] in ['publish','consume','overflow']]+[dict(type=4,data=0,time_ps=e['time_ps']) for e in a['cancelled']]
    exp.sort(key=lambda e:(e['time_ps'],0 if e['type']==2 else 1))
    want=[(e['type'],e['data'],max(0,(e['time_ps']-5000)//10000+1)) for e in exp]
    shared=[(int(t),int(d,16),int(edge)) for t,d,edge in re.findall(r'A_SHARED_RX seq=\d+ type=(\d+) data=([0-9a-f]+) edge=(\d+)',text)]
    logs=[]
    for l in text.splitlines():
        if l.startswith('RX_LEDGER_ACT '):logs.append({k:int(v,16) if k=='data' else v if k=='label' else int(v) for k,v in re.findall(r'(\w+)=([^ ]+)',l)})
    inline=[(x['type'],x['data'],x['edge']) for x in logs];assert want==shared==inline
    assert len(want)=={8:92,16:110,234:68}[n] and [x['seq'] for x in logs]==list(range(len(want)))
    wanted={x['time_ps'] for x in exp};snaps={};edge=0
    for t,b,aft,ids in groups(wave):
        def g(v,k):
            x=v.get(ids.get('tb_uart_rx.'+k),'x');return None if any(z in x for z in 'xz') else int(x,2)
        if g(b,'clk')==0 and g(aft,'clk')==1:edge+=1
        if t in wanted:snaps[t]=dict(edge=edge,before={k:g(b,k) for k in ['rx_valid','rx_ready','clear_errors','overrun','frame_error']},after={k:g(aft,k) for k in ['rx_valid','rx_ready','clear_errors','overrun','frame_error']})
    fields={'valid':'rx_valid','ready':'rx_ready','clear':'clear_errors','ov':'overrun','fe':'frame_error'};rows=[]
    for l,e in zip(logs,exp):
        snap=snaps[e['time_ps']];assert l['edge']==snap['edge']
        for prefix,part in [('pre','before'),('post','after')]:
            for k,port in fields.items():assert l[prefix+'_'+k]==snap[part][port] and snap[part][port] is not None,(n,l['seq'],prefix,k)
        rows.append(dict(log=l,oracle=e,snapshot=snap))
    for marker in ['RX_SNAPSHOT_CHECK_PASS','RX_CAPTURE_CROSSCHECK_PASS','ordered=1 edge_match=1','RX_SELFCHECK_PASS']:assert marker in text
    return dict(status='PASS',N=n,events=len(want),ordered_shared_inline_oracle=True,all_event_edges_match=True,snapshot_fields_checked=10*len(want),snapshot_mismatches=0,rows=rows)

def run():
    wrap,rx,groups=oracles();native=read(W/'run.json');compiled=read(W/'compile.json');assert compiled['all_compiled'];rows=[];ns=runner_functions();controls=[]
    for row in native['rows']:
        ident=row['id'];n=row['N'];proc=row['process'];text=Path(proc['stdout']).read_text(encoding='utf-8-sig');assert proc['returncode']==0 and not proc['timed_out'] and '$finish called' in text
        wave=W/'build'/(ident+'.vcd');out=dict(id=ident,N=n,process=proc,normal_finish=True)
        if ident.startswith('wrap'):
            a=wrap(wave,n);assert a['status']=='PASS';save(H/f'new-{ident}-wave.json',a)
            req=requests(wave,groups);logged=[{k:int(v,16 if k in ['addr','data'] else 2 if k=='strb' else 10) for k,v in re.findall(r'(\w+)=([^ ]+)',l)} for l in text.splitlines() if l.startswith('REGIF_REQ ')]
            assert req==logged and req==read(H/f'wrapper-request-correlation-N{n}.json')['actual'];save(H/f'new-{ident}-requests.json',dict(exact=True,rows=req))
            boundary=tx_boundary(text,n,[q for q in req if q['tx_accept']]);save(H/f'new-TX-boundary-N{n}.json',boundary)
            assert not ns['analyze_run'](dict(returncode=0,timed_out=False,log_truncated=False),text,n)
            controls.append(dict(N=n,name='correct_new_actual_log',expected='PASS',actual='PASS'))
            l=re.findall(r'^REGIF_REQ .*$',text,re.M)[1];comp=re.search(r'^REGIF_TX_FRAME event=COMPLETE .*$',text,re.M).group(0)
            start=re.search(r'^REGIF_TX_FRAME event=START .*$',text,re.M).group(0)
            mutated=[('second_request_edge',text.replace(l,re.sub(r'edge=(\d+)',lambda m:'edge='+str(int(m[1])+1),l,1),1)),('flip_busy',text.replace(l,re.sub(r'busy=([01])',lambda m:'busy='+str(1-int(m[1])),l,1),1)),('complete_edge',text.replace(comp,re.sub(r'edge=\d+','edge=999999',comp,1),1)),('observed_edge',text.replace(comp,re.sub(r'observed_edge=\d+','observed_edge=999999',comp),1)),('start_edge',text.replace(start,re.sub(r'edge=(\d+)',lambda m:'edge='+str(int(m[1])+1),start,1),1))]
            if n==16:
                gp=re.search(r'^REGIF_GPIO_ACCEPT .*$',text,re.M).group(0);mutated.append(('gpio_seq_edge',text.replace(gp,re.sub(r'seq=\d+ edge=\d+','seq=99 edge=999999',gp),1)))
            for name,txt in mutated:
                errors=ns['analyze_run'](dict(returncode=0,timed_out=False,log_truncated=False),txt,n);assert errors,(n,name);controls.append(dict(N=n,name=name,expected='REJECT',actual='REJECT',errors=errors))
            out.update(status='PASS_LIMITED_PUBLIC_FUNCTION_AND_EXACT_TX_EDGE',checks=a['checks'],requests=len(req),complete=6,cancel=3)
        elif ident in ['rx8','rx16','rx234']:
            a=rx(wave,n);assert a['status']=='PASS';save(H/f'new-{ident}-wave.json',a);s=rx_timeline(wave,text,n,a,groups);save(H/f'new-{ident}-timeline.json',s);out.update(status='PASS_LIMITED_PUBLIC_FUNCTION_ORDER_AND_SNAPSHOT',port_checks=a['port_checks'],events=s['events'],snapshot_fields=s['snapshot_fields_checked'],mismatches=0)
        else:
            wanted=read(resolve('work/peripherals/rx/tests/rx-plan-1.3.5.json'))['negative']['expected_markers'] if ident=='rxneg' else ['REGIF_CAP_GOOD_PASS','REGIF_CAP_BAD_STOP_DETECTED','REGIF_CAP_EXTRA_DETECTED','REGIF_CAP_MISSING_DETECTED','REGIF_CAP_LAST_HALF_STOP_CANCEL','REGIF_CAP_CONTROL_PASS','REGIF_CAP_SELFCHECK_PASS']
            assert all(m in text for m in wanted);assert not any(x in text for x in ['CHK_FAIL','SELFCHECK_FAIL','TB_WATCHDOG_TIMEOUT']);out.update(status='PASS_SCOPED_NEGATIVE_CONTROLS',markers=wanted)
        rows.append(out)
    save(H/'new-runs.json',dict(compilers=7,new_DUT=7,rows=rows,CPU_CoreMark_PDS_runs=0,hardware='STOPPED'))
    save(H/'V3-controls.json',dict(status='PASS_LIMITED',rows=controls,new_DUT=0,incoming_entrypoints_executed=False))
    print(json.dumps([dict(id=x['id'],status=x['status'],events=x.get('events'),mismatches=x.get('mismatches')) for x in rows]))
if __name__=='__main__':run()
