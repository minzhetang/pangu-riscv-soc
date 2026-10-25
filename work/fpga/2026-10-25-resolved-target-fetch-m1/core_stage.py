"""Same O2 images, actual Pango primitive model; only candidate frontend changes."""
from pathlib import Path
import ctypes,sys,shutil,re,hashlib,ast
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_redirect as s
C=s.B;T=s.T;M=s.M
def prepare():
    assert s.read(H/'small-result-v2.json')['status']==s.read(H/'regression-result.json')['status']=='PASS';s.protect()
    shutil.copyfile(C/'manual-plan.json',H/'core-manual-plan.json');shutil.copyfile(C/'build-result.json',H/'build-result.json')
    (H/'stage_coremark.py').write_text('from stage_redirect import *\n',encoding='ascii')
    tb=(C/'tests/tb_board_coremark.sv').read_text();cpu='board_dut.soc.cpu_core'
    declarations=f'''    integer fetch_fd=0,pref_seen=0,pref_class=0,pref_cycle=0;
    reg pref_req,pref_hit,pref_redir;reg [31:0] pref_target,pref_pc,pref_id_pc;
    reg [31:0] pref_settled_cycle=0;
    wire monitor_pref_req={cpu}.redirect_request,monitor_pref_hit={cpu}.redirect_fetch_hit;
    wire monitor_pref_valid={cpu}.fetch_redirect_valid;
    wire [31:0] monitor_pref_tag={cpu}.fetch_redirect_pc,monitor_target={cpu}.redirect_target;
    wire [31:0] monitor_id_pc={cpu}.id_pc,monitor_pc_reg={cpu}.pc_reg;
    wire [31:0] monitor_if_pc={cpu}.if_pc,monitor_if_inst={cpu}.if_inst,monitor_inst=board_dut.soc.inst;
    wire monitor_if_valid={cpu}.if_valid,monitor_id_valid={cpu}.id_valid;
    // PRE signals are sampled before the edge, monitor_* after NBA at settled marker.
    always @(posedge clk)if(rst_n)begin
        pref_cycle=monitor_ticks+1;pref_req=monitor_pref_req;pref_hit=monitor_pref_hit;
        pref_target=monitor_target;pref_pc=monitor_pc;pref_id_pc=monitor_id_pc;
        pref_redir={cpu}.pipeline_advance&&{cpu}.id_valid&&!{cpu}.eei_hold&&{cpu}.control_flush;
        if(pref_cycle%2==1&&pref_req)$fdisplay(fetch_fd,"REQ|%0d|%08x|%08x",pref_cycle,pref_id_pc,pref_pc);
        if(pref_redir)$fdisplay(fetch_fd,"REDIR|%0d|%08x|%08x|%0d|%08x|%08x",pref_cycle,pref_id_pc,pref_target,pref_hit,monitor_pref_tag,monitor_inst);
        #1;
        if(pref_cycle%2==1&&pref_req)$fdisplay(fetch_fd,"SAMPLE|%0d|%08x|%08x|%08x",pref_cycle,pref_id_pc,monitor_pref_tag,monitor_inst);
        if(pref_redir)$fdisplay(fetch_fd,"APPLY|%0d|%08x|%0d|%08x|%08x|%0d|%08x|%08x|%0d",pref_cycle,pref_id_pc,pref_hit,pref_target,monitor_pc_reg,monitor_if_valid,monitor_if_pc,monitor_if_inst,monitor_id_valid);
        pref_settled_cycle=pref_cycle;
    end
'''
    marker='    // 37.037 ns period at 1 ps precision, nominal 27 MHz.';assert tb.count(marker)==1;tb=tb.replace(marker,declarations+marker)
    marker='if(!serial_fd)$fatal(1,"PIN_LOG_OPEN");';assert tb.count(marker)==1;tb=tb.replace(marker,marker+'\n        fetch_fd=$fopen("fetch.log","w");if(!fetch_fd)$fatal(1,"FETCH_LOG_OPEN");')
    marker='        if(PHASE_ADDR!=0&&pre_write&&pre_addr==PHASE_ADDR)begin'
    gate=f'''        if(monitor_pref_req)begin
            pref_class={cpu}.id_jump?({cpu}.id_alu_src?9:8):{cpu}.id_funct3;
            if((pref_seen&(1<<pref_class))==0)begin
                pref_seen=pref_seen|(1<<pref_class);if(wave_until<cycle+16)wave_until=cycle+16;
            end
        end
'''
    assert tb.count(marker)==1;tb=tb.replace(marker,gate+marker)
    tb=tb.replace('$fclose(serial_fd);','$fclose(serial_fd);$fclose(fetch_fd);')
    (H/'tests/tb_board_coremark.sv').write_text(tb,encoding='ascii')
    checker=(C/'check_coremark.py').read_text();checker=checker.replace("import stage_coremark as s","import stage_redirect as s\nfrom fetch_audit import audit_core")
    checker=checker.replace('from cpu_program_reference import Reference','''from cpu_program_reference import Reference as BaseReference
class Reference(BaseReference):
    def __init__(self,*args):super().__init__(*args);self.prefetch_expected=[]
    def step(self):
        old=self.flush;pc=self.pc;super().step()
        if self.flush!=old:
            target=self.pc;word=int.from_bytes(self.rom[target:target+4],'little') if target<32768 else 0
            self.prefetch_expected.append(dict(pc=pc,target=target,request=target%4==0,eligible=target%4==0 and word!=0,word=word))
''')
    checker=checker.replace("H/'manual-plan.json'","H/'core-manual-plan.json'")
    a="eq('tail',metrics['tail'],32);expected_adv=len(ref.EX)+2*ref.flush+ref.stall+19"
    b="prefetch=audit_core(d/'fetch.log',ref.prefetch_expected,image,d/'trace.log',ref.pc)\n    eq('tail',metrics['tail'],32);expected_adv=len(ref.EX)+2*ref.flush-sum(r['eligible'] for r in ref.prefetch_expected)+ref.stall+19"
    assert checker.count(a)==1;checker=checker.replace(a,b)
    checker=checker.replace("timer_reads=timer_reads,GPIO_actual= gpio,UART_frames=len(frames),detail=detail,","timer_reads=timer_reads,GPIO_actual= gpio,UART_frames=len(frames),detail=detail,prefetch_audit=prefetch,")
    (H/'check_coremark.py').write_text(checker,encoding='utf-8')
    targets=[];plans={}
    for name in ['performance','validation']:
        tid=name+'-N234';d=H/'cases'/tid/'source';d.mkdir(parents=True);build=H/'build'/name;build.mkdir()
        a=next(a for a in s.read(T/'build-result.json')['artifacts'] if a['id']==name)
        for ext,key in [('bin','bin_sha'),('elf','ELF_sha')]:
            p=C/'build'/name/('program.'+ext);assert s.sha(p)==a[key];shutil.copyfile(p,build/p.name)
        for f in (H/'source').iterdir():shutil.copyfile(f,d/f.name)
        init=C/'cases'/tid/'source/init_tables.svh';shutil.copyfile(init,d/'init_tables.svh')
        # Same complete ROM/RAM tables, not a new program or regenerated compiler output.
        assert s.sha(init)==s.sha(d/'init_tables.svh')
        for key,expected in [('ROM',(build/'program.bin').read_bytes()+bytes(32768-(build/'program.bin').stat().st_size)),('RAM',b'\xa5'*32768)]:
            body=re.search(rf'{key}_BITS\s*=\s*\{{(.*?)\}};',init.read_text(),re.S)[1]
            assert int(''.join(re.findall(r"4096'h([0-9a-fA-F]+)",body)),16).to_bytes(32768,'little')==expected
        output=H/'compile'/(tid+'.vvp');phase=a['symbols']['timing_phase']
        argv=[s.lib.IVL,'-B',s.lib.LIB,'-g2012','-Wall','-DM0_VERIFY','-I',d,'-I',M/'verification','-s','tb_board_coremark',f'-Ptb_board_coremark.PHASE_ADDR={phase}','-o',output,*list(d.glob('*.v')),*list(d.glob('*.sv')),H/'tests/tb_board_coremark.sv',s.lib.VENDOR/'GTP_DRM18K_E1.v',s.lib.VENDOR/'GTP_GRS.v']
        targets.append(dict(id=tid,argv=list(map(str,argv)),output=str(output)))
        plans[tid]=dict(old_run=str(C/'runs'/tid),phase_address=phase,INIT_sha256=s.sha(init),bin_sha256=a['bin_sha'],n=234)
    s.save(H/'core-compile-plan.json',dict(maximum=2,timeout_seconds=120,fail_fast=True,targets=targets))
    s.save(H/'frozen-case-plan.json',dict(cases=plans,max_physical_cycles=6000000,run_seconds=360,compile_seconds=120))
    # Reuse full pin timeline and native window audit, adapting only report source.
    au=(C/'audit_uart.py').read_text().replace("frozen=Path(plan['old_run'])/'ram-output.txt';assert s.sha(frozen)==plan['expected_report_sha256'];expected=frozen.read_bytes()", "expected=(d/'ram-output.txt').read_bytes();assert check['detail']['report_bytes']==len(expected)")
    au=au.replace("len(frames)==plan['expected_UART_bytes']","len(frames)==len(expected)").replace("plan['expected_report_sha256']","s.sha(d/'ram-output.txt')")
    (H/'audit_uart.py').write_text(au,encoding='utf-8');shutil.copyfile(C/'audit_wave.py',H/'audit_wave.py')
    files=[f for f in H.rglob('*') if f.is_file() and (f.name in ['core_stage.py','fetch_audit.py','check_coremark.py','stage_coremark.py','audit_uart.py','audit_wave.py','core-manual-plan.json','build-result.json','frozen-case-plan.json','core-compile-plan.json'] or f.is_relative_to(H/'tests') or f.is_relative_to(H/'cases/performance-N234') or f.is_relative_to(H/'cases/validation-N234') or f.is_relative_to(H/'build'))]
    s.save(H/'core-frozen.json',dict(files=[dict(path=str(f),sha256=s.sha(f)) for f in files]));print('Frozen two unchanged O2/official-model targets and independent hit/timing checks')
def protect():
    s.protect();assert all(s.sha(x['path'])==x['sha256'] for x in s.read(H/'core-frozen.json')['files'])
def compile():
    protect();assert not ctypes.windll.shell32.IsUserAnAdmin();rows=[]
    for t in s.read(H/'core-compile-plan.json')['targets']:
        r=s.bounded(t['argv'],H,'compile-'+t['id'],120);okay=r['returncode']==0 and not r['timed_out'] and not r['cap'] and Path(t['output']).is_file()
        rows.append(dict(id=t['id'],status='PASS' if okay else 'FAIL',output=t['output'],sha256=s.sha(t['output']) if okay else None,process=r));print(t['id'],rows[-1]['status'],flush=True)
        if not okay:break
    s.save(H/'core-compile-result.json',dict(status='PASS' if len(rows)==2 and all(r['status']=='PASS' for r in rows) else 'STOPPED',rows=rows))
def run():
    protect();c=s.read(H/'core-compile-result.json');assert c['status']=='PASS';rows=[];import check_coremark as ck
    for t in c['rows']:
        assert s.sha(t['output'])==t['sha256'];tid=t['id'];d=H/'runs'/tid;d.mkdir()
        r=s.bounded([s.lib.VVP,'-N','-M-','-M'+str(s.lib.LIB),t['output'],'+MAX_CYCLES=6000000'],d,'run-'+tid,360)
        s.save(d/'process.json',r);shutil.copyfile(r['stdout'],d/'stdout.log');print(tid,'DUT_EXIT',r['returncode'],r['elapsed_seconds'],flush=True)
        try:
            assert r['returncode']==0 and not r['timed_out'] and not r['cap'],r
            checked=ck.check(tid);s.save(d/'check-result.json',checked);assert checked['status']=='PASS',checked['errors']
        except Exception as e:s.save(H/'core-result.json',dict(status='STOPPED',case=tid,error=repr(e),completed=rows));raise
        rows.append(dict(id=tid,status='PASS',process=r,check=checked));print(tid,'STRICT_PASS',flush=True)
    s.save(H/'core-result.json',dict(status='PASS',new_DUT_runs=2,rows=rows));s.save(H/'simulation-result.json',dict(status='PASS',new_core_DUT_runs=2,rows=rows))
if __name__=='__main__':{'prepare':prepare,'compile':compile,'run':run,'verify':protect}[sys.argv[1]]()
