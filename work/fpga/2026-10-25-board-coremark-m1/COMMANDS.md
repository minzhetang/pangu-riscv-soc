# 本轮实际命令

2026-10-25，D133。没有重新GCC构建镜像、PDS或硬件调用。镜像/ELF来自F136按SHA核同，不拿旧VVP/波形代新执行。编排stage_coremark.py prepare →固定外部compile→普通run；audit_uart/audit_wave/quality_compare仅重审原始新证据。
初始目录独立创建、防覆盖；原生VCD窗口与全UART实际变化文本分开。所有模型/旧源/二进制本地依赖须先满足，不宣称Git干净克隆一键复现。

## 完整实际argv

### performance-N234

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe' '-B' 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' '-g2012' '-Wall' '-DM0_VERIFY' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\verification' '-s' 'tb_board_coremark' '-Ptb_board_coremark.PHASE_ADDR=67584' '-o' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\compile\performance-N234.vvp' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\alu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\control.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\cpu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\gpio_core.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\local_regif_txgpio_m1.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\regfile.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\uart_tx.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\board_reset_sync.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\board_top.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\cycle_counter64.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\memory_model.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\soc_data_adapter.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\performance-N234\source\soc_top.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\tests\tb_board_coremark.sv' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_DRM18K_E1.v' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_GRS.v'
```
cwd：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1`；rc=0；墙钟44.437秒；进程上限120秒。

### validation-N234

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe' '-B' 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' '-g2012' '-Wall' '-DM0_VERIFY' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\verification' '-s' 'tb_board_coremark' '-Ptb_board_coremark.PHASE_ADDR=67592' '-o' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\compile\validation-N234.vvp' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\alu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\control.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\cpu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\gpio_core.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\local_regif_txgpio_m1.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\regfile.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\uart_tx.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\board_reset_sync.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\board_top.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\cycle_counter64.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\memory_model.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\soc_data_adapter.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\cases\validation-N234\source\soc_top.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\tests\tb_board_coremark.sv' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_DRM18K_E1.v' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_GRS.v'
```
cwd：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1`；rc=0；墙钟44.187秒；进程上限120秒。

### performance-N234

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\compile\performance-N234.vvp' '+MAX_CYCLES=6000000'
```
cwd：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\runs\performance-N234`；rc=0；墙钟201.875秒；进程上限360秒。

### validation-N234

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\compile\validation-N234.vvp' '+MAX_CYCLES=6000000'
```
cwd：`D:\A_FPGA_Comp\work\fpga\2026-10-25-board-coremark-m1\runs\validation-N234`；rc=0；墙钟209.235秒；进程上限360秒。

