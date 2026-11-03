# 高阶任务2：独立BTB/M-mode候选有限仿真验收

2026-11-03；D322/F282。结论：独立候选有限接收，不合入D300/SM2，不宣称完整高阶2、完整M-mode或完整ISA。

## 实际成果与范围

本阶段从B已收HL4源码及M0未验证补丁建立独立source-before/source，八个模块中仅cpu_hl4.v改变。原整套S/U、Sv32、PMP代码仍存在且有已知问题；这里是验证范围限定，并非已隔离成可信的M-only产品核。固定生产CPU、SoC、应用和外设未修改，89项保护清单全部同SHA。无GUI/PDS/JTAG/下载/Flash/新硬件运行。

- 修复目标未对齐在原JAL/JALR/taken branch处报异常，并抑制链接WB。原mepc低位掩码会把错误PC10变成8，因此必须同时核查TRAP_PRE原始异常归属，不能只看CSR最终值。
- 用EX/MEM槽store_consumed保证旧STORE在页表停顿期间只发一次；不简单屏蔽所有stall期写请求，保留旧合法STORE。
- BTB更新增加推进、非stall、非被中断指令限定；对陈旧预测命中非分支的情况恢复PC+4。
- M-mode中断可打断暖机自跳转循环，在当前EX指令前取中断，EPC取该指令PC，抑制其WB/STORE/训练，保留更老副作用；MRET回到被打断指令。

## 可信对照

首批19个冻结程序，预测开/关及组合/同步取指、数据RAM，共76次最终运行；补充JALR目标变化和真实walker停顿中断两个程序，共8次；合计84次全部PASS。另新运行BTB单元12检查通过。程序次数不是完成率。
原源同首批输入的两预测配置：25 PASS、13 FAIL；不是要求旧源全部失败。原源没有本轮同步/补充程序对照，不能补称已测。

|程序|原源预测关/开|修复版组合预测关/开|修复版同步预测关/开|
|---|---|---|---|
|jal|FAIL/FAIL|PASS/PASS|PASS/PASS|
|jalr|FAIL/FAIL|PASS/PASS|PASS/PASS|
|taken_branch|FAIL/FAIL|PASS/PASS|PASS/PASS|
|not_taken_misaligned|PASS/PASS|PASS/PASS|PASS/PASS|
|jal_link_flush|PASS/PASS|PASS/PASS|PASS/PASS|
|jalr_link_flush|PASS/PASS|PASS/PASS|PASS/PASS|
|branch_loop|PASS/PASS|PASS/PASS|PASS/PASS|
|illegal|PASS/PASS|PASS/PASS|PASS/PASS|
|ecall|PASS/PASS|PASS/PASS|PASS/PASS|
|ebreak|PASS/PASS|PASS/PASS|PASS/PASS|
|load_misaligned|PASS/PASS|PASS/PASS|PASS/PASS|
|store_misaligned|PASS/PASS|PASS/PASS|PASS/PASS|
|irq_timer|PASS/FAIL|PASS/PASS|PASS/PASS|
|irq_software|PASS/FAIL|PASS/PASS|PASS/PASS|
|irq_external|PASS/FAIL|PASS/PASS|PASS/PASS|
|irq_priority|PASS/FAIL|PASS/PASS|PASS/PASS|
|irq_masked|PASS/PASS|PASS/PASS|PASS/PASS|
|stale_nonbranch|PASS/FAIL|PASS/PASS|PASS/PASS|
|mprv_store_hold|FAIL/FAIL|PASS/PASS|PASS/PASS|
|jalr_target_change|NOT_RUN/NOT_RUN|PASS/PASS|PASS/PASS|
|irq_during_walk|NOT_RUN/NOT_RUN|PASS/PASS|PASS/PASS|

## 判定、原始证据与工具边界

冻结输入/手工预期分别见FROZEN_PLAN.json（SHA94CF612545B07A36EA905CA15A91F6ACE0EAA8EB486DFB3BDC752B1BF41505FD）和FROZEN_EXTRA_PLAN.json（SHA D3B936E7000DB5EE6097C45E2FEEF56B1B0F4C2269C8D67A801ABE0481EB08A0），均先于对应DUT运行形成。补充计划未修改首批19项预期。正常取指译码执行，不force内部控制，不直接预置最终结果。

每次检查32寄存器、2048×32bit RAM终态、每笔非x0合法WB、每笔STORE地址/数据/字节使能及各自顺序，不去重；异常输入归属与提交后CSR分别检查。记录关键控制和有效WB/STORE中的X/Z，检查IRQ响应上界、MRET后MIE/MPIE/MPP及特权状态。训练日志检查stall期无更新，但本轮尚未构造“branch本身在EX同时遇到取指MMU停顿”的动态反例；该覆盖缺口保留。

普通VCD逐运行新生成。AUDIT.json已解析JAL提交前/后1ps、STORE停顿首次接受/下一拍抑制、暖机循环IRQ81拍EPC28等五个代表性快照，严格分开时钟沿前后。日志有全程TRAIN/STALL，不能拿取指PC当退休PC。独立离线检查器复核84账本，11个重复/丢失/错数据/错异常归属/X/错内存/截断/重复结束负向控制全部拒绝；这些负向控制是离线检查器测试，不是新DUT失败。

首轮寄存器比较器把list和tuple作比较，导致错误FAIL；before-RESULTS.json保留，before-RESULTS-rechecked.json仅对同一原日志重判，不冒新DUT。同步首轮TB把非pipeline_advance相位当trap提交沿，导致重复/错误快照及过早撤IRQ；after-sync原日志/TB快照保留，修正观察相位后新跑after-sync-r2及final-sync。预期未放宽。

初始沙箱连接TB编译再次0xC0000005；已记录SANDBOX_TOOL_ERROR.json，首次同名编译日志被随后成功尝试复用，初始stderr没有独立保留，不能称该原日志完整。其失败码来自实际工具回执，M0原失败另保留。经已批准普通用户沙箱外执行编译/展开成功，不安装/改PATH/改安全设置；根因仍UNKNOWN。最终编译均rc0，有control/regfile继承timescale及alu缺显式timescale警告，未屏蔽或修RTL来消警。

每例400周期上限、10秒进程限时；编译35秒限时。最终全部在400周期明确结束、进程rc0，无TIMEOUT；END是测试平台有界结束，不是应用真实停机。各次墙钟时长/完整命令/退出码/Job清理在COMMANDS.json；最终OwnedJob无残留。同步模型为寄存式取指/数据读，page-table端口使用固定合法根叶PTE0xCF，无真实DRM/PDS时序签核。

## 同条件局部周期对照

同一五次循环程序、输入、初态、编译源码和对应存储时序，仅改变BTB_ENABLE。签名STORE首次接受周期：组合读31→29；同步读61→57。WB/STORE/终态一致。这只是小程序签名到达的2/4时钟改善，包含启动开销，不是退休IPC、CoreMark跑分或实机提升；无本版频率/资源数据，不能声称综合效率收益。

## 尚未关闭与采用条件

- redirect与取指MMU stall同时发生时链接保留仍未动态收敛；本次不能关闭原R1全部内容。BTB非stall更新限定已有代码，但branch held期间训练次数的CPU级覆盖仍缺。
- 完整异常优先级、向量mtvec、长期中断/嵌套、xRET返回较低特权清MPRV、S/U委派、sie/sip掩码、PMP宽度/TOR、walker PMP/access fault、fault-cache上下文均未完成；原审查问题不因这批有限通过撤销。
- stale_nonbranch为外部指令端口刷新后的恢复诊断；不证明FENCE.I、缓存一致性或完整地址空间换映射。MPRV固定superpage仅用于制造真实stall，不证明Sv32/PMP正确。
- 没有重跑整套生产ISA回归、CoreMark，未取得本候选综合/P&R/资源/时序/位流/实机/片上分析。既有生产CoreMark/ILA与收益不移植。
- 无真实退休PC，WB/STORE分流，固定ROM4KiB/RAM8KiB/零初态、有限400周期；保留非全ISA与非工业产品认证边界。

六层状态：材料完整性=本独立阶段已核；单元仿真=12检查有限通过；CPU级软件复现=84运行有限通过；生产接口/全系统兼容=未验；FPGA综合/实现=NOT_RUN；硬件/正式性能/ILA=NOT_RUN。交付表述仅为“独立动态预测＋有限M-mode异常/中断仿真候选”。

建议保留为独立候选，不替换当前板级基线。下一最有价值的工作是针对取指MMU停顿与redirect重叠建立一个真实指令最小反例，再决定能否关闭链接丢失及训练次数问题；不需要新B工单或硬件。

## 入口与规范依据

工作入口：`work/advanced/2026-11-03-btb-mmode-m1/START_HERE.md`；准确diff为RTL_DIFF.patch；全结果final*-RESULTS.json，原对照before-RESULTS-rechecked.json；完整原日志logs、每例输入/events/VCD在runs。SHA256SUMS.json列出文件大小和SHA，verify_manifest.py核验。

核查RISC-V官方RV32I v2.1 §1.1.2/1.1.5（IALIGN与目标异常归属）及Machine ISA v1.13 §2.1.1.9、§2.1.3.2（中断有界判定、优先级、返回）。本阶段测试16时钟响应门是冻结的工程上界，不是规范指定固定16拍。
- https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html
- https://docs.riscv.org/reference/isa/v20260120/priv/machine.html
