from native import *
G=R/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin'
it=int(sys.argv[1]);need=it in [1,192]
if not need:raise SystemExit('Unplanned iteration count')
for mode in ['performance','validation']:
 d=H/'build'/f'{mode}-{it}';d.mkdir(exist_ok=False)
 flags=['-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-fno-common','-fno-pie','-fno-stack-protector','-fno-unwind-tables','-fno-asynchronous-unwind-tables','-mno-relax','-msmall-data-limit=0','-Wall','-Wextra','-Werror','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,--build-id=none','-T',H/'firmware/link.ld',f'-Wl,-Map,{d/"program.map"}',*['-I'+str(H/x)for x in ['firmware','port','upstream']],'-DTOTAL_DATA_SIZE=2000',f'-DITERATIONS={it}','-D'+mode.upper()+'_RUN=1']
 native(f'gcc-{mode}-{it}',[G/'riscv-none-elf-gcc.exe',*flags,'-o',d/'program.elf',H/'firmware/start.S',*sorted((H/'upstream').glob('*.c')),H/'port/core_portme.c','-lgcc'])
 native(f'objcopy-{mode}-{it}',[G/'riscv-none-elf-objcopy.exe','-O','binary',d/'program.elf',d/'program.bin'])
 native(f'nm-{mode}-{it}',[G/'riscv-none-elf-nm.exe','-n',d/'program.elf'])
 b=(d/'program.bin').read_bytes()
 if not(0<len(b)<=32768 and len(b)%4==0):raise RuntimeError('binary size')
 (d/'program.hex').write_text(''.join(f'{int.from_bytes(b[i:i+4],"little"):08x}\n'for i in range(0,len(b),4))+''.join('00000013\n'for _ in range(8192-len(b)//4)))
 sy={s.split()[2]:int(s.split()[0],16)for s in (H/'logs'/f'nm-{mode}-{it}.log').read_text().splitlines()if len(s.split())==3}
 save(d/'symbols.json',sy)
 # Independent native algorithm oracle; host time is deliberately fixed, NEVER a measurement.
 hp=H/'host'/f'{mode}-{it}';hp.mkdir()
 header=(H/'port/core_portme.h').read_text().replace('#include <stddef.h>','#include <stddef.h>\n#include <stdint.h>').replace('typedef ee_u32 ee_ptr_int;','typedef uintptr_t ee_ptr_int;').replace('~3U','~(uintptr_t)3').replace('NO VALID SCORE','HOST CRC ORACLE ONLY')
 (hp/'core_portme.h').write_text(header)
 native(f'host-gcc-{mode}-{it}',[Path('D:/mingw64/bin/gcc.exe'),'-O2','-std=c99','-static-libgcc','-I'+str(hp),'-I'+str(H/'upstream'),'-DTOTAL_DATA_SIZE=2000',f'-DITERATIONS={it}','-D'+mode.upper()+'_RUN=1',*sorted((H/'upstream').glob('*.c')),H/'host_port.c','-o',hp/'oracle.exe'])
 native(f'host-oracle-{mode}-{it}',[hp/'oracle.exe'])
 print(mode,it,len(b),flush=True)
