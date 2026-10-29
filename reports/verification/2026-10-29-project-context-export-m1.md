# 已有工程模式导出：出现上游Compile启动，已终止

2026-10-29，D189批准1.2.0，F177/D190。唯一原生调用为pds_shell.exe -project <新执行副本/flow.pds> -run gen_netlist。新副本只添加func_sim_only ON/sdf_annotate FALSE，状态列表未改，准确diff见EXPORT_OPTIONS.patch。

实际进程0.531秒、rc1。stdout明确出现`Process "Compile" started.`，随后执行副本compile/board_top_comp.adf被删除。磁盘监督在枚举与stat之间遇FileNotFound而终止进程；HOST_ERROR/process.json保留。不能把这写成“上游执行0”或“计划中的编译完成”：已进入Compile启动阶段，没有完成证据，没有新网表或连接通过。

原监督动作匹配只覆盖`Executing : compile`，漏掉Process格式，实际停止由文件竞争异常触发；这是A监督器预检不足，不假称预定动作监测完整工作。当前不修改冻结监督脚本或重跑。目录限额监测对可变输出应允许文件消失，同时对受保护输入仍严格校验；后续应先离线验证两类日志格式。

400个保护条目（原件、F176镜像及原FIC预综合依赖）SHA全部相同；原位流/RTL/约束未改。新执行副本可变缓存被工具修改，不能说“所有文件不变”。F176静态镜像真实性仍有效，但“复制完成状态即可避免前置重跑”的假设被本次原生行为推翻。原taskkill rc1/未独立验树；随后WMI只读拒绝，没有提权，完整Toolhelp快照确认根不存在、当前PPID后代0。这不是历史子进程没有运行的证明。无GUI/新DUT/硬件；许可本次提示5天，原4Critical/CDC及over_temp STOP保持。

## 后续判断

停止重复-project/-run导出尝试。F174本机实际帮助已给出`gen_netlist -force_to_run`的准确说明：Run this action without checking the status。它是**软件任务状态检查选项**，不是硬件强制下载；可考虑仅对gen_netlist使用并指定已核pnr.adf，不运行工程的自动前置流程。但此前范围明确禁止该选项，当前绝不执行；也不能仅凭说明保证成功。

推荐待批一次新范围：仅`set_arch`及`gen_netlist -input_db_file <已有副本> -func_sim_only -sdf_annotate FALSE -force_to_run`，0-project/-run/GUI/主动上游实现/仿真/硬件。若仍出现上游动作或新错误，立即停止，不追加试错。依据为本机HELP_SANITIZED.txt，非猜参数或修改完成状态。

证据目录`work/analysis/2026-10-29-project-context-export-m1/`：APPROVAL、PATCH_RECEIPT、EXPORT_OPTIONS.patch、POSTFLIGHT、HOST_ERROR、SUMMARY及logs/export-once/process.json/原日志。原始日志/工程副本仅本地保留，不纳入Git。
