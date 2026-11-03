# A-MEM-ADAPT-M1：固定一拍同步存储的软件适配复验

日期：2026-10-24；工作目录按阶段启动日期保留为`2026-10-23-memory-adapt-m1`。F130 / D118。Git：项目无`.git`，没有commit。

## 1. 大白话结论与验收边界

原CPU直接接注册读存储会读错拍；本轮在**新CPU副本**增加默认关闭的两拍模式：先给存储一拍取数据，再让流水线推进一拍。真实C启动、相同CoreMark镜像均能在这个一拍延迟模型下得到原来的状态和逐笔轨迹，没有靠NOP或更改结果绕过。

**有限纯软件验收通过，不是FPGA存储映射或作品验收。**默认模式763例、新小程序12次、C与CoreMark6次，共781次新DUT运行PASS，0FAIL/0TIMEOUT；七份完整新VCD独立41320项核验PASS。不能把这个数字当项目完成率。

代价明确：同样工作约用两倍物理时钟，**不是效率提升**，也未永久选定最终架构。CoreMark仍只有每参数1迭代的CRC正确性基线，`get_time=0`，保留原“至少10秒”/`Errors detected`提示，无正式分数。over_temp停止条件不变。

## 2. 授权、源码与保护

承接F129/D117报告§8单独提出的A-MEM-ADAPT-M1，用户随后明确“继续”，批准该阶段。与D115仅M0/队员包装分开；不是追认D115含CPU修改、完整SoC、安装或硬件权限。本轮另通过工具权限审批取得**一个最多16目标的非管理员沙箱外仅编译批次**，每目标60秒、首错停，已用完；781次仿真均普通权限。

工作根目录：`D:\A_FPGA_Comp\work\system\2026-10-23-memory-adapt-m1`。

|文件|F108/source-before SHA-256|新source SHA-256|
|---|---|---|
|cpu.v|555CB51AC20FFC439B61BB29D4F4D9F4DC02C38B54A37291A79519CD413B8114|7179EF273E62389280A23F962B696E3B8E09F3985CC72D76E5E80C7A0C59518D|
|alu.v|6393472BC3635DA83213E0E9883766D5076C37EA60319F32F1DE5C420F68065E|相同|
|control.v|23CDBDFDD45DD60D6C7D95A13CC51927999A640FE5E30CAF8D324FA91AA87067|相同|
|regfile.v|AE36F070B994EEF41AF1636516D737EDA240C2A18AF83048ADC3E3E2391C8468|相同|

原整组源位于`D:\A_FPGA_Comp\work\icarus\2026-10-21-cpu-shifti-reject\source`，没有覆盖。3155项事前冻结保护与结束后复核一致：原源码/旧TB、763例四份输入及预期、实际C/CoreMark镜像和原预期、相关旧模型/结果、工具与新验证源等，详`frozen.json`。源码比较准确diff为`cpu.diff`。队员包/外设及公共旧证据不改。

新增验证材料包括`PLAN.md`、`source-before/`、`source/`、`memory_model.sv`、`tb_mem_adapt.sv`、有界runner、只读新波形审计器、结果聚合器。runner在首次准备前曾有多一个右括号的Python语法错误，已在首次编译/DUT运行与输入冻结前纠正，不是CPU错误或DUT失败。

## 3. 唯一功能改动及技术依据

仅`source/cpu.v`：

- 参数`SYNC_MEMORY=0`保持旧组合读合同；`1`启用保守两拍模式，不增端口/ISA。
- 所有PC、IF/ID、ID/EX、EX/MEM、MEM/WB、valid、EEI状态使用同一上升沿使能。phase0存储采样、流水保持；phase1消耗响应、流水推进。不造新时钟/不改RF边沿。
- RF实际we只在推进沿；STORE实际mem_wren只在存储采样沿；非写沿wstrb=0。重复的两条相同SW仍是两次合法事件，不去重。
- ALU/control/regfile和原立即数/前推/load-use/分支/EEI语义不改。

官方资源规则沿用已视觉核验F125/F129：UG041002 v1.10实际37/41/44页、DS04001 v1.5实际10页；旧`GTP_DRM18K_E1`16bit×1024小模型13检查保留，不重跑。本轮用明确注册读模型实现一拍接口，**没有直接用厂商primitive承载完整CPU存储**。

## 4. 实测结果

### 4.1 默认兼容回归

14个原TB分别编译，763例全部使用本轮新CPU、新VVP和新运行目录；全RF/测试内存、有序WB/STORE、适用的LOAD/bus strobe/RAM/EEI停止事件均检查。

- 763 PASS，0FAIL/0TIMEOUT；各例结果见`RESULT_MATRIX.md`和`regression-result.json`。
- 独立冻结stall期望746项、flush期望743项均PASS。
- 旧17项stall和20项flush **NOT_SPECIFIED原样保留**；另与旧实测共1526项计数比对一致，见`history-counts.json`。历史一致不等新增独立期望。
- 这是**默认模式763例**，不是同步模式763例；没有改旧TB来凑新模式。

### 4.2 存储定向程序（每个两模式，各6次）

|原冻结输入|覆盖目的|默认物理沿|同步物理沿|逻辑stall/flush，两模式相同|结果|
|---|---|---:|---:|---|---|
|P01|ROM常量load→ALU|11|23|1/0|两模式PASS|
|P02|重复SW、紧邻load、SB/SH保留其他lane|18|37|1/0|两模式PASS|
|P03T|load→taken BEQ、错路取消|13|27|1/1|两模式PASS|
|P03N|load→not-taken BEQ、合法STORE|13|27|1/0|两模式PASS|
|P04|错路STORE及WB冲刷、目标只一次|13|27|0/1|两模式PASS|
|P05|EBREAK前旧load排空、停止后无写|9|19|0/0|两模式PASS|

32RF/256字节RAM、原逐笔WB/STORE/LOAD、停止kind/PC与期望计数保持。P02两个相同SW均保留；同步STORE只在phase0，RF写只在phase1。新TB逐有效物理沿检查关键X/Z、暂停全部流水状态、取指PC/指令配对和停止后副作用。

### 4.3 原真实C与固定CoreMark镜像，不重新编译软件

|输入|模式|物理沿|流水推进沿|存储保持沿|逻辑stall/flush|墙时秒|结果|
|---|---|---:|---:|---:|---|---:|---|
|C启动|0|642|642|0|2/97|0.391|PASS|
|C启动|1|1285|642|643|2/97|0.391|PASS|
|CoreMark performance|0|1101315|1101315|0|22483/155217|21.437|PASS|
|CoreMark performance|1|2202631|1101315|1101316|22483/155217|29.281|PASS|
|CoreMark validation|0|1180725|1180725|0|23001/168293|22.391|PASS|
|CoreMark validation|1|2361451|1180725|1180726|23001/168293|31.171|PASS|

这些整段计数含启动/排空/验证尾窗，不是内核计时或退休CPI；墙时是主机仿真耗时，不是FPGA性能。TB显式1ns/1ps、10ns周期只是验证时钟，未声称硬件100MHz或正式27MHz测量。同步物理沿=`2×推进沿+1`，含起始采样/尾窗；两种模式使用4/8物理尾拍，保持相同逻辑尾窗。raw stall/flush高电平采样在同步模式为逻辑次数两倍，已单列，没有隐藏等待。

C逐笔263 WB、13 READ、16 STORE、439 EX-PC与旧冻结预期一致，全32RF/16K RAM一致。CoreMark performance逐笔526027 WB、59090 READ、19201 STORE、768391 EX；validation逐笔560029 WB、59554 READ、19106 STORE、821131 EX。所有事件逐笔流式摘要与原冻结摘要一致，READ/STORE共用有序MEM流，不去重；全32RF/32K RAM一致。

performance的seedcrc/list/matrix/state分别e9f5/e714/1fd7/8e3a；validation分别18f2/e3c1/0747/8d84。原输出buffer溢出/错误状态、迭代/容量和停止检查按原模型执行；**运行不足10秒的原上游错误提示仍在，不能称官方CoreMark通过或有成绩**。两种模式RAM输出见各`ram-output.txt`。

### 4.4 新波形独立核验

`audit_waves.py`只读六份完整同步小例及同步C的新VCD；每个timestamp区分沿前数据与沿后NBA，不能混用：

- 共41320检查PASS，核phase交替、完整暂停状态保持、一拍ROM/DATA响应、同址读前写语义、IFID-PC配对、RF/STORE沿资格、空闲wstrb。
- 独立从VCD生成每笔EX/WB/READ/STORE，按总日志顺序逐笔比对，不去重；独立逐lane重放RAM并核最终字节。
- 新CoreMark VCD只保留首4096物理拍及停止尾窗；中间不是完整波形。全程由TB不变量、完整逐笔流/全状态检查覆盖，**不把七份完整VCD审计说成四份CoreMark全程逐沿VCD审计**。

详细检查/真实沿前沿后样本：`wave-audit.json`。旧M0反例/旧函数滞后模型与原14FAIL均保留；新模式通过不改写旧源同步不兼容结论。

## 5. 工具、命令、警告与产物

既有Icarus/vvp13.0，绝对路径：
`D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe`、同目录`vvp.exe`；不重装/改PATH。本轮未重复版本查询，工具身份在保护SHA内。

- 16次编译全部rc0，总编译墙时2.048秒，0错误；每目标60秒限、首错停。警告保留于`compile-diagnostics.json`和每次stderr：CPU四模块无显式timeunit/precision、泛用模型数组8192项敏感表警告，未改原RTL消警。
- 小例/回归每进程30秒，C30秒/100000物理沿，CoreMark180秒/按原推进数两倍加128上限；0超时，全部以EBREAK停止后尾窗正常结束。不是仅凭rc0/$finish/VCD存在判PASS。
- `compile-plan.json`固定16条完整argv；`COMMANDS.md`保存全部797条实际编译/运行命令、cwd、限时。每次真实原生rc、耗时、stdout/stderr见`logs/<job>/process.json`及原日志。
- `runs/<id>-sync0或1/`保存新VCD、trace、全RF/RAM、result；763例在`runs/regression/<id>/`。新编译产物在`compile/`，VVP各自SHA见`compile-result.json`。
- `summary.json`为阶段权威汇总；`small-result.json`、`regression-result.json`、`programs-result.json`分层证据；`SHA256SUMS.txt`覆盖本阶段新产物，`frozen.json`保护旧输入/期望/工具等3155项。

复现应在**唯一新目录**复制/审核脚本并重新冻结路径，不在本目录重复prepare/compile/run覆盖产物；runner对已存在结果拒绝覆盖。新沙箱外权限仍另申请，本批用完不变成常设许可。

## 6. 当前成果与下一范围（建议，未批准）

已打通：真实程序镜像→固定一拍同步行为存储→CPU正常执行/唯一副作用→原全状态与有序流检查。这消除了M0沿前/沿后错拍这一明确风险，但仍未打通C→UART/GPIO，未完成实际DRM存储、FPGA/ILA或可信计时。

保留局限：无真实退休PC；WB/STORE分流而非统一退休顺序（泛用READ/STORE另有顺序）；固定内存/复位初态；同步模式仅有限新程序；无多等待/ready/error；完整32K ROM共享取指/常量读、32K RAM的官方primitive布局/初始化/碰撞尚未验，资源/Fmax未知。不得用本轮结果解除over_temp或宣称最终质量。

**唯一下一实施建议A-MEM-MAP-M2，尚未授权**：新独立目录用现有官方`GTP_DRM18K_E1`模型建立完整32K ROM/32K字节写RAM适配，复用本次CPU整组与镜像，不改CPU/ISA/B合同；核ROM取指与数据常量双读端口/必要复制、地址分bank与初始化、byte lane及避免未定义碰撞，先小模型自检再原六程序/C/有限双CRC。实际端口/碰撞若必须扩CPU或改接口，保留证据停止。仅普通命令行模型仿真，**不启动PDS或生成新位流**；任何新沙箱外编译另固定目标/限次申请。

推荐先做M2是因为本轮只解决CPU采样时序，尚不能把行为数组当目标资源；先关闭容量/端口/初始化风险再以此接系统，减少大返工。B原包装已批准，继续与A解耦；不重派核心、不重复索包，既有最小整改与10/27 18返回窗口不变，送达/开工仍按真实回执。A完整TX/GPIO系统、正式计时/优化、PDS和硬件各自范围门槛保持。
