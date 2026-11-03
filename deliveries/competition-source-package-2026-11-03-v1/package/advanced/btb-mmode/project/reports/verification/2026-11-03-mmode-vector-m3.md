# 独立M3：M-mode向量入口与CSR后中断响应

2026-11-03，D324/F284。**有限软件候选可接收，不替换D300/SM2板级基线，不宣称完整高阶任务2。**

## 结果与修复

本轮先复制M2八模块，冻结11个程序，核三类M-mode中断的直接/向量入口、外部>软件>定时器优先级、mstatus/mie使能后的响应、同步异常与pending IRQ冲突及MRET返回。预测开关、组合/同步存储四配置。最终正式PLAN-v2对应44/44 PASS；原108项相关回归108/108 PASS，合计152次最终有界仿真，无TIMEOUT。每例400周期结束、native rc0；编译35秒、运行10秒进程限时，Job无残留。

发现M2对所有CSR均抑制中断：当已pending的IRQ刚经mstatus.MIE开启，紧邻的清MIE CSR可以抢先执行，丢掉应在前一CSR后判断的中断。最小程序在PC24开启MIE、PC28清MIE。正式同输入前源40PASS/4FAIL；修复版44PASS。

修复仅独立cpu_hl4.v两行：从ex_suppress_int移除ex_is_csr；csr_commit_eff增加非interrupt_taken条件。取中断时EPC=28，不提交该CSR，也不产生它的WB/STORE；处理后MRET回到28，再真正执行清MIE，最终继续主程序。其它七模块不变，准确diff见RTL_DIFF.patch。

官方Machine ISA v1.13的Machine Interrupt Registers条款规定：相关CSR写入后立即评估中断条件。由此选择在紧邻CSR执行前取中断，而不是允许后继CSR绕过这次评估。规范参考为本轮实际打开的[官方源码](https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/priv/machine.adoc)，搜索intr_mip_mie_xret_csrwr（本轮文本行1205–1210）；该main链接可变，版本标题为1.13。官网版本页本轮访问失败，没有据失败页面补写内容。

## 正式逐项结果

|冻结程序|M2前源，四配置|M3，四配置|核查内容|
|---|---|---|---|
|irq_3_vector0/1|各4PASS|各4PASS|软件中断，0x100/0x10C入口|
|irq_7_vector0/1|各4PASS|各4PASS|定时器中断，0x100/0x11C入口|
|irq_11_vector0/1|各4PASS|各4PASS|外部中断，0x100/0x12C入口|
|priority_external|4PASS|4PASS|三源pending，选择外部|
|priority_software|4PASS|4PASS|软件/定时器pending，选择软件|
|mie_enable_pending|4PASS|4PASS|先MIE后mie，下一可推进边界响应|
|adjacent_disable_precise|4FAIL|4PASS|不允许后继CSR抢先屏蔽已使能pending IRQ|
|exception_beats_pending_vectored|4PASS|4PASS|ECALL优先，向量模式同步异常仍到base|

所有通过检查全32寄存器、8KiB测试RAM终态、有序逐笔非x0 WB/STORE及字节掩码、不去重、精确EPC/cause/tval、重定向目标、提交后MIE/MPIE/MPP/特权状态、返回后的执行及关键有效控制/副作用中的X。未选中入口放置禁止STORE标记，不能仅靠最终结果掩盖错入口。实际CSR使能至首次trap间隔：组合配置1时钟、同步配置2时钟（均一个pipeline推进间隔）；冻结工程门为最多3推进间隔，不是规范指定3拍。

独立账本复核44项、10个离线错误控制全部拒绝（错向量/EPC/trap状态、重复trap/WB、丢STORE、错寄存器/内存、X及截断）。原108相关回归由继承检查器按原冻结预期判断；没有因修改预期凑PASS。六个代表性新VCD快照分清沿前与沿后1ps：定时器向量地址0x11C、EPC28、mstatus0x1880；相邻清MIE CSR在首次IRQ时commit=0，MRET后才commit=1。VCD为RTL仿真，不是片上ILA。

## 测试设计纠错与历史

首轮TB设irq_done后，没有else将外部IRQ撤低，违反冻结的一次IRQ输入约定，导致反复重入；首轮原TB/日志/VCD/first-RESULTS保留。修正夹具后曾得到旧PLAN的44PASS，但其中disable_adjacent_pending原预期本身过宽，不能作为正式正确性验收。本轮重新核规范后另建PLAN-v2及合法新镜像、保留旧结果；新预期先于前后源新运行冻结，不能把原来的“通过”沿用。AUDIT-initial-expectation.json只属旧预期历史。

最终M3并非原先“没有RTL问题”的判断：该初步判断已被相邻CSR反例和规范核查取代。原PLAN、first/final旧运行不纳入最终152次数。无silent rewrite。

## 边界与下一步

- 原89生产/应用保护项、M2全部959项清单均SHA未变；独立source-before精确继承M2，只有M3 cpu_hl4.v变化。公共模型/生产预期/已验SoC及板上镜像未动。
- 编译全部成功，仍有control/regfile继承timescale、ALU无显式timescale警告，未屏蔽。用已有合法Icarus普通用户沙箱外执行，不安装/改PATH/管理员/许可证/安全配置。旧普通沙箱0xC根因不因本轮成功关闭。
- 六层：材料及有限CPU软件复验通过；生产接口/完整系统兼容未验；候选综合/P&R/频率/资源、位流、实机/正式测量/ILA均NOT_RUN。没有本轮性能提升主张。
- 无真实退休PC、WB/STORE分流、固定ROM/RAM/零初态、有限400周期；未验完整中断矩阵、嵌套/长时运行、S/U/PMP/Sv32、低特权xRET/MPRV等，不能称完整ISA/M-mode/高阶2。
- 当前保留M3为新的有限独立候选，生产作品继续D300/SM2+D320应用。下一唯一高价值软件工作：固定一个真实短程序，在同一存储时序和输入下做BTB开关的严格功能/周期对照；不自动PDS、上板或合入主线。

入口work/advanced/2026-11-03-mmode-vector-m3/START_HERE.md。PLAN-v2、after-v2-RESULTS、各回归RESULTS、AUDIT、COMMANDS及runs中的输入/事件/普通VCD为证据，SHA256SUMS和MANIFEST_CHECK用于材料核验，不能替代功能结果。
