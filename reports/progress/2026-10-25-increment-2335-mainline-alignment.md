# 2335增量主线审收与八问答复

日期：2026-10-25，北京时间。结论：**有条件接收**。原核心、包装及有限功能可以保留；仍有验证器自身错误和最终索引差额，不能把队员PASS或本机rc0升格为整包最终验收。

## 1. 本轮实际范围与阅读覆盖

已完整阅读接收窗口`D:\A_FPGA_Comp\deliveries\increment-review-20261024-2335-v01\MAINLINE_PROMPT.txt`（含第六节）及原`MAINLINE_ASKS.md`八问。原件目录为`D:\A_FPGA_Comp\队员成果接收\increment-20261024-2335`。逐项表及证据索引在`reports/progress/evidence/2026-10-25-increment-2335-alignment/READING_CHECKLIST_COMPLETED.md、READING_COVERAGE.json、coverage-details/`。

79文件/13,031,245B：25全文阅读、54完整解析，0仅哈希/0未读。17 JSON全字段、27原日志1428行（头/体/控制/原生结果，不只PASS）、5配置VCD全时间线、4清单、37文本文件67个diff hunk及全部修改Python/SV分段完整核查；截断处补读。主清单78/78＋清单自身=79；CHANGED新值76/76及15旧值、SOURCE_INDEX23/23同实物。主清单SHA256 **F6D9D9709DA7E60EFA30A83C1D8985D17445AFB0CFD446AB542C53DCB0B9539C**。无路径逃逸/reparse/链接；本轮未解压/执行包内程序。

继承链1345→1740→1930→0030→1735→2335，1735实际使用`deliveries/increment-review-20261024-1735-v01/extracted`，不存在的同名接收目录不当缺交。14依赖解析见dependencies.json。0030的002716结果已按同SHA找到原results.json，不缺交。当前history两结果与current同SHA，只是镜像，不是第二次DUT。旧1.0.2映到1.0.3、1.3.2映到1.3.3是替代而非同SHA历史，V4需澄清。

ZIP SHA **90C45380DEFBE503484443276AA0D23CC8C5BDB635F6829960CD55F4F8181441**仅队员声明；本机只有目录，没有独立核ZIP。目录已能审收，无需重索整包，不能宣称ZIP和目录已独立核同。

## 2. 六层结论与最新主线对齐

|层级|本轮结论与证据边界|
|---|---|
|材料完整|79项到齐并完整阅读/解析、继承可定位；最终活动索引/版本仍有V4差额|
|队员模块自测|包装1.0.3/run231958原13行PASS；RX1.3.3/run232514原30PASS+1预期watchdog TIMEOUT。有限波形支持功能，验证账本不全正确|
|本机独立复验|从源码新编译/运行包装N16/N234、RX N8/N16/N234及两个小负测。5配置公开引脚独立模型通过，但实际共享账本4处/配置错序，不能写成整体PASS。W06另A补足|
|接口兼容|沿原CORE/LOCAL-REGIF-TXGPIO-M1/1.0.0及质量补充，核心/包装SHA未变；RX只有CORE，不自动批准RX寄存器包装|
|系统集成|F141是提示中历史快照；当前稳定F143/O2、F146取指收益候选仍暂缓，F147未解释sdm2adm告警。本轮没有CPU/CoreMark/PDS新运行，不撤销旧有限系统结果|
|硬件|STOPPED，未上电/JTAG/下载/Flash/供电或SCBV/温控变更；没有新实机证据|

TX、GPIO、RX、wrapper SHA分别21044928…988C、03380919…F95E、BDCD02CA…9F34、5C81EE8F…64FA；精确整SHA/实际来源见dependencies.json与工作目录输入表。未修改任何收到的RTL/TB/旧结果/冻结计划或主线系统源。

## 3. 实际本机执行与严格判定

工具为现有Icarus/vvp13.0显式绝对路径、-B及VPI路径，无安装/PATH或破解ModelSim。收到的脚本只审阅；不用其VVP/PYC。本机新VVP均从源码生成。RX正式TB未改，额外加A只读final观察模块导出共享数组，不force/写内部信号。

实际12编译进程：11成功、1 A选项顺序失败（`-s: No such file or directory`）保留；成功编译无警告/错误。11次原生运行全部正常结束/rc0，无进程超时/截断，但两次A首版W06因time0 X判失败，不能称11/11功能全通过。后来仅修改A新TB显式X→0复位事件，在新v2文件另编译/运行两次并完整波形通过。UTF8源路径准备错误在guard截停、未启动编译器，亦保留不计DUT。失败没有伪装队员缺陷或删证据。

|本次新运行|独立功能/控制结果|实际主机耗时，仅运行开销|
|---|---|---|
|wrap16/wrap234|有限功能PASS，日志验证器仍V2/V3|0.063/0.109s|
|rx8/rx16/rx234|公开接口有限功能PASS；共享账本顺序FAIL各4项|0.062/0.094/0.656s|
|rxneg/txcapture|限定负向控制PASS，不代表原形式化/监视器全正确|0.047/0.047s|
|w06-16/w06-234（A v1）|FAIL：time0 GPIO/同步/引脚X，历史保留|0.031/0.062s|
|w06v2-16/w06v2-234|原W06合同边界有限PASS|0.046/0.063s|

原5 VCD重审分别18,022/240,081/42,188/92,732/889,084检查，合1,282,107，全部公开模型吻合；新5配置也独立核查，分开留证，不把重审当新DUT或测试数量当质量。包装36请求各字段/实际globaledge完全匹配；N16六GPIO写，TX9接受/11拒绝；N2349/1。两者各6完整TX帧+3复位取消，独立原始引脚无bad stop。RX原内联92/110/68有序type/data与公开模型一致。

所有命令、argv/cwd、超时/周期上限、原生rc、结束原因及完整日志/VVP/VCD路径见本证据目录COMMANDS.md、new-run-summary.json和`work/peripheral-review/2026-10-25-increment-2335/{plan,compile-result,resume-plan,compile-result-resume,run-result,w06-reset-*}.json、logs/、build/`。普通VCD；未重跑CPU/CoreMark/真实Windows清树/watchdog非法参数矩阵或PDS。

## 4. 按整改逐项关闭，不混淆核心与验证缺陷

### 已关闭或有限接收

1. 共享独立TX监视器已提供，正式与负测共用且只读clk/rst_n/uart_tx；RX共享capture亦确实实例化，旧“未提交”已取代，但不等全部语义合格。
2. 包装请求首edge/地址/strobe/error/ready/接受分类及所有实际沿号：36笔核同。不能继续说“完全不检查地址”。其余关联见V3。
3. RX所有事件沿号和内联有序type/data：92/110/68全部匹配；旧consume加一沿问题已闭。N16 5e edge8081 pre_FE1→post_FE0有真实支持，该具体FE缺口已闭，post_clear另列V1。
4. RX overall FAIL传播：当前case_status/classify_config原生rc/截断/globalFAIL控制均正确下传；源入口非零返回路径已审，未运行收到的入口。纯函数与原控制证据支持关闭这项，不等Windows机制本轮重跑。
5. **W06闭环**：原合同完成沿E+10N按沿前ready拒绝，不排队；E+10N+1才接受。B原1.0.3未覆盖不豁免；A已独立补测N16/N234，两轮/配置共4TX接受(5A/3C/5A/3C)、2拒绝、0GPIO，9,613/137,797独立检查全通过。回复包W06_SUPPLEMENT给源码/原日志/完整命令参数/两VCD/结果/SHA。B只引用A-W06-SUPPLEMENT，无需再开发或重跑；不得回称B原run覆盖。
6. **GPIO1.0.2有限功能可接收**：复核F123的W1/W8/W16及负测原结果、核心0338…F95E及计划BACF…47BE、TB D1C6…CF43/负测9479…7038；计划实物来自receiving-window-supplement-20261022-2214的gpio-plan.json。1.0.2是验证包，核心仍1.0.0。当前包装六次写/两级同步又得到主线新证据。已有1930 run_gpio.py SHA6CDD…34CC实际委托1735 runner_common，最终入口应指此组合；未声称旧入口已修或新跑Windows清树。F123 60.078/59.063s超时反例保留。此项不无限PENDING，不要求重写GPIO或重跑全旧矩阵。

### 剩余V1–V4（本批有限条件，不扩大核心开发）

|任务/优先级/负责人|准确证据|最小改动/验收|
|---|---|---|
|V1 P0 B：RX单一捕获与快照|**实际新DUT**共享数组三配置各4处错序。N16 seq92/93应ACCEPT B2→CONSUME B2，实CONSUME→ACCEPT；A1同字节亦错序。N8 seq74/75、78/79；N23450/51、54/55。内联/核心均对，不是RX核心FAIL。现嵌套成员存在循环不是一一/多重集证明；等数不同频次控制仍放行。原快照N16第176沿pre_ready0实际1、post_valid1实际0；5e post_clear0为后来撤销值，同事件NBA后实际1|只改TB/capture/必要检查和新计划，不改RX核心。公开沿前pre、NBA稳定后post（建议1ps，早于1ns刺激变化），后来时刻另列。逐笔type/data/edge一一有序，不去重；保持DUT reset/在途取消，跨测试历史显式保存。A1/B2、A1/A1、重复/错序/错字节/缺失/多余、DROP/CANCEL负控及三配置受影响复验通过|
|V2 P0 B：完整TX结束|现COMPLETE在stop中心后，早于完整10N结束7/N16、116/N234拍。现原/新完整引脚正确，尚未实跑末半stop复位反例；其风险为静态推论，不冒称该用例动态FAIL|保持公开引脚独立监视，在完整10N后COMPLETE，之前reset记CANCEL，可另记STOP_SAMPLE；不读ready/last byte回填。补1个末半stop复位控制，包装N16/N234+共享负测限定复验，原6完整+3取消期望不改、无核心改动|
|V3 P1 B：实际日志关联|第二请求edge+1仍递增、翻busy、COMPLETEedge999999、GPIO seq99/edge999999，现analyze_run均接受；首地址/首edge错误已能拒绝，不倒退宣称未改|与独立合同/实际请求和引脚时间线核非首edge/busy/事件edge/GPIO seq，所有这些变异须拒绝，正确控制通过，不能特判给定数字；与V2合批避免重复复验|
|V4 P1 B、A导入配合：最终元数据|主清单通过；模块子清单仍1过期PYC；RUNBOOK§6将231958称1.0.1；RX functional_expected已改但event_ledger仍旧40/39等，106285/200000旧预算与旧status run残留；新版替代错标旧历史，同SHA结果镜像未分清|只在新最终树/版本修活动索引；排缓存/VVP、单一权威计划/预算/版本，旧历史指确切SHA或明确未交过渡版/替代，不回写冻结旧包。无需为元数据重跑DUT，002716原件不缺交、不重索旧整包|

完整反例见回复包EVIDENCE/COUNTEREXAMPLES.json，以及本证据目录`new-wave-rx*.json、rx-ledger-timeline-N*.json、wrapper-request-correlation-*.json、isolated-controls.json、tx-monitor-boundary.json、semantics.json`。三配置快照字段差异分别见timeline文件，不只挑5e修数字。真实共享数组与合成负测分列，未证实的旧字节静态疑点不升级成实际数据FAIL。

## 5. MAINLINE_ASKS八问书面定案

完整可转交文本在`D:\A_FPGA_Comp\deliveries\mainline-increment-2335-response-2026-10-25-v1\TEAMMATE_REPLY.md`，本报告同时明确：

1. **接收**：整体有条件接收；上列六类已闭不重复，剩V1–V4，核心/包装/回执不缺、不重派。
2. **独立复验**：实际5正式配置+2小负测，以及A W06 v1失败/v2成功，工具13.0，12编译/11运行分列；不是只准备、旧波形重审或队员自测。RX共享序列不合格须如实保留。
3. **W06**：不能靠限制声明豁免；现A原合同范围N16/N234实际补足关闭，B只引用精确SHA，无重复实施。
4. **GPIO**：1.0.2有限功能可接收，原入口超时留历史、最终入口指1930+1735组合；不无限挂PENDING，不重做核心。
5. **旧根包**：A负责继承/导入映射与主线验收，B只负责新最终树活动索引自洽；旧handoff/check_package open不回写、不默认PASS，也不要求B无限修根。当前不需要改旧根的新授权。
6. **A边界**：CPU/同步存储/SoC/Timer/CoreMark/PDS/最终集成归A。无再缺B核心/包装或ACK；本批只需V1–V4验证交付差额，RX MMIO未批准、无新增B系统任务。不等A厂家答复/工具告警才收敛验证。
7. **窗口**：仍2026-10-27 18:00北京时间。新增2.1h/余0.5–1h仅队员预测非承诺；B反馈此次真实剩余量/冲突及未完项，不必重算历史。若冲突按原窗交真实完成+未闭，A给最小取舍、负责人决定，不自行延期/取消RX/降低标准。
8. **格式/立即行动**：B立即做V1–V4验证差额及最终封包，无需等接口/核心重新审批。新`stage-return-final-20261027-v01`目录（冲突递增），START_HERE、delivery、MODULE_STATUS、OPEN_ITEMS、CHANGED_FILES、DIFF、SHA256SUMS、SOURCE_INDEX、DEPENDENCIES、HISTORY_ALIASES、coverage_map；依赖精确到增量ID/相对路径/版本/SHA及用途。改动测试/计划先冻结，受影响编译/运行原日志及argv/cwd/rc/超时/截断、普通VCD、逐笔账本/results；旧已收依赖只引用。目录即可，ZIP可选、如有A独立核。无新核心开发，A收到差额后仅做必要复验，未声称已自动外发/收到ACK。

## 6. 主线立即衔接、授权与停止

A先完成本次公共状态吸收和集中回复，保护F143稳定/F146独立候选。B验证差额不阻断A既有TX/GPIO系统使用，也不把B承担A取指/PDS/过温咨询；A下次按已有阶段权限处理告警/证据，新增工具/硬件/重大修复仍过真实门槛。本次接收不自动批准新系统、RX包装、CPU/CoreMark重跑或PDS。

10/27窗口不自动延、11/4官方提交仍需正式测量/硬件与ILA等证据，不能用软件通过代替。当前需要负责人做的唯一交接动作是转发回复目录；A没有代联系队员。V1/V2为验证器缺陷，不以改预期/删重复事件或接管重写核心消解。

工作单元按D126审范围后Git同步：仅自己报告/回复/紧凑证据/审查脚本和A自写TB白名单，收到原源码/整个增量/工具/授权/专有模型/大型VCD及原日志/公共记忆排除。Git成功不升格任何功能/系统/硬件验收。原件保护与收尾哈希见本证据目录postflight-final.json和SHA256SUMS-final.txt；本轮结束不自动扩下一实施。
