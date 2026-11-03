"""Independent edge-oriented audit of the new VCD, no simulation or input edits."""
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent
M0=HERE.parent
sys.path.insert(0,str(M0))
import run as old

def frames(path):
    ids={};scope=[];values={};changes={};time=0;header=True
    with path.open(encoding='ascii') as f:
        for line in f:
            s=line.strip();parts=s.split()
            if header:
                if s.startswith('$scope'):scope.append(parts[2])
                elif s.startswith('$upscope'):scope.pop()
                elif s.startswith('$var'):ids['.'.join(scope[1:]+[parts[4]])]=parts[3]
                elif s.startswith('$enddefinitions'):header=False
            elif s.startswith('#'):
                if changes:
                    before=values.copy();values.update(changes)
                    yield time,before,values.copy(),ids
                    changes={}
                time=int(s[1:])
            elif s and not s.startswith('$'):
                if s[0] in 'bB' and len(parts)==2:changes[parts[1]]=parts[0][1:].lower()
                elif s[0] in '01xXzZ':changes[s[1:]]=s[0].lower()
        if changes:
            before=values.copy();values.update(changes);yield time,before,values.copy(),ids

def audit(entry):
    name=f"{entry['id']}-i{entry['if_sync']}-d{entry['data_sync']}"
    rom=[int(s,16) for s in (M0/'inputs'/f"{entry['id']}.program.hex").read_text().split()]
    ram=[int(s,16) for s in (M0/'inputs'/f"{entry['id']}.data.hex").read_text().split()]
    def data(a):
        if a is None:return None
        if 256<=a<512:return ram[(a-256)//4]
        if a<256:return rom[a//4]
        return None
    def fetch(a):return rom[a//4] if a is not None and 0<=a<1024 else None
    iq=0x00100073;dq=0;errors=[];checks=0;edges=0;cycle=0;wb=[];stores=[];loads=[]
    mismatches=[];load_edges=[];prewarm=[];stop_seen=False;poststop=0
    for t,b,a,ids in frames(Path(entry['wave'])):
        def val(v,key):
            s=v.get(ids.get(key,''))
            return None if s is None or 'x' in s or 'z' in s else int(s,2)
        if val(b,'clk')!=0 or val(a,'clk')!=1:continue
        edges+=1
        pc=val(b,'pc');addr=val(b,'addr');rst=val(b,'rst_n')
        r_before=data(addr);i_before=fetch(pc)
        expected_inst=iq if entry['if_sync'] else i_before
        expected_data=dq if entry['data_sync'] else r_before
        def ck(got,want,label):
            nonlocal checks
            checks+=1
            if got!=want and len(errors)<30:errors.append(dict(time_ps=t,label=label,expected=want,actual=got))
        ck(val(b,'inst'),expected_inst,'memory instruction before edge')
        ck(val(b,'rdata'),expected_data,'memory data before edge')
        if rst==0:prewarm.append(dict(time_ps=t,pc=pc,response_after=fetch(pc)))
        else:
            cycle+=1
            if val(b,'dut.mem_valid') and val(b,'dut.mem_reg_write') and val(b,'dut.mem_rd'):
                wb.append([val(b,'dut.mem_rd'),val(b,'dut.wb_write_data')])
                if stop_seen:errors.append(dict(time_ps=t,label='WB after stop'))
            if val(b,'wen'):
                stores.append([addr,val(b,'wdata'),val(b,'strb')])
                if stop_seen:errors.append(dict(time_ps=t,label='STORE after stop'))
            if val(b,'dut.ex_valid') and val(b,'dut.ex_mem_to_reg'):
                loads.append([addr,val(b,'rdata')])
                ck(val(a,'dut.mem_mem_rdata'),val(b,'rdata'),'MEM/WB sampled pre-edge LW data')
                load_edges.append(dict(time_ps=t,cycle=cycle,load_pc=val(b,'dut.ex_pc'),addr=addr,
                    ideal_word=r_before,response_before=val(b,'rdata'),response_after=val(a,'rdata'),
                    CPU_captured_after=val(a,'dut.mem_mem_rdata'),rd=val(b,'dut.ex_rd')))
            if not any(val(b,k) for k in ['dut.stall_if','dut.flush_if','dut.eei_hold']):
                ck(val(a,'dut.if_pc'),pc,'IFID sampled pre-edge PC')
                ck(val(a,'dut.if_inst'),val(b,'inst'),'IFID sampled pre-edge instruction')
                if val(a,'dut.if_inst')!=fetch(val(a,'dut.if_pc')):
                    mismatches.append(dict(time_ps=t,pc_before=pc,inst_before=val(b,'inst'),
                        pc_after=val(a,'pc'),inst_after=val(a,'inst'),IFID_pc=val(a,'dut.if_pc'),
                        IFID_inst=val(a,'dut.if_inst'),architectural_word=fetch(val(a,'dut.if_pc'))))
            if val(b,'stopped'):
                stop_seen=True;poststop+=1
        if val(b,'bus_write') and addr is not None and 256<=addr<512:
            wd=val(b,'bus_wdata');mask=val(b,'bus_strb')
            for lane in range(4):
                if mask & (1<<lane):ram[(addr-256)//4]=(ram[(addr-256)//4]&~(255<<(lane*8))) | (wd&(255<<(lane*8)))
        iq=i_before;dq=r_before
        ck(val(a,'inst'),iq if entry['if_sync'] else fetch(val(a,'pc')),'memory instruction after edge')
        ck(val(a,'rdata'),dq if entry['data_sync'] else data(val(a,'addr')),'memory data after edge')
    ck(wb,entry['actual']['wb'],'VCD vs raw log ordered WB')
    ck(stores,entry['actual']['stores'],'VCD vs raw log ordered STORE')
    ck(loads,entry['actual']['loads'],'VCD vs raw log ordered LOAD')
    ck(ram,list(entry['actual']['ram'].values()),'independent memory final vs raw log')
    if not stop_seen or poststop<8:errors.append(dict(label='stop/post-stop evidence incomplete'))
    return dict(id=name,status='PASS' if not errors else 'FAIL',checks=checks,errors=errors,
        scope='memory model and trace consistency, not architectural compatibility PASS',
        wave_sha256=old.sha(entry['wave']),active_cycles=cycle,prewarm=prewarm,poststop_edges=poststop,
        architecture_IF_mismatch_count=len(mismatches),first_IF_mismatches=mismatches[:8],load_edges=load_edges,
        ordered_WB=wb,ordered_STORE=stores)

old.verify()
result=old.read(HERE/'result.json')
audits=[audit(x) for x in result['cpu']]
summary=dict(scope='new VCD read-only audit, no new DUT runs',audits=audits,
    status='PASS' if all(x['status']=='PASS' for x in audits) else 'FAIL',
    total_checks=sum(x['checks'] for x in audits))
old.save(HERE/'wave-audit.json',summary)
print(json.dumps(dict(status=summary['status'],checks=summary['total_checks'],
    modes=[dict(id=x['id'],status=x['status'],first_errors=x['errors'][:1],IF_mismatches=x['architecture_IF_mismatch_count']) for x in audits]),ensure_ascii=False))
