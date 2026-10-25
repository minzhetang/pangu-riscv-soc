"""Conditional one-candidate PDS cost check, no bitstream or hardware."""
from pathlib import Path
import collections,ctypes,json,re,shutil,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_coremark as s
OLD=s.P/'work/fpga/2026-10-25-board-top-m1'
def prepare():
    assert s.read(H/'quality-compare.json')['all_seeds_benefit']
    assert s.read(H/'uart-audit.json')['status']==s.read(H/'wave-audit.json')['status']=='PASS';s.protect()
    pd=H/'pds';pd.mkdir();src=pd/'source';src.mkdir()
    for f in (H/'source').iterdir():shutil.copyfile(f,src/f.name)
    init=H/'cases/performance-N234/source/init_tables.svh';shutil.copyfile(init,src/'init_tables.svh')
    f=src/'memory_model.sv';text=f.read_text();assert text.count('    `include "init_tables.svh"')==1
    text=text.replace('    `include "init_tables.svh"',(src/'init_tables.svh').read_text())
    text=re.sub(r'`ifdef M0_VERIFY\n.*?`endif\n','',text,flags=re.S)
    assert '$fatal' not in text and '.mem[' not in text
    f.write_text(text,encoding='ascii')
    for name in ['clock_27mhz.fdc','board_pins.fdc']:shutil.copyfile(OLD/'pds'/name,pd/name)
    shutil.copyfile(OLD/'pin-plan.json',H/'pin-plan.json')
    tcl=(OLD/'pds/build.tcl').read_text();assert not any(x in tcl for x in ['gen_bit','cfg_','jtag','server','scbv'])
    (pd/'build.tcl').write_text(tcl,encoding='ascii')
    s.save(H/'pds-plan.json',dict(maximum=1,non_admin=True,timeout_seconds=1200,argv=[str(s.lib.PDS),'-file',str(pd/'build.tcl')],
        constraints_same_SHA256={n:s.sha(pd/n) for n in ['clock_27mhz.fdc','board_pins.fdc']},
        initialization=s.sha(init),conditional='both new seeds correct and faster plus pin/wave audits PASS',bitstream=False,hardware='STOPPED',
        files=[dict(path=str(p),sha256=s.sha(p)) for p in sorted(pd.rglob('*')) if p.is_file()]))
    print('Frozen 1 candidate PDS compile/syn/map/pnr/report target, no execution')
def run():
    s.protect();plan=s.read(H/'pds-plan.json');assert not ctypes.windll.shell32.IsUserAnAdmin()
    assert all(s.sha(x['path'])==x['sha256'] for x in plan['files'])
    assert not any((H/'pds'/n).exists() for n in ['compile','synthesize','device_map','place_route','report_timing'])
    r=s.bounded(plan['argv'],H/'pds','pds-once',1200);s.save(H/'pds-process.json',r)
    print('PDS exited',r['returncode_hex'],'inspect fresh outputs only; NOT acceptance')
def params(text):return {m[1]:re.sub(r'\s+','',m[2]) for m in re.finditer(r'\.(\w+)\s*\(([^()]*)\)',text)}
def bits(expr):
    m=re.fullmatch(r"(\d+)'([bh])([0-9a-fA-F]+)",expr);assert m
    v=int(m[3],2 if m[2]=='b' else 16);assert v<(1<<int(m[1]));return v
def audit():
    pd=H/'pds';process=s.read(H/'pds-process.json');assert process['returncode']==0 and not process['timed_out'] and not process['cap']
    flow=s.log(pd/'flow.log');assert not re.search(r'^E:',flow,re.M)
    stages=dict(compile='Action compile: Real time elapsed' in flow and (pd/'compile/error_info.txt').stat().st_size==0,
        synthesis='has been successfully synthesized' in flow,mapping='has been successfully mapped' in flow,
        pnr='has been placed and routed successfully' in flow,timing='Report timing is finished successfully' in flow)
    assert all(stages.values())
    vm=s.log(pd/'synthesize/board_top_syn.vm');tables=s.log(pd/'source/init_tables.svh');arrays={}
    for k in ['ROM','RAM']:
        body=re.search(rf'{k}_BITS\s*=\s*\{{(.*?)\}};',tables,re.S)[1]
        arrays[k]=int(''.join(re.findall(r"4096'h([0-9a-fA-F]+)",body)),16)
    def piece(b,h,k,c):
        return sum(((arrays[k]>>((b*1024+c*16+j//2)*32+h*16+(j%2)*8))&255)<<(j*9) for j in range(32))
    rx=re.compile(r'GTP_DRM18K_E1\s*/\*\s*(.*?)\s*\*/\s*#\((.*?)\)\s*(\\?\S+)\s*\((.*?)\);',re.S)
    drms={};chunks=0
    for m in rx.finditer(vm):
        ident=re.fullmatch(r'\\bank\[(\d+)\]\.halfword\[(\d+)\]\.(rom|ram)_block',m[1]);assert ident
        b,h,k=int(ident[1]),int(ident[2]),ident[3].upper();p=params(m[2])
        assert p['DATA_WIDTH_A']==p['DATA_WIDTH_B']=='16' and p['GRS_EN']=='"FALSE"' and p['DOA_REG']==p['DOB_REG']=='0'
        assert p['RAM_MODE']==('"TRUE_DUAL_PORT"' if k=='ROM' else '"SINGLE_PORT"')
        for c in range(64):assert bits(p[f'INIT_{c:02X}'])==piece(b,h,k,c),(b,h,k,c)
        assert (b,h,k) not in drms;drms[(b,h,k)]=p;chunks+=64
    shared=[]
    for b in range(8):
        for h in range(2):
            assert (b,h,'RAM') in drms
            if (b,h,'ROM') not in drms:
                assert h==1 and (b,0,'ROM') in drms and all(piece(b,0,'ROM',c)==piece(b,1,'ROM',c) for c in range(64))
                for port in ['ri','rd']:
                    for bit in list(range(8))+list(range(9,17)):
                        net=f'\\storage/bank[{b}].{port}[0] [{bit}]'
                        assert len(re.findall(r'\.(?:I[0-5])\s*\(\s*'+re.escape(net)+r'\s*\)',vm))==2,(b,port,bit)
                shared.append((b,h))
    assert len(drms)==32-len(shared)
    def module(n):
        a=vm.index('module '+n+'\n');return vm[a:vm.index('endmodule',a)]
    ffrx=re.compile(r'GTP_DFF\w*\s*/\*\s*(.*?)\s*\*/\s*#\((.*?)\)\s*(\\?\S+)\s*\((.*?)\);',re.S)
    rf=list(ffrx.finditer(module('regfile')));assert len(rf)==992 and all(params(x[2])['INIT']=="1'b0" for x in rf)
    reset=module('board_reset_sync');ff=list(ffrx.finditer(reset));assert len(ff)==3
    for i,m in enumerate(ff):
        assert m[1].strip()==f'\\release_ff[{i}]' and params(m[2])=={'GRS_EN':'"TRUE"','INIT':"1'b0"}
        p=params(m[4]);assert p['CLK']=='clk' and p['C']=='N0' and p['D']==("1'b1" if i==0 else f'release_ff[{i-1}]')
    assert '.I (key0_n)' in reset and '.Q (sys_rst_n)' in reset
    pnr=s.log(pd/'place_route/board_top_pnr.netlist');mapped=len(re.findall(r';gopDRM18K$',pnr,re.M));assert mapped==len(drms)
    prr=s.log(pd/'place_route/board_top.prr');pinplan=s.read(H/'pin-plan.json')['pins'];pins={}
    for line in prr.splitlines():
        a=[v.strip() for v in line.split('|')]
        if len(a)>8 and a[1] in pinplan:pins[a[1]]=dict(direction=a[2],loc=a[3],bank=a[4],VCCIO=a[5],standard=a[6])
    assert len(pins)==15 and all(pins[k]['loc']==v and pins[k]['VCCIO']=='3.3' and pins[k]['standard']=='LVCMOS33' for k,v in pinplan.items())
    ccr=s.log(pd/'constraint_check/constraint_check.ccr');assert '0 error(s), 0 critical warning(s), 0 warning(s), out of 94 constraint(s)' in ccr
    rtr=s.log(pd/'report_timing/board_top.rtr');timing={}
    for kind,corner,body in re.findall(r'(Setup|Hold|Recovery|Removal) Summary\((Slow|Fast) Corner\):(.*?)(?=\n\w|\Z)',rtr,re.S):
        m=re.search(r'clk_27mhz\s+clk_27mhz\s+([\d.-]+)\s+([\d.-]+)\s+(\d+)\s+(\d+)',body);assert m
        timing[f'{kind.lower()}_{corner.lower()}']=dict(slack_ns=float(m[1]),total_negative_ns=float(m[2]),failing_endpoints=int(m[3]),endpoints=int(m[4]))
    assert len(timing)==8 and all(x['slack_ns']>0 and x['failing_endpoints']==0 for x in timing.values())
    warning_lines=[l for l in flow.splitlines() if l.startswith('W:')];warnings=collections.Counter(re.sub(r'^(W: [^:]+):.*',r'\1',l) for l in warning_lines)
    final=s.log(pd/'report_timing/run.log');ui=re.findall(r"Timing-4086: Port '([^']+)'",final);uo=re.findall(r"Timing-4087: Port '([^']+)'",final)
    assert len(ui)==5 and len(uo)==9 and 'Total Latches: 0' in s.log(pd/'synthesize/board_top.snr')
    resources=dict(LUT=sum(map(int,re.findall(r'\|\s+LUT\s+\|\s+(\d+)',prr))),FF=sum(map(int,re.findall(r'\|\s+FF\s+\|\s+(\d+)',prr))),DRM18=mapped,DRM36=(mapped+1)//2,IO=15,latches=0)
    assert resources['LUT']>1000 and resources['FF']>1000
    stdout=s.log(H/'logs/pds-once/stdout.log');days=re.search(r'license will invalid in (\d+) days',stdout)
    assert not list(pd.rglob('*.bit')) and not list(pd.rglob('*.sbit'))
    for f in (H/'source').iterdir():
        if f.name!='memory_model.sv':assert s.sha(f)==s.sha(pd/'source'/f.name)
    original=s.read(OLD/'pds-audit.json')
    result=dict(status='CANDIDATE_INTERNAL_27MHZ_PASS_WITH_LIMITS',stages=stages,process=process,resources=resources,old_resources=original['resources'],
        timing=timing,old_timing=original['timing'],pins=pins,INIT_pieces_matched=chunks,DRM18_synth_and_PNR=mapped,shared_identical_ROM_halves=shared,RF_zero_init_FFs=992,
        warning_counts=dict(warnings),constant_probe_count=warnings['W: Loop was found during constant probe.'],constant_probe_root_cause='OPEN',
        inputs_without_external_delay=ui,outputs_without_external_delay=uo,license_checkout='SUCCESS_THIS_RUN',license_days_remaining=int(days[1]) if days else 'NO_EXPIRY_PROMPT',
        tool='PDS2022.2-SP6.4 build146967',device='PG2L100H-6IFBG676',constraints_SHA256=s.read(H/'pds-plan.json')['constraints_same_SHA256'],
        no_bitstream=True,hardware='STOPPED',protected=s.protect(),limitations=['internal STA only, no measured Fmax or IO/CDC closure','7 constant-probe warnings previously open, do not infer harmless','synthesis INIT/PNR identities checked, not config readback or post-layout simulation'])
    s.save(H/'pds-audit.json',result);print(json.dumps(dict(status=result['status'],resources=resources,timing=timing,license_days=result['license_days_remaining'])))
if __name__=='__main__':{'prepare':prepare,'run':run,'audit':audit}[sys.argv[1]]()
