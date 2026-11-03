# A线事件记录应用交付与恢复入口

2026-11-03。**状态：SOFTWARE_AND_TWO_BOARD_SCENARIOS_READY_TIMEOUT_PENDING_USER**。这份包不代表高阶2、全CPU/工业产品或所有板级可靠性已经验收。

已打通：真正编译的裸机C→原SM2 CPU/SoC→同步GPIO/目标timer→事件环形记录/规则→物理UART；正常及顺序错误两种板级完整账本和LED已有限通过。固定应用再次完整重载成功，自动128样本/约12.8秒报告与前次同字节。本次等待现场输入的接收窗口到期，0字节，尚未收到操作完成回执；超时板级仍未验收，不是已经证明超时程序失败。软件权限不能替代实体按键。

先读 `A_REPORT.md`，再读 `ARCHITECTURE_AND_LIMITS.md`、`UART_PROTOCOL.md`；实际证据在 `evidence/`。代码/镜像/初始化对应见 `COVERAGE_AND_PROVENANCE.md` 和 `SOURCE_COPY_MANIFEST.json`。`REPRODUCTION.md` 给出可执行离线复查与已经实测的软件重建入口；历史RTL运行脚本明确标为有本地依赖，不伪装全部开箱可跑。

准备提交/演示时用 `DEMO_GUIDE.md` 的真实操作口径，不把旧CoreMark/ILA或PPT展示当成本应用实测。没有新拍摄视频或应用ILA。images/含固定event位流与完整CRAM SVF，不提供自动硬件执行入口，不写Flash；合法PDS/GCC/Icarus工具本体及许可证不随包。

最大未闭项：此前在人工测试后DONE/DONE_I/GOUTEN变0的原因未知；同镜像重载可恢复不等根因解决。原失败与不完整运行全部保留。当前只读状态不等温度安全，芯片保护不改。各有限通过只在所测输入/批次/当前接口边界成立。

主线基础D300/SM2恢复包保持，不替换为本应用或高阶CPU。需要恢复CoreMark时使用其原身份入口，不能混用程序与位流。
