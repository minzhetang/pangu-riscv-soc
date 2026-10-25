# 最终阶段候选v01：资料、独立复验与最小差额

2026-10-25；目录虽名20261027，实际审查日期不是10/27。**整体有条件接收**：原核心和有限功能保持，已证的共享顺序/指定关联变异/新增末半stop取消关闭，余R1快照、R2绝对事件沿号、R3活动元数据。不是整包最终PASS或A新增系统/实机验收。

## 1. 实际检查范围

原件`D:\A_FPGA_Comp\队员成果接收\stage-return-final-20261027-v01`：70文件15,438,166B，主清单69/69核同，SHA **0C2970D74D4EA19C3A291A9F095666777C3243B687E817AD69C3BAA2A52EDFA8**；SOURCE_INDEX28项、10精确依赖、两新计划13artifact和历史8别名均可定位核SHA。无链接/reparse/异常路径；本轮不解压、不执行收到的入口/VVP/PYC、不重索旧整包。ZIP未生成符合原批准。

逐项70阅读表见`reports/progress/evidence/2026-10-25-stage-final-v01-review/READING_CHECKLIST_COMPLETED.md、READING_COVERAGE.json`：12当前全文、6当前完整差额＋已核原文、1同SHA完整旧读复用、51完整解析，0仅哈希/未读。复用按F148已全文证据与SHA，不冒称重新全文读。15JSON全字段/27日志1431行/5VCD全时间线/两计划SHA/主清单/DIFF全46hunk/27文件核查；9代码文件差额精确重建，5元数据文件不能重建当前实物，见R3。原未显示完的计划字段以结构化查询补查，不以PASS标记/总数代替证据。

## 2. 分层与实际执行

|层级|结论|
|---|---|
|材料|全到齐、主SHA/源索引/继承核同；CHANGED一SHA、DIFF五元数据块及活动说明仍不一致|
|B自测|计划RX1.3.4/run191037、包装1.0.4/run190737，PASS_LOCAL声明；功能波形支持、严谨快照和绝对沿号未全通过|
|A本机|新独立目录实际7编译/7运行正常，5正式公开端口有限功能通过；RX共享顺序新DUT关闭，快照/绝对沿号未闭|
|接口|CORE/LOCAL-REGIF-TXGPIO-M1原合同不改、核心/包装SHA未变；不自动扩大RX寄存器包装|
|系统|F143/O2稳定，F146候选仍由F147告警解释缺口暂缓；本轮0CPU/CoreMark/PDS/许可查询，不升级或撤销旧系统有限验收|
|硬件|STOPPED，0设备/JTAG/上电/下载/Flash/供电/SCBV/跳线/温控|

原5配置独立公开模型分别包装N16 18,022/N234 240,081、RX N8 42,504/N16 93,088/N234 889,328检查通过。全部36请求字段/沿号准确；原重审与新DUT严格分开，不以检查数代质量或完成率。W06仍A既有补证RESULTS SHA EA54…27CBA6、GPIO仍F123/F139/F148有限接收，二者不重跑。

工具现有MSYS2 Icarus/vvp13.0绝对路径，显式-B/VPI，不改PATH/安装/许可。执行清单在`work/peripheral-review/2026-10-25-stage-final-v01/plan.json`：7固定编译分别60秒限（本批外部工具许可另核、已用完），普通vvp分别30秒限，包装预算300000、RX5045/11319/110967、小负测20000。原11输入复制SHA一致；A额外final observer只读RX共享数组type/data/edge，不写信号/force。7编译无警告/错误，7新运行均rc0、正常$finish/无进程超时/未截断，严格验证器仍识别R1/R2失败，不能说7/7全面验收。

完整argv/cwd/rc/日志/新VVP/VCD/SHA在该work的plan/compile/run.json、logs各process/stdout/stderr和build；紧凑结果在本证据目录`new-runs.json、verification-receipt.json、new-*-wave/shared.json、V3-controls.json`。未执行收到的Python模块入口；已审纯函数由AST隔离验证，不执行安装、清树或其程序main。真实Windows清树/旧GPIO矩阵/watchdog非法参数未新跑，旧结果不变。

## 3. 已闭与剩余证据

|项|原/新实际证据|本次判断|
|---|---|---|
|V1共享顺序|新final观察数组与独立模型、内联全部type/data/edge一一相等92/110/68；异字节B2和同字节A1均真实覆盖|原4错序/配置关闭，不要求重开发共享捕获|
|V1部分快照|N16 CONSUME edge176 pre_ready1/post_valid0、5e edge8081 pre_clear1/pre_FE1→post_clear1/post_FE0及OV1均真|对应旧缺口关闭，不能延伸为所有快照合格|
|R1快照|N16 seq0 edge170 t1695000ps ACCEPT日志pre_valid1，真实0；seq30 edge2618 t26175000ps日志pre/post_valid1/0，真实0/1。三配置pre_valid差41/50/29、post_valid差8/16/2。新实跑全字段账本与原B日志逐行同，独立新公开波形通过|仍FAIL验证快照，不是RX核心FAIL。原因是S+1发现valid上升却回标S，+1ps也是晚一拍；直接复制DROP pre_clear作为post亦非普遍真实采样方法|
|V2完整帧/取消|COMPLETE已晚于stop中心，实际pin完整；共享小负测在末半stop复位得到CANCEL1/complete仍2，原各6完整3取消保持|无提前COMPLETE、取消有限控制已闭|
|R2事件绝对沿|N16实际E37/end197，日志START38/end198；两配置所有6完整事件均晚真实E+10N1拍。COMPLETE=日志START+10N只证明相对差|精确原事件沿尚未闭。可分event_edge与observed_edge，不改DUT或原合同；晚观察不等真实帧多一拍|
|V3指定关联|正确两配置analyze_run通过，非首edge+1/busy翻转/COMPLETE999999/GPIO99-999999变异全部拒绝；36真实请求全字段波形核同|限定变异及请求/GPIO关联关闭，绝对TX边界随R2，不另扩新任务|
|R3清单/diff|主SHA正确；CHANGED中SOURCE_INDEX宣称71757…B08D9，实物/主SHA AADC…77A2D；DIFF五块DEPENDENCIES/HISTORY_ALIASES/MODULE_STATUS/SOURCE_INDEX/delivery不能重建当前元数据，代码9块全部可重建|元数据条件仍未闭，不阻核心有限功能，不改旧包|
|R3活动说明|RX计划expected_by_config仍40/39等，与functional_expected41/41等冲突；旧106285/200000/旧status编号、旧5e post_clear0/content-equivalence未清。STATUS当前1.3.4段仍10/24及post_clear0。wrapper README/RUNBOOK旧monitor SHA C8CF…而现A638…D784；W01–W10活动负测引用旧run|仅新版本收敛/明确历史，不回改旧冻结计划，不因文档修改重跑DUT|

反例详`COUNTEREXAMPLES.json、rx-ledger-timeline-N*.json、new-TX-boundary-N*.json、diff.json、intake.json`。收到代码行定位：RX `ledger_push_cur`、posedge capture、`post_snapshot`，共享捕获与逐笔crosscheck；TX monitor的posedge检测与cnt=10N-1事件打印；runner `analyze_events`相对START校验。不能把新的成员比较修正忽略、也不能因总事件数正确忽略快照错误。

## 4. 下一步、责任与权限

B不再需要新核心开发、W06/GPIO重跑、CPU/SoC/PDS/硬件或重批接口。仅R1验证TB同真实事件沿的pre/post、R2事件/观察沿对齐并有限回归、R3新活动元数据；建议在新v02交差额、源码/TB/计划/原日志/VCD/results/SHA及准确继承。已闭项不用重做，元数据-only只解析核SHA。A负责必要差额复验/导入映射与A主线；旧根OPEN_PREEXISTING保留、不能转嫁无限修根或伪写PASS。

10/27 18:00北京时间返回窗口不变，用户转述B净工时6.0h(4.5–7.5)、余0.25h仅自述估计，不是独立验证或吸收返工承诺。仅问此次剩余净工时/是否冲突；冲突则原窗交真实已完+未闭，A给最小取舍负责人决定，不自行延期/取消RX/降低标准。当前无需用户提供旧包/再批普通信号选择，只需转交集中答复；未声称自动外发或ACK送达时间。

回复入口`deliveries/mainline-stage-final-response-2026-10-25-v1/START_HERE.md`、TEAMMATE_REPLY详细给具体事件/正确预期与R1/R2修法边界。收到新包不自动改变A稳定F143/F146候选与F147告警或over_temp STOP；本轮完成审收/记忆/精确Git单元后停止，原输入/源/失败均保留。
