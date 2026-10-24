# A-SOC-TXGPIO-M1：真实C与队员包装的有限软件系统验收

日期：2026-10-24；授权D120；事实F134。独立目录：`D:\A_FPGA_Comp\work\system\2026-10-24-soc-txgpio-m1\integration-0030-v1`。无Git。整包审收另见`D:\A_FPGA_Comp\reports\progress\2026-10-24-increment-0030-mainline-alignment.md`（F133/D121）。

## 1. 实际打通的流程

F132原C镜像 → F130两拍CPU → F131完整32K ROM/32K RAM官方primitive功能模型 → A侧MMIO路由 → 收到的B包装1.0.0及原TX/GPIO → 三笔真实GPIO写、输入/输出读回、12个真实串行帧 → main返回0 → EBREAK停止。N16、N234均通过独立全状态/有序事件/逐物理钟外设模型检查。不是替身包装、预置结果或仅打印TB的PASS。

CPU、ALU、control、regfile、B包装/TX/GPIO均未改；新目录只忠实复制已审源，增加实际GPIO接受观察宏绑定，源位置与SHA见`source-receipts.json`。3358冻结项、原F132准备及收到材料保护记录核同。历史F132的完整系统NOT_RUN仅被本次新运行取代，不改写旧证据。

## 2. 工具、输入与执行

现有Icarus/vvp13.0，绝对路径`D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\`，显式-B及VPI路径，不改PATH。完整argv/cwd/超时/原生rc见本目录`COMMANDS.md`、`compile-plan.json`、`result.json`。额外4个固定非管理员外部仅编译目标已分别经工具审批，许可已用完，不扩为以后任意执行。

|新目标|编译耗时s|普通运行耗时s|实际结果|
|---|---:|---:|---|
|wrapper-N16|0.078|0.046|原TB W01–W10十个标记齐，有限正向通过|
|wrapper-N234|0.094|0.079|原TB W05/W06/W09三个标记齐，有限正向通过|
|system-N16|50.094|0.969|独立系统检查PASS|
|system-N234|44.485|2.359|独立系统检查PASS|

各编译60s/首错停；各运行30s，系统+MAX_CYCLES=100000；0超时/0截断，各native rc0。包装TB编译stderr空；两个系统编译各保留CPU四模块继承gpio_core timescale警告，以及Pango原模型GTP_DRM18K_E1.v:933隐式grsn警告，无编译错误。未为消警告修改冻结源/官方模型。

C632B、RV32I/ILP32，原启动/链接与初始化文件不变。ELF SHA `8C31C7C5AD48D37E99B9C4A669B8A2B20604AEA60A0453A215A87C2250DA8ED0`；BIN SHA `90E6FBB6837309313723E3851BD7B58A410E1692A5FEFB84171ABF1CFD2023B6`。手工预期沿F132冻结，未按DUT回填。

## 3. 判定证据

|项目|N16|N234|
|---|---:|---:|
|物理周期 / 流水推进|4179 / 2089|28779 / 14389|
|stall / flush|303 / 319|2353 / 2369|
|合法WB / 内存事件 / EX-PC事件|724 / 385 / 1129|4824 / 2435 / 7279|
|GPIO实际核心接受|3|3|
|UART完整公开串行帧|12|12|
|独立MMIO读值核对|300|2350|

GPIO接受均为物理沿411:5a、421:5a、429:a5；相同5a仍保留两笔实际核心输入使能，不靠输出变化计数。UART实解码`PG100 M1\r\nAA`，两个A独立保留。手工结果数组`13579bdf,0,126,5a,5a,a5,3c,c3,12,a5,0,0`，签名534f4331、a0=0、恢复sp=18000、stopkind2/PC68均匹配。

核完整寄存器/32K RAM终态、每笔合法WB与MEM各自顺序（不去重）、独立串行解码、逐钟沿前ready/错误与GPIO核心真实使能，ROM/RAM/IO互斥与一次STORE一次请求。保持相位无额外GPIO写或TX启动；未知/错误/重复/漏事件不靠最终结果掩盖。依据独立参考执行核stall/flush及EX路径，物理周期=2×推进+1，推进=EX+2×flush+stall+19（含32物理拍尾部观察）均一致。EX-PC不是退休PC。

在新真实正向日志的独立派生副本上，检查器正确控制1项通过，重复WB/漏STORE/错WB/错UART引脚/额外GPIO接受/错MMIO读/未知引脚7项均拒绝；原始输入日志SHA未变化。`checker-negative-result.json`记录这些是检查器控制，**0额外DUT运行**，不冒充7个新增CPU测试。

## 4. 即时质量分析：已识别什么，不能推断什么

`quality-metrics.json`记录N16 UART起始间隔176拍，核心最早161拍；N234间隔2348拍，最早2341拍。N234十二帧线活动28080物理拍，整段28779拍，当前演示主要等待串行输出；N16还刻意等待E4096输入改变，不能拿其整段时长当计算基准。轮询读数N16 GPIO_IN127/TX_STATUS169；N234分别4/2342，输出读均4。

这是确定下一测量对象的证据，不是CoreMark成绩、退休CPI或创新收益。不能通过少输出、删等待、主机仿真更快来声称CPU计算提速。两拍存储约2倍物理时钟成本仍在；后续应先取得计算区独立可信计时与同条件CoreMark基线，再依据瓶颈选择局部优化，不预设FIFO/Cache/预测器。

## 5. 验收边界及下一步

有限软件系统流程可接收，包装可作为该基线使用；B整包仍有条件接收，其runner/账本问题见F133集中回复。包装原TB正向新运行不关闭其缺标记误PASS、刺激计数和W10负测缺口；A自有系统检查器不冒充B W10完成。RX本轮无新DUT运行。

保留无真实退休PC/统一WB-STORE提交顺序、固定内存和初态/输入、有限12字节程序等局限；不是全ISA/所有MMIO竞态/完整C运行库证明。Pango功能模型不等目标实际映射、资源、Fmax或上板。无正式CoreMark计时、FPGA/ILA证据。

当前D120有限软件子阶段完成，继续保留基线、与B局部整改并行；下一有价值范围是可信计时与CoreMark计算/输出分离，但Timer/新实施不在D120，须另列清范围获批后开始。没有自动扩大CPU、RX包装或硬件。over_temp STOP不变。

证据入口：`summary.json、result.json、source-receipts.json、frozen.json、compile-diagnostics.json、checker-negative-result.json、quality-metrics.json、COMMANDS.md、SHA256SUMS.txt`；`runs\system-N16`与`runs\system-N234`含新VCD、trace/bus/终态/检查结果，`logs`保留真实进程stdout/stderr。
