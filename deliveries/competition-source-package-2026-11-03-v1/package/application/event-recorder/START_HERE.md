# A线事件记录应用：三场景有限验收版 v2

2026-11-03 / D320/F277。**固定应用第一版正常/顺序错误/等待超时的板级账本和LED检查已完成。** 不等工业产品、全ISA、全部板级稳定性或高阶2通过。

先读 **A_REPORT.md**，然后ARCHITECTURE_AND_LIMITS、UART_PROTOCOL；STATUS.json是机器可读状态。firmware和fpga/含完整当前应用源码，software含冻结event/dense产物，images含固定event sbit/完整CRAM SVF。完整身份见COVERAGE_AND_PROVENANCE、SOURCE_COPY_MANIFEST及SHA256_MANIFEST。原D300 CoreMark恢复基线保持独立，不用本应用镜像混代。

新超时实际报告在evidence/board/M5/capture-timeout-r2：index22接受state1、index42超时（差20样本/54000000tick），随后两上下文冻结；292B、fault2/frozen1/rejected1/late0，LED0/7均亮。原M4 normal-r2/order-r2成功及全部先前FAIL/0B等待和未知配置状态变化也保留。完成后只读DONE/DONE_I/GOUTEN仍1，不等旧根因已关闭。

`python -B verification/recheck_reports.py --output <全新结果目录>`只离线逐笔重查，不开硬件或执行DUT；旧失败必须仍被拒绝。build_software.py有明确工具目录/独立输出、已实际重建event/dense同bin，不自动替换ROM。完整依赖和有本地路径的历史脚本限制见REPRODUCTION；合法PDS/GCC/Icarus需自备，没有工具安装包、许可证或专有模型。

真实演示按DEMO_GUIDE，采集期间无串口输出属设计；需要现场配合及匹配版本，不把旧CoreMark/ILA画面移植给应用。本包未拍新视频，未对外发送。后续现场下载仍按当前具体范围/就绪与有界控制器，不复用已消费入口，不提供自动Flash/硬件入口。

v1检查点和ZIP原样保留，v2明确接续迟到回执后新一次真实采集；不能用v2通过改写v1曾经0字节/到期的事实。
