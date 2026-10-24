"""Mainline stage runner: fixed inputs, bounded processes, no incoming entrypoints."""
from pathlib import Path
import sys,json,hashlib,subprocess,time,importlib.util,shutil,struct,re,ctypes,difflib
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
OLD=P/'work/system/2026-10-24-soc-txgpio-m1/integration-0030-v1'
CM=P/'work/system/2026-10-23-coremark-correctness-m1'
T=P/'tools/iverilog-13.0-msys2-ucrt64/ucrt64';IVL=T/'bin/iverilog.exe';VVP=T/'bin/vvp.exe';LIB=T/'lib/ivl'
VENDOR=Path('D:/PDS/PDS_2022.2-SP6.4/arch/vendor/pango/verilog/simulation')
GCC=P/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin'
def sha(p):
    d=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):d.update(b)
    return d.hexdigest().upper()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
def verify_originals():
    rows=read(H/'protected-originals.json')['files'];assert all(sha(x['path'])==x['sha256'] for x in rows)
    for n in ['cpu.v','alu.v','control.v','regfile.v','memory_model.sv','local_regif_txgpio_m1.v','uart_tx.v','gpio_core.v']:
        assert sha(H/'source'/n)==sha(H/'source-before'/n)
    return len(rows)
def bounded(argv,cwd,name,seconds):
    folder=H/'logs'/name;folder.mkdir();start=time.monotonic();timed=cap=False;cleanup=None
    with (folder/'stdout.log').open('xb') as out,(folder/'stderr.log').open('xb') as err:
        p=subprocess.Popen(list(map(str,argv)),cwd=cwd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,
            creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        while p.poll() is None:
            timed=time.monotonic()-start>seconds
            cap=any((Path(cwd)/n).exists() and (Path(cwd)/n).stat().st_size>m*1024*1024 for n,m in [('trace.log',256),('bus.log',128),('wave.vcd',128)])
            if timed or cap:
                try:
                    q=subprocess.run(['C:/Windows/System32/taskkill.exe','/PID',str(p.pid),'/T','/F'],capture_output=True,timeout=8)
                    cleanup=dict(native_rc=q.returncode,tree_state='NOT_INDEPENDENTLY_ENUMERATED_NO_SUCCESS_CLAIM')
                except Exception as e:cleanup=dict(error=str(e),tree_state='UNKNOWN')
                break
            time.sleep(.025)
        try:rc=p.wait(timeout=2)
        except subprocess.TimeoutExpired:rc=None
    result=dict(argv=list(map(str,argv)),cwd=str(cwd),returncode=rc,timed_out=timed,cap=cap,cleanup=cleanup,
        elapsed_seconds=round(time.monotonic()-start,6),timeout_seconds=seconds,
        stdout=str(folder/'stdout.log'),stderr=str(folder/'stderr.log'))
    save(folder/'process.json',result);return result
def log(p):
    with Path(p).open('rb') as f:b=f.read(8*1024*1024+1)
    assert len(b)<=8*1024*1024;return b.decode('utf-8',errors='replace').replace('\r\n','\n')
def elf_tools():
    spec=importlib.util.spec_from_file_location('elf',P/'work/system/2026-10-23-c-boot-m1/check_c_boot.py')
    e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e);return e
def init_table(image,path):
    words=[int.from_bytes(image[i:i+4],'little') for i in range(0,len(image),4)];assert len(image)%4==0
    with path.open('x',encoding='ascii') as f:
        for name,data in [('ROM',words+[0]*(8192-len(words))),('RAM',[0xa5a5a5a5]*8192)]:
            text=''.join(f'{v:08x}' for v in reversed(data));chunks=[text[i:i+1024] for i in range(0,len(text),1024)]
            f.write(f'localparam [262143:0] {name}_BITS = {{'+',\n'.join("4096'h"+c for c in chunks)+'};\n')
        f.write('localparam integer ROM_BYTES=32768, RAM_BYTES=32768, RAM_BASE=65536;\n')
def build():
    verify_originals();e=elf_tools();installed={Path(x['path']):x['sha256'] for x in read(P/'work/toolchain-readiness/2026-10-22-xpack-rv32i/installed-files.json')}
    for n in ['gcc','objcopy','objdump','readelf','nm']:assert sha(GCC/f'riscv-none-elf-{n}.exe')==installed[GCC/f'riscv-none-elf-{n}.exe']
    artifacts=[]
    for name in ['smoke','performance','validation']:
        d=H/'build'/name;d.mkdir();fw=H/'firmware'
        flags=['-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-fno-common','-fno-pie','-fno-stack-protector',
            '-fno-unwind-tables','-fno-asynchronous-unwind-tables','-mno-relax','-msmall-data-limit=0','-Wall','-Wextra','-Werror',
            '-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,--build-id=none','-Wl,-T,'+str(fw/'link.ld'),'-Wl,-Map,'+str(d/'program.map'),
            '-I'+str(fw),'-I'+str(H/'port'),'-I'+str(H/'upstream')]
        sources=[fw/'start.S',fw/'timer_smoke.c'] if name=='smoke' else [fw/'start.S',*sorted((H/'upstream').glob('*.c')),H/'port/core_portme.c']
        if name!='smoke':flags+=['-DTOTAL_DATA_SIZE=2000','-DITERATIONS=1','-D'+name.upper()+'_RUN=1']
        commands=[('compile',[GCC/'riscv-none-elf-gcc.exe',*flags,'-o',d/'program.elf',*sources,'-lgcc']),
            ('objcopy',[GCC/'riscv-none-elf-objcopy.exe','-O','binary',d/'program.elf',d/'program.bin']),
            ('objdump',[GCC/'riscv-none-elf-objdump.exe','-d','-M','no-aliases',d/'program.elf']),
            ('readelf',[GCC/'riscv-none-elf-readelf.exe','-h','-A','-l','-sW',d/'program.elf']),
            ('undefined',[GCC/'riscv-none-elf-nm.exe','-u',d/'program.elf'])]
        records=[]
        for kind,argv in commands:
            r=bounded(argv,d,'build-'+name+'-'+kind,60 if kind=='compile' else 20);records.append(r)
            if r['returncode']!=0 or r['timed_out'] or r['cap']:
                save(H/'build-result.json',dict(status='STOPPED',program=name,records=records));raise RuntimeError('C build failed; inspect original logs')
        image=(d/'program.bin').read_bytes();symbols=e.elf_symbols(d/'program.elf');raw=(d/'program.elf').read_bytes()
        assert raw[:7]==b'\x7fELF\x01\x01\x01' and struct.unpack_from('<H',raw,18)[0]==243 and struct.unpack_from('<I',raw,36)[0]==0
        assert len(image)<=32768 and len(image)%4==0 and symbols['__bss_end']<=0x16000 and symbols['__stack_top']==0x18000
        assert not log(records[-1]['stdout']).strip()
        decoded=re.findall(r'^\s*([0-9a-f]+):\s+([0-9a-f]{8})\s+([a-z0-9.]+)',log(records[2]['stdout']),re.M)
        allowed={'lui','auipc','jal','jalr','beq','bne','blt','bge','bltu','bgeu','lb','lh','lw','lbu','lhu','sb','sh','sw','add','sub','sll','slt','sltu','xor','srl','sra','or','and','addi','slti','sltiu','xori','ori','andi','slli','srli','srai','ebreak'}
        assert decoded and all(x[2] in allowed for x in decoded)
        artifacts.append(dict(id=name,bytes=len(image),symbols=symbols,bin_sha=sha(d/'program.bin'),ELF_sha=sha(d/'program.elf'),commands=records))
    save(H/'build-result.json',dict(status='PASS_BUILD_ONLY_NOT_EXECUTED',artifacts=artifacts));print([(x['id'],x['bytes']) for x in artifacts])
def freeze():
    verify_originals();built=read(H/'build-result.json');assert built['status']=='PASS_BUILD_ONLY_NOT_EXECUTED'
    targets=[dict(id='unit',argv=list(map(str,[IVL,'-B',LIB,'-g2012','-Wall','-s','tb_timer_unit','-o',H/'compile/unit.vvp',H/'source/cycle_counter64.sv',H/'source/soc_data_adapter.sv',H/'tests/tb_timer_unit.sv'])),output=str(H/'compile/unit.vvp'))]
    artifacts={x['id']:x for x in built['artifacts']}
    for name,n in [('baseline',16),('baseline',234),('smoke',16),('performance',16),('validation',16)]:
        tid=f'{name}-N{n}';d=H/'cases'/tid;d.mkdir();source=d/'source';source.mkdir()
        for p in (H/'source').iterdir():shutil.copyfile(p,source/p.name)
        if name=='baseline':image=(OLD.parent/'build/soc.bin').read_bytes();symbols=read(OLD.parent/'firmware-artifacts.json')['symbols']
        else:image=(H/'build'/name/'program.bin').read_bytes();symbols=artifacts[name]['symbols']
        init_table(image,source/'init_tables.svh');shutil.copyfile(H/'tests/tb_timed_system.sv',source/'tb_timed_system.sv')
        out=H/'compile'/(tid+'.vvp');names=['cycle_counter64.sv','local_regif_txgpio_m1.v','uart_tx.v','gpio_core.v','cpu.v','alu.v','control.v','regfile.v','memory_model.sv','soc_data_adapter.sv','soc_top.sv','tb_timed_system.sv']
        argv=[IVL,'-B',LIB,'-g2012','-Wall','-I',source,'-s','tb_timed_system',f'-Ptb_timed_system.N={n}',f'-Ptb_timed_system.PHASE_ADDR={symbols.get("timing_phase",0)}','-o',out,*[source/n for n in names],VENDOR/'GTP_DRM18K_E1.v',VENDOR/'GTP_GRS.v']
        targets.append(dict(id=tid,argv=list(map(str,argv)),output=str(out),program=name,N=n))
    save(H/'compile-plan.json',dict(maximum=6,each_timeout_seconds=90,fail_fast=True,compile_only=True,targets=targets))
    files=set(p for p in H.rglob('*') if p.is_file());files.update([IVL,VVP,VENDOR/'GTP_DRM18K_E1.v',VENDOR/'GTP_GRS.v'])
    save(H/'frozen.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(files)]))
    for n in ['soc_top.sv','soc_data_adapter.sv']:
        with (H/(n+'.diff')).open('x',encoding='utf-8') as f:f.writelines(difflib.unified_diff((H/'source-before'/n).read_text(encoding='utf-8-sig').splitlines(True),(H/'source'/n).read_text().splitlines(True),fromfile='source-before/'+n,tofile='source/'+n))
    print('Frozen 6 exact compile-only targets; no compiler or DUT executed by freeze')
def frozen():
    rows=read(H/'frozen.json')['files'];assert all(sha(x['path'])==x['sha256'] for x in rows);return len(rows)
def compile_all():
    frozen();assert not ctypes.windll.shell32.IsUserAnAdmin();rows=[]
    for t in read(H/'compile-plan.json')['targets']:
        p=bounded(t['argv'],H,'compile-'+t['id'],90)
        ok=p['returncode']==0 and not p['timed_out'] and not p['cap'] and Path(t['output']).is_file()
        rows.append(dict(id=t['id'],status='PASS' if ok else 'FAIL',process=p,output=t['output'],sha256=sha(t['output']) if Path(t['output']).is_file() else None))
        print(t['id'],rows[-1]['status'],flush=True)
        if not ok:break
    save(H/'compile-result.json',dict(status='PASS_COMPILE_ONLY' if len(rows)==6 and all(x['status']=='PASS' for x in rows) else 'STOPPED',rows=rows,protected=frozen()))
def run_one(tid):
    frozen();c=next(x for x in read(H/'compile-result.json')['rows'] if x['id']==tid);assert c['status']=='PASS' and sha(c['output'])==c['sha256']
    d=H/'runs'/tid;d.mkdir();r=bounded([VVP,'-N','-M-','-M'+str(LIB),c['output'],'+MAX_CYCLES=10000000'],d,'run-'+tid,240 if tid.startswith(('performance','validation')) else 45)
    save(d/'process.json',r);assert r['returncode']==0 and not r['timed_out'] and not r['cap'],r
    shutil.copyfile(r['stdout'],d/'stdout.log');print(tid,'PROCESS_ENDED_NOT_FUNCTIONAL_PASS',r['elapsed_seconds'],flush=True)
if __name__=='__main__':
    {'build':build,'freeze':freeze,'compile':compile_all,'verify':lambda:print(verify_originals(),frozen()),'run':lambda:run_one(sys.argv[2])}[sys.argv[1]]()
