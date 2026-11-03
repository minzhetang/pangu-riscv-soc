# 固定CoreMark256：真实片上流水线效率与证据报告

日期：2026-11-01。范围：D288/D289固定性能程序的观察与解释，未优化CPU或基准算法。

## 本轮结果

取得链表、矩阵、状态机、另一处矩阵调用共4个不同的真实FPGA窗口；每个140通道、1024点，原始WDF/工程、逐点CSV、分析JSON、从WDF重建的VCD及波形图已保存。不是RTL仿真，也不是旧WDF重放。

新调试镜像一次完整原厂CRAM SVF配置后自动输出、两次新KEY0运行共3份1123B物理UART报告，均逐字节匹配冻结性能报告，5个CRC及538539600个目标周期相同。27MHz标称计时为19.945911111秒；没有把宿主等待时间当目标时间。无独立校频或EEMBC认证，本报告不签发正式认证成绩。

实际完成5次dbg_run：连采4次中的第一个链表数据未被保留，后用独立单次补齐；最终只有4个不同、经严格关联核定的窗口。另有原0x310选点等待取消，未当成功数据。所有工具/串口所属Job正常原生0退出、Job空、无强清；实际电源断开未获新确认，不写成已断电。

## 固定版本与来源

- 工程目标PG2L100H-6IFBG676/盘古100Pro+；扫描能证明系列PG2L100H及公开ID，不证明完整速度等级/封装。
- PDS2022.2-SP6.4 build146967；本次实际许可提示剩余2天，需通过合法渠道及时续期，不推断确切失效时刻。
- ELF SHA FA9822A21D61AE72E807541CFB9676EE308D3F247EF7180F84E74151AD7B0D1C；bin SHA0160BF311C70A8CCDDDF1B4F19B96C4F5B7357CB2E4BD04E69DB9A87DBC8C21E，16352B。
- 新调试sbit SHA51A361EFAB8DD43A13464820063A127B9E80B953B212452FC8C511118E7A0222；完整原厂SVF SHA2B25399F6A8CFF190262C6A042E1EAF6311D6F79401E23043B1AF5FB4441FFFB。
- 独立副本仅3个RTL文件7处PAP_MARK_DEBUG注释；功能文本、固定软件/算法不改。1792功能INIT与非调试基线逐片相同，15引脚/94约束同；14个source-before及source文件各与其冻结回执匹配，22项保护原件后验SHA不变。
- 构建FIC F03A9F4D…18163首行曾放派生注释，Debugger拒绝。运行FIC F932FE45950D7B3CF1513404DF4794970490E76070C85270E750977934CC4B06仅把magic恢复首行，所有键值/140探针顺序完全同；未借此重构或重新下载。原失败保留。
- 证据主入口：[RESULTS.json](../../work/fpga/2026-11-01-coremark256-ila-efficiency-m1/RESULTS.json)、[BUILD_AUDIT](../../work/fpga/2026-11-01-coremark256-ila-efficiency-m1/BUILD_AUDIT.json)、[原有限重载基线](../../work/hardware-baselines/2026-11-01-coremark256-full-svf-v1/BASELINE.json)。

## 观察方法与口径

`soc/cpu_core/id_pc`虽名为id_pc，实际位于ID/EX寄存器，配合id_valid表示EX候选；不是取指PC，也不是退休PC。有效EX事件限定为sys_rst_n=1、eei_hold=0、pipeline_advance=1、id_valid=1；不得将两拍保持的同一PC计两次。

CPU `source/cpu.v`第25–31行的SYNC_MEMORY两相适配每两个物理周期推进一次。实采中advance逐点交替、timer_ticks逐点+1；这是结构性存储节奏，不是每隔一拍都发生RAW停顿。逻辑槽位=advance为1的采样点；槽位有效率=有效EX事件/逻辑槽位；物理事件密度=有效EX事件/计时ROI内物理采样点。两者都不是退休IPC。

冻结计时ROI为低32位start=0x0000f20f、end=0x201a685f，规则start<sample_ticks<=end；该运行未跨低32位回绕。链表入口很早，窗口前449点在计时外，故仅575个物理采样/287槽参与效率统计；不把初始化或计时前数据混入算法效率。

每次触发均要求PC、valid、advance、hold、reset全条件匹配，原始采样索引512须命中，未移动索引迁就结果。PC通过固定bin反汇编/ELF函数区间对应；每个有效PC须对齐且在固定镜像范围。stall须对应非x0目的load及真实消费者编码，并验证下一槽valid=0、再下一槽valid=1；flush须对应合法分支/JAL/JALR，验证两空槽后有效目标，直接B/JAL目标还须等于冻结机器码算得目标。分支仅核taken标志和控制流一致性，未采集操作数的比较真值不独立证明；JALR完整操作数/目标计算未重建。

## 实测结果

|窗口|ROI物理点/总点|逻辑槽|有效EX事件|槽位有效率|物理事件密度|无效槽|load-use|控制冲刷|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|list|575/1024|287|210|73.171%|0.36522|77|6|35|
|matrix|1024/1024|512|418|81.641%|0.40820|94|0|47|
|state|1024/1024|512|420|82.031%|0.41016|92|8|42|
|matrix_repeat|1024/1024|512|422|82.422%|0.41211|90|0|45|

14个load-use与169个控制冲刷均完整观察到后继关系。矩阵94个无效槽=47×2，状态92=8+42×2，矩阵重复90=45×2；链表77个无效槽中6+35×2=76，其余1槽为ROI首个逻辑槽sample450，未强行归因。[逐槽集合核对](../../work/fpga/2026-11-01-coremark256-ila-efficiency-m1/BUBBLE_ACCOUNTING.json)确认气泡无重复计入。非推进物理拍另计，未重复算为气泡损失。

这些窗口是围绕函数入口的局部样本，包含调用者/CRC/软件乘法，不等于整段函数运行，更不是全程随机采样。矩阵另一次调用422/512与前一次418/512并不要求相同：观察到冲刷45/47、软件乘法EX事件131/127的组成差异，但未采集的操作数原因不做确定推断，不将差异包装成提速或硬件不稳定。

函数归属：链表210有效EX中186属于core_bench_list，其余24属于start_time/main/iterate；矩阵418中57为matrix_mul_matrix_bitextract、127为__mulsi3、139为crc16、95为matrix_test；状态420中169为core_state_transition、103为core_bench_state、100为crcu16、43为calc_func、5为cmp_complex。状态8个load-use有7个在core_state_transition、1个在calc_func；不能把窗口全部计数声称为目标函数本体耗时。

### 可定位的真实例子

- 链表sample548，PC0x578，机器码00c0006f（JAL）跳到0x584；550/552两个逻辑槽valid=0，554目标首次有效。sample554的load写x14，556一空槽，558的0x588真实读x14，符合单槽load-use停顿；不由此宣称已观察到前推数据值。
- 状态sample516，PC0x1ee8，load写x15；518空槽，520的0x1eec消费x15。详见逐笔事件，证明真实关键算法附近的停顿关系。
- 矩阵sample6，PC0x1b6c，机器码fce95ae3，taken分支目标0x1b40；8/10空槽，12目标有效。它属于窗口内调用者matrix_test，而非把所有控制流算进bitextract本体。

### 从真实采样绘制的图

图只显示代表性64点片段；统计使用完整1024点并按ROI限定。原始WDF无改写；CSV/JSON保留每点；普通VCD由真实WDF重建，1ps时间刻度仅按标称27MHz显示，不是原生VCD导出或仿真波形。

![链表原始采样局部](../../work/fpga/2026-11-01-coremark256-ila-efficiency-m1/qualified-windows/list/list-waveform.png)

![状态机原始采样局部](../../work/fpga/2026-11-01-coremark256-ila-efficiency-m1/qualified-windows/state/state-waveform.png)

另有matrix/matrix_repeat同名PNG及完整数据，见qualified-windows目录。4张PNG已逐张视觉检查。

## 性能解释与代价

首先可确认的是两相存储适配的推进上限：在本版SYNC_MEMORY=1下，无气泡时也最多每两个物理周期推进一次。在局部逻辑槽中，控制冲刷贡献大于已观察的load-use；不能据此算出整个CoreMark可提速百分比。矩阵窗口有明显软件乘法/CRC辅助路径，说明只盯矩阵函数入口本身会漏掉工作，但该偏置窗口不足以证明全程第一热点。

本轮不是优化；同一固定性能程序非调试/调试都为538539600ticks，未取得计算加速。若后续改进须先说明全程权重、兼容同步存储与正确性的方式，再冻结同条件候选/回归，不能据局部比例直接砍时序或自动扩M/Cache/预测器。

|实现|最终LUT|FF|DRM36等效|IO|最小主时钟setup/hold ns|
|---|---:|---:|---:|---:|---|
|固定性能非调试|1805|1519|14|15|23.279 / 0.129|
|本版140×1024观察|2931|3838|18|15|24.876 / 0.113|
|观察开销|+1126|+2319|+4|0|非运行频率提升|

非调试审计28 DRM18换算14 DRM36；原生mapped表14/18对应上述归一口径。最终LUT/FF取布局布线分区和，非mapping前1813/2942。主27MHz内部8类时序0failing不等于全设计时序/CDC/IO关闭：仍有Place-2028一条、Route-2036三条调试时钟Critical、7条constant-probe等告警。不得因有真实波形撤销这些限制，所有140路布线未逐根独立证明。

## 采样留存修复与原始失败

原0x310 core_list_find符号无静态调用引用且原等待未触发；0x530 core_bench_list有明确编译调用。WINDOW_PLAN_V2在本批数据前修改入口，保留旧计划/取消记录，不证明所有可能间接调用不存在。

连续4次native保存产生名实错位：原list_revised.dprj/WDF实际是矩阵谓词/矩阵数据，matrix_revised实际为状态机，state_revised与matrix_repeat_revised为同一最后数据。先前严格分析3项拒绝保留；未改动原数据或放宽512检查。按保存dprj的确切140bit谓词与WDF512点共同核定三份，复制到qualified-windows并保存关联表；重复数据只算一次。缺失链表另开会话单采一次、无下一次dbg_run，复制后正常退出。内部更新时机仅为机制推断，不把确定根因扩大到未查工具实现。

原首行FIC导入失败、旧0x310等待取消/工具error态、早期UART300秒无数据窗口、宿主readback正则使用等号而原生使用冒号的断言失败均保留；它们分别是格式/选点/接收窗口/宿主检查问题，不是CPU失败，也未当新有效采样或按键。实际新配置仅H53完整SVF一次；采集会话均0Program，保护/Flash/SCBV无改动。

## 证据与边界

|窗口|原始WDF SHA-256|
|---|---|
|list|`B2540C779588038E2BE627BA09D3DC3A926E6A8E178E206C5E737CDA8BB9273E`|
|matrix|`7832DA2D24665F27868673637E14751DDE01EFA9C1CCC7217C06BF0D499255F3`|
|state|`07B8A52B66F49D534B1D725048EEEDB1511D9CDC99C9BB0F05B146584BD4F104`|
|matrix_repeat|`9503899CFC624D6C9CC769BC20301CD86B2844EB1B271FDB97AA6F834DB06733`|

- [完整命令及会话索引](../../work/fpga/2026-11-01-coremark256-ila-efficiency-m1/COMMANDS.md)；[冻结窗口计划](../../work/fpga/2026-11-01-coremark256-ila-efficiency-m1/WINDOW_PLAN_V2.json)；[留存差额说明](../../work/fpga/2026-11-01-coremark256-ila-efficiency-m1/CAPTURE_RETENTION_ADDENDUM.json)。
- 物理UART H53/H55-r2/H59各1123B，全文SHA73425EECBAB76C9DDE20D58A7F1E85014F346B3242C995C9B6F64B1DCDC0679E，CRC e9f5/e714/1fd7/8e3a/b40f。H55-r2关联矩阵/状态/重复，H59关联新链表；H53为同新调试镜像自动启动正控制。
- MEASUREMENT_CHECK中内层underlying_host_parser.hardware_valid=false是原宿主解析器元数据；本轮实机判断依据外层physical_uart_capture_complete、全文核对、版本身份和真实接收/退出证据，不改内层字段伪造验收。
- 每点wren/地址/数据按原顺序保留，不去重；它是观察端口，不含可重建全架构提交的WB/STORE统一轨迹，也不把同拍EX PC当该STORE的来源。全寄存器与所有访存的实机参考模型逐笔一致性本轮未取得。
- 无真实退休PC/全程IPC/完整前推数据与JALR目标；窗口边界与确定性函数触发偏置限制全程推论。采样格式二值不证明物理无亚稳态或CDC正确。
- 未校准实际时钟，未量温度/电压或闭环SCBV接线。bit27照录、不独立停止依D237，不改芯片保护，也不认定它是假过温。旧原生Program身份异常的唯一根因仍未知；完整SVF路径只在固定版本范围已见证。
- 本轮工具已退出，无新硬件操作。D245待审文档保持本地，未Commit/Push。阶段目标完成；下一建议将本轮实测、双种子长测与固定恢复配方整合进比赛技术报告/演示材料，优化另定可验范围，不自动实施。
