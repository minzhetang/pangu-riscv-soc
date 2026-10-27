from pathlib import Path
import json,hashlib
P=Path('D:/A_FPGA_Comp');H=P/'work/analysis/2026-10-27-measurement-path-m0-v2';M=P/'.project-memory';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));v=read(H/'TIMED_WINDOW_PROFILE.json');c=read(H/'COST_AND_VALIDITY.json');post=read(H/'POSTFLIGHT.json');D=P/'deliveries/mainline-board-coremark8-bitstream-scope-2026-10-27-v1';scope=read(D/'SCOPE_STATUS.json')
assert '## F-162' not in (M/'FACTS.md').read_text(encoding='utf-8-sig');assert '## D-163' not in (M/'DECISIONS.md').read_text(encoding='utf-8-sig')
gaps=[dict(requirement='CPU合法C/同步片内存储/TXGPIO/Timer',evidence='F130–143/F151/F160全态、逐笔、计时、UART',status='FINITE_SOFTWARE_EVIDENCE_ACCEPTED',owner='A/B existing integration',next='Protect stable RTL; do not reopen unrelated ISA'),dict(requirement='最新短程序CPU位流',evidence='F162: oldPDS1 vs8 INIT one byte; old flow no bitstream generation',status='PENDING_PDS_SCOPE',owner='A',next='one unchanged8-image PDS build, not hardware'),dict(requirement='CoreMark双种子>=10秒与真实时钟',evidence='F160performance8 nominal0.623313s; validation onlyold2; SIM ONLY marker',status='NOT_MET',owner='A + approved FPGA platform',next='after bringup, separate calibrated measurement port and both-seed candidate scope'),dict(requirement='CPU实际运行/片上关键算法波形',evidence='only CPUsoftware simulations and PDS logicalimplementation; noCPUhardware',status='BLOCKED_SAFETY_AND_PERMISSION',owner='A/user/Pango platform',next='safe usable platform + separate hardware/ILA authorization'),dict(requirement='效率收益/资源时序对照',evidence='F162EXdensity69.61775%, softmul59.0527%EX; F146candidate warning held',status='ANALYSIS_READY_NOT_NEW_OPTIMIZATION_GAIN',owner='A',next='use measured bottleneck; no automatic M/cache/AI'),dict(requirement='最终初赛报告/视频/代码RAR/照片/签字授权',evidence='F118 source8 unchanged; interim reports exist',status='FINAL_ARTIFACTS_NOT_ACCEPTED',owner='A prepares,user signs/submits',next='reuse credible sections; mark hardware/score gaps honestly; no upload or signature action now')]
(H/'GAP_MATRIX.json').write_text(json.dumps(gaps,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=f'''# 主线正式测量路径与流水线窗口分析（只读）

2026-10-27，F162/D163。**下一优先是让已验证的CPU短程序形成可核准位流；暂不把约11.2–14.9主机小时的双160仿真设为默认动作。** 当前已打通C→片内同步存储→CPU→Timer/UART软件闭环，仍缺CPU位流、CPU实机、真实时基/正式双种子测量和片上波形。本轮0C构建/0RTL编译/0新DUT/0ISA模型运行/0PDS/0硬件。

## 新取得的证据，而非重跑旧测试

只顺序消费F160已归档trace，逐块核原索引/压缩块/原字节和SHA，不修改归档，不调用CPU参考。实际计数**11317031条/274238774B**，与原完整流数量/哈希一致；用原ELF静态函数表和镜像字解析PC，仅作分类。{post['protected']}条输入/片段索引与块前后SHA核同，{post['host_seconds']:.3f}秒、峰{post['peak_bytes']}B。8个赛题原件SHA同F118；本轮复用已视觉核证据及固定官方commit两份规则正文，不重新渲染指南或声称重新打开官网。

计时器LOAD读数61967→16891419，差16829452物理ticks；按已设置27MHz约0.623313秒，**不是实测板上秒数**。事件c对应同沿前timer=c-1，统计区间为**61968<c<=16891420**，不得混用时钟沿前后或取指/退休PC。

|计时窗口项目|实际留存轨迹统计|
|---|---:|
|EX事件|5858143|
|WB事件|4036358|
|READ / STORE|440048 / 114704|
|两拍模式下逻辑推进槽位|8414726|
|EX事件/逻辑槽位|69.617751%|
|EX事件/物理tick|0.348089|
|未观察到EX的逻辑槽位|2556583|
|相邻EX间隔2 / 4 / 6物理tick|4496996 / 165710 / 1195436|

这些是EX发射事件密度和间隔，**不是退休IPC/整机利用率，也不能仅由缺EX把所有损失准确归因stall或flush**。4/6间隔提示后续控制流/依赖捕获重点，仍需同沿控制信号闭环。原F160整程序stall297886/flush1332226含启动和串口，不混作本表计时窗口计数。

函数`__mulsi3`占窗口EX **3459392/5858143 = 59.052707%**；状态转换537536、链表521008、matrix_mul_matrix_bitextract356256。最高热点PC0x3528/0x352c/0x3534/0x3538均在软件乘法例程，各579584次。**这不是59.1%的时间占比、异常或已实现加速**。它说明纯RV32I下软乘成本应在报告中解释；不据此擅增M扩展、改官方算法、绕过乘法或恢复F146候选。

ILA_EVIDENCE_DRAFT按原ELF给出链表、矩阵/软乘和状态转换窗口以及id_pc/id_valid/advance/stall/flush/现有timing_phase写事务选点。它只是主线技术草案，未植入/使用ILA，也没有要求队员返工。

## 软件测试通过与正式结果之间的距离

官方EEMBC固定commit1f483d5b8316753a742cbf5590caf5bd0a4e4777的本地README Run Rules明确：>=10秒、2000B、性能及验证两组种子校验、统一编译选项/类型；barebones说明强调用外部时间参考检查计时。两份本地原件路径在INPUTS。无需再次安装GCC或为跑分扩ISA。

当前port仍写死SIM ONLY/NO VALID SCORE，HAS_FLOAT=0和整数time_in_secs是允许的配置，但会截断显示；应保留原始ticks并用有理数精确分析，不能把格式变漂亮当提速。实际8迭代报告有**Errors detected**；官方core_main在不足10秒时递增total_errors，短程预冻结报告也包含该结果。正常返回/CPU有限检查通过不构成官方有效跑分，不能删该行或删短时长检查来宣称合格。

未来160若按短点线性外推，性能/验证名义时长约12.466/13.413秒；依两次已有采集速度，**仅两DUT**条件主机估计约{c['both_DUT_hours'][0]:.2f}–{c['both_DUT_hours'][1]:.2f}小时，尚不含参考/最终检查/构建。不同输入/主机负载/采集实现并未受控，非工期保证、先验oracle或速度收益；原F159约15.34小时是当时条件，不静默改成实测。

160程序/参考尚未构建或执行；现8版TB32M拍、参考25M步、checker明确要求短警告等仍不适用正式长测。生产候选上限16GiB/4GiB不是已实际验证全部最大体积。即使未来仿真足10名义秒，仍缺真实FPGA时基/运行/ILA证据。B离线ABI仍512MiB/6M行，不作为A长测必需依赖或偷偷扩其合同。

## PDS的真实差距及最小下一阶段

旧F142 PDS流只到report_timing，不含gen_bit_stream，使用1迭代ROM；新8迭代ROM与旧ROM仅**offset15904: 1→8**一字节不同，新表逐字节等于15912B镜像+零填充。这证明镜像来源可追溯，**不证明8镜像已被PDS实现**。

初版只读预检按13文件直接SHA比对被memory_model拒绝，保留`work/analysis/2026-10-27-measurement-path-m0/PREPARATION_NOTE.json`。回查原件表明PDS生产形式将INIT内联并去掉M0_VERIFY只读验证视图；12文件字节相同，memory_model按该确定性转换后非空白字符完全一致。没有改任何功能源或测试预期，也不把不同文件形态静默当“13份生产文件SHA一致”。

唯一推荐新阶段**A-BOARD-COREMARK8-BITSTREAM-M1**：新独立副本复用F16013源/8镜像和F142引脚/27MHz约束；不改CPU/软件，不新增GCC/Icarus/DUT，最多1次PDS普通CLI全流程生成.sbit。验收新ROM/RAM INIT逐块、真实器件/资源/最终内部时序、SCBV及全部警告、退出后鲜产物和SHA。沿D010只在新位流生成明确High Voltage；实际配置供电仍工程假设，过温STOP不变。

详范围`deliveries/mainline-board-coremark8-bitstream-scope-2026-10-27-v1/IMPLEMENTATION_SCOPE.md`，SHA **{scope['scope_SHA256']}**，**PENDING：本轮没有执行或批准**。PDS1800秒/阶段2400秒、单次；现有许可正常checkout失败就停，不读许可内容或改环境。先得到无调试基准位流，可用于之后短程序bringup与ILA插入开销对照；不把基准位流当最终含ILA作品。

## 关键路径与截止前检查节点

|顺序/负责人|通过标准与边界|
|---|---|
|当前A：保护F160/软件质量分析|本轮已完成新窗口统计、镜像差距和可核scope；无CPU改动或新加速结论|
|下一A：获批后CPU短程序位流|新鲜.sbit+INIT/引脚/最终时序/告警，仍未下载；独立于B资源工具|
|A/用户/平台：真实CPU短程运行|须先解除安全相关阻塞并单独授权平台/实体动作；再实际核CRC/UART/计数，不凭POWER或bitstream通过|
|A：可信正式计量与双种子|另明确port/时基/迭代与检查器范围；先校准真实时钟/Timer，再满足>=10秒及官方CRC，不少做工作或去打印换收益|
|A：ILA/定向打磨|明确捕获同沿语义/范围，抓链表矩阵状态关键算法；据瓶颈挑一项有可比收益/代价的改进，不预设M/Cache/预测器|
|A+B/用户：冻结作品材料|按既核表单匿名PDF、代码RAR、<=3分钟H264视频、照片与签字授权逐项形成。模块/仿真材料可复用，硬件和创新缺口如实保留|

按现有已核同年公告，截止仍为11/4 18:00；本轮未重新联网查新公告。建议10/27–28完成软件位流准备，10/28–30将安全可用平台/实际CPU与计量取证列首要条件，10/31–11/2冻结报告/视频，11/3核格式/匿名/入口并留上传余量。它们是检查窗口，不是工期/安全保证；若到10/29仍无可用平台证据，需要负责人决定合法远程平台的真实账号/费用/硬件权限或接受缺口，不用软件长跑替代。

旧许可10/25提示9天仅属当次记录，不推算今日余额/精确到期，下一PDS只读脱敏实际提示并提醒正规续期。7条constant-probe、14个外部IO时序/真实CDC、核心板供电和过温解释均未在本轮关闭。

B仅原D158/G1–G3资源差额，回复送达/ETA未知，原10/27 18外设窗口不改；A不重复其外设或等它整包。当前唯一人类动作是批准上述具体PDS纯软件构建范围；无需接线、登录、上电或扫描。
'''
(P/'reports/progress/2026-10-27-measurement-path-and-window-profile.md').write_text(report,encoding='utf-8')
for n in ['CURRENT.md','INDEX.md','TODO.md','COLLABORATION.md']:
 hist=M/'history/2026-10-27-measurement-path';hist.mkdir(exist_ok=True);(hist/n).write_bytes((M/n).read_bytes())
fact=f'''## F-162：旧8迭代计时窗口热点及CPU位流缺口只读核实

- 2026-10-27，`reports/progress/2026-10-27-measurement-path-and-window-profile.md`及`work/analysis/2026-10-27-measurement-path-m0-v2/`。只计数F160原11317031条/274238774B trace，{post['protected']}条输入/索引/块SHA核同，{post['host_seconds']:.3f}s/峰{post['peak_bytes']}B；0构建/新DUT/ISA模型/PDS/硬件。8题目原件同F118，复用既核规则及本地官方固定commit文档，不称重新视觉/联网复核。
- 窗口timer61967→16891419，对应61968<c<=16891420；EX5858143、逻辑槽8414726，EX/槽69.617751%、EX/物理tick0.348089，非退休IPC。间隔2/4/6计4496996/165710/1195436；不能由缺EX直接分摊全部stall/flush。__mulsi3占3459392/5858143=59.052707% EX，非时间占比或已实现加速；关键算法/PC草案保留。
- 旧PDS仅到report_timing，1迭代INIT与新8逐字节仅offset15904 1→8；新8匹配镜像，尚无新8 PDS/CPU sbit。12生产源同SHA，memory_model的验证视图去除/INIT内联后字符核同，原先13直接SHA假设预检失败留存；无源修改。
- 8实际报告仍SIM ONLY/Errors detected，名义0.623313s，不满足正式>=10秒；新双160仅条件估计DUT{c['both_DUT_hours'][0]:.2f}–{c['both_DUT_hours'][1]:.2f}小时，非oracle/新运行/工期，F159旧15.34估值保留。硬件时基/CPU/ILA与许可当前提示未新取得；B差额及over_temp STOP不变。

'''
dec=f'''## D-163：优先短程序CPU位流准备，暂缓把双160仿真作为默认主线

- 2026-10-27，F162实际窗口/原镜像/PDS流程与官方固定规则支持。A技术排序选择保护F160，先补8镜像CPU软件位流，再经安全放行/单独权限做短程真实运行、正式计时双种子及ILA；不追加CPU保留编码或未经证明的加速功能。软乘EX热点只作后续质量证据，不自动扩M/Cache/AI或优化F146。
- 已备唯一下一scope A-BOARD-COREMARK8-BITSTREAM-M1 /1.0.0，SHA {scope['scope_SHA256']}，新独立目录，13功能RTL/8镜像/FDC不改，12源同字节+memory确定性生产绑定；1次PDS正常checkout及生成位流，0GCC/Icarus/DUT，无硬件。High Voltage仅沿D010新副本软件选项，不改变供电假设或停止。**PENDING，尚待用户明确批准**，技术排序/备包不是实施许可。
- 理由：已有8仿真结果尚未成为CPU位流；约11.2–14.9h双160仿真仍不能替代FPGA时基/ILA，当前不默认花该成本。未采用删SIM警告/时间检查当正式成绩，或拿旧PDS INIT套新镜像；未来正式port/迭代/checker需要独立范围，旧M2 1+1已用完。
- B仍D158具体守卫差额，不等待/重派核心，不改变窗口/承诺；A准备报告和可用平台路径。软件位流许可也不含PDS GUI/配置许可/安装/管理员/服务器/JTAG/上电/下载/Flash，over_temp STOP保持。

'''
for n,head,entry in [('FACTS.md','# 已验证事实与约束',fact),('DECISIONS.md','# 重要决策记录',dec)]:
 p=M/n;s=p.read_text(encoding='utf-8-sig');p.write_text(s.replace(head,head+'\n\n'+entry,1),encoding='utf-8')
current='''# 当前阶段与入口

更新：2026-10-27，F162/D163（主线只读路径/窗口分析）；恢复完整读WORKING_POLICY v1.3。

- **已验主线**：F160性能8纯软件全态/逐笔/计时/663UART有限通过，F143稳定/F151校准；非正式CoreMark/FPGA。旧M2 1+1已用完。
- **当前阶段**：只读窗口分析完成；软乘占59.05% EX（非时间占比），最新8镜像尚无CPU位流。唯一下一A-BOARD-COREMARK8-BITSTREAM-M1仅已备范围，**PENDING批准**：1次PDS纯软件、无新C/仿真/功能RTL/硬件，不自动双160。
- **协作/安全**：B v02有条件接收，D158三守卫差额回复已备未代发/新ETA未知；原10/27 18外设窗保持。F146暂缓/F147告警、over_temp STOP、实际供电/时基/CPU实机/ILA缺口不变，A不等B工具。

入口：`reports/progress/2026-10-27-measurement-path-and-window-profile.md`；`work/analysis/2026-10-27-measurement-path-m0-v2/TIMED_WINDOW_PROFILE.json、IMAGE_IMPLEMENTATION_GAP.json、COST_AND_VALIDITY.json、INPUTS.json、POSTFLIGHT.json`；待批`deliveries/mainline-board-coremark8-bitstream-scope-2026-10-27-v1/IMPLEMENTATION_SCOPE.md、SCOPE_STATUS.json`。B与旧验收按INDEX/TODO/COLLAB v1.90。

Git：上单元5720e49b/33项/616路径已核；本只读分析/待批scope待按D126同步，不以提交升级授权。
'''
(M/'CURRENT.md').write_text(current,encoding='utf-8')
p=M/'INDEX.md';s=p.read_text(encoding='utf-8-sig');a=s.index('最近更新：');b=s.index('\n',a);s=s[:a]+'最近更新：2026-10-27，F162/D163：只读8迭代窗口/热点与CPU位流差距核实，下一唯一1次PDS软件位流scope PENDING；0新DUT/PDS/硬件，B差额独立。'+s[b:];i=s.index('\n',s.index('|---|---|'))+1;s=s[:i]+'|当前主线测量路径/热点/待批CPU位流|F162/D163；`../reports/progress/2026-10-27-measurement-path-and-window-profile.md`和`../work/analysis/2026-10-27-measurement-path-m0-v2/TIMED_WINDOW_PROFILE.json、IMAGE_IMPLEMENTATION_GAP.json、PRODUCTION_BINDING.json、COST_AND_VALIDITY.json、GAP_MATRIX.json、ILA_EVIDENCE_DRAFT.json、INPUTS.json、POSTFLIGHT.json`。只读旧trace，不重跑；EX密度/软乘热点非退休IPC/提速。待批`../deliveries/mainline-board-coremark8-bitstream-scope-2026-10-27-v1/IMPLEMENTATION_SCOPE.md`，1PDS/0仿真/无硬件；原13直接SHA预检失败保留于无v2目录|\n'+s[i:];p.write_text(s,encoding='utf-8')
p=M/'TODO.md';s=p.read_text(encoding='utf-8-sig').replace('# 待办事项','# 待办事项\n\n## 当前主线路径 F162/D163（2026-10-27）\n\n- [x] 旧8窗口11317031条/274238774B计数及热点、ROM1→8差距、12源+memory生产绑定核实，0新DUT/PDS；报告与证据按INDEX。\n- [ ] 批准具体`deliveries/mainline-board-coremark8-bitstream-scope-2026-10-27-v1/IMPLEMENTATION_SCOPE.md`后，仅1次PDS软件CPU位流/退出后INIT与时序/警告/SHA验收，0新C/仿真/硬件。当前PENDING。\n- [ ] 安全可用FPGA平台/正式时基/双种子>=10秒及ILA分别定范围和权限，不用约11.2–14.9h条件仿真代实机，不扩M/Cache/AI。\n- [ ] 复用既有证据形成真实匿名交付材料，按已核11/4 18:00保留上传余量；无硬件不承诺取证达标。\n\n### 以下只读路径待做项已由F162完成，新的PDS范围仍待批\n',1);p.write_text(s,encoding='utf-8')
p=M/'COLLABORATION.md';s=p.read_text(encoding='utf-8-sig');i=s.index('版本：COLLAB');s=s[:i]+'''版本：COLLAB v1.90；2026-10-27，F162/D163。A完成8程序只读效率/正式测量路径，下一CPU位流1次PDS仅已备PENDING；不改CPU/外设或自动长跑。A拥有计量/构建/片上取证，B只D158 G1–G3局部差额，回复已备未代发/新ETA未知，不重复外设核心/不要求B改ABI或等其整包；原10/27 18外设窗不变。硬件STOP与F146暂缓/F147告警保持。

### 历史v1.89（A只读阶段现完成，B结论/范围保持）

'''+s[i:];p.write_text(s,encoding='utf-8')
for n in ['CURRENT.md','INDEX.md','FACTS.md','DECISIONS.md','TODO.md','COLLABORATION.md']:
 t=(M/n).read_text(encoding='utf-8-sig');assert 'F162' in t or 'F-162' in t
print('Read-only profile/path report and six memories written/reread; next PDS scope remains pending')
