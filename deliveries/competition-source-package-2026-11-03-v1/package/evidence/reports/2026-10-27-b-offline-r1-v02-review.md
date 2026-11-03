# B离线R1 v02：有条件接收，三个生产守卫仍需补齐

2026-10-27，F161/D162。**C0–C3具体反例已得到主线独立支持，但不能据此将通用资源/失败守卫认定全部完成。** 整体有条件接收；已证比较/路径功能保留，资源工具不接入A生产验收链。此次没有CPU/ISA/DUT/安装/PDS或硬件操作，F160主线不变。

## 身份、覆盖与分层

原件`D:/A_FPGA_Comp/队员成果接收/B-VERIFY-OFFLINE-M0-return-v02/`，540文件、539条SHA、5161927B，清单SHA **5F06E6D6BCC3034D7EA1753BAE1168613519D45318881AD43B85E6F63371C8ED**；计划SHA **82C42434FDE78495B6A3F9F945756F1ADE464EEEB6A5E9DC3D63E5C5F442AA4F**。所有原字节读/哈希，JSON/源码AST完整解析；两份故意无效JSON被识别为负向输入，不误报缺失或不可读。逐文件状态见READING_COVERAGE，未把机器解析当全部人工语义判断。

关键RUN、support、worker、测试驱动/生成器和六固定fixture已完整源码审查。537项CHANGED_FILES、85项SOURCE_INDEX均与新旧文件匹配；1.56MB原DIFF的59段全部回查v01并应用得到v02相同行内容。原37例计划/预期逐对象一致，历史计划/结果与原件同SHA，冻结API/codec同A原包。B的54条结果逐项与计划、父rc、worker结果、原stdout/结果日志对应，无材料内不一致；这只是B原运行证据，不计A新运行。

|层次|结论|
|---|---|
|材料完整性|可接收，540/539与元数据/继承链核同，原件未改|
|B自身测试|54/54 PASS_LOCAL资料确有支持；三个新守卫测试判据不足，不能直接升级生产验收|
|A本机复现|独立冻结25项，81.281秒，22 PASS / 3 FAIL；另便携入口独立再次重现同三失败，均非DUT|
|比较功能/ABI|7种子及四旧流9378498条真实逐笔重放有限通过，保留重复事件；冻结ABI1.0.0字节同A，没有换CPU参考|
|系统集成|本工具未接入A在线采集或生产验收；F160既有结果不改变|
|硬件|STOPPED；无温度/供电/FPGA验收提升|

A没有为本轮重新执行整54或生成128MiB压力；B旧37/压力证据与A所做25项明确分列。已发现P0阻塞，不为获得更多计数重复全套。没有新DUT、ISA参考或CoreMark成绩。

## 已关闭与实际剩余

C0默认8条MATCH；C1的1B门槛启动前LIMIT/5、没有worker；C2在256B下LIMIT/5且没有超限result/worker-result；C3优化模式拒绝且副本工具树不变。另-O/-OO、足量结果容量、非零rc/缺结果/只打印PASS、受保护无效JSON、CASE先验上限等有限本机证据成立。CASE/index先stat源码及B原日志已审，归档index上限项本轮没有另计A新运行。

|项|原授权验收|A实际证据|定位|
|---|---|---|---|
|G1运行中内存|越界时终止并wait，父也有测量/上限，None不当0|固定32MiB资源夹具，16MiB阈值下峰52289536B，158次越界观测跨0.828秒；kill列表为空，worker正常rc0，结束后父才LIMIT/5|原件RUN.py:150–154只记录peak，:262事后比较；正常结果合并丢掉父peak且无父运行中限额。后两项为静态证据，不虚构已动态测父超限|
|G2日志有界写入|运行中及最终文件均<=限额|B固定flood、4096B阈值，A独立观测最大5242880B，B原raw_stdout_bytes同值；最终才截到4096B，仍LIMIT/5|RUN.py:145直写文件，:155轮询大小，:174事后truncate。最终失败码正确但过程限额未执行|
|G3主期限/总期限|1秒主阶段停止，1秒清理；观察kill<=1.1s/总<=2.1s|固定sleep实际到2.016s才kill，2.031s结束，TIMEOUT/6。总2.031在2.1内，**失败在主阶段并未按1秒停止**|RUN.py:140/160用case+cleanup当kill线，:166/170又给fresh cleanup；worker.py:152将remaining重新锚定启动后时钟。额外总超界仅静态风险，未宣称实际发生|

B原R1-TIMEOUT计划max_elapsed=2.6放宽了原任务100ms观察容差，不能作关闭依据；原37未改仍保留。A内存/期限两项是固定资源fixture驱动同一个真实execute_case，仅测父守卫，不是假装完成记录比较或CPU测试。日志则为真实CLI固定fixture。

## 最小差额与并行关系

D162维持D158范围，只需G1–G3局部监督/内部deadline与相应测试纠正，不动冻结API/codec、原37、比较语义、CPU/外设或主线采集。父限额采用已有256MiB硬上限，不新增CASE字段；轮询中的内存/测量失败、可封顶写入的PIPE消费、一个主deadline与一个总deadline、同绝对worker deadline是推荐实现，B自行收敛细节。禁止新通用runner、任意命令/清树或冻结内核修改。

回唯一独立v03，准确diff/新SHA/预冻结新增判据/真实父与worker码/kill及清理时刻/运行中内存与文件峰值/相关回归。原37与已有压力输入可复用同SHA版本，不必重建大数据；不要重跑UART/GPIO/RX、CPU或PDS。若必要修改超D158边界或超工作容量，集中列原因/最小方案再交负责人，不自行扩。

可直接转交的完整回复和可运行三个小反例位于`D:/A_FPGA_Comp/deliveries/mainline-b-offline-r1-review-response-2026-10-27-v1/START_HERE.md、TEAMMATE_REPLY.md、REPRODUCE_GUARDS.py`。包已备，A未代发/未推定B收到新回复或承诺ETA。默认校验v02清单；当前代码运行应三FAIL、entry rc1，这是反例重现成功，不是通过验收。

10/27 18:00为原外设窗口，不由本轮R1自动顺延；未另设B新承诺日期。A负责公共状态/复验/主线正式测量路径，B不再等待新核心审批，也不需要重发已收大包。工具整改不阻塞F160的主线只读决策，硬件STOP不变。

## 复查入口

`D:/A_FPGA_Comp/work/analysis/2026-10-27-b-offline-r1-review/`的INTAKE、READING_COVERAGE、MATERIAL_AUDIT、PATCH_CHECK、CODE_DIFF、FROZEN_PLAN、RESULTS、REVIEW_RESULTS、COMMANDS及POSTFLIGHT；logs逐例真实rc/stdout/stderr、两个资源probe全观测和便携复现分列。原B包、v01以及F160的60执行冻结输入均SHA核同。私人路径与大原件不纳入Git；报告不记录许可证或机器标识。
