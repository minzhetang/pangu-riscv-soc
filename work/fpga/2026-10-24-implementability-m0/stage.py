"""Approved M0: fixed source copies, independent checks, bounded CLI; no hardware."""
from pathlib import Path
import sys,json,hashlib,shutil,re,ast,subprocess,time,ctypes,difflib,types,importlib.util
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
B=P/'work/system/2026-10-24-timed-coremark-m1';M=P/'work/system/2026-10-24-memory-map-m2-v2'
OLD=P/'work/system/2026-10-24-soc-txgpio-m1/integration-0030-v1'
TOOLS=P/'tools/iverilog-13.0-msys2-ucrt64/ucrt64';IVL=TOOLS/'bin/iverilog.exe';VVP=TOOLS/'bin/vvp.exe';LIB=TOOLS/'lib/ivl'
VENDOR=Path('D:/PDS/PDS_2022.2-SP6.4/arch/vendor/pango/verilog/simulation')
PDS=Path('D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def save(p,o):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def extract(path,names,ns):
    tree=ast.parse(Path(path).read_text(encoding='utf-8-sig'));nodes=[x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name in names]
    assert {n.name for n in nodes}==set(names);exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns);return ns
def protect():
    r=read(H/'frozen.json');assert all(sha(x['path'])==x['sha256'] for x in r['files']);return len(r['files'])
def bounded(argv,cwd,name,limit):
    d=H/'logs'/name;d.mkdir(exist_ok=False);start=time.monotonic();timed=False;cap=False
    with (d/'stdout.log').open('xb') as out,(d/'stderr.log').open('xb') as err:
        proc=subprocess.Popen(list(map(str,argv)),cwd=cwd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
        while proc.poll() is None:
            timed=time.monotonic()-start>limit
            cap=any((Path(cwd)/n).exists() and (Path(cwd)/n).stat().st_size>256*1024*1024 for n in ['trace.log','bus.log','wave.vcd'])
            if timed or cap:
                kill=subprocess.run(['C:/Windows/System32/taskkill.exe','/PID',str(proc.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=8)
                save(d/'cleanup.json',dict(returncode=kill.returncode,tree_verified='NOT_INDEPENDENTLY_ENUMERATED'));break
            time.sleep(.1)
        try:rc=proc.wait(timeout=2)
        except subprocess.TimeoutExpired:rc=None
    r=dict(argv=list(map(str,argv)),cwd=str(cwd),returncode=rc,returncode_hex=None if rc is None else f'0x{rc&0xffffffff:08X}',timed_out=timed,cap=cap,elapsed_seconds=round(time.monotonic()-start,6),timeout_seconds=limit,stdout=str(d/'stdout.log'),stderr=str(d/'stderr.log'))
    save(d/'process.json',r);return r
def log(p):return Path(p).read_text(encoding='utf-8-sig',errors='replace').replace('\r\n','\n')
def table(rom,ram,path):
    assert len(rom)==len(ram)==8192
    with path.open('x',encoding='ascii') as f:
        for name,words in [('ROM',rom),('RAM',ram)]:
            value=''.join(f'{x&0xffffffff:08x}' for x in reversed(words));chunks=[value[i:i+1024] for i in range(0,len(value),1024)]
            f.write(f'localparam [262143:0] {name}_BITS = {{'+',\n'.join("4096'h"+c for c in chunks)+'};\n')
        f.write('localparam integer ROM_BYTES=32768,RAM_BYTES=32768,RAM_BASE=65536;\n')
def prepare():
    for x in read(B/'postflight.json')['source_SHA']:assert sha(B/'source'/x['file'])==x['sha256']
    for n in ['source-before','source','verification','models','cases','compile','runs','logs','build','pds']:(H/n).mkdir(exist_ok=False)
    save(H/'APPROVAL.json',dict(date_beijing='2026-10-24',decision='D129',source='User explicit 同意 after exact M0 request',scope_file=str(P/'deliveries/mainline-fpga-implementability-scope-2026-10-24-v1/IMPLEMENTATION_SCOPE.md'),scope_sha=sha(P/'deliveries/mainline-fpga-implementability-scope-2026-10-24-v1/IMPLEMENTATION_SCOPE.md'),approved=['own production-memory view','minimal source/engineering integration','necessary bounded simulation','PDS CLI compile/synthesis/map/pnr/timing'],forbidden=['bitstream','hardware/server/JTAG/Flash','CPU or B RTL changes','SCBV/power/thermal','new tools/license configuration']))
    for f in (B/'source').iterdir():
        if f.is_file():shutil.copyfile(f,H/'source-before'/f.name);shutil.copyfile(f,H/'source'/f.name)
    old=(H/'source-before/memory_model.sv').read_text();s=old
    decl='    wire [31:0] rom[0:8191],ram[0:8191];'
    assert s.count(decl)==1;s=s.replace(decl,'`ifdef M0_VERIFY\n    `include "memory_observe_decl.svh"\n`endif')
    (H/'verification/memory_observe_decl.svh').write_text(decl+'\n',encoding='ascii')
    start=s.index('        // synthesis translate_off');end=s.index('        // synthesis translate_on',start)+len('        // synthesis translate_on')
    block=s[start:end];(H/'verification/memory_observe_bank.svh').write_text(block+'\n',encoding='ascii')
    s=s[:start]+'`ifdef M0_VERIFY\n        `include "memory_observe_bank.svh"\n`endif'+s[end:]
    start=s.index('        // synthesis translate_off');end=s.index('        // synthesis translate_on',start)+len('        // synthesis translate_on')
    block=s[start:end];(H/'verification/memory_protocol_checks.svh').write_text(block+'\n',encoding='ascii')
    s=s[:start]+'`ifdef M0_VERIFY\n        `include "memory_protocol_checks.svh"\n`endif'+s[end:]
    s=s.replace('    initial begin\n        if(LATENCY!=1)', '`ifdef M0_VERIFY\n    initial begin\n        if(LATENCY!=1)').replace('    end\nendmodule','    end\n`endif\nendmodule')
    assert '.mem[' not in s and '$fatal' not in s.replace('$fatal(1,"only fixed one-edge memory supported");','')
    (H/'source/memory_model.sv').write_text(s,encoding='ascii')
    with (H/'SOURCE_DIFF.patch').open('x',encoding='utf-8') as f:f.writelines(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='source-before/memory_model.sv',tofile='source/memory_model.sv'))
    # Expand only our new verification includes, compare EXACT original code.
    expanded=s
    for name in ['memory_observe_decl.svh','memory_observe_bank.svh','memory_protocol_checks.svh']:
        expanded=re.sub(r'`ifdef M0_VERIFY\n[ \t]*`include "'+name+r'"\n`endif',lambda m:(H/'verification'/name).read_text().rstrip('\n'),expanded)
    expanded=expanded.replace('`ifdef M0_VERIFY\n','').replace('`endif\n','')
    assert re.sub(r'\s+','',expanded)==re.sub(r'\s+','',old),'M0_VERIFY expansion must preserve all tokens'
    save(H/'equivalence.json',dict(verification_expansion_token_equal=True,functional_binding_tokens_changed=False,CPU_and_other_10_sources_unchanged=True,CoreMark_rerun_needed=False))
    for n in ['check_timed_v2.py','cpu_program_reference.py','peripheral_checker.py']:shutil.copyfile(B/n,H/'models'/n)
    shutil.copyfile(B/'build-result.json',H/'build-result.json');shutil.copytree(B/'build/smoke',H/'build/smoke')
    targets=[]
    for tid in ['baseline-N16','baseline-N234','smoke-N16','selftest']:
        d=H/'cases'/tid;d.mkdir();src=d/'source';src.mkdir()
        for f in (H/'source').iterdir():shutil.copyfile(f,src/f.name)
        if tid=='selftest':
            table([((0x31415927+i*0x10103)^(i<<19))&0xffffffff for i in range(8192)],[((0xdeadbeef-i*0x30107)^(i<<17))&0xffffffff for i in range(8192)],src/'init_tables.svh')
            shutil.copyfile(M/'tb_full_memory.sv',src/'tb_full_memory.sv');top='tb_full_memory';extra=[];files=[src/'memory_model.sv',src/'tb_full_memory.sv']
        else:
            shutil.copyfile(B/'cases'/tid/'source/init_tables.svh',src/'init_tables.svh');shutil.copyfile(B/'tests/tb_timed_system.sv',src/'tb_timed_system.sv')
            n=int(tid.split('-N')[1]);top='tb_timed_system';extra=[f'-Ptb_timed_system.N={n}'];files=list(src.glob('*.v'))+list(src.glob('*.sv'))
        output=H/'compile'/(tid+'.vvp');argv=[IVL,'-B',LIB,'-g2012','-Wall','-DM0_VERIFY','-I',src,'-I',H/'verification','-s',top,*extra,'-o',output,*files,VENDOR/'GTP_DRM18K_E1.v',VENDOR/'GTP_GRS.v']
        targets.append(dict(id=tid,argv=list(map(str,argv)),output=str(output)))
    save(H/'compile-plan.json',dict(maximum=4,each_timeout_seconds=120,fail_fast=True,only_compile=True,targets=targets))
    # Full CoreMark image for physical mapping avoids a trivial demo-only image.
    pd=H/'pds';src=pd/'source';src.mkdir()
    for f in (H/'source').iterdir():shutil.copyfile(f,src/f.name)
    shutil.copyfile(B/'cases/performance-N16/source/init_tables.svh',src/'init_tables.svh')
    # Flatten ONLY own include to avoid a tool-specific implicit include path.
    f=src/'memory_model.sv';x=f.read_text();x=x.replace('    `include "init_tables.svh"',(src/'init_tables.svh').read_text())
    x=re.sub(r'`ifdef M0_VERIFY\n.*?`endif\n','',x,flags=re.S);assert '.mem[' not in x and '$fatal' not in x;f.write_text(x,encoding='ascii')
    (pd/'clock_27mhz.fdc').write_text('create_clock -name {clk_27mhz} -period {37.037037} -waveform {0.000000 18.518519} [get_ports {clk}]\n',encoding='ascii')
    tcl=['set m0_dir [file normalize [file dirname [info script]]]','cd $m0_dir']
    tcl += [f'add_design [file join $m0_dir source {f.name}]' for f in src.iterdir() if f.suffix in ['.v','.sv']]
    tcl += ['add_constraint [file join $m0_dir clock_27mhz.fdc]','set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676','compile -top_module soc_top','synthesize -ads -selected_syn_tool_opt 2','dev_map','pnr','report_timing']
    (pd/'build.tcl').write_text('\n'.join(tcl)+'\n',encoding='ascii')
    assert not any(v in (pd/'build.tcl').read_text() for v in ['gen_bit','jtag','cfg_','server','scbv'])
    originals={f for f in B.rglob('*') if f.is_file() and f.suffix in ['.v','.sv','.svh','.py','.json','.bin','.elf','.c','.h','.S','.ld']}
    files=originals|{f for f in H.rglob('*') if f.is_file()}|{IVL,VVP,PDS,VENDOR/'GTP_DRM18K_E1.v',VENDOR/'GTP_GRS.v',M/'tb_full_memory.sv'}
    save(H/'frozen.json',dict(files=[dict(path=str(f),sha256=sha(f)) for f in sorted(files)]))
    print('Prepared 4 fixed Icarus targets and PDS CLI source; verification tokens equal; 0 new DUT')
def compiles():
    protect();assert not ctypes.windll.shell32.IsUserAnAdmin();rows=[]
    for t in read(H/'compile-plan.json')['targets']:
        r=bounded(t['argv'],H,'compile-'+t['id'],120);ok=r['returncode']==0 and not r['timed_out'] and not r['cap'] and Path(t['output']).is_file()
        rows.append(dict(id=t['id'],status='PASS' if ok else 'FAIL',process=r,output=t['output'],sha256=sha(t['output']) if ok else None));print(t['id'],rows[-1]['status'],flush=True)
        if not ok:break
    save(H/'compile-result.json',dict(status='PASS' if len(rows)==4 and all(x['status']=='PASS' for x in rows) else 'STOPPED',rows=rows,protected_files=protect()))
def checker(tid):
    sys.path.insert(0,str(H/'models'))
    from cpu_program_reference import Reference
    from peripheral_checker import ContractModel,decode_frames
    ns=dict(H=H,s=sys.modules[__name__],Reference=Reference,ContractModel=ContractModel,decode_frames=decode_frames,re=re,json=json,hashlib=hashlib)
    extract(H/'models/check_timed_v2.py',{'data_row','counter_pre','check'},ns)
    return ns['check'](tid)
def run():
    c=read(H/'compile-result.json');assert c['status']=='PASS';protect();rows=[]
    for t in c['rows']:
        assert sha(t['output'])==t['sha256'];tid=t['id']
        if tid=='selftest':
            for bad in [0,1,2,3]:
                d=H/'runs'/f'selftest-{bad}';d.mkdir();r=bounded([VVP,'-N','-M-','-M'+str(LIB),t['output'],f'+BAD={bad}'],d,f'run-selftest-{bad}',45);text=log(r['stdout'])+log(r['stderr'])
                ok=(r['returncode']==0 and 'MAP_SELFTEST_PASS checks=49416 write_edges=122' in text) if bad==0 else (r['returncode']!=0 and 'MEMORY_PROTOCOL' in text and 'NEGATIVE_NOT_REJECTED' not in text)
                assert ok and not r['timed_out'] and not r['cap'],r
                rows.append(dict(id=f'selftest-{bad}',status='PASS' if bad==0 else 'EXPECTED_REJECTION',process=r));print(rows[-1]['id'],rows[-1]['status'],flush=True)
        else:
            d=H/'runs'/tid;d.mkdir();r=bounded([VVP,'-N','-M-','-M'+str(LIB),t['output'],'+MAX_CYCLES=100000'],d,'run-'+tid,45)
            save(d/'process.json',r);shutil.copyfile(r['stdout'],d/'stdout.log');result=checker(tid);save(d/'check-result.json',result)
            assert result['status']=='PASS',result['errors'];rows.append(dict(id=tid,status='PASS',process=r,check=result));print(tid,'FULL_STATE_ORDERED_EVENTS_PASS',flush=True)
    save(H/'simulation-result.json',dict(status='PASS',rows=rows,new_DUT_runs=len(rows),protected_files=protect()))
def pds():
    assert read(H/'simulation-result.json')['status']=='PASS';protect();assert not ctypes.windll.shell32.IsUserAnAdmin()
    d=H/'pds';assert not any((d/n).exists() for n in ['compile','synthesize','device_map','place_route','report_timing'])
    r=bounded([PDS,'-file',d/'build.tcl'],d,'pds-flow',1200);save(H/'pds-process.json',r)
    print('PDS_PROCESS_EXITED',r['returncode_hex'],'inspect fresh reports; NOT success claim',flush=True)
if __name__=='__main__':{'prepare':prepare,'compile':compiles,'run':run,'pds':pds,'verify':lambda:print(protect())}[sys.argv[1]]()
