# 正式计量软件M1：四构建通过，参考预检错误停止

2026-10-29 F180/D194–195。用户批准1.0.0，在唯一`work/software/2026-10-29-formal-coremark-m1`副本执行。原CPU/SoC/算法/启动链接/旧程序与已转交包不改，PDS/硬件0。

新port只参数化27MHz常量、flags/内存描述与诚实候选标记，保留整数秒、原rawtick和超限拒绝，准确PORT_DIFF.patch；新增各case的build_identity.h。预冻结FROZEN_PLAN在C前。四次GCC/16辅助命令全部原生0；performance2/validation2/performance256/validation256分别16344/16348/16352/16356B，ELF/bin/map/完整argv、原日志与SHA均保留。不是四程序功能通过。

第一reference-performance2子进程rc1，0.078秒；在Scheduled创建/任何指令step前`initial_word(seed1)`报no initial word。是A新预检误把ELF BSS零值当file-backed，不是CPU或程序动态失败。没有重试/其它参考、RTL编译或DUT。四份静态ELF随后核种子/BSS布局/合法I反汇编；性能零种子在BSS，由原CRT真实清零，不能把原RAM A5预置成0绕过。正式N256任何参考CRC/全态仍NOT_RUN。

静态诊断第一版漏导入re/NameError在解析反汇编时停止，补齐该标准库导入后完成纯静态核查，未运行程序/模型。冻结参考worker不覆盖；修订`reference_worker-r1-PENDING.py`与REFERENCE_FIX_PENDING.patch已备未运行，仅允许BSS声明预检，并要求参考执行后seed1/2实际为期望。原件保护SHA复核相同。

当前STAGE_RESULT、STATIC_ELF_DIAGNOSIS、BUILD_RESULTS、BUILD_POSTFLIGHT、PROTECTED_INPUTS及每build/RESULT是权威入口。1次参考入口失败/0实际参考步/0完成先验/0RTL编译/0DUT，绝不写参考PASS。未改冻结预期或用新值回填；未安装/联网/PDS/许可/GUI/硬件。

按阶段失败停止要求停止；下一需批准一次替代参考入口及剩余未用验证工作，四C不重建、CPU/RTL不改。若原7200秒deadline已过，必须明确新恢复阶段预算，保留旧时钟及失败，不静默重置。硬件STOP/B0待回执/旧包身份不变。本轮实现尚未完整验收，Git归档暂不宣称已完成。
