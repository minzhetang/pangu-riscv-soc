# 本次实际命令（PowerShell）

日期：2026-10-22；F-114/D-101。以下为已执行原命令；不要覆盖原目录复跑。
复现使用新独立输出目录，并相应冻结新计划。原始request/process/stdout/stderr全部保留。

所有目标工具命令普通权限、无管理员/沙箱外编译；编译60秒限，其余20秒。

```powershell
Set-Location -LiteralPath 'D:\A_FPGA_Comp\work\toolchain-readiness\2026-10-22-xpack-rv32i\runs-ordinary'

# version: exit0, 0.5139s; timeout 20s
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-gcc.exe' '--version'

# target: exit0, 0.017s; timeout 20s
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-gcc.exe' '-dumpmachine'

# multilib: exit0, 0.0198s; timeout 20s
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-gcc.exe' '-print-multi-lib'

# libdir: exit0, 0.0187s; timeout 20s
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-gcc.exe' '-march=rv32i' '-mabi=ilp32' '-print-multi-directory'

# libgcc: exit0, 0.0199s; timeout 20s
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-gcc.exe' '-march=rv32i' '-mabi=ilp32' '-print-libgcc-file-name'

# compile: exit0, 1.8914s; timeout 60s
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-gcc.exe' '-march=rv32i' '-mabi=ilp32' '-O2' '-ffreestanding' '-fno-builtin' '-fno-common' '-fno-pie' '-fno-stack-protector' '-fno-unwind-tables' '-fno-asynchronous-unwind-tables' '-mno-relax' '-msmall-data-limit=0' '-Wall' '-Wextra' '-Werror' '-nostdlib' '-nostartfiles' '-Wl,--no-relax' '-Wl,--build-id=none' '-Wl,-T,D:\A_FPGA_Comp\work\toolchain-readiness\2026-10-22-xpack-rv32i\smoke.ld' '-Wl,-Map,smoke.map' '-o' 'smoke.elf' 'D:\A_FPGA_Comp\work\toolchain-readiness\2026-10-22-xpack-rv32i\start.S' 'D:\A_FPGA_Comp\work\toolchain-readiness\2026-10-22-xpack-rv32i\smoke.c' '-lgcc'

# readelf: exit0, 0.2702s; timeout 20s
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-readelf.exe' '-h' '-A' '-l' '-sW' 'smoke.elf'

# objdump: exit0, 0.3414s; timeout 20s
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-objdump.exe' '-d' '-M' 'no-aliases' 'smoke.elf'

# objcopy: exit0, 0.2841s; timeout 20s
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-objcopy.exe' '-O' 'binary' 'smoke.elf' 'smoke.bin'

# undefined: exit0, 0.2699s; timeout 20s
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-nm.exe' '-u' 'smoke.elf'
```

stdout/stderr由受控Python执行器分别写入每项日志，并在进程退出后核产物。
`objdump/stdout.log`即完整反汇编；readelf同理。

## 本轮驱动与只读检查（按先后顺序，非重跑授权）

Python绝对路径：C:\Espressif\tools\python\python.exe；均加-B，不生成pycache。
deployment脚本prepare/fetch(网络失败)/fetch-external(截断SHA失败)；
diagnose_xpack_download.py；resume_xpack_download.py；
deploy_xpack_rv32i.py deploy；test_xpack_rv32i.py prepare；
test_xpack_rv32i.py ordinary；check_xpack_rv32i_artifacts.py；
finalize_xpack_rv32i.py prepare；记忆更新后finalize_xpack_rv32i.py final。
脚本位于D:\A_FPGA_Comp\scripts\verification；网络三操作经单独工具审批，未执行下载中的脚本。
hex由独立检查器按bin小端字/字节生成并反向比较；无目标C执行、CPU模拟或硬件。
