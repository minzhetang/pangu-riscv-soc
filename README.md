# 盘古100Pro+ RISC-V SoC

面向盘古100Pro+（MES2L676-100HP）、目标器件PG2L100H-6IFBG676的比赛项目。包含五级流水线CPU、同步存储适配、UART TX/GPIO包装及裸机C验证。

状态快照：**2026-10-24，F136有限软件基线**。源码可审查不代表完整RV32I兼容、FPGA可实现性或作品全部要求已通过。

## 已验证与尚未验证

|事项|当前证据|
|---|---|
|CPU执行裸机C及同步存储|有限软件系统通过，存储32K ROM/32K RAM使用官方primitive功能模型|
|UART/GPIO|原程序N16/N234回归无退化，真实CPU读写及公开串行输出通过；B整包仍有局部验证/元数据整改|
|物理时钟计数|64位自由运行、组合只读、高低高读取；计时单元增强296检查及真实C通过|
|CoreMark短运行|2K总数据、两个种子、各1迭代，CRC/全状态/有序副作用/计时与后置UART通过|
|计算区原始时钟数|性能种子2,103,648；验证种子2,263,000；不是主机运行秒数|
|正式CoreMark成绩|**未取得**。不足10秒的原提示保留；27MHz仅为软件频率设定|
|PDS实际映射/资源/Fmax|**未验证**，不能用官方功能模型替代|
|当前系统上板、片上波形|**未验证**；over_temp原因未闭环，硬件操作保持停止|

本轮CPU、队员包装/TX/GPIO及官方算法未改。性能组检查器曾漏计启动BSS清零，初版FAIL保留；CoreMark最终结论以`check-result-v2.json`为准。有限结果不能证明CPU整体正确，也没有已测创新或提速收益。

## 目录与验收入口

首次提交保留原工作路径，避免移动或重写已冻结成果：

- `work/system/2026-10-24-timed-coremark-m1/source/`：本阶段整组RTL。`memory_model.sv`为项目自写绑定，不含Pango专有primitive实现，亦不是已验证生产可综合内存。
- 同目录`firmware/`、`port/`：启动/链接、计时C及CoreMark平台适配。
- 同目录`tests/`、Python检查文件：计时单元、系统监视和独立判定；仅白名单内文件入仓。
- 同目录`runs/*/check-result*.json`及少量报告：选定的软件验收证据；波形和大型原始日志留在本地。
- [本阶段验证报告](reports/verification/2026-10-24-timed-coremark-m1.md)、[前一系统报告](reports/verification/2026-10-24-soc-txgpio-m1-system.md)。报告中的本地绝对路径不代表该资源已随仓库分发。
- [首次提交范围](docs/repository/FIRST_COMMIT_SCOPE.md)、[逐文件SHA-256清单](docs/repository/first-commit-files.json)、[外部依赖与复现边界](docs/repository/EXTERNAL_DEPENDENCIES.md)。

## 复现边界

既有环境为Icarus/vvp 13.0、xPack RISC-V GCC 15.2.0-1、PDS 2022.2-SP6.4。工具、授权、专有模型及CoreMark上游算法源不在首次提交中；不会从本仓库自动安装或下载它们。

计时单元`tb_timer_unit_v2`只依赖本仓库三个源文件及现有Icarus，无需PDS模型。下面是PowerShell入口示例，**本次Git准备没有重新运行仿真**；先自行将两个变量设为本机已有合法工具的绝对路径，不修改系统PATH：

```powershell
$iverilog = '<absolute-path-to-iverilog.exe>'
$vvp = '<absolute-path-to-vvp.exe>'
$ivlLib = '<absolute-path-to-ivl-library-directory>'
$baseline = 'work/system/2026-10-24-timed-coremark-m1'
New-Item -ItemType Directory -Force build | Out-Null
& $iverilog -B $ivlLib -g2012 -Wall -s tb_timer_unit_v2 -o build/timer-unit.vvp "$baseline/source/cycle_counter64.sv" "$baseline/source/soc_data_adapter.sv" "$baseline/tests/tb_timer_unit_v2.sv"
if ($LASTEXITCODE -ne 0) { throw 'Compile failed; do not execute its output' }
Push-Location build
try { & $vvp -N -M- "-M$ivlLib" timer-unit.vvp } finally { Pop-Location }
```

**完整SoC尚不具备干净克隆后一键复现入口。**保留的阶段Python脚本含本机路径、历史保护记录和外部依赖；部分历史文件不在首提中。不可直接执行这些脚本并假定已具备依赖。后续应独立整理可迁移运行器、初始化生成与外部模型定位；本次不为入仓改动验证逻辑或伪造重新复现。

## 仓库边界

`.gitignore`采用明确文件白名单，新增文件须审查后更新清单；默认不收工具/安装包、专有模型、授权或凭据、机器标识、照片/原始资料、完整交付包、本地项目记忆及大型构建/波形产物。`.gitattributes`关闭换行自动转换，以保持冻结文件的原始SHA；不修改全局Git配置。

忽略规则不保护已跟踪文件，也挡不住强制添加。首次提交/推送前仍须核对实际暂存清单和敏感信息；本次只准备，没有初始化项目仓库、暂存、提交、关联远端或推送。

本仓库未替全部工程统一授予新的开源许可。CoreMark及其他第三方依赖的版权/许可仍归各自权利人；工具授权文件与应保留的开源版权声明是两类不同材料。
