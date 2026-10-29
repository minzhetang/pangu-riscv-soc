# 已完成工程上下文：离线复用预检

2026-10-29，F176/D188；没有启动PDS或其他原生工具。来源F171/R4实际成功构建及F175导出前置失败。

## 已完成的可检查成果

`work/analysis/2026-10-29-project-context-preflight-m0/mirror/`保存原build完整副本及父级debug.fic，共70文件、21644039字节。原69个build文件逐项SHA与mtime_ns核同，FIC字节核同；使用copy2保留真实时间，不改文件内容/伪造完成时间。副本不是已验收的新工程。

对flow.pds以数据形式解析括号结构，未eval/source任何命令。compile、synthesize、devmap、pnr的原cmd状态均2，报告时序/位流亦2；gen_netlist、power为0。43个直接_file引用全部存在并落在mirror内（包括../debug.fic），无遗漏或越界；source/init_tables.svh也存在。项目文件与原件逐字节相同，未把状态0改2。

这弥补了F175只带单个DB、丢失工程完成上下文的准备不足；仍不能把静态完整当原生载入/导出成功。

## 两个必须明确的路径边界

1. **impl.tcl是重建历史脚本**：含compile/synthesize/dev_map/pnr/report_timing/gen_bit_stream及原绝对路径；严禁source或作为-file入口。原flow.tcl也包含完整实现流程，不执行。复制脚本只是保留历史上下文，不能当执行授权。
2. **FIC嵌套输入不是相对镜像路径**：designInputFile仍指向原R4/pre/synthesize/board_top_syn.adf（560888B，现存，哈希见NESTED_DEPENDENCY）。保留FIC不改；这是明确登记的原件只读依赖。因此不能把“43个直接项目引用全部位于副本”夸大为完全脱离原目录的独立包。导出不应重新插核，若工具要求回到该阶段则停止；不改FIC路径/时间来掩盖差异。

## 推荐的下一原生范围，未执行

使用官方已文档化的“打开既有工程”模式，在**新的执行副本**运行一次：

`pds_shell.exe -project <执行副本/build/flow.pds> -run gen_netlist`

与此前-file export.tcl创建新initial上下文不同；本次显式允许-run仅指定Generate Netlist，不用Rerun All或-force_to_run。先在执行副本的gen_netlist任务中添加func_sim_only ON/sdf_annotate FALSE，仅改变导出设置，准确diff复核，所有_gci_state和上游选项保持。不可在原件或本次已核镜像上直接改写。

依据为此前已阅读的安装版PDS用户手册V1.5 §5.3/§9.11（实际166/252页）及F174本机实际帮助；文档示例程序名为pds.exe，本机pds_shell的-project模式仍须实际验证，不能预报兼容或成功。原生若认为前置失效，不能因此执行新的实现，立即停止，不复用旧错误或修改完成状态。

**风险控制**：优先使用完整、同字节/同时间镜像保证真实输入与完成输出对应；显式固定目标步骤；监督新日志，一旦出现实际执行compile/synthesize/dev_map/pnr/report_timing/gen_bit_stream则中止并报告越界/失败，不以杀进程后当0发生。事后核全部原件/既有镜像哈希和任务输出，区分原生打开、导出和连接核查。监控不构成“已证明绝不会自动重跑”的承诺；该行为仍是下一次有限验证的停止条件。

## 当前状态与证据

输入/输出入口：prepare.py、SOURCE_INVENTORY.json、PROJECT_REFERENCES.json、PATH_AUDIT.json、NESTED_DEPENDENCY.json、SUMMARY.json。0原生调用、0新网表/连接验收、0新DUT/硬件；没有执行包内脚本或安装程序。

CPU/程序/约束/B接口不改。F171的4条Critical、CDC和实际硬件/ILA/CoreMark证据仍未闭，over_temp STOP不变。下一执行范围见`deliveries/mainline-project-context-export-scope-2026-10-29-v1/IMPLEMENTATION_SCOPE.md`；它需要新PDS进程授权，当前仅准备，不复用此前单次额度。
