# 正式测量软件M1：有限纯软件验收通过

2026-10-29，F181/D196–197。工作目录：`D:/A_FPGA_Comp/work/software/2026-10-29-formal-coremark-m1`。四C不重编，应用已备r1 BSS预检：声明零值可在BSS，但Reference RAM保留A5，执行原CRT后再验证实际seed1/2。保留旧rc1和0步预检失败，不归为CPU错误。旧STAGE_CLOCK未改；RECOVERY_CLOCK核原deadline尚有效并沿用，完成时尚余5698秒，未延长。

|程序|构建|独立ISA参考步数|raw ticks / 名义27MHz秒|crcfinal|新RTL/DUT|
|---|---|---:|---|---|---|
|performance2|PASS，16344B|2164556|4207378 / 0.155829|72be|PASS，6930633物理拍|
|validation2|PASS，16348B|2268113|4526490 / 0.167648|fe8c|PASS，7239909物理拍|
|performance256|PASS，16352B|188179549|538539600 / 19.945911|b40f|NOT_RUN|
|validation256|PASS，16356B|201767006|579425414 / 21.460201|798f|NOT_RUN|

N2两例严格比较全RF、32KiB RAM、每笔EX/WB/READ/STORE各自有序，不去重；独立stall/flush分别259567/520587、259810/546006，原尾拍32；真实计时采样、初始化合法STORE、无窗内IO、无错误重复副作用、完整UART引脚时轴/字节和普通窗口VCD检查通过。短case依旧报告不足10秒/Errors detected，即使main返回0也不能报官方成绩。256两例仅独立参考CRC/全态/有序摘要与计时先验，不是新DUT；两例有Correct operation validated字符串也不等正式成绩。

两编译原生rc0，45.109/44.890秒；两新DUT原生rc0，391.312/416.016秒，正常stop；两最终检查39.469/40.968秒。参考N2 7.032/7.265秒，N256 536.672/575.844秒，均在原限额。父/直接子资源收据在process.json，最终检查子峰值约373MB，低于512MiB；监督明确不另测编译器内部后代，不能宣称全进程树资源已测。0超时/超限。编译保留既有timescale继承、部分RTL未声明timeunit/precision及Pango模型隐式grsn警告，未改RTL凑消警。

测量解析器48项主机正负控全部通过（0.468秒）：缺失/重复字段、CRC/final/迭代、flags缺失、截断、错误/溢出delta、错误时基、额外输出、重复状态均拒绝。正控仅候选或短功能，永不输出hardware_valid/formal_score_valid=true。用精确有理数计算名义率，不靠HAS_FLOAT0整数显示报分；真实频率和双种子>=10秒/重复实机输出仍需后续取证，模型与主机控制分别统计。

27项原始输入SHA及冻结短程源码/模型/TB/case/先验全部复核同；13功能RTL、上游六源、启动链接/旧软件不改。唯一功能相关允许diff为新port元数据/可追溯flags/名义时基常量，参考只预算守卫及独立BSS预检，TB仅参数及12M拍限额。完整`EXACT_SOURCE_DIFF.patch`、`PORT_DIFF.patch`、`REFERENCE_FIX_PENDING.patch`保留。新镜像INIT在`initialization/*2.svh、*256.svh`；合法PDS原语未复制，自己的观测头按SHA复制到verification并记录DEPENDENCIES。旧脚本绝对依赖/一次性入口已标，不宣称一键可任意目录重跑。

入口：`RESULTS-M1.json`（分层总表）；`BUILD_RESULTS.json`（4C/完整GNU argv/cwd/原rc）；`SHORT_COMPILE_PLAN.json`与`logs/*/process.json`（完整实际编译/参考/仿真/检查命令）；`build/<case>/{program.elf,program.bin,program.map,build_identity.h}`；`oracles-recovery/<case>/{expected.json,expected-report.txt,expected-ram.bin,expected-registers.hex}`；`runs/*/{functional-result.json,check-result.json,uart-audit.json,wave-audit.json,streams.json,wave.vcd}`；`HOST_CONTROL_PLAN.json、HOST_CONTROL_RESULTS.json`；`SHA256SUMS-FINAL.txt`。阶段封存1036文件/184669372B（生成清单时快照，后续文件需另注），低于2GiB。原诊断把两JSON写在项目根，已同字节复制回本工作目录并保留根历史，不覆盖删除。

这是软件候选的有限验收，非完整RV32I、非256 RTL、非正式CoreMark或实机。仍无真实退休PC/统一WB-STORE提交顺序，固定存储与初态，窗口VCD不等ILA。未启动PDS/硬件服务器、GUI/设备枚举/JTAG/上电/Flash/新位流；SCBV/供电/温控/over_temp STOP不变。旧8位流和已转B全包不改，不能将旧位流当新256程序。B0仍待用户转回；下一应交独立测量候选增量，B3须真实安全准入和相应权限，未代发或上传。

本报告接替F180/D195的“尚未运行”当前状态，保留其历史失败。范围内执行结束，不自动优化CPU、长跑256或恢复硬件。
