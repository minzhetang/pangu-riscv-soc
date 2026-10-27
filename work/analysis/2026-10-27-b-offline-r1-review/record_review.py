from pathlib import Path
import json,hashlib,shutil
P=Path('D:/A_FPGA_Comp');H=P/'work/analysis/2026-10-27-b-offline-r1-review';M=P/'.project-memory';D=P/'deliveries/mainline-b-offline-r1-review-response-2026-10-27-v1';r=json.loads((H/'REVIEW_RESULTS.json').read_text(encoding='utf-8-sig'));post=json.loads((H/'POSTFLIGHT.json').read_text(encoding='utf-8-sig'))
assert '## F-161' not in (M/'FACTS.md').read_text(encoding='utf-8-sig');assert '## D-162' not in (M/'DECISIONS.md').read_text(encoding='utf-8-sig')
report='''# B离线R1 v02：有条件接收，三个生产守卫仍需补齐

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
'''
p=P/'reports/progress/2026-10-27-b-offline-r1-v02-review.md';p.write_text(report,encoding='utf-8')
hist=M/'history/2026-10-27-b-offline-r1-v02';hist.mkdir()
for n in ['CURRENT.md','INDEX.md','TODO.md','COLLABORATION.md']:(hist/n).write_bytes((M/n).read_bytes())
fact='''## F-161：B资源工具v02已收，三个过程守卫独立反例成立

- 2026-10-27，`reports/progress/2026-10-27-b-offline-r1-v02-review.md`及`work/analysis/2026-10-27-b-offline-r1-review/`分层证据。v02原件540文件/539SHA/5161927B，manifest5F06E6D6…3371C8ED、plan82C42434…F442AA4F核同；537变更/85索引、原DIFF59段可精确应用；原37/历史快照与frozen API不改。全部字节读取/解析含2故意坏JSON，54条B原结果/原日志无内在不一致，但仍为PASS_LOCAL。
- A独立冻结25项实际22P/3F（81.281秒），7种子+4旧流9378498条逐笔有限通过；C0–C3反例具体修复成立。三失败：16MiB阈值下真实资源夹具峰52289536B、0.828s越界而不kill；4KiB日志限额实际文件曾5242880B再截断；1秒主期限到2.016s才kill/总2.031s。后者总额在2.1内，失败为主期限，而非实际总超界。父峰被覆盖/无运行中父限制及fresh等待为静态剩余，不冒动态实证。
- 同字节源码副本/固定资源fixture，不改B或冻结预期；另便携入口再次重现三失败，rc1预期，不是DUT。A未重跑全54/新128MiB压力，不将B自测、旧流重放或文件核同当CPU/系统验收。原v01/v02及F160的60冻结输入后验核同；F160主线结果保持，硬件STOP。
- 总体有条件接收，G1–G3生产准入未闭；原“R1回执未知”被实际收到v02取代，新的差额回复送达/ETA仍未知。可转`deliveries/mainline-b-offline-r1-review-response-2026-10-27-v1/`，未代发，不扩原D158范围/窗口/硬件。C0–C3及现有有限功能不重复派发。

'''
decision='''## D-162：有限接收B v02，R1只补三组过程守卫，不扩任务或让A等待

- 2026-10-27，F161清单/原37/源diff与25项本机证据。接收材料及已证C0–C3/逐笔比较；资源生产准入仍有G1内存、G2日志写入、G3主期限三个实测反例。未采用以最后LIMIT/TIMEOUT、截断后大小或54PASS_LOCAL代替过程约束。
- 沿用已批D158，B只改自己的局部监督/内部绝对deadline及测试：运行中内存与测量失败/父256MiB硬限（不加外部字段）、有界日志落盘、主/总deadline和共享worker绝对时钟；新1秒测试kill<=1.1秒/总<=2.1秒，纠正新增2.6判据，原37/冻结API/比较语义不动。范围显著增大或需改冻结层仍停相关项请负责人，不自动接管或另开通用runner。
- 一次具体可转回复包已备，B回独立v03和最小差额/原始守卫证据/相关回归，既有输入可复用同SHA，不重跑外设/CPU。未代发、不推定新回执/ETA；10/27 18原外设窗口不自动改，也未替B承诺新截止。
- A不采用该工具替换生产比较器，不等待它阻塞F160主线只读正式测量/交付决策；CPU/新DUT/长跑/工具安装/PDS/硬件均无新增授权，over_temp STOP不变。

'''
for n,head,entry in [('FACTS.md','# 已验证事实与约束',fact),('DECISIONS.md','# 重要决策记录',decision)]:
 p=M/n;s=p.read_text(encoding='utf-8-sig');assert s.startswith(head);p.write_text(s.replace(head,head+'\n\n'+entry,1),encoding='utf-8')
p=M/'CURRENT.md';s=p.read_text(encoding='utf-8-sig').replace('F160/D160–161；恢复','F161/D162（B审收），主线F160保持；恢复',1);s=s.replace('B R1 F158/D158新回执未知、原10/27 18窗口不改；A不等B整包。','B R1 v02已收且有条件接收，G1–G3过程守卫待最小差额；回复已备未代发/新ETA未知。原10/27 18外设窗口不改，A不等工具整包。',1);s=s.replace('历史/协作按INDEX/COLLAB v1.88/TODO。','B审收`reports/progress/2026-10-27-b-offline-r1-v02-review.md`及`deliveries/mainline-b-offline-r1-review-response-2026-10-27-v1/`；历史/协作按INDEX/COLLAB v1.89/TODO。',1);p.write_text(s,encoding='utf-8')
p=M/'INDEX.md';s=p.read_text(encoding='utf-8-sig');a=s.index('最近更新：');b=s.index('\n',a);s=s[:a]+'最近更新：2026-10-27，F161/D162：B资源工具v02有条件接收，25独立检查22P/3F；C0–C3已证，运行中内存/日志写入/主期限仍待差额。主线F160及硬件STOP保持。'+s[b:];anchor='|---|---|';i=s.index('\n',s.index(anchor))+1;s=s[:i]+'|当前B R1 v02审收/三组最小差额|F161/D162；`../reports/progress/2026-10-27-b-offline-r1-v02-review.md`及`../work/analysis/2026-10-27-b-offline-r1-review/REVIEW_RESULTS.json、READING_COVERAGE.json、RESULTS.json、COMMANDS.md、POSTFLIGHT.json`。540/539、原37和59diff核同；B54自测/A25（22P3F）/便携反例分列。可转`../deliveries/mainline-b-offline-r1-review-response-2026-10-27-v1/TEAMMATE_REPLY.md`，未代发/新ETA未知；不重复核心，F160/硬件STOP不变|\n'+s[i:];p.write_text(s,encoding='utf-8')
p=M/'TODO.md';s=p.read_text(encoding='utf-8-sig');s=s.replace('# 待办事项','# 待办事项\n\n## 当前B R1 v02 F161/D162（2026-10-27）\n\n- [x] 540/539与原37/537变更/85索引/59diff核同；B54原日志审查与A25独立（22P3F）分列，C0–C3有限关闭。\n- [ ] 转交`deliveries/mainline-b-offline-r1-review-response-2026-10-27-v1/`（已备未代发）；B在D158范围仅G1内存/父守卫、G2有界日志、G3主/总绝对deadline及判据差额，回实际容量/ETA，不自动改窗口。\n- [ ] 接收独立v03，先审diff/冻结计划再复现三守卫及相关回归；不重发核心/大输入、不替B重写、不在未验生产守卫上叠加新功能。\n- [ ] A按F160继续正式测量/初赛证据路径只读决策，不等待B工具、不开新DUT或硬件。\n\n### 以下B R1回执未知/未收v02仅历史，现由F161实际收件取代；新差额回执仍未知\n',1);p.write_text(s,encoding='utf-8')
p=M/'COLLABORATION.md';s=p.read_text(encoding='utf-8-sig');i=s.index('版本：COLLAB');s=s[:i]+'''版本：COLLAB v1.89；2026-10-27，F161/D162。B资源工具v02已收，540/539/原37核同，25项A独立22P/3F；C0–C3有限接受，G1内存/父守卫、G2日志、G3主期限仍为原D158最小差额，不新派核心。回复包已备未代发/新容量ETA未知；原10/27 18外设窗不变。A保留F160，不把B工具接入生产、不等它阻主线，不扩大CPU/硬件；over_temp STOP。

### 历史v1.88（B回执未知已由实际收到v02取代，主线F160结论保留）

'''+s[i:];p.write_text(s,encoding='utf-8')
for n in ['CURRENT.md','INDEX.md','FACTS.md','DECISIONS.md','TODO.md','COLLABORATION.md']:
 text=(M/n).read_text(encoding='utf-8-sig');assert ('F161' in text or 'F-161' in text) and ('STOP' in text or '停止' in text)
print('Report + six memory files incremented and reread; original history kept')
