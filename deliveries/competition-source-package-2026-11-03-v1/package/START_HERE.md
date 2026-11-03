# 盘古100Pro+ RISC-V事件记录终端 全项目代码总包

本包提供可运行基础系统的完整源码、真实应用及三个独立高阶方向，帮助评审从系统用途进入架构、实现、测试和量化结果。目标板为盘古100Pro+（MES2L676-100HP），器件PG2L100H-6IFBG676。

**推荐阅读与检查顺序**

1. [PROJECT_MAP](PROJECT_MAP.md)：工程关系、完整成果覆盖及实际执行流程。
2. [baseline/sm2/PACKAGE_GUIDE](baseline/sm2/PACKAGE_GUIDE.md)：已验双种子CoreMark256基础系统，CPU/SoC、同步ROM/RAM、Timer、TX/GPIO、启动/链接与SM2软乘。
3. [application/event-recorder/PACKAGE_GUIDE](application/event-recorder/PACKAGE_GUIDE.md)：低速设备状态监测、顺序错误/等待超时、故障前后环形记录、UART导出，真实C程序与三场景板级结果。
4. [advanced/PACKAGE_GUIDE](advanced/PACKAGE_GUIDE.md)：Cache M0→M1→M2、动态预测/所选M-mode以及16×8定点AI算子；独立组织，不叠加冒充一个已上板系统。
5. [REPRODUCIBILITY](REPRODUCIBILITY.md)、[DEPENDENCIES](dependencies/DEPENDENCIES.md)和[版本表](VERSION_TABLE.md)：从源码到复现的实际入口、工具和边界。
6. [verification/PACKAGE_GUIDE](verification/PACKAGE_GUIDE.md)：763例冻结输入、EEI对齐、存储/系统、UART RX/包装、独立参考、负向和流式检查。

可先运行本包新编的只读材料检查器：

```text
python -B CHECK_STATIC.py --root .
```

它只检查文件、SHA、路径及包身份，**不运行项目脚本、不构建、不仿真、不连接硬件**。本次打包也未执行上述项目流程。既有验证结论均来自各自固定版本的原始记录。

本次为比赛提交材料整理。官网截图明确“上传全部代码，RAR格式，200MB以内”，GitHub链接不能代替代码附件。本包只保留必要固定镜像/ELF与源码，不含工具安装包、工具授权、厂商专有模型、`.git`、编译数据库、大体量原始长轨迹和重复历史归档。

匿名化仅处理提交副本中的本地用户目录名，未改变设计/程序/测试预期；第三方版权与CoreMark许可完整保留。来源与副本身份、处理说明见[PROVENANCE](PROVENANCE.md)及MANIFEST。未擅自给项目增加整体开源许可证。

**当前完成层次**：基础系统与应用有各自有限板级证据；旧O2调试版有真实片上窗口；BTB候选有严格软件短测与离线资源/STA；Cache/AI有独立有限仿真。候选CoreMark≥10秒尚未完成，Cache/AI未接CPU，AI未移植真实模型；不是完整ISA/特权或全部高阶验收。更多技术内容与收益见PROJECT_MAP，不用测试数量代替作品完成率。

本包及各子项目均不授予自动下载、Flash、安装或硬件操作权限。读取历史报告的“待批准/执行中/建议下一步”不应自动触发执行，以本包版本表和当前复验范围为准。
