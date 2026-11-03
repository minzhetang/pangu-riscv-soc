"""Read-only new CPU VCD audit; model outputs settle 0.2ns after rising edge.
Consume PRE-edge values and examine settled values no earlier than edge+1ns.
This is functional-model evidence, not post-route timing or physical RAM evidence.
"""
from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
import run_m2 as m
spec=importlib.util.spec_from_file_location('vcd_helper',m.M1/'audit_waves.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def audit(name):
    d=m.H/'runs'/(name+'-sync1');r=m.read(d/'result.json')
    args=dict(a[1:].split('=',1) for a in r['process']['argv'] if a.startswith('+'))
    rom=[0]*8192;ram=[0xa5a5a5a5]*8192
    a=[int(x,16) for x in Path(args['IMAGE']).read_text().split()];rom[:len(a)]=a
    if 'RAM_IMAGE' in args:
        a=[int(x,16) for x in Path(args['RAM_IMAGE']).read_text().split()];ram[:len(a)]=a
    rb=int(args['ROM_BYTES']);db=int(args['RAM_BYTES']);base=int(args['RAM_BASE'])
    errors=[];checks=0;edges=0;pending=None;events=[];representative=[]
    def ck(ok,label,t):
        nonlocal checks
        checks+=1
        if not ok:errors.append(dict(time_ps=t,check=label))
    def get(values,names,name,scope='dut'):
        b=values.get(names['tb_mem_adapt.'+scope+'.'+name],'x')
        return None if any(c in b for c in 'xz') else int(b,2)
    def settle(p,after):
        t,pre,names,ei,ed=p
        g=lambda name,scope='dut':get(pre,names,name,scope)
        out=lambda name,scope='dut':get(after,names,name,scope)
        ck(out('inst','memory')==ei,'settled primitive IF response',t)
        if not g('mem_wren'):ck(out('rdata','memory')==ed,'settled primitive DATA response (non-write)',t)
        ck(out('if_bank_q','memory')==((g('pc')>>12)&7),'registered IF bank',t)
        region=2 if base<=g('mem_addr')<base+db else (1 if g('mem_addr')<rb else 0)
        ck(out('region_q','memory')==region,'registered DATA region',t)
        ck(out('data_bank_q','memory')==(((g('mem_addr')-base if region==2 else g('mem_addr'))>>12)&7),'registered DATA bank',t)
        if not g('pipeline_advance'):
            for name in ['pc_reg','if_pc','if_inst','id_pc','id_rs1_data','id_rs2_data','id_imm','id_rs1','id_rs2','id_rd',
                'ex_pc','ex_alu_result','ex_rs2_data','ex_rd','mem_alu_result','mem_mem_rdata','mem_rd','eei_state',
                'if_valid','id_valid','ex_valid','mem_valid','eei_stop_valid','eei_stop_kind','eei_stop_pc']:
                ck(g(name)==out(name),'held '+name,t)
        elif not g('eei_hold'):ck(out('pc')==g('pc_next'),'PC advance',t)
        if g('pipeline_advance') and not g('flush_if') and not g('stall_if') and not g('eei_hold'):
            ck(out('if_pc')==g('pc') and out('if_inst')==ei,'IFID PC/word response association',t)
        if g('mem_wren') or g('ex_mem_to_reg') or g('flush_if'):
            representative.append(dict(edge_ps=t,settle_at_or_after_ps=t+1000,phase=g('memory_phase'),
                pipeline_advance=g('pipeline_advance'),ex_pc=g('ex_pc'),address=g('mem_addr'),
                consumed_data=g('mem_rdata'),settled_data=out('rdata','memory'),store=g('mem_wren'),
                old_region=g('region_q','memory'),response_region=out('region_q','memory')))
    last=None
    for t,pre,post,names in v.groups(d/'wave.vcd'):
        if pending and t>=pending[0]+1000:settle(pending,pre);pending=None
        last=post
        g=lambda name,scope='dut':get(pre,names,name,scope)
        if g('clk')!=0 or get(post,names,'clk')!=1 or g('rst_n')!=1:continue
        assert pending is None
        edges+=1;pc=g('pc');addr=g('mem_addr');advance=g('pipeline_advance')
        ei=rom[pc>>2] if pc<rb else 0
        ed=ram[(addr-base)>>2] if base<=addr<base+db else (rom[addr>>2] if addr<rb else 0)
        pending=(t,pre,names,ei,ed)
        ck(advance==g('memory_phase'),'phase and advance',t)
        if advance and g('id_valid') and not g('eei_hold'):events.append(f"EX|{g('id_pc'):08x}")
        if advance and g('ex_valid') and g('ex_mem_to_reg'):
            ck(g('mem_rdata')==ed,'CPU consumes correct physical load response',t)
            events.append(f"READ|{g('ex_pc'):08x}|{addr:08x}|{g('mem_rdata'):08x}|{g('mem_load_data'):08x}")
        if g('we','dut.rf') and g('mem_rd'):
            ck(advance==1,'RF write only advance edge',t)
            events.append(f"WB|{g('mem_rd')}|{g('wb_write_data'):08x}")
        if g('mem_wren'):
            ck(not advance and g('ex_valid')==1,'STORE only valid sample edge',t)
            value=g('mem_wdata');mask=g('mem_wstrb');w=(addr-base)>>2
            events.append(f"STORE|{g('ex_pc'):08x}|{addr:08x}|{value:08x}|{mask:x}")
            for lane in range(4):
                if mask&(1<<lane):ram[w]=(ram[w]&~(255<<(lane*8)))|(value&(255<<(lane*8)))
        else:ck(g('mem_wstrb')==0,'idle strobe zero',t)
    if pending:settle(pending,last)
    ck(edges==r['metrics']['physical'],'full waveform physical edges',-1)
    ck(events==(d/'trace.log').read_text(encoding='ascii').splitlines(),'all ordered fresh events match VCD, no dedup',-1)
    got=[int(x,16) for x in (d/'ram.hex').read_text().split()]
    ck(got==[(ram[i>>2]>>((i%4)*8))&255 for i in range(db)],'actual primitive RAM dump equals independent replay',-1)
    return dict(id=name,status='PASS' if not errors else 'FAIL',checks=checks,physical_edges=edges,
        events=len(events),errors=errors,representative=representative)
if __name__=='__main__':
    rows=[audit(n) for n in m.names[:7]]
    out=dict(status='PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL',cases=rows,
        scope='seven complete NEW primitive-backed CPU VCDs, before edge vs settled +1ns; no CoreMark full-wave claim')
    m.save(m.H/'wave-audit.json',out)
    print(json.dumps(dict(status=out['status'],checks=sum(r['checks'] for r in rows),cases=[dict(id=r['id'],status=r['status'],errors=r['errors'][:3]) for r in rows])))
