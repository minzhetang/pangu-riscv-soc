"""Ordinary C build and independent artifact validation; NOT CPU/SoC execution."""
from pathlib import Path
import sys,json,hashlib,importlib.util,struct,re
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;P=H.parents[2]
spec=importlib.util.spec_from_file_location('bounded_helpers',P/'work/system/2026-10-23-memory-adapt-m1/run_stage.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);s.HERE=H
spec=importlib.util.spec_from_file_location('elf_helpers',P/'work/system/2026-10-23-c-boot-m1/check_c_boot.py')
elf=importlib.util.module_from_spec(spec);spec.loader.exec_module(elf)
TOOLS=P/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin'
exe={n:TOOLS/('riscv-none-elf-'+n+'.exe') for n in ['gcc','readelf','objdump','objcopy','nm']}
def save(p,o):s.save(p,o)
def build():
    old=P/'work/system/2026-10-24-memory-map-m2-v2'
    for r in s.read(old/'frozen.json')['files']:assert s.sha(r['path'])==r['sha256']
    for r in s.read(old/'summary.json')['sources']:assert s.sha(H/'source'/r['file'])==r['source_sha']
    installed={Path(r['path']):r['sha256'] for r in s.read(P/'work/toolchain-readiness/2026-10-22-xpack-rv32i/installed-files.json')}
    for path in exe.values():assert s.sha(path)==installed[path]
    manual=dict(date_beijing='2026-10-24',created_before_DUT=True,
        expected_results=[0x13579bdf,0,126,0x5a,0x5a,0xa5,0x3c,0xc3,12,0xa5,0,0],
        signature=0x534f4331,main_return=0,gpio_writes=[0x5a,0x5a,0xa5],
        tx_bytes=list(b'PG100 M1\r\nAA'),stop_kind=2,stack_top=0x18000,stack_reserved_bytes=8192,
        UART_N=[16,234],DUT_runs=0,complete_system_status='NOT_RUN_B_PACKAGE_PENDING')
    save(H/'manual-expectations.json',manual)
    files=set(p for p in H.rglob('*') if p.is_file())
    files.update(Path(r['path']) for r in s.read(old/'frozen.json')['files'])
    files.update(exe.values());files.update([old/'summary.json',old/'SHA256SUMS.txt'])
    files.update(P/'deliveries/mainline-stage-alignment-2026-10-23-v1'/n for n in ['TXGPIO_REGIF_CONTRACT.md','IMPLEMENTATION_SCOPE.md'])
    save(H/'preparation-frozen.json',dict(files=[dict(path=str(p),sha256=s.sha(p)) for p in sorted(files)]))
    b=H/'build';fw=H/'firmware'
    flags=['-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-fno-common','-fno-pie',
        '-fno-stack-protector','-fno-unwind-tables','-fno-asynchronous-unwind-tables','-mno-relax','-msmall-data-limit=0',
        '-Wall','-Wextra','-Werror','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,--build-id=none',
        '-Wl,-T,'+str(fw/'link.ld'),'-Wl,-Map,'+str(b/'soc.map'),'-o',str(b/'soc.elf'),str(fw/'start.S'),str(fw/'main.c'),'-lgcc']
    commands=[('version',[exe['gcc'],'--version']),('compile',[exe['gcc'],*flags]),
        ('readelf',[exe['readelf'],'-h','-A','-l','-sW',b/'soc.elf']),
        ('disassemble',[exe['objdump'],'-d','-M','no-aliases',b/'soc.elf']),
        ('objcopy',[exe['objcopy'],'-O','binary',b/'soc.elf',b/'soc.bin']),('undefined',[exe['nm'],'-u',b/'soc.elf'])]
    records=[]
    for name,argv in commands:
        r=s.bounded(argv,b,'firmware-'+name,60 if name=='compile' else 20);records.append(dict(id=name,**r))
        if r['returncode']!=0 or r['timed_out']:
            save(H/'firmware-build.json',dict(status='TOOL_OR_BUILD_ERROR',commands=records,DUT_runs=0));return
    image=(b/'soc.bin').read_bytes();symbols=elf.elf_symbols(b/'soc.elf');raw=(b/'soc.elf').read_bytes()
    assert raw[:7]==b'\x7fELF\x01\x01\x01' and struct.unpack_from('<H',raw,18)[0]==243 and struct.unpack_from('<I',raw,36)[0]==0
    assert len(image)<=32768 and len(image)%4==0
    assert 0x10000<=symbols['__data_start']<=symbols['__data_end']<=symbols['__bss_start']<=symbols['__bss_end']<=0x16000
    assert symbols['__stack_top']==0x18000 and symbols['__stack_bottom']==0x16000
    undefined=s.text_log(records[-1]['stdout']);assert not undefined.strip()
    dis=s.text_log(next(r['stdout'] for r in records if r['id']=='disassemble'))
    decoded=re.findall(r'^\s*([0-9a-f]+):\s+([0-9a-f]{8})\s+([a-z0-9.]+)',dis,re.M)
    allowed={'lui','auipc','jal','jalr','beq','bne','blt','bge','bltu','bgeu','lb','lh','lw','lbu','lhu','sb','sh','sw',
        'add','sub','sll','slt','sltu','xor','srl','sra','or','and','addi','slti','sltiu','xori','ori','andi','slli','srli','srai','ebreak'}
    assert decoded and all(row[2] in allowed for row in decoded),[row for row in decoded if row[2] not in allowed]
    ebreaks=[int(pc,16) for pc,word,op in decoded if word=='00100073'];assert len(ebreaks)==1
    words=[int.from_bytes(image[i:i+4],'little') for i in range(0,len(image),4)]
    with (b/'soc.mem32.hex').open('x',encoding='ascii') as f:f.write(''.join(f'{w:08x}\n' for w in words))
    with (b/'soc.byte.hex').open('x',encoding='ascii') as f:f.write(''.join(f'{v:02x}\n' for v in image))
    assert b''.join(int(x,16).to_bytes(4,'little') for x in (b/'soc.mem32.hex').read_text().split())==image
    assert bytes(int(x,16) for x in (b/'soc.byte.hex').read_text().split())==image
    # Produce the same bounded-token INIT input format as accepted F131.
    rom=words+[0]*(8192-len(words));ram=[0xa5a5a5a5]*8192
    with (H/'source/init_tables.svh').open('x',encoding='ascii') as f:
        for name,data in [('ROM',rom),('RAM',ram)]:
            text=''.join(f'{v:08x}' for v in reversed(data));chunks=[text[i:i+1024] for i in range(0,len(text),1024)]
            f.write(f'localparam [262143:0] {name}_BITS = {{'+',\n'.join("4096'h"+c for c in chunks)+'};\n')
        f.write('localparam integer ROM_BYTES=32768, RAM_BYTES=32768, RAM_BASE=65536;\n')
    save(H/'firmware-artifacts.json',dict(status='BUILD_AND_STATIC_CHECKS_PASS_NOT_CPU_EXECUTION',bytes=len(image),words=len(words),symbols=symbols,
        text_instructions_statically_decoded=len(decoded),mnemonics=sorted({row[2] for row in decoded}),ebreak_pc=ebreaks[0],
        image_sha256=s.sha(b/'soc.bin'),ELF_sha256=s.sha(b/'soc.elf'),stack_reserved_bytes=8192,
        assertions=['ELF32LE/RISC-V/flags0','data/BSS/layout/stack bounds','no undefined symbols','finite disassembly mnemonic whitelist','hex roundtrip'],
        limits='mnemonic whitelist is not full encoding/CPU semantic certification; no CPU/SoC execution'))
    save(H/'firmware-build.json',dict(status='PASS',commands=records,DUT_runs=0,complete_system='NOT_RUN_B_PACKAGE_PENDING'))
    print(json.dumps(dict(build='PASS',bytes=len(image),instructions=len(decoded),ebreak_pc=ebreaks[0],CPU_runs=0,SoC_runs=0)))
if __name__=='__main__':build()
