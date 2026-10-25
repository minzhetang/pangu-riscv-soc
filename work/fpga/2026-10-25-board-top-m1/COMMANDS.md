# 本阶段实际命令与结果入口

2026-10-25，D131。绝对路径为实际本地环境，不是干净克隆一键复现；不安装/改PATH/许可证。
编排顺序：stage_board.py prepare → build（初版新C NUL诊断保留，build/board-v2为修正后产物）→固定2目标外部compile→普通run（3次）→单次外部pds；随后checker_negatives/audit_waves/audit_pds仅检查证据，0新DUT/PDS。

## 实际完整argv

### firmware-0

```powershell
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-gcc.exe' '-march=rv32i' '-mabi=ilp32' '-O2' '-ffreestanding' '-fno-builtin' '-fno-common' '-fno-pie' '-fno-stack-protector' '-fno-unwind-tables' '-fno-asynchronous-unwind-tables' '-mno-relax' '-msmall-data-limit=0' '-Wall' '-Wextra' '-Werror' '-nostdlib' '-nostartfiles' '-Wl,--no-relax' '-Wl,--build-id=none' '-Wl,-T,D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\firmware\link.ld' '-Wl,-Map,D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2\program.map' '-o' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2\program.elf' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\firmware\start.S' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\firmware\board_smoke.c' '-lgcc'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2`；rc=0；墙钟0.406秒；上限60秒。

### firmware-1

```powershell
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-objcopy.exe' '-O' 'binary' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2\program.elf' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2\program.bin'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2`；rc=0；墙钟0.171秒；上限60秒。

### firmware-2

```powershell
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-nm.exe' '-n' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2\program.elf'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2`；rc=0；墙钟0.172秒；上限60秒。

### firmware-3

```powershell
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-objdump.exe' '-d' '-M' 'no-aliases' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2\program.elf'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2`；rc=0；墙钟0.188秒；上限60秒。

### firmware-4

```powershell
& 'D:\A_FPGA_Comp\tools\xpack-riscv-none-elf-gcc-15.2.0-1\bin\riscv-none-elf-readelf.exe' '-h' '-A' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2\program.elf'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\build\board-v2`；rc=0；墙钟0.172秒；上限60秒。

### reset

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe' '-B' 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' '-g2012' '-Wall' '-DM0_VERIFY' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\cases\board\source' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\verification' '-s' 'tb_reset' '-o' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\compile\reset.vvp' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\board_reset_sync.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\tests\tb_reset.sv'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1`；rc=0；墙钟0.125秒；上限120秒。

### board

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe' '-B' 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' '-g2012' '-Wall' '-DM0_VERIFY' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\cases\board\source' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\verification' '-s' 'tb_board_system' '-o' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\compile\board.vvp' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\alu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\control.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\cpu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\gpio_core.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\local_regif_txgpio_m1.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\regfile.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\uart_tx.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\board_reset_sync.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\board_top.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\cycle_counter64.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\memory_model.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\soc_data_adapter.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\source\soc_top.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\tests\tb_board_system.sv' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_DRM18K_E1.v' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_GRS.v'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1`；rc=0；墙钟51.438秒；上限120秒。

### reset

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\compile\reset.vvp'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\runs\reset`；rc=0；墙钟0.109秒；上限45秒。

### board5-N234

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\compile\board.vvp' '+MAX_CYCLES=100000' '+K=5'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\runs\board5-N234`；rc=0；墙钟1.719秒；上限45秒。

### board12-N234

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\compile\board.vvp' '+MAX_CYCLES=100000' '+K=12'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\runs\board12-N234`；rc=0；墙钟1.829秒；上限45秒。

### PDS

```powershell
& 'D:\PDS\PDS_2022.2-SP6.4\bin\pds_shell.exe' '-file' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\pds\build.tcl'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-top-m1\pds`；rc=0；墙钟74.422秒；上限1200秒。

PDS日志/数据库只保留本地忽略；不复制自动输出的授权来源或主机信息。Tcl未调用gen_bit_stream；无设备/服务器/JTAG操作。
