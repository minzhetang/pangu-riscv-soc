"""D149: two-iteration calibration, unchanged F143 RTL and official algorithms."""
from pathlib import Path
import ast,hashlib,json,re,sys,shutil,subprocess,time,struct,ctypes,difflib,importlib.util
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;P=H.parents[2]
B=P/'work/fpga/2026-10-25-board-coremark-m1';T=P/'work/system/2026-10-24-timed-coremark-m1'
R=P/'work/analysis/2026-10-25-coremark-measurement-readiness-m0'
M=P/'work/fpga/2026-10-24-implementability-m0'
TOOLS=P/'tools/iverilog-13.0-msys2-ucrt64/ucrt64';IVL=TOOLS/'bin/iverilog.exe';VVP=TOOLS/'bin/vvp.exe';LIB=TOOLS/'lib/ivl'
GCC=P/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin';VENDOR=Path('D:/PDS/PDS_2022.2-SP6.4/arch/vendor/pango/verilog/simulation')
def sha(p):
    d=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):d.update(block)
    return d.hexdigest().upper()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,o):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def log(p):
    data=Path(p).read_bytes();assert len(data)<=8*1024*1024
    return data.decode('utf-8-sig').replace('\r\n','\n')
def protect():
    rows=read(H/'protected-originals.json')['files']
    for x in rows:assert sha(x['path'])==x['SHA256'],x['path']
    return len(rows)
def bounded(argv,cwd,name,seconds):
    d=H/'logs'/name;d.mkdir(exist_ok=False);start=time.monotonic();expired=cap=False;cleanup=None
    with (d/'stdout.log').open('xb') as out,(d/'stderr.log').open('xb') as err:
        proc=subprocess.Popen(list(map(str,argv)),cwd=cwd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
        while proc.poll() is None:
            expired=time.monotonic()-start>seconds
            cap=any((Path(cwd)/n).is_file() and (Path(cwd)/n).stat().st_size>256*1024*1024 for n in ['trace.log','bus.log','wave.vcd']) or any((d/n).stat().st_size>8*1024*1024 for n in ['stdout.log','stderr.log'])
            if expired or cap:
                try:
                    k=subprocess.run(['C:/Windows/System32/taskkill.exe','/PID',str(proc.pid),'/T','/F'],capture_output=True,timeout=8);cleanup=dict(returncode=k.returncode,tree_not_independently_verified=True,no_success_claim=True)
                except Exception as e:cleanup=dict(error=repr(e),no_success_claim=True)
                break
            time.sleep(.1)
        try:rc=proc.wait(timeout=2)
        except subprocess.TimeoutExpired:rc=None
    result=dict(argv=list(map(str,argv)),cwd=str(cwd),returncode=rc,returncode_hex=None if rc is None else f'0x{rc&0xffffffff:08X}',timed_out=expired,cap=cap,cleanup=cleanup,elapsed_seconds=round(time.monotonic()-start,6),timeout_seconds=seconds,stdout=str(d/'stdout.log'),stderr=str(d/'stderr.log'))
    save(d/'process.json',result);return result
def elf_symbols(p):
    data=Path(p).read_bytes();assert data[:7]==b'\x7fELF\x01\x01\x01'
    fields=struct.unpack_from('<HHIIIIIHHHHHH',data,16);assert fields[1]==243 and fields[3]==0 and fields[6]==0
    sections=[struct.unpack_from('<10I',data,fields[5]+i*fields[10]) for i in range(fields[11])];out={}
    for section in sections:
        if section[1]!=2:continue
        st=sections[section[6]];strings=data[st[4]:st[4]+st[5]]
        for offset in range(section[4],section[4]+section[5],section[9]):
            name,value,size,info,other,index=struct.unpack_from('<IIIBBH',data,offset);text=strings[name:].split(b'\0',1)[0].decode('utf-8')
            if text:out[text]=value
    return out
def initial_word(p,address):
    data=Path(p).read_bytes();off=struct.unpack_from('<I',data,28)[0];size,count=struct.unpack_from('<HH',data,42)
    for i in range(count):
        typ,foff,virt,physical,filesz,memsz,flags,align=struct.unpack_from('<8I',data,off+i*size)
        if typ==1 and virt<=address and address+4<=virt+filesz:return struct.unpack_from('<I',data,foff+address-virt)[0]
    raise AssertionError('no initial word')
def table(image,p):
    assert len(image)%4==0 and len(image)<=32768
    with p.open('x',encoding='ascii') as f:
        for name,data in [('ROM',image+bytes(32768-len(image))),('RAM',bytes([0xa5])*32768)]:
            value=data[::-1].hex();chunks=[value[i:i+1024] for i in range(0,len(value),1024)]
            f.write('localparam [262143:0] '+name+'_BITS = {'+',\n'.join("4096'h"+c for c in chunks)+'};\n')
        f.write('localparam integer ROM_BYTES=32768,RAM_BYTES=32768,RAM_BASE=65536;\n')
def prepare():
    for n in ['source','source-before','port','port-before','firmware','upstream','models','models-before','tests','build','compile','cases','runs','logs','oracles']:(H/n).mkdir(exist_ok=False)
    save(H/'APPROVAL.json',dict(date_beijing='2026-10-25',decision='D149',user_reply='同意，继续',scope=str(R/'NEXT_IMPLEMENTATION_SCOPE.md'),scope_SHA256=sha(R/'NEXT_IMPLEMENTATION_SCOPE.md'),stage='A-COREMARK-ITER2-M1',iterations=2,CPU_RTL_changes=False,new_DUT_maximum=2,formal_score=False,hardware='STOPPED'))
    rows=read(R/'INPUTS.json')['files'];base=read(P/'work/analysis/2026-10-25-prefetch-warning-m0/INPUTS.json')['source']
    for x in base:assert sha(x['path'])==x['SHA256']
    for p in (B/'source').iterdir():
        if p.is_file():
            for folder in ['source','source-before']:shutil.copyfile(p,H/folder/p.name)
    assert len(list((H/'source').iterdir()))==13
    for p in (T/'port').iterdir():
        if p.is_file():
            for folder in ['port','port-before']:shutil.copyfile(p,H/folder/p.name)
    for n in ['start.S','link.ld','timer.h']:shutil.copyfile(T/'firmware'/n,H/'firmware'/n)
    for p in (T/'upstream').iterdir():
        if p.is_file():shutil.copyfile(p,H/'upstream'/p.name)
    for n in ['cpu_program_reference.py','peripheral_checker.py']:
        shutil.copyfile(B/'models'/n,H/'models'/n);shutil.copyfile(B/'models'/n,H/'models-before'/n)
    # Only verification budget, not ISA/model semantics, is changed in the copy.
    p=H/'models/cpu_program_reference.py';s=p.read_text(encoding='utf-8-sig');assert s.count('self.steps<2000000')==1;p.write_text(s.replace('self.steps<2000000','self.steps<5000000'),encoding='utf-8')
    p=H/'port/core_portme.c';s=p.read_text(encoding='utf-8-sig');assert s.count('seed4_volatile=1')==1
    s=s.replace('volatile ee_s32 seed3_volatile=0x66, seed4_volatile=1, seed5_volatile=0;','''#ifndef ITERATIONS
#define ITERATIONS 1
#endif
#if ITERATIONS < 1 || ITERATIONS > 2147483647
#error "ITERATIONS must be a positive signed 32-bit integer; automatic zero is disabled"
#endif
volatile ee_s32 seed3_volatile=0x66, seed4_volatile=ITERATIONS, seed5_volatile=0;''')
    assert 'seed4_volatile=ITERATIONS' in s;p.write_text(s,encoding='utf-8')
    tb=(B/'tests/tb_board_coremark.sv').read_text(encoding='utf-8-sig');assert tb.count('6000000')==3
    (H/'tests/tb_board_coremark.sv').write_text(tb.replace('6000000','8000000'),encoding='utf-8')
    plan=read(B/'manual-plan.json');plan['authorization']='D149';plan['date']='2026-10-25';plan['coremark']['iterations']=2;plan['coremark']['N']=234;plan['budgets']=dict(compile_seconds=120,coremark_run_seconds=600,physical_cycles=8000000,each_log_bytes=256*1024*1024,reference_steps=5000000,reference_seconds=600)
    save(H/'manual-plan.json',plan)
    # Include current copies and exact original relevant inputs, not all history.
    for root in [B/'models',B/'source',T/'port',T/'upstream',T/'firmware']:
        rows += [dict(path=str(p),SHA256=sha(p)) for p in root.iterdir() if p.is_file()]
    rows += [dict(path=str(p),SHA256=sha(p)) for p in H.rglob('*') if p.is_file()]
    unique={r['path']:r for r in rows};save(H/'protected-originals.json',dict(files=list(unique.values())))
    save(H/'SOURCE_DIFFS.json',dict(port=''.join(difflib.unified_diff((H/'port-before/core_portme.c').read_text().splitlines(True),(H/'port/core_portme.c').read_text().splitlines(True),fromfile='port-before/core_portme.c',tofile='port/core_portme.c')),TB=''.join(difflib.unified_diff((B/'tests/tb_board_coremark.sv').read_text().splitlines(True),(H/'tests/tb_board_coremark.sv').read_text().splitlines(True))),reference_budget_only=True,RTL_changes=[]))
    print('Prepared independent iter2 copy, frozen originals, no GCC/compiler/DUT execution')
def build():
    protect();installed={Path(x['path']):x['sha256'] for x in read(P/'work/toolchain-readiness/2026-10-22-xpack-rv32i/installed-files.json')}
    for n in ['gcc','objcopy','objdump','readelf','nm']:assert sha(GCC/f'riscv-none-elf-{n}.exe')==installed[GCC/f'riscv-none-elf-{n}.exe']
    rows=[]
    for name in ['performance','validation']:
        d=H/'build'/name;d.mkdir();fw=H/'firmware';flags=['-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-fno-common','-fno-pie','-fno-stack-protector','-fno-unwind-tables','-fno-asynchronous-unwind-tables','-mno-relax','-msmall-data-limit=0','-Wall','-Wextra','-Werror','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,--build-id=none','-Wl,-T,'+str(fw/'link.ld'),'-Wl,-Map,'+str(d/'program.map'),'-I'+str(fw),'-I'+str(H/'port'),'-I'+str(H/'upstream'),'-DTOTAL_DATA_SIZE=2000','-DITERATIONS=2','-D'+name.upper()+'_RUN=1']
        sources=[fw/'start.S',*sorted((H/'upstream').glob('*.c')),H/'port/core_portme.c']
        jobs=[('compile',[GCC/'riscv-none-elf-gcc.exe',*flags,'-o',d/'program.elf',*sources,'-lgcc']),('objcopy',[GCC/'riscv-none-elf-objcopy.exe','-O','binary',d/'program.elf',d/'program.bin']),('objdump',[GCC/'riscv-none-elf-objdump.exe','-d','-M','no-aliases',d/'program.elf']),('readelf',[GCC/'riscv-none-elf-readelf.exe','-h','-A','-l','-sW',d/'program.elf']),('undefined',[GCC/'riscv-none-elf-nm.exe','-u',d/'program.elf'])]
        records=[]
        for kind,argv in jobs:
            r=bounded(argv,d,'build-'+name+'-'+kind,60 if kind=='compile' else 20);records.append(r)
            if r['returncode'] or r['timed_out'] or r['cap']:
                save(H/'build-failure.json',dict(program=name,records=records));raise RuntimeError('C build failed, stop')
        symbols=elf_symbols(d/'program.elf');image=(d/'program.bin').read_bytes();assert len(image)%4==0 and len(image)<=32768 and symbols['__bss_end']<=0x16000 and symbols['__stack_top']==0x18000
        assert initial_word(d/'program.elf',symbols['seed4_volatile'])==2
        assert not log(records[-1]['stdout']).strip()
        decoded=re.findall(r'^\s*([0-9a-f]+):\s+([0-9a-f]{8})\s+([a-z0-9.]+)',log(records[2]['stdout']),re.M)
        allowed={'lui','auipc','jal','jalr','beq','bne','blt','bge','bltu','bgeu','lb','lh','lw','lbu','lhu','sb','sh','sw','add','sub','sll','slt','sltu','xor','srl','sra','or','and','addi','slti','sltiu','xori','ori','andi','slli','srli','srai','ebreak'}
        assert decoded and all(x[2] in allowed for x in decoded)
        rows.append(dict(id=name,bytes=len(image),symbols=symbols,bin_sha=sha(d/'program.bin'),ELF_sha=sha(d/'program.elf'),ELF_seed4=2,commands=records));print(name,'C_BUILD_PASS',len(image),flush=True)
    save(H/'build-result.json',dict(status='PASS_BUILD_ONLY_NOT_DUT',artifacts=rows));protect()
def compiles():
    assert not ctypes.windll.shell32.IsUserAnAdmin();protect();plan=read(H/'compile-plan.json');assert plan['maximum']==2;rows=[]
    for t in plan['targets']:
        r=bounded(t['argv'],H,'compile-'+t['id'],120);ok=r['returncode']==0 and not r['timed_out'] and not r['cap'] and Path(t['output']).is_file()
        rows.append(dict(id=t['id'],status='PASS' if ok else 'FAIL',process=r,output=t['output'],sha256=sha(t['output']) if ok else None));print(t['id'],rows[-1]['status'],flush=True)
        if not ok:break
    save(H/'compile-result.json',dict(status='PASS' if len(rows)==2 and all(x['status']=='PASS' for x in rows) else 'STOPPED',rows=rows,protected=protect()))
def run_one(tid):
    protect();compiled=read(H/'compile-result.json');assert compiled['status']=='PASS';row=next(x for x in compiled['rows'] if x['id']==tid);assert sha(row['output'])==row['sha256']
    d=H/'runs'/tid;d.mkdir(exist_ok=False);r=bounded([VVP,'-N','-M-','-M'+str(LIB),row['output'],'+MAX_CYCLES=8000000'],d,'run-'+tid,600)
    save(d/'process.json',r);shutil.copyfile(r['stdout'],d/'stdout.log');print(tid,'DUT_EXIT',r['returncode'],'host_seconds',r['elapsed_seconds'],flush=True)
    if r['returncode'] or r['timed_out'] or r['cap']:raise RuntimeError('DUT runtime failed, stop')
    import check_coremark
    result=check_coremark.check(tid);save(d/'check-result.json',result);print(tid,'STRICT_CHECK',result['status'],flush=True)
    if result['status']!='PASS':raise RuntimeError('functional verification failure, stop')
    protect()
if __name__=='__main__':
    if sys.argv[1]=='run':run_one(sys.argv[2])
    else:dict(prepare=prepare,build=build,compile=compiles)[sys.argv[1]]()
