# 1735增量主线审收：有条件接收

日期：2026-10-24（北京时间）；F139/D127。本报告基于原件和新的本机结果，不用接收窗口初检或队员PASS替代主线验收。技术系统基线仍F136/D123–124，Git状态另承接F138/D126。

## 结论与六层状态

**整体有条件接收；既有包装/三核心继续保留，现有软件系统不回退。**本批确实关闭了若干旧缺口，也有验证侧问题未闭，不需要重派核心开发。

|层次|本次结论|边界|
|---|---|---|
|材料与完整性|本增量可接收，最终组成包仍有条件|73文件全覆盖；旧根包不自洽、新模块子清单有缓存/别名问题，不称完整最终包通过|
|队员自测|原日志支持包装13 PASS、RX30 PASS+1预期watchdog TIMEOUT|runner自检、entry负测是机制证明，不等DUT/系统|
|本机复现|6个新源码编译及6次普通权限有界仿真完成；5份新功能VCD独立模型有限通过|包装2、RX3、RX负测1；非法/看门狗只审原证据，未新增运行；未重跑CPU/CoreMark|
|接口兼容|包装与原合同/当前系统一致，三核心/包装RTL未变；RX已批准核心接口保留|RX未集成、负测捕获等价性未证，不扩RX包装|
|系统集成|继承F134真实C→GPIO→UART及F136计时/双参数短CoreMark有限验收|本次0新系统运行；不是新的系统总验收或正式≥10秒成绩|
|硬件|未验，over_temp STOP保持|无PDS/服务器/设备枚举/JTAG/上电/位流/Flash或供电设置操作|

## 阅读、继承与完整性证据

原件`D:\A_FPGA_Comp\队员成果接收\increment-20261024-1735.zip`，SHA256 `FB1D7DEF3E1D57A3F9EDA6512D8159162819F0193887F92C50AABECE83502004`。

提取根`D:\A_FPGA_Comp\deliveries\increment-review-20261024-1735-v01\extracted`，下述包内路径均以此为根。独立重核80条目（7目录/73文件），总12267403B；规范化反斜杠后核路径、大小、重复、链接/加密标志及每条ZIP流SHA，全部与实物/接收清单一致。主SHA72/72、变更70/70及16旧值、SOURCE_INDEX19/19核同。**DIFF全部29文本文件、所有hunk逐行应用到旧源并与新实物对照**；未纳入diff的41项是另有逐SHA及结构/波形审阅的结果、日志、子清单和VCD，不是遗漏源码。

逐项填写副本：`D:\A_FPGA_Comp\reports\progress\evidence\2026-10-24-increment-1735-alignment\READING_CHECKLIST_COMPLETED.md`及`READING_COVERAGE.json`，对应接收窗口原READING_CHECKLIST的73行；原表/原件不覆盖。**23项全文阅读、50项完整解析核查，未读0、仅哈希0**。关键源码/计划全文；12 JSON全部字段解析，30原日志1503行完整解析，44结果行逐项与输入/日志引用关联，两份结构schema独立复核。先前输出截断的runner尾段和selfcheck已单独补读。五原VCD和五新功能VCD逐配置解析全部时间戳，未把非空/PASS末行作证据。

继承链1345→1740→1930→0030→1735按路径取最近有效版本；`dependencies.json`记录15项实际来源，含RX正式/负向/非法/watchdog/include、包装/TX/GPIO、schema和runner辅助。关键继承：

|依赖|完整实际路径/版本|
|---|---|
|包装|`D:\A_FPGA_Comp\队员成果接收\increment-20261024-0030\work\regif\txgpio-m1\src\local_regif_txgpio_m1.v`，SHA5C81EE8F…D264FA|
|TX/GPIO/RX|`D:\A_FPGA_Comp\队员成果接收\stage-return-20261023-1345\work\peripherals\src\uart_tx.v`、`gpio\src\gpio_core.v`、`rx\src\uart_rx.v`，SHA21044928…988C/03380919…F95E/BDCD02CA…9F34|
|共享比较器|`D:\A_FPGA_Comp\队员成果接收\increment-20261023-1930\work\peripherals\rx\tb\rx_ledger_check.svh`，C8FFFF1A…7868；只比较type/data，不比较时间/状态|
|包装回执|`D:\A_FPGA_Comp\队员成果接收\increment-20261024-0030\work\regif\txgpio-m1\docs\CONTRACT_RECEIPT.md`；D115原批准有效，不重索或重批|

## 逐整改结论与反例

|事项|本次判定|关键证据与精确限制|
|---|---|---|
|旧delivery新SHA错误|已关闭|70/70新值核同，旧包不倒改；META_CORRECTIONS明确纠错|
|First/Next error=0误正常结束|已关闭限定项|`work/peripherals/scripts/runner_common.py`的实际API调用读取错误码，经`_enumeration_error`只允许18；主线隔离模拟实际snapshot函数First/Next×0/18/5共6项符合；不是真实进程枚举|
|清理时限/限长/未知rc既有修正|保留条件支持|完整自检原记录：正常hang总1.172/cleanup0.156s；故意失败加手工清理总4.141s、清树3.016s；unknown总4.046s，均原阈值内。文档4.172/3.031等与该run JSON不符，采用原JSON。未新运行Windows真实清树，F123的60.078/59.063s失败保留|
|包装缺TEST_PASS仍PASS|已关闭限定项|新run_regif精确/唯一标记及analyze_run检查；收到2正确+12拒绝控制。主线原日志2正确+13项各missing/duplicate共28隔离控制通过；不沿用旧表达式反例|
|W01与GPIO重复写漏计|已关闭功能/数量项，时间字段未闭|原/新VCD均支持N16实际26请求=9TX+6GPIO+11拒绝，N23410=9+0+1；每配置6完整+3取消。GPIO A5,A5,5A/11,11,22逐笔保留。逐请求seq/addr/data/strobe/error/ready/busy/真实核心使能均一致，但N16有11/26、N234有1/10的edge日志比实际采样沿少1：两个Active always间edge_count竞争；例如N16首请求日志edge8、实际第9沿|
|持续独立TX帧捕获|未关闭|包装TB132–150仍以tx_ready回升认COMPLETE，字节取last_tx_byte；该值由显式check_tx_frame→decode_tx更新（245–280），不是持续串流独立解码。日志增删拒绝只能证明比较端。当前帧波形正确，不推断一定存在额外DUT帧|
|包装逐笔关联的自动判定|部分关闭|主线已独立关联全部36笔请求；但正式analyze_events主要比较数量/数据序列，不核seq/edge/addr/strobe/flags关联。隔离把seq1的addr改fc、edge改999999仍被analyze_run接受。要求补实际字段一致性，不要求更改RTL|
|RX同字节替换、5e DROP、CANCEL采样实现|具体补项已收到/功能支持，字段对齐未关闭|新A1/A1场景三配置各增4事件，92/110/68逐笔type/data与独立协议时间线吻合；CANCEL post确已#1读取公开端口，不再填常数。5e pre_clear已1，不重复补DROP/同字节。全部字段仍混采，见下例|
|RX正式捕获路径负测|未关闭|正式TB199–308内嵌采样/串行延迟/异步CANCEL；负向TB35–84另建rx_public_capture，人工cap_line_good/cancel且替换时先把data置new。共用末端比较宏不等捕获复用或等价；15负向marker及本机该负测通过只支持另一路径|
|RX失败传播|新增实证缺口，未关闭|run_rx.py171–180仅传播TIMEOUT/TOOL_ERROR；传overall=FAIL和含TEST_PASS的block实际返回PASS。最终main只看rows，因此配置级native非零/截断/全局失败可能被逐行吞掉。现有六新运行真实rc0，不是假称本次DUT已失败|
|冻结计划/说明/模块子清单|有条件|新RX计划event_ledger.expected_by_config仍旧40/39、49/48、28/27，而实际/内嵌预期为41/41、50/50、29/29；tb_max旧通用字段与新预算并存。RUNBOOK还留旧TB SHA/版号，W01–W10说明VCD字节旧值，W06文字包含ready回归沿请求但本TB只发busy内请求，不能声明该边界已由此覆盖|

RX时间线具体反例：三配置全量公开端口合同模型分别42188/92732/889084检查无不符，但账本pre/post不等统一事件沿前后。N16 5e实际S=第8081沿、80805000ps，沿前FE=1、OV=1、clear=1；NBA后FE=0、OV=1。账本pre_FE却0、pre_clear取上次1，混用时刻。post_clear=0可作为后来撤销后的观察值，但若如此须另标观察时间，不能把它与S前态混成同一快照。三配置消费记录均少标1沿；ACCEPT的pre_valid取已发布的1，CONSUME的post_valid多仍填1。主线`rx-ledger-timeline-N*.json`保留每笔对照，不靠单个数字判定关闭。CANCEL改为实测后态的具体修正可接收，不能因此把所有RX状态字段一并关掉。

模块子清单65项：64项内容可匹配，其中命名历史`results-regif-m1-20261024-002716.json`未按该名携带，但0030的`results.json`同SHA，已解析继承等价物，**不是缺失功能结果**。1项PYC SHA过期，不执行该缓存。最终新包应排除缓存、明确别名/来源，不回改旧包。根handoff check_package既有manifest/source/link FAIL继续单列；B只为新交付生成可解析自洽索引，A维护旧基线和主线导入映射，不无授权改原handoff。

## 新编译、仿真与证据位置

独立目录`D:\A_FPGA_Comp\work\peripheral-review\2026-10-24-increment-1735`。8输入逐SHA复制/前后保护，原件未改。工具既有Icarus/vvp13.0，绝对路径及-B/VPI设置，PATH不变。普通沙箱单目标probe再次0xC0000005，保留原process；经工具审批后**一次固定六目标非管理员沙箱外仅编译**均rc0，未重装/改策略。随后6次vvp普通权限运行，无进程超时，正常$finish且真实检查结果核对；该批外部编译许可已用完，不是常设执行权限。

|新目标|结果|普通运行秒|独立端口比较/账本|
|---|---|---:|---|
|包装N16|有限通过|0.078|18022检查；26请求/9TX/6GPIO/11拒绝，6完整+3取消|
|包装N234|有限通过|0.093|240081检查；10/9/0/1，6+3|
|RX N8|有限通过|0.063|42188检查；92事件，最后5013拍/预算5045|
|RX N16|有限通过|0.094|92732检查；110事件，最后11287拍/预算11319|
|RX N234|有限通过|0.609|889084检查；68事件，最后110935拍/预算110967|
|RX负测N16|限定通过|0.031|15个控制/检出标记；不证明正式捕获等价|

编译各60s限、运行各30s限，0编译警告/错误；普通VCD。5原波形合计1282107端口比较；5新功能波形独立重核相同数量，分别计数，不把原波形重审叫新DUT。独立源码/所有日志和完整命令在native目录`plan.json、compile-probe.json、compile-batch.json、run-result.json、logs/*/process.json`；波形`build/*.vcd`，新VVP本机生成，未执行来包VVP/PYC。

审收证据根：`D:\A_FPGA_Comp\reports\progress\evidence\2026-10-24-increment-1735-alignment`。`intake-checks、diff-check、structured、logs-parsed、semantics、isolated-controls、wave-summary、ledger-timeline-summary、new-run-summary、postflight.json`及逐配置JSON；`SHA256SUMS.txt`含审阅脚本/本机产物完整SHA。postflight核ZIP与73原件、8复验输入和F136整组8源SHA不变。机制mock/日志变异不计DUT。

## 衔接与最小后续

A不等待B重新开发/批准；保持F136有限系统，继续方向为生产可综合存储绑定、PDS映射/资源/Fmax的**A-FPGA-IMPLEMENTABILITY-M0**，仍未获新实施/PDS执行批准，本次未启动。正式CoreMark与FPGA/ILA缺口保持。RX没有包装或系统验收，不因新核心有限通过自动接入CPU。

B现在仅收敛既有验证端：持续TX公开引脚捕获与逐请求/真实沿关联；RX同一正式捕获路径的负测/统一时刻快照及失败传播；新计划/索引去歧义。保留所有已收核心/合同、已闭entry/err0、功能支持/旧失败，无需重交旧材料或重跑CPU。修后只跑受影响包装两配置/RX三配置与小型机制负测；元数据-only不重跑DUT。详可直接转发`D:\A_FPGA_Comp\deliveries\mainline-increment-1735-response-2026-10-24-v1\TEAMMATE_REPLY.md`。

10/27 18:00（北京时间）窗口不自动变。新增2.7h/剩余0.5–1h均队员估计，非主线独立计时或足够工时承诺；仅需补本次真正剩余工作的差额/冲突。若不足，按原窗交真实完成部分与未闭项，由A提出最小取舍、负责人决定，不自动缩RX/延期/降低标准。回复已生成待用户人工转交，未代发或声称送达。硬件STOP保持。
