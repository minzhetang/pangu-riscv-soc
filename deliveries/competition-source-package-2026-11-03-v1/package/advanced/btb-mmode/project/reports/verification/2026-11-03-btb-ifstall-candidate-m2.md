# 独立高阶候选M2：取指停顿、跳转与异常提交

2026-11-03，D323/F283。结论：**M2有限软件候选可接收，保护D300/SM2板级基线；不宣称完整高阶任务2完成。**

## 问题、证据及修复

M1在MMU取指停顿期间仍允许EX的redirect清空自身ID/EX，但EX/MEM因stall保持，导致JAL/JALR的链接结果没有进入后级。新的真实取指程序先用已有MRET/S态翻译路径运行到PC0xFF8，再让PC0x1000产生自然I-TLB miss。没有force、没有直接预置最终结果；既有S/PMP/Sv32仅为制造停顿的固定夹具，不增加这些实现范围或认定它们正确。

代表性新VCD确认：

- M1第26拍前：id_pc=0xFF8、id_valid=1、stall_all=1、i_hit=0、redirect=1；沿后ID变无效，最终x5链接缺失，签名STORE数据为0。
- M2第26拍：保持同一指令，redirect=0；第30拍stall消失才redirect，并将x5=0xFFC送入EX/MEM。合法链接WB恰好一次，目标签名STORE为0xFFC，错误路径STORE不存在。
- B原始HL4对not-taken分支在26–29拍stall中训练四次，第30拍又训练一次；M1/M2同一分支只在第30拍训练一次。本阶段补齐了M1尚缺的CPU级动态训练覆盖，不将它冒称M2新加的BTB门控。
- 新未对齐JAL叠加IF miss：第26拍异常已存在但不提交/重定向；第30拍提交EPC0xFF8、cause0、tval0xFFA，较老WB保留，故障指令无链接/STORE副作用。EBREAK叠加停顿另测。

M2只在独立cpu_hl4.v增加`!stall_all`到预测纠正redirect、异常提交及RET有效条件，令控制转移与实际流水线推进一致；准确diff在工作目录RTL_DIFF.patch。未修改BTB、MMU、PMP、CSR、ALU、control、regfile模块，未改生产RTL、外设、公共模型或冻结生产预期。

该方案在本有限、有界页表响应环境中验证；若MMU永不响应，异常也可能被等待。本阶段不证明总线超时机制或所有异常优先级。SRET/低特权返回及RET与stall直接重叠尚未单独动态验证，不因共用门控被称已验。

## 冻结输入与逐项结果

正式新输入为PLAN-v2.json及PLAN-trap.json。每条先给出手工WB/STORE/trap、最终状态与训练/解析次数，随后才跑对应DUT。每项下列结果均包含预测开/关×组合/同步取指及数据存储四配置：

|程序|M1同输入对照|M2|实际要点|
|---|---|---|---|
|jal_ifmiss|4 FAIL|4 PASS|保留x5=0xFFC，只到达目标一次，无错误STORE|
|jalr_ifmiss|4 FAIL|4 PASS|前推目标0x2000、链接及冲刷|
|beq_ifmiss_v2|4 FAIL|4 PASS|合法+8偏移，停顿后只解析/训练一次|
|bne_hold_training|4 PASS|4 PASS|not-taken保持；原B源码另有4 FAIL，重复训练5次|
|misaligned_jump_ifmiss|4 FAIL|4 PASS|停顿后正确异常归属，无故障链接副作用|
|ebreak_ifmiss|4 FAIL|4 PASS|异常提交与推进对齐，保留较老WB|

M1对照共4 PASS/20 FAIL，B原始HL4仅对前四程序另测0 PASS/16 FAIL。M2新用例24/24 PASS；复制并核SHA的M1原21程序/四配置相关回归84/84 PASS。**当前M2共108次最终有界运行通过，不把历史试验重复累计，也不以数量代表完成率。**

每次检查32寄存器及8KiB测试RAM终态、每笔非x0 WB、每笔STORE地址/数据/掩码及各自顺序，不去重。新用例还检查真实IF miss重叠、focus训练/解析次数、stall期无训练/重定向、trap提交前EPC/cause/tval及提交后CSR、最终特权状态。每例400周期明确结束，10秒进程限时，编译35秒；所有最终native rc0，无TIMEOUT，OwnedJob无残留。END是TB有界结束，不代表应用真实停机。

AUDIT.json独立重查24条新账本及84条回归账本；9个离线故障控制（缺/重链接、缺/重解析训练、错STORE、丢IF miss证据、截断及X）全部拒绝。八个代表性VCD快照严格分提交前和后1ps，不拿取指PC作退休PC。负向控制不是新DUT故障。无真实退休PC、WB/STORE分流、零初态、固定16KiB ROM/8KiB RAM/固定superpage PTE等限制保持。

## 原失败、测试错误与工具状态

初版BEQ计划使用0x1008正偏移，超出有符号13位B立即数范围，编码实际跳回PC0。这是本轮测试设计错误，不是CPU缺陷。原PLAN.json、prepare.py、对应日志/VCD/结果全部保留，不倒改。另立PLAN-v2.json，改为合法+8到0x1000，并独立解码核验编码；手工WB/STORE预期不变，前后源重新运行。无效旧BEQ结果不纳入正式CPU结论。

初版TB把TLB miss期无效物理地址的X一并判为控制失败；保留tb-initial.sv/run-initial.py及首轮结果。正式检查仍覆盖PC、有效控制、实际被IF接受的PA/指令及有效WB/STORE，不能以无效端口X制造CPU故障，也不放过有效数据X。

异常补测的第一次命令末段Python路径拼写错误，after-trap当时未启动；纠正路径后真实运行八次通过。该命令错误不混算DUT失败。本轮已知Icarus普通用户外部执行路径均成功；没有安装、管理员、环境/安全设置修改。M1沙箱0xC0000005根因仍未知，不因本轮成功宣布工具全面修复。编译保留control/regfile继承timescale及ALU无显式timescale警告，无编译错误、未屏蔽警告。

## 保护、身份和采用边界

- 八个source-before与M1最终源逐字节核同；source-original-hl4与M1原源核同；仅M2 cpu_hl4.v变化。
- 89个生产/应用保护文件SHA不变；M1原1410项文件清单全部核同，旧成果/失败/预期不改。
- 所有最终编译的RTL/TB输入SHA与当前文件一致，运行的VVP/程序身份及完整命令在COMMANDS.json。新报告和状态变更不重写原试验结果。
- 本轮没有新性能主张。M1小循环2/4时钟局部差值仍仅属M1数据；未拿生产CoreMark、资源、频率、实机/ILA数据替M2背书。
- 材料/哈希：已核；有限CPU软件复验：108 PASS；生产接口/全系统兼容：未验；本候选综合/P&R/频率/资源：NOT_RUN；位流/实机/ILA/正式性能：NOT_RUN。

可以把“取指停顿与跳转重叠导致链接丢失、branch保持期间训练次数”的**上述有限反例**从待复现推进为已修/已动态覆盖，不能据此关闭原R1全部时序组合。S/U委派、PMP/TOR/宽度、xRET低特权MPRV、walker权限/访问错误、fault-cache上下文等原审查问题仍未完成；不得称完整M-mode、完整HL4或完整高阶2。

当前推荐：保留M2为新的独立软件候选，板级继续使用已验D300/SM2。考虑11月4日用户已提供的作品截止，优先准确冻结已有成果，不在未验候选上冒进替换作品。下一唯一高价值软件项为补核有限M-mode的mtvec向量入口与CSR更新后中断响应，再决定是否值得用固定短程序进行候选性能分析；无新B工单、无自动PDS或硬件范围。

## 复现入口

`work/advanced/2026-11-03-btb-mmode-m2/START_HERE.md`、SUMMARY.json、AUDIT.json、RTL_DIFF.patch、COMMANDS.json；每次原输入/events/VCD见runs。PLAN-v2/PLAN-trap为新冻结计划，FROZEN_PLAN/FROZEN_EXTRA_PLAN保持M1 SHA；全包文件大小和SHA在SHA256SUMS.json，MANIFEST_CHECK.json为静态校验结果。材料检查不代替功能验证。
