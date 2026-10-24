# M0实际命令与执行边界

日期2026-10-24；固定本地路径。不是干净克隆一键运行入口；外部模型/初始化/历史目录保留本地。

编排由已验证Python（-B）调用stage.py prepare → compile → run，随后普通stage.py pds在CreateProcess处Win623失败；工具批准后仅一次pds_external_once.py。audit_results.py仅解析新产物，无新DUT/PDS执行。未安装/改PATH；不重复执行同目录（独占创建防覆盖）。

## 编译（固定4目标，非管理员外部批，各120s，首错停止）

### baseline-N16

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe' '-B' 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' '-g2012' '-Wall' '-DM0_VERIFY' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\verification' '-s' 'tb_timed_system' '-Ptb_timed_system.N=16' '-o' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\baseline-N16.vvp' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\alu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\control.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\cpu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\gpio_core.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\local_regif_txgpio_m1.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\regfile.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\uart_tx.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\cycle_counter64.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\memory_model.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\soc_data_adapter.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\soc_top.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N16\source\tb_timed_system.sv' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_DRM18K_E1.v' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_GRS.v'
```

### baseline-N234

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe' '-B' 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' '-g2012' '-Wall' '-DM0_VERIFY' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\verification' '-s' 'tb_timed_system' '-Ptb_timed_system.N=234' '-o' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\baseline-N234.vvp' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\alu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\control.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\cpu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\gpio_core.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\local_regif_txgpio_m1.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\regfile.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\uart_tx.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\cycle_counter64.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\memory_model.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\soc_data_adapter.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\soc_top.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\baseline-N234\source\tb_timed_system.sv' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_DRM18K_E1.v' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_GRS.v'
```

### smoke-N16

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe' '-B' 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' '-g2012' '-Wall' '-DM0_VERIFY' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\verification' '-s' 'tb_timed_system' '-Ptb_timed_system.N=16' '-o' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\smoke-N16.vvp' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\alu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\control.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\cpu.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\gpio_core.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\local_regif_txgpio_m1.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\regfile.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\uart_tx.v' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\cycle_counter64.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\memory_model.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\soc_data_adapter.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\soc_top.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\smoke-N16\source\tb_timed_system.sv' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_DRM18K_E1.v' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_GRS.v'
```

### selftest

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe' '-B' 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' '-g2012' '-Wall' '-DM0_VERIFY' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\selftest\source' '-I' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\verification' '-s' 'tb_full_memory' '-o' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\selftest.vvp' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\selftest\source\memory_model.sv' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\cases\selftest\source\tb_full_memory.sv' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_DRM18K_E1.v' 'D:\PDS\PDS_2022.2-SP6.4\arch\vendor\pango\verilog\simulation\GTP_GRS.v'
```

## 仿真（7个普通权限进程，各45s，系统周期上限100000）

### baseline-N16

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\baseline-N16.vvp' '+MAX_CYCLES=100000'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\runs\baseline-N16`。

### baseline-N234

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\baseline-N234.vvp' '+MAX_CYCLES=100000'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\runs\baseline-N234`。

### smoke-N16

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\smoke-N16.vvp' '+MAX_CYCLES=100000'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\runs\smoke-N16`。

### selftest-0

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\selftest.vvp' '+BAD=0'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\runs\selftest-0`。

### selftest-1

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\selftest.vvp' '+BAD=1'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\runs\selftest-1`。

### selftest-2

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\selftest.vvp' '+BAD=2'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\runs\selftest-2`。

### selftest-3

```powershell
& 'D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\vvp.exe' '-N' '-M-' '-MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\compile\selftest.vvp' '+BAD=3'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\runs\selftest-3`。

## PDS（仅批准的一次外部CLI，1200s上限）

```powershell
& 'D:\PDS\PDS_2022.2-SP6.4\bin\pds_shell.exe' '-file' 'D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\pds\build.tcl'
```
工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0\pds`。
本命令普通上下文先失败，外部对照完成；只解析/综合/映射/pnr/report_timing，Tcl无gen_bit_stream。
进程退出后由audit_results.py检查新报告、INIT、资源、最终多角STA、原件SHA及新波形。未执行硬件工具。
原stdout/stderr/process位于logs；PDS自身run/flow日志可能自动带授权路径，保持本地忽略，不复制到公共报告/仓库。
