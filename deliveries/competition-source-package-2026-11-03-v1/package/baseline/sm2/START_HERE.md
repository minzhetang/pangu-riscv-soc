# SM2有限验收恢复快照 — 2026-11-02

入口证据`evidence/RESULTS.json`；固定performance/validation分开，当前板上最后驻留为validation。主线D300接受定义EEI内的SM2非调试运行版本，原O2及所有失败保留。

性能256：496232016周期、18.378963556标称秒；相对538539600周期减少7.855984%，吞吐增8.525767%。验证256：522673286周期、19.358269852标称秒，两份新输出一致。五CRC、完整报告、UART无错误、正常退出/空Job均有各自证据；不是完整ISA或物理签核。

`*/pds/source`是实际实现源，`*/pds/flow.tcl`为原相对路径构建入口；`configuration`是实际用过的固定sbit/SVF，不包含PDS或厂商模型。复制未执行新构建。启动/链接/端口与固件在`*/software`，原始完整编译命令在evidence。软件重建还需合法取得匹配SHA的六份CoreMark上游文件、版权及Apache-2.0许可材料，以及原xPack GNU15.2.0-1 rv32i/ilp32工具链；见UPSTREAM_DEPENDENCIES.json。本包不是已验证的独立软件构建包，也不是最终比赛提交包。

本地恢复仍需确认连接、真实阶段权限、工具/许可证和固定身份。不得自动点击脚本配置，不固化Flash、不改SCBV/供电/跳线/芯片保护，bit27照录。不要把复制/哈希校验当新实机结果。

报告：D:/A_FPGA_Comp/reports/hardware/2026-11-02-sm2-dualseed-and-uart-closure.md。旧O2片上分析只适用于其固定调试程序，不能冒称本SM2已有ILA；剩余调试Critical、物理CDC/IO、独立校频/温度及完整退休边界保留。UART断接后恢复不等唯一根因已查明。
