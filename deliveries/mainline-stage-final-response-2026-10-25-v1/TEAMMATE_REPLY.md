# 给B队员及其AI：最终阶段v01复核结论与最后限定差额

70文件已收到，主SHA69/69、SOURCE_INDEX28项、10依赖和13计划artifact实物核对通过。全部文件已按全文阅读/完整差额＋已审原文/同SHA复用/完整解析分类核查。A已从源码用现有Icarus/vvp13.0实际重编7目标并运行：包装N16/N234、RX N8/N16/N234、RX负测、共享TX捕获负测，全部正常结束且原生rc0/无编译告警错误；五配置公开端口有限功能通过。候选仍**有条件接收**，并非整包最终验收；以下直接作为本轮书面反馈，无需重开接口或核心审批。

## 已接收并关闭，不重复开发/索包

- **V1共享事件顺序关闭**：真实新DUT的只读final数组导出与独立公开模型、内联账本三方逐笔type/data/edge完全一致，N8/N16/N234为92/110/68；原4处/配置错序已消除。同字节/异字节实际路径均核过，核心功能不改。
- **V1具体快照部分关闭**：N16第176沿CONSUME pre_ready=1/post_valid=0正确；5e第8081沿pre_clear1/pre_FE1→post_clear1/post_FE0/OV1正确，三配置对应原字段问题已收窄。其余ACCEPT快照仍R1，不重新要求补DROP或CONSUME这些已证项。
- **V2功能部分关闭**：TX不再在stop中点提前记COMPLETE；本机共享负测确实执行末半stop复位，CANCEL=1、完整帧仍2，控制通过。现有正式各6完整/3取消/0bad stop及公开串行pin正确，剩事件绝对沿号R2，不是TX核心失败。
- **V3指定关联变异关闭**：非首edge+1、busy翻转、COMPLETE edge999999、GPIO seq/edge错改均通过正式analyze_run的已审纯函数拒绝，正确控制通过；所有36真实请求与独立波形吻合。不重复22例入口自检或全旧矩阵。TX绝对时基只随R2核，不另派一套任务。
- W06继续由A-W06-SUPPLEMENT关闭，RESULTS SHA EA54D33B…27CBA6匹配，B无需重跑；GPIO1.0.2有限功能结论保持，无需新GPIO开发/全矩阵。旧F123 60.078/59.063秒失败和根包OPEN_PREEXISTING保留。

## R1（P0，B）：只修剩余RX事件快照，不改RX核心

实际反例可在你方原VCD和A新运行同时复核：
- N16 seq0/edge170（1695000ps）ACCEPT：日志pre_valid=1，真实发布沿前0，NBA后1。
- N16 seq30/edge2618（26175000ps）ACCEPT：日志pre_valid=1/post_valid=0，实际应0/1。当前+1ps观察发生在晚一拍的捕获沿，拿到了随后consume后的值；把时间标回旧沿不能修正快照。
- N8/N16/N234分别仍有pre_valid 41/50/29处、post_valid 8/16/2处不匹配；其余当前已检查字段均吻合。

最小推荐：保留已正确的共享捕获及冻结程序/预期。内联账本在独立串行解码确定的真实S事件沿保存不可变pre公开端口快照，NBA后同一沿+1ps读取真实post；不要在下一posedge才发现valid上升后把edge回标。真正consume→replace同沿先CONSUME后ACCEPT，两个事件各带该沿pre/post，不用negedge晚态冒充沿态。可先收集当沿事件，统一在NBA后补全，不读取隐藏DUT状态、不靠预置最终值。

删除DROP post_clear直接复制pre_clear的特判，改为真实post公开输入采样；现5e应仍为1，不是要求改它的预期。复位/CANCEL继续来自真实DUT reset/在途状态，监视器若跨用例保留历史须显式区分全局账本与DUT复位，不丢事件。**不能以固定写pre_valid=0或从期望表回填解决。**只需新的TB/必要捕获检查/冻结计划和受影响RX三配置原日志/VCD；保持92/110/68和功能预期，逐条校验所有pre/post、无X/Z、无漏/重复；全程不改RX RTL。

## R2（P1，B）：TX事件沿号对齐原合同，区分事件沿与观察沿

N16第一次实际接受/串行起始E=37，完整10N结束应197；当前START记38、COMPLETE记198。N234同样所有6个COMPLETE都比真实E+10N晚1拍。你方COMPLETE=日志START+10N成立，但日志START本身晚1拍，不能据此宣称原合同E+10N精确匹配。

保留已经正确的完整帧/复位取消功能；只统一event_edge定义并与实际接受/公开pin跳变独立关联。若监视器晚一拍才观察，另列observed_edge，event_edge应是真实事件沿；不要只把两个日志相对差视为证明，不改TX/包装RTL或软件/合同。验收：N16首帧event end=197，N234按其实际E+2340；所有原正式完整帧逐笔匹配，六帧/三取消及末半stop复位控制无退化；必要串行事件edge变异仍拒绝。只复验受影响包装N16/N234及共享TX小负测，可合批，勿扩大矩阵。

## R3（P1，B；A管导入）：最终元数据一次收敛，元数据-only不重跑DUT

- 主SHA清单正确，但CHANGED_FILES对SOURCE_INDEX写71757D0B…B08D9，实物/主SHA为AADC4220…77A2D。SOURCE_INDEX自身28条都可解析，不要求重发依赖。
- DIFF.patch的全部9个代码文件差额能对实际旧源重建，但DEPENDENCIES/HISTORY_ALIASES/MODULE_STATUS/SOURCE_INDEX/delivery五个元数据块不能重建当前实物。请从确切2335旧源与最终当前文件重生成，不能在已生成diff后再改这些活动文件而不更新。
- 活动RX1.3.4计划的event_ledger.expected_by_config仍40/39、49/48、28/27，与functional_expected的41/41、50/50、29/29冲突；expected_per_configuration仍106285/200000旧预算、旧status run号，ledger旧5e post_clear0/content-equivalence与新规则冲突。按当前配置5045/11319/110967和实际新证据设唯一权威值；历史内容移到明确historical字段，原旧文件不回写。
- RX STATUS顶端把1.3.4标为10/24且仍说post_clear0/内容等价，和本文新证据不符。wrapper README/RUNBOOK仍引用旧共享TX monitor SHA C8CFFA9F…（现A638BCE5…D784）；W01–W10活动证据列仍指旧232004/231843。只修活动引用，不删除历史；旧根和旧包不动。

先冻结源/说明/计划，再生成SOURCE_INDEX、准确DIFF/CHANGED，最后生成主SHA，保证索引与清单无循环自包含。每个活动引用都定位并核版本/SHA，原旧计划/结果标历史，所有更正写入新v02。纯文档/索引修改只做解析/哈希自查，不能算新DUT，也不要求重跑DUT。

## 现在做什么、等待什么与窗口

B现在仅做R1、R2两项验证端修正及R3最终索引；核心/包装/新功能开发均无需继续。接口原批准有效，不等A CPU/PDS/厂家答复；若真的必须改核心或已批接口，先交最小矛盾，不自行扩大。A负责差额复验、导入映射、CPU/存储/SoC/Timer/CoreMark/PDS/最终系统和报告；本次未把B结果升级成A新系统/硬件验收。

交`stage-return-final-20261027-v02/`（冲突用唯一新版本）及入口START_HERE；包含R1/R2更新TB/必要检查、新冻结计划、原生compile/run日志与命令/rc/结束原因、普通VCD/完整账本/results，R3新的索引/清单/diff、OPEN_ITEMS和精确继承。已收不变核心、W06/GPIO及旧包只引用，不重发整套历史，目录即可、ZIP仍可选。A已接收v01中能关闭的项，后续只核差额及相关回归。

返回窗口仍2026-10-27 18:00北京时间；6.0h及余0.25h是你方自述估计，不当作无条件吸收本轮返工的承诺。请只反馈R1–R3实际剩余净工时与窗口冲突；若冲突按原窗先交真实完成+未闭清单，A给最小取舍、负责人决定，不自动延期/取消RX/降低标准。

硬件STOPPED，0新PDS/服务器/JTAG/上电/下载/Flash/SCBV/供电/跳线/温控权限。A没有代发本文，负责人转交后无需再批准上述原范围普通验证修正。
