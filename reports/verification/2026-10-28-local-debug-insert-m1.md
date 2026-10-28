# 本地调试插核M1：首次入口因GUI边界停止

2026-10-28（北京时间），D169批准、F166结果、D170处理。**尚未插核，未生成新FIC或调试位流。**F160软件系统及F163无调试CPU位流保持原验收，不以本次停止推翻旧功能结果，也不把旧结果移作本阶段通过。

|项目|真实结果|
|---|---|
|独立副本|`D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1/`；原13功能RTL/程序/约束复制保留|
|首次包装准备|漏建logs父目录，在mkdir、Popen之前失败，厂商程序实际启动0次。属A脚本错误，保留原件并补齐目录，用独立v2入口继续首次原生调用；未更改Tcl/ADF/调用参数，未重置总时钟|
|实际调用|既有cdt_ins.exe -batch probe.tcl，一次、60秒上限；实际1.718秒。检测到该进程有可见顶层窗口，保护停止，最终rc1；不能把被监督终止的rc1当工具自身给出的设计错误|
|CLI/载入|stdout194B、stderr0B；A_INS_PROBE_BEGIN/NETS_BEGIN/NETS_END/PROBE_END均未见，Tcl执行/网表载入未证明|
|GUI原因|未观察或操作窗口内容，不知道是主界面、许可、参数或其他弹窗；不能仅凭可见窗口断言批处理不支持、许可证无效或ADF错误|
|许可|正常原生日志保留，但未解析到无歧义的新成功/余期；仍只引用10/27实际PDS提示7天，不能据日期推算今日余期或虚构新许可问题|
|清理|原生根进程已经退出；taskkill rc255必须保留，独立全部后代快照未取得。随后Get-Process仅针对cdt_ins查询计0；CIM查询被拒绝，不把它写成成功的进程快照|
|预算/保护|46原件、5已冻结探针输入及13功能源后验同，详POSTFLIGHT；源码未添加保留标记，0新C/编译/DUT/PDS构建/设备或硬件调用|
|未执行|信号连接/生成FIC/DebugCore插入/布局布线/调试时序/新位流，以及真实FPGA/波形/正式分数，均未执行|

实际命令（仅记录，本阶段已停止，不是重试指令）：

```text
D:/PDS/PDS_2022.2-SP6.4/bin/cdt_ins.exe -batch D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1/scripts/probe.tcl
cwd: D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1/ins-input
```

阶段目录内：`APPROVAL.json、PROTECTED_ORIGINALS.json、PROBE_FROZEN_INPUTS.json、PREPARATION_ERROR.json、PROBE_ATTEMPT.json、NATIVE_START_01.json、PROBE_RESULT.json、PROBE_RESULT_V2.json、SUMMARY.json、STATUS.json、COMMANDS.md、POSTFLIGHT.json、SHA256SUMS.json`。完整原始日志与真实process.json在`logs/inserter-probe-01/`，只本地；初始化、ADF、程序、旧例和厂商模型不上传。

原`COUNTERS.json`的used1/first_failure记录的是第一次包装的预留及误分类，不抹除或复用为“已经启动1个厂商程序”的证据；PREPARATION_ERROR将其纠正为准备错误，NATIVE_START_01/process/V2记录唯一实际原生调用。未再调用原生工具，没有用剩余次数猜参数或开GUI。

根进程峰106414080B，监督父峰65708032B；这是本次两个进程观测，不是全部后代的峰。复制的有界监督增加了仅检查自身子进程可见窗口的保护，没有读取桌面或其他用户窗口内容，也未枚举设备。

下一项最小可执行工作是：**经另行批准后，仅启动一次本地Inserter GUI，查看实际界面/当前提示与正确入口**。建议上限3分钟，不点击构建/插核，不启动Debugger/配置器/硬件服务器，不操作许可配置、账号、驱动或系统环境，不连接硬件；如遇许可申请或无法可靠只读检查即停。若只能通过GUI配置FIC，再报告实际界面和具体范围，不自动扩为完整GUI插核。

之所以申请新权限，是AGENTS/WORKING_POLICY与D169 scope明确排除GUI，且本次已经触及首接口停止条件；不是需要用户找技术咨询或选择信号设计。即使软件调试准备后续成功，over_temp STOP、SCBV实际供电缺口、7旧警告/外部IO限制以及实机/ILA/正式分数缺口仍不解除。
