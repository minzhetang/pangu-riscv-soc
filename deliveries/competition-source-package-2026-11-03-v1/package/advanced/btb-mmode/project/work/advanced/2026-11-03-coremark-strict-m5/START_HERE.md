# M5：不接板的CoreMark/可靠性检查点

先读项目报告reports/verification/2026-11-03-coremark-resource-no-board.md，再读AUDIT.json、SUMMARY.json。

当前推荐参数：BTB_ENABLE=1、BTB_INDEX_BITS=5（32项）、SYNC_MEMORY=1。CPU八模块仍与M3/M4同字节，推荐的是新参数/包装配置，不替换生产CPU。

`upstream`与原已收CoreMark源同SHA；`port`继承既有端口；独立`firmware/start.S`新增保存main返回和明确done签名。双程序build包含ELF/bin/hex/符号及命令，ITERATIONS=1，不是正式成绩。

- `FROZEN_REFERENCE.json`：DUT前冻结的零计时mock完整参考；`strict-RESULTS.json`四次PASS。
- `TIMED_PLAN/RESULTS`及`TIMED32_PLAN/RESULTS`：时钟方程先冻结，64项/关闭与32项共6次；timer每次实际读都核方程。其动态参考按独立地址序列和时钟值生成，不声称所有动态值事先固定。
- `FAULT_PLAN`与`fault-final-RESULTS`：六程序四配置24PASS。
- 带r32和r2的七个最终RESULTS：同步32项46相关程序PASS。首轮元数据覆盖缺口已保留，r2每命令独立日志见command-records。
- `runs`完整WB/STORE/state/uart及前2048拍/完成附近普通VCD；`expected`/`timed-expected`为完整逐笔参考。
- `COMMANDS_FINAL.json`为实际日志快照＋独立命令记录合并。旧COMMANDS因并发覆盖不能当全量，详报告。工具/模型/测试错误不混入DUT故障。

本树入口使用原工作树合法Python3/Icarus13/GCC15.2及OwnedJob；本轮不安装、不改PATH。build.py/prepare*.py已有输出时拒绝覆盖；run.py可用新stage名复跑固定计时配置；run-timed*.py使用一次计划守卫，重跑需独立副本与新计划，不静默改原证据。旧reference-before.py只是M4历史，不是本轮正确CoreMark入口。audit.py需原89保护项、M4源及离线PDS报告，不能宣称任意搬目录一键全历史验收。

没有真实退休PC、全S/U/PMP/Sv32/完整ISA验证。完整高阶2与硬件仍未完成；不把不足10秒的模拟计算时间报正式CoreMark或实机频率。
