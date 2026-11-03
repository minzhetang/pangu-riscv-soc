# v02 冻结保存

主线 F152/D151 已接收 v02 为当前活动的**有限软件交付**。本目录是按主线要求做的本地冻结保存，不是 v03、不是新交付包、不是新 DUT 运行。

- 活动交付：`work/B-RETURN/stage-return-final-20261027-v02/`
- 冻结镜像：`work/B-RETURN/frozen-v02-20261026/FROZEN_V02/stage-return-final-20261027-v02/`
- 主线接收：`MAINLINE_ACCEPTANCE/`（ACCEPTANCE、IMPORT_MAP、START_HERE、TEAMMATE_REPLY）
- 冻结依赖：`DEPENDENCIES_FROZEN.json` 及 `DEPENDENCIES/`
- 冻结索引：`FREEZE_INDEX.json`（v02 文件、计划、日志、VCD、依赖、验收文件）
- 冻结记录：`FREEZE_RECORD.json`
- 外层清单：`SHA256SUMS.txt`

保持原样、不修改：

- R1/R2/R3 原运行结果、COM-01 旧文案、v02 `results.json`、v01/旧包。
- W06 继续由 `A-W06-SUPPLEMENT` 关闭，GPIO 1.0.2 继续有限接收；不重跑。
- 旧根 `OPEN_PREEXISTING` 由 A 处理；硬件 `STOPPED`。
- 不生成 ZIP，不制作 v03。
