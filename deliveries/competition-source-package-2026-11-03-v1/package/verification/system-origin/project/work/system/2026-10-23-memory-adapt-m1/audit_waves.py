"""Read only NEW full VCDs; separate pre-edge samples from post-NBA values."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def groups(path):
    scope=[];names={};values={};changes={};t=None;header=True
    with path.open(encoding='ascii') as f:
        for raw in f:
            s=raw.strip()
            if header:
                if s.startswith('$scope'):scope.append(s.split()[2])
                elif s.startswith('$upscope'):scope.pop()
                elif s.startswith('$var'):
                    a=s.split();names['.'.join(scope+[a[4]])]=a[3]
                elif s.startswith('$enddefinitions'):header=False
                continue
            if s.startswith('#'):
                if t is not None:
                    before=values.copy();values.update(changes)
                    yield t,before,values.copy(),names
                t=int(s[1:]);changes={}
            elif s and s[0] in '01xz':changes[s[1:]]=s[0]
            elif s.startswith('b'):
                v,k=s[1:].split();changes[k]=v
        if t is not None:
            before=values.copy();values.update(changes);yield t,before,values.copy(),names
def audit(directory):
    result=read(directory/'result.json');args=result['process']['argv']
    args=dict(a[1:].split('=',1) for a in args if a.startswith('+'))
    rom=[0]*8192;image=[int(v,16) for v in Path(args['IMAGE']).read_text().split()]
    rom[:len(image)]=image;ram=[0xa5a5a5a5]*8192
    if 'RAM_IMAGE' in args:
        initial=[int(v,16) for v in Path(args['RAM_IMAGE']).read_text().split()];ram[:len(initial)]=initial
    base=int(args['RAM_BASE']);rb=int(args['ROM_BYTES']);db=int(args['RAM_BYTES'])
    checks=0;edges=0;holds=0;rows=[];traces=[];errors=[]
    held=['pc_reg','if_pc','if_inst','id_pc','id_rs1_data','id_rs2_data','id_imm','id_rs1','id_rs2','id_rd',
          'id_reg_write','id_mem_write','id_mem_to_reg','id_alu_src','id_branch','id_jump','id_auipc','id_alu_ctrl','id_funct3',
          'ex_pc','ex_alu_result','ex_rs2_data','ex_rd','ex_reg_write','ex_mem_write','ex_mem_to_reg','ex_branch','ex_jump','ex_funct3',
          'mem_alu_result','mem_mem_rdata','mem_rd','mem_reg_write','mem_mem_to_reg',
          'if_valid','id_valid','ex_valid','mem_valid','id_system_kind','eei_state','eei_stop_valid','eei_stop_kind','eei_stop_pc']
    for t,pre,post,names in groups(directory/'wave.vcd'):
        def get(v,name,scope='dut'):
            s=v.get(names['tb_mem_adapt.'+scope+'.'+name],'x')
            return None if any(c in s for c in 'xz') else int(s,2)
        if get(pre,'clk')!=0 or get(post,'clk')!=1 or get(pre,'rst_n')!=1:continue
        edges+=1
        def check(ok,label):
            nonlocal checks
            checks+=1
            if not ok:errors.append(dict(time_ps=t,check=label))
        pc=get(pre,'pc');addr=get(pre,'mem_addr');phase=get(pre,'memory_phase');advance=get(pre,'pipeline_advance')
        check(advance==phase,'phase/advance');check(get(post,'memory_phase')==1-phase,'phase alternates')
        expected_i=rom[pc>>2] if pc<rb else 0
        expected_d=ram[(addr-base)>>2] if base<=addr<base+db else (rom[addr>>2] if addr<rb else 0)
        check(get(post,'iq','memory')==expected_i,'one-edge IF response')
        check(get(post,'dq','memory')==expected_d,'one-edge DATA read-before-write')
        if not advance:
            holds+=1
            for name in held:check(get(pre,name)==get(post,name),'hold '+name)
            check(get(pre,'we','dut.rf')==0,'RF write disabled during hold')
        elif not get(pre,'eei_hold'):
            check(get(post,'pc')==get(pre,'pc_next'),'PC advance')
        if advance and not get(pre,'flush_if') and not get(pre,'stall_if') and not get(pre,'eei_hold'):
            check(get(pre,'inst')==expected_i,'consumed IF word matches PC')
            check(get(post,'if_pc')==pc and get(post,'if_inst')==expected_i,'IFID word/PC pairing')
        if advance and get(pre,'id_valid') and not get(pre,'eei_hold'):
            traces.append(f"EX|{get(pre,'id_pc'):08x}")
        if advance and get(pre,'ex_valid') and get(pre,'ex_mem_to_reg'):
            traces.append(f"READ|{get(pre,'ex_pc'):08x}|{addr:08x}|{get(pre,'mem_rdata'):08x}|{get(pre,'mem_load_data'):08x}")
        if get(pre,'we','dut.rf') and get(pre,'mem_rd'):
            check(advance==1,'WB only advance edge')
            traces.append(f"WB|{get(pre,'mem_rd')}|{get(pre,'wb_write_data'):08x}")
        if get(pre,'mem_wren'):
            check(not advance and get(pre,'ex_valid')==1,'STORE only valid hold/sample edge')
            value=get(pre,'mem_wdata');mask=get(pre,'mem_wstrb');word=(addr-base)>>2
            traces.append(f"STORE|{get(pre,'ex_pc'):08x}|{addr:08x}|{value:08x}|{mask:x}")
            for lane in range(4):
                if mask&(1<<lane):ram[word]=(ram[word]&~(255<<(8*lane)))|(value&(255<<(8*lane)))
        else:check(get(pre,'mem_wstrb')==0,'idle strobe zero')
        if get(pre,'ex_mem_to_reg') or get(pre,'mem_wren') or get(pre,'flush_if'):
            rows.append(dict(time_ps=t,phase=phase,advance=advance,pc=pc,ex_pc=get(pre,'ex_pc'),address=addr,
                rdata_before=get(pre,'mem_rdata'),response_after=get(post,'dq','memory'),
                load_data=get(pre,'mem_load_data'),wren=get(pre,'mem_wren'),rf_we=get(pre,'we','dut.rf'),
                flush=get(pre,'flush_if'),stall=get(pre,'stall_if')))
    check(edges==result['metrics']['physical'],'full waveform physical count')
    check(holds==result['metrics']['memory_holds'],'full waveform hold count')
    expected_trace=(directory/'trace.log').read_text(encoding='ascii').splitlines()
    check(traces==expected_trace,'all ordered EX/WB/READ/STORE match fresh logs; no dedup')
    final_bytes=[(ram[i>>2]>>((i%4)*8))&255 for i in range(db)]
    check(final_bytes==[int(s,16) for s in (directory/'ram.hex').read_text().split()],'independent lane-memory replay')
    return dict(id=directory.name,status='PASS' if not errors else 'FAIL',checks=checks,physical_edges=edges,hold_edges=holds,
        trace_events=len(traces),errors=errors,representative_edges=rows,sha256=hashlib.sha256((directory/'wave.vcd').read_bytes()).hexdigest().upper())
if __name__=='__main__':
    names=['P01','P02','P03T','P03N','P04','P05','cboot']
    rows=[audit(H/'runs'/(n+'-sync1')) for n in names]
    out=dict(status='PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL',
        scope='seven complete NEW sync VCDs; independently separate pre-edge consumption/post-NBA response',cases=rows)
    with (H/'wave-audit.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
    print(json.dumps(dict(status=out['status'],checks=sum(r['checks'] for r in rows),cases=[dict(id=r['id'],status=r['status'],errors=r['errors'][:3]) for r in rows])))
