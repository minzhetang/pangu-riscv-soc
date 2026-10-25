"""D133: unchanged board RTL, two preserved images; software validation only."""
from pathlib import Path
import ast,ctypes,hashlib,importlib.util,json,re,shutil,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
B=P/'work/fpga/2026-10-25-board-top-m1';T=P/'work/system/2026-10-24-timed-coremark-m1'
M=P/'work/fpga/2026-10-24-implementability-m0'
spec=importlib.util.spec_from_file_location('m0bounded_library',M/'stage.py');lib=importlib.util.module_from_spec(spec);sys.modules[spec.name]=lib;spec.loader.exec_module(lib);lib.H=H
read,save,sha,log,bounded=lib.read,lib.save,lib.sha,lib.log,lib.bounded
def protect():return lib.protect()
def prepare():
    for name in ['source','source-before','models','models-before','tests','cases','build','logs','compile','runs']:(H/name).mkdir(exist_ok=False)
    originals=read(B/'postflight.json')['source'];assert len(originals)==13
    for row in originals:
        f=B/'source'/row['file'];assert sha(f)==row['sha256'];shutil.copyfile(f,H/'source'/f.name);shutil.copyfile(f,H/'source-before'/f.name)
    for n in ['cpu_program_reference.py','peripheral_checker.py','check_timed_v2.py']:
        shutil.copyfile(T/n,H/'models-before'/n)
        if n!='check_timed_v2.py':shutil.copyfile(T/n,H/'models'/n)
    shutil.copyfile(T/'manual-plan.json',H/'manual-plan.json');shutil.copyfile(T/'build-result.json',H/'build-result.json')
    save(H/'APPROVAL.json',dict(date_beijing='2026-10-25',decision='D133',user_reply='同意继续',
        scope='A-BOARD-COREMARK-M1: two finite N234 board-top runs, unchanged RTL/images/algorithm',
        forbidden=['RTL/ISA/algorithm changes','PDS/bitstream/hardware/server/JTAG/Flash','new tools/environment/license changes','formal score or speedup claim']))
    cases={};targets=[]
    tb=(B/'tests/tb_board_system.sv').read_text()
    tb=tb.replace('module tb_board_system;\n    localparam integer N=234,PHASE_ADDR=0;', 'module tb_board_coremark #(parameter integer PHASE_ADDR=0);\n    localparam integer N=234;')
    tb=tb.replace('integer key_pattern=5;reg [4:0] key_n=0;', 'integer key_pattern=0;reg [4:0] key_n=0;\n    integer serial_fd=0;')
    tb=tb.replace('limit=10000000','limit=6000000').replace('limit>10000000','limit>6000000')
    tb=tb.replace('if(!$value$plusargs("K=%d",key_pattern))key_pattern=5;\n        if(key_pattern!=5&&key_pattern!=12)$fatal(1,"UNFROZEN_KEYS");','key_pattern=0;')
    tb=tb.replace('$dumpvars(1,tb_board_system);','$dumpvars(1,tb_board_coremark);')
    tb=tb.replace('events_fd=$fopen("trace.log","w");bus_fd=$fopen("bus.log","w");','events_fd=$fopen("trace.log","w");bus_fd=$fopen("bus.log","w");\n        serial_fd=$fopen("uart-pins.log","w");if(!serial_fd)$fatal(1,"PIN_LOG_OPEN");')
    position='    always @(posedge clk)if(rst_n)begin'
    extra='''    // Continuous actual pin transitions, independent of native VCD windows.
    always @(uart_tx or rst_n) begin
        #0.001;
        if(serial_fd) $fdisplay(serial_fd,"PIN|%0t|%0d|%b|%b|%b",$realtime,cycle,clk,rst_n,uart_tx);
    end
'''
    assert tb.count(position)==1;tb=tb.replace(position,extra+position)
    position='        if(board_dut.soc.cpu_core.pipeline_advance)begin'
    windows='''        if((cycle<=wave_until||pre_addr==32'h20000100||pre_addr==32'h20000104||stopped)&&!dumping)begin $dumpon;dumping=1;end
        if(cycle>wave_until&&pre_addr!=32'h20000100&&pre_addr!=32'h20000104&&!stopped&&dumping)begin $dumpoff;dumping=0;end
'''
    assert tb.count(position)==1;tb=tb.replace(position,windows+position)
    tb=tb.replace('$fclose(events_fd);$fclose(bus_fd);','$fclose(events_fd);$fclose(bus_fd);$fclose(serial_fd);')
    assert 'tb_board_system' not in tb and 'key_pattern=5' not in tb
    (H/'tests/tb_board_coremark.sv').write_text(tb,encoding='ascii')
    for name in ['performance','validation']:
        oldart=next(a for a in read(T/'build-result.json')['artifacts'] if a['id']==name)
        tid=name+'-N234';d=H/'cases'/tid/'source';d.mkdir(parents=True);build=H/'build'/name;build.mkdir()
        for f in (H/'source').iterdir():shutil.copyfile(f,d/f.name)
        oldbin=T/'build'/name/'program.bin';oldelf=T/'build'/name/'program.elf';assert sha(oldbin)==oldart['bin_sha'] and sha(oldelf)==oldart['ELF_sha']
        shutil.copyfile(oldbin,build/'program.bin');shutil.copyfile(oldelf,build/'program.elf')
        init=T/'cases'/(name+'-N16')/'source/init_tables.svh';shutil.copyfile(init,d/'init_tables.svh')
        # Independent full byte roundtrip, not just copied-file hashes.
        text=init.read_text();arrays={}
        for key in ['ROM','RAM']:
            body=re.search(rf'{key}_BITS\s*=\s*\{{(.*?)\}};',text,re.S);assert body
            arrays[key]=int(''.join(re.findall(r"4096'h([0-9a-fA-F]+)",body[1])),16).to_bytes(32768,'little')
        image=oldbin.read_bytes();assert arrays['ROM']==image+bytes(32768-len(image)) and arrays['RAM']==bytes([0xa5])*32768
        oldcheck=read(T/'runs'/(name+'-N16')/'check-result-v2.json');assert oldcheck['status']=='PASS'
        report=T/'runs'/(name+'-N16')/'ram-output.txt';assert report.stat().st_size==oldcheck['detail']['report_bytes']
        phase=oldart['symbols']['timing_phase'];assert 0x10000<=phase<0x18000
        cases[tid]=dict(image=str(build/'program.bin'),bytes=len(image),bin_sha256=sha(oldbin),ELF_sha256=sha(oldelf),INIT_sha256=sha(init),phase_address=phase,
            expected_raw_ticks=oldcheck['detail']['raw_ticks'],expected_stamps=oldcheck['detail']['stamps'],expected_UART_bytes=report.stat().st_size,expected_report_sha256=sha(report),
            old_run=str(T/'runs'/(name+'-N16')),raw_tick_equality='prior baseline comparison after independent timer/architecture checking',gpio_keys=0,n=234)
        output=H/'compile'/(tid+'.vvp')
        argv=[lib.IVL,'-B',lib.LIB,'-g2012','-Wall','-DM0_VERIFY','-I',d,'-I',M/'verification','-s','tb_board_coremark',f'-Ptb_board_coremark.PHASE_ADDR={phase}','-o',output,*list(d.glob('*.v')),*list(d.glob('*.sv')),H/'tests/tb_board_coremark.sv',lib.VENDOR/'GTP_DRM18K_E1.v',lib.VENDOR/'GTP_GRS.v']
        targets.append(dict(id=tid,argv=list(map(str,argv)),output=str(output)))
    save(H/'frozen-case-plan.json',dict(cases=cases,max_physical_cycles=6000000,run_seconds=360,compile_seconds=120,file_cap_bytes=256*1024*1024,
        waveform='native window VCD + continuous independent public UART transition text, no full-run native VCD claim',formal_score=False))
    # The known-correct v2 retains BSS phase0, every legal event and physical time.
    tree=ast.parse((T/'check_timed_v2.py').read_text());parts=[ast.get_source_segment((T/'check_timed_v2.py').read_text(),n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['data_row','counter_pre','check']]
    funcs='\n\n'.join(parts).replace('0 if cycle<16 else 0x3c if cycle<4096 else 0xc3','0').replace('0 if c<16 else 0x3c if c<4096 else 0xc3','0')
    header="from pathlib import Path\nimport json,re,sys,hashlib\nsys.dont_write_bytecode=True\nH=Path(__file__).resolve().parent\nsys.path.insert(0,str(H/'models'))\nimport stage_coremark as s\nfrom cpu_program_reference import Reference\nfrom peripheral_checker import ContractModel,decode_frames\n"
    (H/'check_coremark.py').write_text(header+funcs+'\n',encoding='utf-8')
    save(H/'compile-plan.json',dict(maximum=2,fail_fast=True,timeout_seconds=120,only_compile=True,targets=targets))
    originals={x['path']:x for x in read(B/'frozen.json')['files']}
    for f in [*H.rglob('*'),*(B/'source').iterdir(),T/'check_timed_v2.py',*[(T/'runs'/(name+'-N16')/f) for name in ['performance','validation'] for f in ['check-result-v2.json','ram-output.txt']]]:
        if f.is_file():originals[str(f)]=dict(path=str(f),sha256=sha(f))
    save(H/'frozen.json',dict(files=list(originals.values())))
    print('Frozen13 RTL/two exact images/CRCs/v2 checker; 0 new compilation or DUT',flush=True)
def compiles():
    protect();assert not ctypes.windll.shell32.IsUserAnAdmin();rows=[]
    for t in read(H/'compile-plan.json')['targets']:
        r=bounded(t['argv'],H,'compile-'+t['id'],120);okay=r['returncode']==0 and not r['timed_out'] and not r['cap'] and Path(t['output']).is_file()
        rows.append(dict(id=t['id'],status='PASS' if okay else 'FAIL',process=r,output=t['output'],sha256=sha(t['output']) if okay else None));print(t['id'],rows[-1]['status'],flush=True)
        if not okay:break
    save(H/'compile-result.json',dict(status='PASS' if len(rows)==2 and all(x['status']=='PASS' for x in rows) else 'STOPPED',rows=rows,protected=protect()))
def run():
    c=read(H/'compile-result.json');assert c['status']=='PASS';protect();rows=[]
    import check_coremark
    for t in c['rows']:
        assert sha(t['output'])==t['sha256'];tid=t['id'];d=H/'runs'/tid;d.mkdir()
        r=bounded([lib.VVP,'-N','-M-','-M'+str(lib.LIB),t['output'],'+MAX_CYCLES=6000000'],d,'run-'+tid,360)
        save(d/'process.json',r);shutil.copyfile(r['stdout'],d/'stdout.log');print(tid,'DUT_EXIT',r['returncode'],'seconds',r['elapsed_seconds'],'checking real evidence',flush=True)
        assert r['returncode']==0 and not r['timed_out'] and not r['cap'],r
        result=check_coremark.check(tid);save(d/'check-result.json',result);assert result['status']=='PASS',result['errors']
        plan=read(H/'frozen-case-plan.json')['cases'][tid];assert result['detail']['raw_ticks']==plan['expected_raw_ticks'] and result['detail']['stamps']==plan['expected_stamps']
        assert sha(d/'ram-output.txt')==plan['expected_report_sha256']
        rows.append(dict(id=tid,status='PASS',process=r,check=result));print(tid,'FULL_STATE_ORDERED_EVENTS_TIMING_UART_PASS',flush=True)
    save(H/'simulation-result.json',dict(status='PASS',new_DUT_runs=2,rows=rows,protected=protect(),formal_score=False))
if __name__=='__main__':{'prepare':prepare,'compile':compiles,'run':run,'verify':lambda:print(protect())}[sys.argv[1]]()
