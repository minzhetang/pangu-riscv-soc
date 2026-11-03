# 成果覆盖与来源

最终阶段状态以STATUS.json和START_HERE.md为准。这里区分交付了什么材料与验证到了哪一层。

|项目|随包位置|已取得证据与边界|
|---|---|---|
|实际裸机C/启动/链接|firmware/|与M2固定生产构建输入一致；原start.S旧注释勘误见架构说明|
|event/dense冻结程序|software/production0-r1、production1-r1|ELF/bin/hex/map/符号；板级只加载event，dense未声称已上板|
|CPU/SoC/存储/Timer/外设RTL|fpga/source/|M3已绑定应用的整组14文件，不混历史源；CPU仍SM2未改|
|引脚/时钟/窄域异步约束与PDS入口|fpga/|实际M3输入，27MHz；未作完整IO/CDC/MTBF签核|
|精确差异与实现审计|evidence/implementation/|只改ROM载荷，初始化/时序/资源原审计；不是新构建|
|实际可恢复应用镜像|images/|sbit与完整官方CRAM SVF，各自SHA及配对证据；不自动授权配置/Flash|
|有限RTL测试输入/TB|simulation/|原M2参数化平台与冻结计划；未包含大RAMdump/VCD，不能在包内重审全部动态观测|
|RTL运行/量化结论|evidence/software/|M1同口径比较及M2快速/过载/慢周期/128形状结果，非当前板级dense对照|
|板级原始输出与失败|evidence/board/|原物理UART字节、逐笔报告检查、用户观察及工具退出；旧失败不覆盖|
|报告逐笔离线入口|verification/|解析header/每条E/END，旧FAIL必须仍被拒绝；重放不是新DUT|
|便携软件编译入口|build_software.py|明确工具目录/新输出目录、进程超时、逐字节bin一致性；本轮event/dense均实测同bin|
|原始运行脚本参考|historical-scripts/|保留准确旧方法但有A本地依赖，不宣称可直接执行|
|演示与易读说明|DEMO_GUIDE.md、UART_PROTOCOL.md|待用户按实际现场拍摄；包内没有新视频/应用ILA|

固定应用CPU SHA-256：`60F02899294C5BEF04E522622E32764A13B910008ADD85A73FE607550F9AF272`。
程序event SHA-256：`CBB37E60674713CCFBB0E603BA774ECB82E2460FA7D2DD2707AF34D4175E3D30`。
sbit SHA-256：`D43E4E419CC2F3656F92BCA2AF7BB23EFBE48B3EEC74A019A1D04FAABD60CEDE`。
完整SVF SHA-256：`99729EB81F4FD99E03DE7A19277DE39D59CBC8BBD01D85ADBA8CF22BF47BF06B`。

本应用由主线完成C程序、状态规则、真实CPU/SoC集成验证、软件/硬件证据整理。UART TX、GPIO和local_regif_txgpio_m1继承已接收的B外设成果，不将其原始开发归为主线独作；当前没有B新开发任务。既有CPU/SoC来自主线SM2恢复基线；代码作者、团队继承和AI辅助记录仍按项目既有界定，不以本包复制人冒充所有原始作者。

未随包的工具与大历史依赖：合法xPack GCC15.2.0-1、Icarus13.0、PDS2022.2-SP6.4 build146967及其合法器件库需由接收者自行具备；没有安装包/许可证/专有模型。M1大RAMdump/VCD/reads约783MB仍按原ARTIFACTS保留在主线，不假装本包已含。CPU全历史763等回归与CoreMark/ILA保留原恢复包/仓库快照，不重装进这个应用包，也不冒充新应用验证覆盖。

不能宣称：工业认证/真实工业部署、连续全天采集、精确高速采样、完整原始波形无损还原、UART RX/中断接入、全ISA或全异常正确、完整高阶2完成、应用已有片上ILA、未知配置保持问题已解决、已校准频率或温度安全。
