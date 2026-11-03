# CoreMark分层证据与长测前缀复核

2026-11-03；用户采纳分层复用方案。D330取代D328/D329继续追求本候选192次>=10秒全程RTL长测的当前优先级；原冻结输入、失败及预算不改。本次只构建/运行离线观测检查器，无新DUT、PDS或硬件。

## 可直接用于作品报告的结论

基础版本和独立高阶候选分别举证：基础版本已有256次双种子的真实物理UART输出、五CRC与计时匹配，标称27MHz下分别19.945911111秒、21.460200519秒，重复及完整加载身份见2026-11-01-coremark256-full-svf-identity-closure。时钟未独立校准、无EEMBC认证；不能把这些结果转给新高阶候选。

当前32项BTB候选以严格短测证明有限正确性和同条件周期收益，另以独立PDS报告呈现面积/时序代价：performance/validation计算周期分别2103652→1730128、2263004→1849336，减少17.755979%/18.279597%。程序/种子/一次迭代/同步内存相同。32项较64项仅多约0.6%周期，少611 LUT/1888 FF。旧32项PDS为11299 LUT、5088 FF、16 DRM36，27MHz内部约束通过、STA估算33.9006MHz。该PDS使用一次迭代ROM，不能称192次镜像的新实现报告或实机Fmax。

10次候选短测逐笔WB/STORE、全状态、CRC/端口与计时规则检查、24故障边界和46相关回归的原有限结论保留。本轮没有重复运行这些DUT，也没有扩大完整ISA/特权验收。

## 已失败长测的可用部分

M6 performance守卫在2618.093宿主秒后因TRACE_BACKLOG_LIMIT退出，原campaign按既定策略停止validation，controller退出1，关闭预测未启动。这不是模拟目标时间达到10秒，也没有新CoreMark完整返回/最终CRC/全状态。

根因是pending统计glob('*.bin*')同时纳入了已压缩.bin.gz：performance实际未压缩8,388,608B，归档gzip92,302,580B，合计100,691,188B误超96MiB=100,663,296B门限。是宿主统计口径错误，不是已测出的CPU功能缺陷。原脚本/标准/门限保持，不在本轮修复重跑。

独立目录work/analysis/2026-11-03-coremark-evidence-alternative-v1/r3以流式解压逐笔重放每组31个完整压缩段。顺序参考维护自己的PC/寄存器/内存，WB与STORE各自有序比较；timer按原冻结N−2方程和参考读地址顺序核验，事件沿号单调。性能组逐段压缩/原始SHA与当时TRACE_INDEX核同；validation因campaign终止未写原索引，本次重建接收清单，核gzip完整性并重放，不能说其清单在DUT前冻结。

|种子|完整观测事件|合法WB|STORE|最后观测沿|参考已推进指令|结论|
|---|---:|---:|---:|---:|---:|---|
|performance|16,252,928|15,801,501|451,418|54,208,412|22,942,220|前缀匹配，整例未完成|
|validation|16,252,928|15,831,870|421,049|54,373,882|23,087,117|前缀匹配，整例未完成|

两组均9笔timer读、参考未到done，截断点的待匹配WB/STORE队列均为空；这只说明已观测前缀一致，不证明接下来没有漏事件。没有最终CRC、返回或终态验收。末尾.bin.part整段排除，保留原字节，不擅自拼接或把部分完整record当完整程序。三项新离线负向控制（错误数据/重复首条/半条记录）均明确拒绝。

## 身份、成本及限制

RESULTS记录本次所有M6原件复核前后SHA一致，INPUT_IDENTITIES列出其清单。两个完整前缀实际重放各约3秒；这只是宿主离线审查成本，绝不是新的目标执行时间或新DUT。复核初次宿主编译/重放在进程退出后未等Job消退即判失败，r1/r2日志保留；r3增加有界退出等待后正常通过，算法/原观测/期望不改。

“旧基线实机长测＋新候选严格短测/有限回归＋周期和资源时序对照＋长测前缀”替代本轮继续重跑长测的工作方案，不是对本候选>=10秒条件的等价证明或豁免。完整高阶2、S/U/PMP/Sv32、物理IO/CDC、候选实机/ILA仍未完成。没有真实退休PC，WB/STORE分流，固定初态/内存/有限输入，UART短测采用立即接收字节模型。

## 证据入口

- 基础实机：reports/hardware/2026-11-01-coremark256-full-svf-identity-closure.md及其原始RESULTS/物理UART；
- 新候选：reports/verification/2026-11-03-coremark-resource-no-board.md及M5 AUDIT/原始流；
- 本轮：work/analysis/2026-11-03-coremark-evidence-alternative-v1/下r3/RESULTS、INPUT_IDENTITIES、完整命令/原日志、NEGATIVE_CONTROLS、EVIDENCE_MAPPING及SHA清单；
- 原失败：work/advanced/2026-11-03-coremark-long-m6/CAMPAIGN_on_EXIT、commands/long-performance-p1、原压缩及未完成尾段。

下一唯一价值项是将这份准确分层结论纳入最终技术报告与代码证据索引，不新增CPU优化、DUT长测或硬件操作。
