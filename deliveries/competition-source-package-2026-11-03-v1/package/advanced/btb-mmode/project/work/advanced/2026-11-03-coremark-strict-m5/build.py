from execute import *
G=R/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin'
for mode in ['performance','validation']:
 d=H/'build'/mode;d.mkdir(parents=True,exist_ok=False)
 flags=['-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-fno-common','-fno-pie','-fno-stack-protector','-fno-unwind-tables','-fno-asynchronous-unwind-tables','-mno-relax','-msmall-data-limit=0','-Wall','-Wextra','-Werror','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,--build-id=none','-T',H/'firmware/link.ld',f'-Wl,-Map,{d/"program.map"}',*['-I'+str(H/x) for x in ['firmware','port','upstream']],'-DTOTAL_DATA_SIZE=2000','-DITERATIONS=1','-D'+mode.upper()+'_RUN=1']
 args=[G/'riscv-none-elf-gcc.exe',*flags,'-o',d/'program.elf',H/'firmware/start.S',*sorted((H/'upstream').glob('*.c')),H/'port/core_portme.c','-lgcc']
 if run('gcc-'+mode,args,H,60):raise SystemExit(1)
 for name,more in [('objcopy',['-O','binary',d/'program.elf',d/'program.bin']),('nm',['-n',d/'program.elf'])]:
  if run(name+'-'+mode,[G/('riscv-none-elf-'+name+'.exe'),*more],H,20):raise SystemExit(1)
 data=(d/'program.bin').read_bytes();assert len(data)<=32768 and len(data)%4==0
 (d/'program.hex').write_text(''.join(f'{int.from_bytes(data[i:i+4],"little"):08x}\n' for i in range(0,len(data),4))+''.join('00000013\n' for _ in range(8192-len(data)//4)))
 symbols={line.split()[2]:int(line.split()[0],16) for line in (H/'logs'/('nm-'+mode+'.log')).read_text().splitlines() if len(line.split())==3}
 (d/'symbols.json').write_text(json.dumps(symbols,indent=2));print(mode,len(data),'timing_phase',hex(symbols['timing_phase']))
