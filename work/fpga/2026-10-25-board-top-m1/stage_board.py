"""D131 bounded pure-software board adaptation; no bitstream/hardware actions."""
from pathlib import Path
import ast, ctypes, hashlib, importlib.util, json, re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2]
B=P/'work/fpga/2026-10-24-implementability-m0';T=P/'work/system/2026-10-24-timed-coremark-m1'
E=P/'work/fpga/2026-10-24-board-top-m1/evidence'
spec=importlib.util.spec_from_file_location('m0library',B/'stage.py');m=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=m;spec.loader.exec_module(m);m.H=H
read,save,sha,log,bounded=m.read,m.save,m.sha,m.log,m.bounded
GCC=P/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin'
def protect():return m.protect()
def prepare():
    for name in ['source-before','models-before','models','logs','build','compile','cases','runs','pds']:(H/name).mkdir(exist_ok=False)
    receipt=read(B/'postflight.json')['source'];assert len(receipt)==11
    for row in receipt:
        f=B/'source'/row['file'];assert sha(f)==row['sha256']
        assert not (H/'source'/f.name).exists()
        shutil.copyfile(f,H/'source'/f.name);shutil.copyfile(f,H/'source-before'/f.name)
    for name in ['start.S','link.ld']:shutil.copyfile(T/'firmware'/name,H/'firmware'/name)
    for name in ['cpu_program_reference.py','peripheral_checker.py','check_timed_v2.py']:
        shutil.copyfile(T/name,H/'models-before'/name)
        if name!='check_timed_v2.py':shutil.copyfile(T/name,H/'models'/name)
    save(H/'APPROVAL.json',dict(date_beijing='2026-10-25',decision='D131',user_reply='同意继续',
        scope='A-BOARD-TOP-M1: independent board top/reset/pins/UART/short software validation/PDS timing only',
        forbidden=['CPU/B functional changes','bitstream','hardware/server/JTAG/Flash','SCBV/power/thermal','install/GUI/license/environment changes']))
    pins={'clk':'D18','uart_tx':'C24',**{f'key_n[{i}]':p for i,p in enumerate(['C22','C23','B22','A22','B20'])},
          **{f'led[{i}]':p for i,p in enumerate(['A20','C18','C19','E18','A17','A18','C17','B17'])}}
    lines=[]
    for port,pin in pins.items():
        output=port.startswith(('uart','led'));attrs=dict(PAP_IO_DIRECTION='OUTPUT' if output else 'INPUT',PAP_IO_LOC=pin,PAP_IO_VCCIO='3.3',PAP_IO_STANDARD='LVCMOS33',PAP_IO_NONE='TRUE')
        if output:attrs.update(PAP_IO_DRIVE='8',PAP_IO_SLEW='SLOW')
        lines += [f'define_attribute {{p:{port}}} {{{k}}} {{{v}}}' for k,v in attrs.items()]
    (H/'pds/board_pins.fdc').write_text('\n'.join(lines)+'\n',encoding='ascii')
    (H/'pds/clock_27mhz.fdc').write_text('create_clock -name {clk_27mhz} -period {37.037037} -waveform {0.000000 18.518519} [get_ports {clk}]\n',encoding='ascii')
    save(H/'pin-plan.json',dict(pins=pins,source='T1 PDF23/43-44/50-51 plus original key_led/uart FDC',
        gpio='KEY1..4 pressed=1 in low nibble, high nibble 0',reset='KEY0 async assert, three-edge synchronous release; no debounce',
        baud=dict(clock_hz=27000000,clks_per_bit=234,nominal_baud=27000000/234,error_percent=(27000000/234/115200-1)*100),
        no_input_or_output_delay_invented=True,no_false_paths=True))
    tb=(T/'tests/tb_timed_system.sv').read_text()
    tb=tb.replace('module tb_timed_system #(parameter integer N=16,parameter integer PHASE_ADDR=0);','module tb_board_system;\n    localparam integer N=234,PHASE_ADDR=0;\n    integer key_pattern=5;reg [4:0] key_n=0;')
    tb=tb.replace('reg clk=0,rst_n=0;reg [7:0] gpio_in_async=0;','reg clk=0;wire rst_n=board_dut.sys_rst_n;\n    wire [7:0] gpio_in_async={4\'b0,~key_n[4:1]};')
    tb=re.sub(r'\bdut\.', 'board_dut.soc.', tb)
    tb=tb.replace('soc_top #(.CLKS_PER_BIT(N)) dut(.*);','board_top board_dut(.clk(clk),.key_n(key_n),.uart_tx(uart_tx),.led(gpio_out));\n    assign stopped=board_dut.soc.stopped;\n    assign write_error=board_dut.soc.write_error;\n    assign stop_kind=board_dut.soc.stop_kind;\n    assign stop_pc=board_dut.soc.stop_pc;')
    tb=tb.replace('always #5 clk=~clk;','// 37.037 ns period at 1 ps precision, nominal 27 MHz.\n    always begin #18.518;clk=1;#18.519;clk=0;end')
    tb=tb.replace('$dumpvars(1,tb_timed_system);','$dumpvars(1,tb_board_system);$dumpvars(1,board_dut);')
    tb=tb.replace('repeat(4)@(negedge clk);rst_n=1;',
        'if(!$value$plusargs("K=%d",key_pattern))key_pattern=5;\n        if(key_pattern!=5&&key_pattern!=12)$fatal(1,"UNFROZEN_KEYS");\n        key_n[4:1]=~key_pattern[3:0];key_n[0]=0;\n        repeat(4)@(negedge clk);key_n[0]=1;')
    old='''    always @(negedge clk)if(rst_n)begin
        if(cycle==15)gpio_in_async=8'h3c;
        if(cycle==4095)gpio_in_async=8'hc3;
    end
'''
    assert old in tb;tb=tb.replace(old,'')
    tb='\n'.join(l for l in tb.splitlines() if not l.strip().startswith(('if((cycle<=wave_until','if(cycle>wave_until')))+'\n'
    assert 'tb_timed_system' not in tb and 'gpio_in_async=' in tb and 'always #5' not in tb
    (H/'tests/tb_board_system.sv').write_text(tb,encoding='ascii')
    # New checker adapter, original independent sequential/peripheral models unchanged.
    tree=ast.parse((T/'check_timed_v2.py').read_text());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['data_row','counter_pre','check']]
    funcs='\n\n'.join(ast.get_source_segment((T/'check_timed_v2.py').read_text(),n) for n in nodes)
    funcs=funcs.replace("d=H/'runs'/tid;name,ns=tid.split('-N');n=int(ns);errors=[]", "d=H/'runs'/tid;name,ns=tid.split('-N');n=int(ns);k=s.read(H/'manual-plan.json')['cases'][tid]['key_pattern'];errors=[]")
    funcs=funcs.replace('0 if cycle<16 else 0x3c if cycle<4096 else 0xc3','k').replace('0 if c<16 else 0x3c if c<4096 else 0xc3','k')
    a=funcs.index('    art=None if name');b=funcs.index("    with (d/'trace.log')",a)
    funcs=funcs[:a]+"    art=s.read(H/'firmware-result.json');image=Path(art['program_bin']).read_bytes();symbols=art['symbols']\n"+funcs[b:]
    a=funcs.index("    if name=='baseline':");b=funcs.index("    eq('public UART all bytes",a)
    funcs=funcs[:a]+'''    plan=s.read(H/'manual-plan.json')['cases'][tid]
    eq('hand results',[word('results',i*4) for i in range(8)],plan['results'])
    eq('hand signature',word('signature'),plan['signature'])
    eq('GPIO every accepted write',[v for c,v in gpio],plan['GPIO_writes'])
    expected_bytes=plan['UART_bytes'];detail=dict(key_pattern=k)
'''+funcs[b:]
    header='''from pathlib import Path
import json,re,sys,hashlib
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'models'))
import stage_board as s
from cpu_program_reference import Reference
from peripheral_checker import ContractModel,decode_frames
'''
    (H/'check_board.py').write_text(header+funcs+'\n',encoding='utf-8')
    save(H/'manual-plan.json',dict(frozen_before_DUT=True,cases={f'board{k}-N234':dict(key_pattern=k,
        results=[0x13579bdf,0,k,0x5a,0x5a,0xa5,0,6],signature=0x424d3031,
        GPIO_writes=[0x5a,0x5a,0xa5],UART_bytes=list(b'B'+b'0123456789ABCDEF'[k:k+1]+b'\r\nAA'),
        all_RF_and_RAM='independent sequential model with independently predicted MMIO reads',
        stall_flush='independent model computed from actual legal instruction flow; not prefilled DUT counts') for k in [5,12]},
        reset_cases=['cold high input','async assert off-edge','no clock hold','three-edge release','bounce restart'],
        limits=dict(compile_seconds=120,run_seconds=45,system_cycles=100000,PDS_seconds=1200)))
    print('Prepared independent sources/checker/manual plan; no compilation or DUT yet')
def build():
    d=H/'build/board-v2';d.mkdir()
    flags=['-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-fno-common','-fno-pie','-fno-stack-protector','-fno-unwind-tables','-fno-asynchronous-unwind-tables','-mno-relax','-msmall-data-limit=0','-Wall','-Wextra','-Werror','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,--build-id=none','-Wl,-T,'+str(H/'firmware/link.ld'),'-Wl,-Map,'+str(d/'program.map'),'-o',d/'program.elf',H/'firmware/start.S',H/'firmware/board_smoke.c','-lgcc']
    commands=[('gcc',[GCC/'riscv-none-elf-gcc.exe',*flags]),('objcopy',[GCC/'riscv-none-elf-objcopy.exe','-O','binary',d/'program.elf',d/'program.bin']),('nm',[GCC/'riscv-none-elf-nm.exe','-n',d/'program.elf']),('objdump',[GCC/'riscv-none-elf-objdump.exe','-d','-M','no-aliases',d/'program.elf']),('readelf',[GCC/'riscv-none-elf-readelf.exe','-h','-A',d/'program.elf'])]
    rows=[]
    for name,argv in commands:
        r=bounded(argv,d,'firmware-v2-'+name,60);rows.append(r);assert r['returncode']==0 and not r['timed_out']
    attrs=log(rows[-1]['stdout']);assert 'ELF32' in attrs and 'little endian' in attrs and 'rv32i2p1' in attrs
    arch=re.search(r'Tag_RISCV_arch:\s*"([^"]+)"',attrs);assert arch and arch[1]=='rv32i2p1'
    symbols={}
    for line in log(rows[2]['stdout']).splitlines():
        match=re.fullmatch(r'([0-9a-fA-F]+)\s+\w\s+(\S+)',line)
        if match:symbols[match[2]]=int(match[1],16)
    image=(d/'program.bin').read_bytes();assert 0<len(image)<=32768
    save(H/'firmware-result.json',dict(status='C_BUILD_ONLY_NOT_DUT',program_bin=str(d/'program.bin'),bytes=len(image),symbols=symbols,bin_sha=sha(d/'program.bin'),ELF_sha=sha(d/'program.elf'),commands=rows,ISA=arch[1]))
    sys.path.insert(0,str(H/'models'));from cpu_program_reference import Reference
    model_rows=[]
    for k in range(16):
        gpio=[0];writes=[]
        def rd(pc,a):return {0x20000008:1,0x2000000c:gpio[0],0x20000010:k}[a]
        def wr(pc,a,v,mask):
            assert mask==15 and a in [0x20000000,0x2000000c];writes.append((a,v&255))
            if a==0x2000000c:gpio[0]=v&255
        ref=Reference(image,rd,wr)
        while not ref.stopped:ref.step()
        def word(sym,i=0):
            a=symbols[sym]-0x10000+i*4;return int.from_bytes(ref.ram[a:a+4],'little')
        expected=[0x13579bdf,0,k,0x5a,0x5a,0xa5,0,6]
        assert [word('results',i) for i in range(8)]==expected and word('signature')==0x424d3031
        assert ref.regs[10]==0 and ref.regs[2]==0x18000
        assert [v for a,v in writes if a==0x2000000c]==[0x5a,0x5a,0xa5]
        assert bytes(v for a,v in writes if a==0x20000000)==b'B'+b'0123456789ABCDEF'[k:k+1]+b'\r\nAA'
        model_rows.append(dict(key=k,status='PASS',steps=ref.steps,synthetic_STATUS_always_ready=True,DUT_run=False))
    save(H/'model-preflight.json',dict(status='PASS',rows=model_rows,DUT_runs=0))
    src=H/'cases/board/source';src.mkdir(parents=True)
    rom=image+bytes(32768-len(image));m.table([int.from_bytes(rom[i:i+4],'little') for i in range(0,32768,4)],[0xa5a5a5a5]*8192,src/'init_tables.svh')
    # Same full CoreMark image as F141 for resource/timing comparison, no new score.
    ps=H/'pds/source';ps.mkdir()
    for f in (H/'source').iterdir():shutil.copyfile(f,ps/f.name)
    shutil.copyfile(B/'pds/source/init_tables.svh',ps/'init_tables.svh')
    f=ps/'memory_model.sv';text=f.read_text();text=text.replace('    `include "init_tables.svh"',(ps/'init_tables.svh').read_text());text=re.sub(r'`ifdef M0_VERIFY\n.*?`endif\n','',text,flags=re.S);assert '.mem[' not in text and '$fatal' not in text;f.write_text(text,encoding='ascii')
    tcl=['set m1_dir [file normalize [file dirname [info script]]]','cd $m1_dir']
    tcl += [f'add_design [file join $m1_dir source {f.name}]' for f in ps.iterdir() if f.suffix in ['.v','.sv']]
    tcl += ['add_constraint [file join $m1_dir board_pins.fdc]','add_constraint [file join $m1_dir clock_27mhz.fdc]','set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676','compile -top_module board_top','synthesize -ads -selected_syn_tool_opt 2','dev_map','pnr','report_timing']
    (H/'pds/build.tcl').write_text('\n'.join(tcl)+'\n',encoding='ascii')
    targets=[]
    for tid,top,files in [('reset','tb_reset',[H/'source/board_reset_sync.sv',H/'tests/tb_reset.sv']),('board','tb_board_system',list((H/'source').glob('*.v'))+list((H/'source').glob('*.sv'))+[H/'tests/tb_board_system.sv',m.VENDOR/'GTP_DRM18K_E1.v',m.VENDOR/'GTP_GRS.v'])]:
        argv=[m.IVL,'-B',m.LIB,'-g2012','-Wall','-DM0_VERIFY','-I',src,'-I',B/'verification','-s',top,'-o',H/'compile'/(tid+'.vvp'),*files]
        targets.append(dict(id=tid,argv=list(map(str,argv)),output=str(H/'compile'/(tid+'.vvp'))))
    save(H/'compile-plan.json',dict(maximum=2,timeout=120,fail_fast=True,targets=targets))
    originals={x['path']:x for x in read(B/'frozen.json')['files']}
    files={f for f in H.rglob('*') if f.is_file()}|{GCC/('riscv-none-elf-'+n+'.exe') for n in ['gcc','objcopy','nm','objdump','readelf']}|{E/'archive-receipt.json'}
    for f in files:originals[str(f)]=dict(path=str(f),sha256=sha(f))
    save(H/'frozen.json',dict(files=list(originals.values())));print('C and 16 labelled model-only key cases passed; fixed two-target compile plan frozen')
def compiles():
    protect();assert not ctypes.windll.shell32.IsUserAnAdmin();rows=[]
    for t in read(H/'compile-plan.json')['targets']:
        r=bounded(t['argv'],H,'compile-'+t['id'],120);okay=r['returncode']==0 and not r['timed_out'] and Path(t['output']).is_file()
        rows.append(dict(id=t['id'],status='PASS' if okay else 'FAIL',process=r,output=t['output'],sha256=sha(t['output']) if okay else None));print(t['id'],rows[-1]['status'],flush=True)
        if not okay:break
    save(H/'compile-result.json',dict(status='PASS' if len(rows)==2 and all(r['status']=='PASS' for r in rows) else 'STOPPED',rows=rows,protected=protect()))
def run():
    c=read(H/'compile-result.json');assert c['status']=='PASS';protect();rows=[]
    for t in c['rows']:assert sha(t['output'])==t['sha256']
    reset=H/'runs/reset';reset.mkdir();r=bounded([m.VVP,'-N','-M-','-M'+str(m.LIB),H/'compile/reset.vvp'],reset,'run-reset',45)
    assert r['returncode']==0 and 'RESET_PASS checks=' in log(r['stdout']) and not r['timed_out'];rows.append(dict(id='reset',status='PASS',process=r))
    import check_board
    for k in [5,12]:
        tid=f'board{k}-N234';d=H/'runs'/tid;d.mkdir();r=bounded([m.VVP,'-N','-M-','-M'+str(m.LIB),H/'compile/board.vvp','+MAX_CYCLES=100000',f'+K={k}'],d,'run-'+tid,45)
        save(d/'process.json',r);shutil.copyfile(r['stdout'],d/'stdout.log');result=check_board.check(tid);save(d/'check-result.json',result)
        assert result['status']=='PASS',result['errors'];rows.append(dict(id=tid,status='PASS',process=r,check=result));print(tid,'FULL_STATE_ORDERED_EVENTS_PASS',flush=True)
    save(H/'simulation-result.json',dict(status='PASS',rows=rows,new_DUT_runs=3,protected=protect()))
def pds():
    assert read(H/'simulation-result.json')['status']=='PASS';protect();assert not ctypes.windll.shell32.IsUserAnAdmin()
    assert not (H/'pds/compile').exists();r=bounded([m.PDS,'-file',H/'pds/build.tcl'],H/'pds','pds-flow-once',1200)
    save(H/'pds-process.json',r);print('PDS exited',r['returncode_hex'],'inspect final reports, not success claim',flush=True)
if __name__=='__main__':{'prepare':prepare,'build':build,'compile':compiles,'run':run,'pds':pds,'verify':lambda:print(protect())}[sys.argv[1]]()
