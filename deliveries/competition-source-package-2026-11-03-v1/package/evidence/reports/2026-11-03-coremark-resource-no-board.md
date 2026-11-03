# 无板高阶候选：CoreMark严格验证、功能可靠性与资源/时序对照

2026-11-03；D326–D327/F286。用户明确本阶段不计划上板。本轮完成独立候选的CoreMark功能短测、M-mode故障边界补验及三组真实PDS离线综合/P&R/STA，**推荐32项BTB参数候选**。生产D300/SM2及D320应用不替换，没有生成位流或操作硬件。

## 1. CoreMark证明了什么

完整沿用已收CoreMark上游算法，编译RV32I/ILP32、O2、TOTAL_DATA_SIZE=2000、ITERATIONS=1，分别使用performance/validation种子。上游文件与B原件SHA核同，端口与算法来源保留，未为CRC修改算法。新启动副本保存main返回到0x17FF8、完成签名到0x17FFC。不能仅凭main返回0判正确，因为上游MAIN_RETURN_VAL固定为0；还严格检查全部CRC及端口错误/溢出/调用次数。

performance已知CRC：list E714、matrix 1FD7、state 8E3A；validation：E3C1、0747、8D84。两组实际种子/迭代的RAM初值、portable_init/fini、timer start/stop各一次、错误/溢出0、main返回0、done值600D600D均核查。

第一层：固定零计时器mock，使参考结果在DUT前完整冻结；双参数×预测开关4次DUT。每组约53万/57万笔非x0合法WB、约2万笔STORE，逐笔地址/数据/掩码及各自顺序完全一致，不去重；全32寄存器、全部测试ROM/RAM快照、完整UART字节输出也逐项匹配。没有以摘要哈希替代轨迹。

第二层：增加真实仿真时钟驱动的mtime，先冻结TIMED_PLAN/TIMED32_PLAN时钟规则再DUT：复位后的第N拍计数N−1，一级同步数据口在MEM使用前拍值，因此该拍有效low读取应为N−2；high在本有界范围为0。每例12次hi/lo/hi读取全部按独立方程核查。顺序ISA模型按自己执行的读地址顺序消费由方程计算的值，并核对实际端口返回，随后生成全部WB/STORE/终态/完整输出进行逐笔比较。不是把DUT数据直接当期望回填，也不是事先冻结每个动态时刻的数值；冻结的是时钟响应规则和不变CRC/控制状态。0/64/32项×双参数共6次真实时钟DUT全部通过。程序保存的mtime差与TB计算窗口差4拍，完全符合既定标记开销。

共10次新CoreMark有限运行通过。真实时钟模拟的目标计算时间约0.064–0.084秒（假定27MHz），**不足10秒，不能报正式CoreMark成绩，也不是实机计时**。原输出中“Must execute for at least 10 secs”及由此产生的“Errors detected”保留，按预先规定的短测限制分类，未删去/屏蔽。功能CRC/轨迹通过不等正式成绩通过。没有将宿主90–115秒仿真墙钟作为目标时间。

## 2. 同条件计算周期

所有配置同一ELF/镜像/输入/种子/一次迭代/同步读时序，CPU模块源码不变，仅BTB_ENABLE或BTB_INDEX_BITS改变。区间为CPU对timing_phase=1/2的两笔STORE接受沿，排除初始化、结果格式化及UART输出；它与实际模拟mtime差固定4拍。使用RAM字节/UART立即接受模型，不等串行UART波形验证。

|配置|performance周期|validation周期|较关闭预测的周期减少|
|---|---:|---:|---:|
|关闭BTB|2,103,652|2,263,004|基准|
|64项BTB|1,719,152|1,837,836|18.2777% / 18.7878%|
|32项BTB（推荐）|1,730,128|1,849,336|17.7560% / 18.2796%|

32项较64项多约0.638%/0.626%计算周期。没有减少工作、降低迭代、跳过算法或减少输出获得收益。全程序含打印后的动态指令数会因计时数值的十进制格式化而不同，因此性能比较只采用共同计算窗口；不能拿全程WB数量变化冒称减少基准工作。

## 3. 实际离线PDS对照

PDS 2022.2-SP6.4、Logos2 PG2L100H、speed −6、FBG676、27MHz约束，同一SoC/DRM包装及同一performance1镜像。0/64项只变BTB_ENABLE；32项相对64项只变INDEX_BITS 6→5。各工程独立一次compile/synthesize/dev_map/pnr/report_timing，均native rc0、Job正常空，无gen_bit_stream/服务器/JTAG/下载/Flash。

|配置|LUT|FF|DRM36|IO|STA估算频率|27MHz下Setup裕量|
|---|---:|---:|---:|---:|---:|---:|
|关闭BTB|10,437|3,068|16|15|32.3593MHz|6.134ns|
|64项BTB|11,910|6,976|16|15|30.9665MHz|4.744ns|
|32项BTB|11,299|5,088|16|15|33.9006MHz|7.539ns|

三者Slow/Fast的Setup/Hold/Recovery/Removal八项内部时钟检查均无负裕量或失败端点；constraint_check均0 error/0 critical/0 warning（97条）。**这不是全部流程零warning**：原始flow仍有Verilog、常量探测loop、修剪/未驱动、最大扇出及Timing-4086/4087等告警，完整列表与计数在PDS AUDIT，不靠屏蔽消警。对于原始异步按键采用已有主线的同步级syn_preserve及窄域入口例外，未沿用B旧5ns“假同步”预算；仍不能宣称完整物理CDC/IO签核。

上述频率是工具在一次布局布线后的内部STA估算，不是板上Fmax、校频或跨布局种子的统计保证。32项报告更高不能直接宣传为物理频率提升，尤其不能把它与旧基础CPU约67MHz报告直接比较；本次CPU还带完整未验特权/MMU/PMP路径。没有关闭旧ILA调试版四Critical；本次是独立无ILA工程。

32项相对64项少611 LUT（约5.13%）、1888 FF（约27.06%），计算周期仅多约0.6%，所以推荐32项作为当前**离线候选**。相对关闭BTB仍多862 LUT（约8.26%）及2020 FF（约65.84%），不是零成本；是否最终采用须结合用途，不夸大成无代价提速。

程序初始化身份：三工程源ROM解码同本轮performance1 bin、RAM零初态一致；各综合网表存活的28个程序/数据DRM18K原语共1792段INIT逐值核验通过（部分零银行优化裁剪，不谎称所有逻辑bank都存活）。CPU八模块与实际仿真源逐SHA核同。

## 4. 功能可靠性补强

新增六个M-mode真实指令程序：指令访问错误、load访问错误、store访问错误、只读CSR写、未知CSR访问及未实现M乘法编码。通过公开inst_fault/mem_fault端口制造平台错误，不force内部控制。先冻结EPC/cause/mtval及合法/禁止副作用，每例检查全状态与精确异常归属；四配置24/24通过。未将M扩展或完整非法编码机制列为新实现。

32项改变预测索引风险后，针对拟采用同步/预测开启配置复用原冻结46条相关程序，覆盖MMU停顿旧STORE、IF停顿链接、一次训练、目标变化、陈旧命中恢复、IRQ暖机循环、MRET、CSR优先等；46/46通过。没有机械重跑所有历史生产回归，也没有修改公共模型或旧预期。程序/时钟/内存/副作用正确性底线保持。

本轮没有继续修全S/U、PMP、Sv32；旧TOR、访问宽度、MPRV、委派、walker权限/访问fault、fault缓存上下文问题仍未验收。RTL头部历史功能描述不等主线验收。所选有限M-mode和动态预测更可信，但**完整高阶2、完整特权或完整ISA仍不成立**。

## 5. 验证与记录质量

AUDIT独立重读10次CoreMark完整流、CRC、RAM端口状态、12次计时读取方程与phase差值，10个重复/丢失/错误掩码/CRC/截断/额外副作用负向控制均拒绝。这10项是离线逐笔相等比较及断言的有限自检，未逐项走完整runner/文件解析/超时路径，也不是10次新DUT故障注入。故障24例与32项46例分别保留逐项结果和新普通VCD。没有真实退休PC，WB/STORE仍分流；固定ROM/RAM/初态/有界迭代，不证明任意程序或永久稳定。

并行CoreMark与短回归曾共享COMMANDS.json，导致部分32项首轮过程元数据被后写覆盖，原DUT结果/原日志/VCD未丢。已保存观察快照并恢复全部CoreMark/24故障命令；为补齐32项元数据，改为每命令唯一记录后，在独立r2名称重跑相同46例，首轮保留不覆盖。COMMANDS_FINAL是实际记录合并，不将推算时间伪装成原生时间。

旧TIMED_RESULTS中的model.timer说明字符串错误沿用了“zero mock”；实际TIMED_PLAN、tb-timed、每笔timer读取和完整轨迹表明它是时钟方程模型。原结果保留，reference元数据字符串另存旧副本后修正；不据错误标签重分类真实运行。

无生产源码或已验镜像改变，89保护文件同SHA，旧D325交付不覆盖。新结果不能解除/替代任何硬件安全或实测限制；用户本轮明确不板。

## 6. 交付入口和剩余边界

- 软件：work/advanced/2026-11-03-coremark-strict-m5/START_HERE.md，AUDIT、COMMANDS_FINAL、strict/TIMED/TIMED32/fault及r32-r2结果；build包含双ELF/bin/hex/symbols，expected/timed-expected与runs保留全流、输出及普通窗口VCD。
- 离线实现：work/fpga/2026-11-03-advanced-btb-offline-m1/START_HERE.md，三套源码/约束/flow、实际STA/资源报告、BUILD_EXIT及AUDIT。不带专有模型/工具或许可证。
- 主要未完成：正式>=10秒CoreMark成绩、实机/串口电气/ILA、完整S/U/PMP/Sv32/异常矩阵、完整物理IO/CDC签核。按用户“不上板”目标，硬件项目保持未执行，不以文档豁免。

下一最有价值的工作是将**32项离线候选**及这些范围限制纳入作品技术报告，呈现功能、周期、资源与时序的完整取舍；不自动扩大新ISA、工具安装或硬件阶段。
