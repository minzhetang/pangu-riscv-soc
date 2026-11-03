from execute import *
G=R/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin'
if (H/'program.bin').exists():raise SystemExit('Build outputs exist; preserve them')
args=[G/'riscv-none-elf-gcc.exe','-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-fno-pic','-fno-stack-protector','-msmall-data-limit=0','-mno-relax','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,-Map=program.map','-T',H/'link.ld',H/'start.S',H/'program.c','-o',H/'program.elf']
if run('gcc',args,H,35):raise SystemExit(1)
if run('objcopy',[G/'riscv-none-elf-objcopy.exe','-O','binary',H/'program.elf',H/'program.bin'],H,15):raise SystemExit(1)
if run('objdump',[G/'riscv-none-elf-objdump.exe','-d',H/'program.elf'],H,15):raise SystemExit(1)
data=(H/'program.bin').read_bytes();data+=b'\0'*((-len(data))%4)
(H/'program.hex').write_text(''.join(f'{int.from_bytes(data[i:i+4],"little"):08x}\n' for i in range(0,len(data),4))+''.join('00000013\n' for _ in range(2048-len(data)//4)))
print('ROM bytes',len(data))
