# v02最终阶段交付：R1–R3差额复验与接收

2026-10-25，F152/D151。**可接收，范围为B既有CORE/LOCAL-REGIF的有限纯软件交付**。R1真实事件沿快照、R2绝对事件沿号、R3清单/重建缺口已关闭；一处旧版本说明字符串作为非阻塞N1注记保留。本结论不等最终作品验收、RX系统集成或FPGA验收。

## 收到什么与阅读范围

原件`D:/A_FPGA_Comp/队员成果接收/handoff-mainline-v02-20261025`，其中`artifacts/stage-return-final-20261027-v02`为收到的阶段镜像。外层80文件/79条SHA、阶段70文件15,472,523B/69条SHA全核同；阶段主SHA为`55995427F25973C8030D0ABB1F071471E2B8596CD5DF7B84C081606783D25D70`。目录交付即可，无ZIP不构成缺交；未访问B电脑的原始canonical路径，故“同字节”限收到镜像与声明SHA一致，不宣称另查B机器原件。

80逐项清单在同名evidence的`READING_CHECKLIST_COMPLETED.md/READING_COVERAGE.json`。0未读/0仅哈希：13代码/文档实际完整v01→v02差额加F149已核原文，6同SHA源复用完整旧审，其余结构解析/全文阅读；15阶段JSON全字段解析，44结果行及全部日志/波形引用核实；27原日志1434行逐行解析，5原VCD全部时间线逐配置核验。超长展示补以字段查询/逐行结果/实际差额，不据截断输出作结论。SOURCE_INDEX28项、CHANGED67项新SHA与23项旧SHA、10依赖、13计划artifact、8历史别名全部解析定位。原v01和历史包只读保留，不误报未重复携带的核心/包装缺交；无解压/执行包内入口/VVP/PYC/安装器。

DIFF的27文件47hunk均按确切2335旧源逐行重建当前实物；包括DEPENDENCIES/HISTORY_ALIASES/MODULE_STATUS/SOURCE_INDEX/delivery五个曾失败的元数据块，0上下文/重建错误。两冻结计划分别RX1.3.5 SHA979D6451…17E4、包装1.0.5 SHA5A955CD3…97A9。记录冻结时间/运行号仅作B证据来源，不当A亲自见证B冻结过程。

## 实际本机复验

在`work/peripheral-review/2026-10-25-stage-final-v02`复制11个输入并逐SHA核同，保留原件。已有Icarus/vvp13.0绝对路径及-B/VPI；固定7次非管理员外部编译各60s（本批工具审批另核，现已用完），普通7次vvp各30s。原收到TB/核心不改，A只增只读final observer导出共享RX数组，未force/写内部信号。源码与脚本先审，收到Python只隔离已审纯判定函数作host控制，不执行其main/清树入口。完整argv/cwd/rc/源SHA在work的plan/compile/run与各logs/process；本证据COMMANDS给导航。

|新目标|结果|实际证据|
|---|---|---|
|包装N16|PASS有限|26请求=9TX+6GPIO+11拒绝，6COMPLETE/3CANCEL/0BAD_STOP；所有请求字段/沿和公开pin模型相符，首帧37→197|
|包装N234|PASS有限|10请求=9TX+0GPIO+1拒绝，6/3/0，首帧6→2346；为缩小smoke，不是全W01–W10矩阵|
|RX N8|PASS有限|92事件、920pre/post字段，独立模型/共享捕获/内联逐笔顺序type/data/edge全同|
|RX N16|PASS有限|110事件、1100字段；seq0 edge170与seq30 edge2618均pre_valid0→post_valid1；5e edge8081 pre_clear1/pre_FE1→post_clear1/post_FE0、OV1|
|RX N234|PASS有限|68事件、680字段；全部快照/沿号无差异|
|RX共享捕获负测|PASS限定控制|错/多/漏/顺序及DROP/CANCEL/同沿替换捕获控制和正式要求marker全核|
|TX共享捕获负测|PASS限定控制|好帧、坏stop、多/漏帧、末半stop复位CANCEL，complete仍2|

7编译/7运行均原生rc0、无warning/error、无超时/截断，正常$finish；编译主机0.046–0.063s、仿真0.031–0.703s，仅资源开销，不是FPGA性能。结束仿真时间包装12,796,000/171,476,000ps，RX50,126,000/112,866,000/1,109,346,000ps；两个小负测2,346,000/6,556,000ps。RX预算5045/11319/110967，包装300000、小负测20000。未重跑GPIO全矩阵、Windows清树/非法N/watchdog全套旧机制、CPU回归或CoreMark；B的30PASS+1预期TB watchdog TIMEOUT仍单列为B原运行证据。

## 闭合判断和剩余事项

- **R1关闭**：原与新五波形分列；新RX共270事件、2700个真实pre/post字段全一致，无X/Z/漏/重复/错序。同沿先CONSUME后ACCEPT-REPLACE，共享数组逐笔精确匹配，移除晚一拍回标和DROP post_clear复制特判；不只看计数和PASS。A普通VCD公开模型逻辑检查不证明物理CDC/噪声/MTBF。
- **R2关闭**：每配置9个START逐笔对实际接受沿，6个COMPLETE逐笔对其真实E+10N及字节；另列observed=event+1，两配置12个完整结束均准确，3取消功能和末半stop控制保持。A独立公开pin模型重建帧，不拿相对日志差自证。
- **R3身份/重建关闭**：清单、SOURCE_INDEX/CHANGED、5元数据diff及活动计划/主要文档可解析核同。**N1非阻塞注记**：`work/peripherals/rx/results.json/tests[id=COM-01].expected`一句仍写`rx-plan-1.3.4.sha256`；实际expected_sha256、plan_check、run_manifest、当前脚本和A新源均1.3.5。这是原结果文案残留，不改原文件/不把它说成完全无瑕疵，也不要求B再跑或重封包；A导入收据明确标注正确权威来源。
- 通过已审正式analyze_run在新实际日志做2正确控制+11错误变异（非首请求沿、busy、COMPLETE event/observed、START、GPIO关联）全部拒绝；RX全局rc/截断/FAIL传播6控制通过，均host判据检查非新DUT。
- W06仍A既有补证，GPIO1.0.2有限接收；SHA核同不重跑。旧F123 60.078/59.063s和根OPEN_PREEXISTING保留，不将旧失败改PASS。根包归A/负责人，不再要求B修根。

## 导入、系统与下一步

`import-map.json`固定v02为当前B活动交付，v01/2335等保留历史；TX/GPIO/包装与F143、F151当前各3源码共6项SHA完全相同，记录来源映射即可，无须覆盖主线源或因文档修改重跑系统。RX核心有限模块复验已过，**RX未接入SoC，也未批准RX REGIF/FIFO/中断**。本轮0新CPU/SoC/CoreMark系统DUT、0PDS/许可/硬件，既有F143系统、F151双迭代校准和F146暂缓/F147告警分开保留。

B只需冻结v02并按A具体问题配合复验，无新核心开发、无必须补交、无必需ZIP/v03或重复审批；5项交接问题逐条回答在`deliveries/mainline-stage-final-v02-response-2026-10-25-v1/TEAMMATE_REPLY.md`，已生成可转交、未代发。B自述新增净工时3.5h(2.8–4.6)、余0.25h/无冲突不作独立工期承诺；10月27日18北京时间窗口不变，不自动取消/延期任务。

A下一回到F151后的正式CoreMark长测验证/资源方案：以实测校准为依据，控制原流体积/数小时成本并保留逐笔副作用验证；不是本次收件自动批准≥10s运行或CPU优化。Pango告警外部事实、正式时基/CDC/板级/ILA缺口仍在。over_temp STOP不变，无PDS服务器、设备枚举、JTAG、上电、下载、Flash或供电/SCBV/跳线/温控变更。
