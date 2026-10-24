# FPGA逻辑实现预检M0：有限通过，尚不是板级可下载工程

日期：2026-10-24（北京时间）；授权D129，验收边界D130/F141。

本轮已将F136软件系统推进到**指定FPGA的真实综合、映射、布局布线和内部27MHz时序报告**。CPU和B的功能RTL未改，没有生成位流，没有硬件操作。外部IO/复位时序、板级引脚和实际运行未验收，不能以工具“All Constraints Met”概括为整板时序全部通过。

## 1. 基线、授权和变更

- 原基线：`D:\A_FPGA_Comp\work\system\2026-10-24-timed-coremark-m1`，F136；Git开始锚点`d3a2c088c5a2297ba36b4d77d58da4b631902697`。
- 新独立目录：`D:\A_FPGA_Comp\work\fpga\2026-10-24-implementability-m0`，以下称H；未覆盖历史。
- 原范围：`D:\A_FPGA_Comp\deliveries\mainline-fpga-implementability-scope-2026-10-24-v1\IMPLEMENTATION_SCOPE.md` v1.0.0，SHA `40A1B5B1E77C5F0EB035EE920543387D4FD5C91863B080CC89D9F6287204212E`。用户“同意”批准该完整范围，原PENDING文档留存，当前批准在H/APPROVAL.json及D129。
- 只修改新`source/memory_model.sv`的生产/验证组织：三个只读观察/协议诊断块提取至`verification/*.svh`，以`M0_VERIFY`显式启用。原primitive参数、端口、初始化函数、bank/region延迟、CPU两拍模式、32K ROM/32K RAM及字节写保持。
- 验证宏展开后，与原绑定忽略空白的完整token序列一致；不是只比较几个关键字。新PDS生产副本去除这些验证段，仅展平自有init_tables，未加入Pango仿真模型作为设计源。准确diff：H/SOURCE_DIFF.patch；依据H/equivalence.json。
- 其他10个源、原TB、参考模型、原输入不改；source-before保留。349项冻结输入/既有产物/工具文件结束SHA核同。H/postflight.json和frozen.json为原始证据；不是以文件存在代替验收。

核心源SHA-256：

|文件|SHA-256|
|---|---|
|cpu.v|7179EF273E62389280A23F962B696E3B8E09F3985CC72D76E5E80C7A0C59518D|
|alu.v|6393472BC3635DA83213E0E9883766D5076C37EA60319F32F1DE5C420F68065E|
|control.v|23CDBDFDD45DD60D6C7D95A13CC51927999A640FE5E30CAF8D324FA91AA87067|
|regfile.v|AE36F070B994EEF41AF1636516D737EDA240C2A18AF83048ADC3E3E2391C8468|
|新memory_model.sv|F673773641F1D4BA573EFB0EA4F5BF81CDB8D570CECA2E598C116AD2EB133D27|

## 2. 实际软件复验

现有Icarus/vvp13.0，绝对路径、`-B`与VPI路径，未改PATH。4个固定目标编译/展开实际成功，各120秒上限；已批准的非管理员外部编译批仅此4次，现已用完。编译警告：3个系统目标继承regfile时间单位、alu/control/cpu未显式时间单位；四目标均有官方模型内隐式grsn警告。未修改旧RTL/TB来消除警告；TB明确1ns/1ps，VCD时间刻度1ps，物理计数不是将历史无单位延迟猜为ns。

每个新vvp独立运行、45秒进程上限；系统100000周期上限，普通VCD。7次实际运行，没有重跑763 ISA矩阵或长CoreMark。

|目标|实际结果|物理周期/推进/stall/flush|合法事件EX/WB/READ/STORE|UART帧|主机秒|
|---|---|---|---|---|---|
|baseline-N16|PASS|4179/2089/303/319|1129/724/334/51|12|1.031|
|baseline-N234|PASS|28779/14389/2353/2369|7279/4824/2384/51|12|2.343|
|smoke-N16计时C|PASS|1979/989/94/132|612/373/124/68|6|0.906|
|全容量selftest-0|PASS|49416检查，122真实写沿|双ROM端口/完整RAM初态、8bank×16mask、重复写/复位保持/边界|不适用|1.719|
|selftest-1写ROM|预期拒绝|MEMORY_PROTOCOL，rc1|非法访问被拒绝|不适用|0.719|
|selftest-2有效写但mask0|预期拒绝|MEMORY_PROTOCOL，rc1|非法访问被拒绝|不适用|0.703|
|selftest-3空闲非零strobe|预期拒绝|MEMORY_PROTOCOL，rc1|非法访问被拒绝|不适用|0.719|

三个C系统检查：全RF及32K RAM、逐笔有序EX/WB/READ/STORE，不去重；公开UART/GPIO、可信计数预值、停顿/冲刷及正常停止。它们的check-result与F136完全相同，trace.log、bus.log、registers.hex、ram.hex四文件均逐字节同SHA。不是仅看最终答案或$finish。

新7个VCD均逐行检查完整定义、单调时间戳及非空事件，记录末时间与SHA；没有宣称所有内部信号在整个运行中无X/Z。关键数据/事件由原严格checker检查，未重新做全范围时序仿真或形式等价。H/simulation-audit.json保留范围。

本轮**0次新CoreMark DUT运行**：功能绑定token和初始化未改变，按已批风险策略仅复验三个C目标及全容量单元。F136双种子短运行依旧有效，不能写成本轮新实测或正式≥10秒成绩。

## 3. PDS实际执行与启动错误

工具报告：**PDS 2022.2-SP6.4，Fabric Compiler build146967**；Logos2、PG2L100H、速度-6、封装FBG676。当前软件选项不独立证明实物温度等级/封装丝印。所有阶段由新工程实际执行：

```tcl
set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676
compile -top_module soc_top
synthesize -ads -selected_syn_tool_opt 2
dev_map
pnr
report_timing
```

完整add_design/约束/命令在H/pds/build.tcl和H/COMMANDS.md；唯一约束为27MHz create_clock，无假IO delay、false path或降频。

- 普通受限启动：WinError623系统DLL重定位，CreateProcess失败，PDS没有启动；保留空日志和startup-error.json。不替换DLL/重装/关闭安全、不盲重试。
- 工具审批后一次非管理员固定命令`D:\PDS\PDS_2022.2-SP6.4\bin\pds_shell.exe -file H\pds\build.tcl`，进程1200秒上限，实际70.078秒、rc0、无超时。随后核新compile/synthesis/map/pnr/timing报告和数据库，五阶段实际完成；compile/error_info.txt为空，未发现E:错误或未解析用户黑盒。
- 许可证本次实际checkout成功，提示**剩余10天**。应尽快通过官方方式续期，临近11/4交付存在授权到期风险；不由天数推算精确到期时刻。没有读取/写入许可证内容、机器码或授权路径到报告/公共记忆；工具自行生成的原始日志仅本地忽略，不入Git。
- 没有gen_bit_stream；新目录无.bit/.sbit。没有启动服务器、枚举、JTAG、上电、下载或Flash。

## 4. 存储与寄存器初态证据

PDS使用F136 performance-N16完整初始化（原程序15912字节，补零到32K ROM；32K RAM A5），不是空程序或LED镜像。原F140五初始化反解证据保持。

H/memory-init-audit.json重新从新表计算：

- 合成网表保留28个GTP_DRM18K_E1，1792段288位INIT（516096位）全部逐位匹配；16个RAM半字单元完整保留，两个ROM端口配置和RAM单口/字节写绑定保持。
- bank4–7 ROM为全零，四个高半字与低半字同参数/同端口行为，工具合并相同ROM半字；逐bank/两端口/16数据位检查保留输出各有两个LUT输入用途。不是人为缩ROM或换36K组织。资源与所选程序相关，不保证其他镜像仍是14个DRM。
- PnR导出网表中28个gopDRM18K身份仍在；实际报告为**14个DRM36K资源**，不能把原32个仿真实例写成32个物理DRM36。
- regfile x1–x31的992个GTP_DFF_E全部GRS_EN=TRUE、INIT=0；x0的32个位按恒0被删除。证明综合表达保留冷配置初态，不证明实物已配置、任意热复位清寄存器/RAM或电源行为。
- 局限：没有独立解码PDS二进制映射数据库中的INIT，没有生成/读回位流，没有后布局功能仿真；证据是合成INIT逐位核和PnR门身份，不扩张为实际配置数据已在芯片核验。

## 5. 实际资源和最终时序

|阶段|LUT|FF|DRM36K|IO|APM|
|---|---:|---:|---:|---:|---:|
|综合|1809|1555|14|55|0|
|最终PnR|1806|1555|14/155|55/300|0|

无latch；合成层次明确保留CPU1490 LUT/1437 FF（RF992 FF）、外设45 FF、timer64 FF和storage14 DRM。没有把核心整体剪除为常量设计。

**以下以最终`pds/report_timing/soc_top.rtr`为准**，不混用路由器较早的hold-fix摘要：

|内部clk→clk、4730端点|setup WNS(ns)|hold WHS(ns)|负裕量/失败端点|
|---|---:|---:|---|
|慢角|24.425|0.170|0/0|
|快角|29.561|0.115|0/0|

早期router摘要24.526/0.114与最终显式report_timing的24.425/0.115有差别，均保留，不挑更好数值。最终最差setup路径`cpu_core/ex_rd[4]`→前推/ALU→flush_if/if_valid控制→`cpu_core/if_inst[17]`使能，19逻辑级，逻辑2.891ns、布线9.237ns。最差快角hold为id_mem_write→ex_mem_write，0.115ns。

工具Performance Summary给当前逻辑布局估计79.2896MHz；这是**本镜像/自动IO布局/当前内部约束的估值**，不是已实测工作频率、板级Fmax、CoreMark成绩或提升比例；当前目标仍27MHz。没有据此启动提频/CPU优化。

## 6. 剩余警告与验收限制

|警告/限制|实际证据和处理|
|---|---|
|外部IO缺约束|最终时序9个输入、45个输出未约束：rst_n、8个异步GPIO输入及UART/GPIO/stop/error输出。约束检查9类warning、0 error/critical；没有自造引脚/IO delay。自动分配的55个IO不能用于实体接线。需下一板级阶段处理|
|constant probe loop|compile/sdm2adm出现7次`Loop was found during constant probe`，没有提供具体网。其后综合/PnR/内部STA成功、无latch、必要C流程无退化；**警告根因仍未关闭**，不能断言其等于真实组合环，也不能直接说无害。后续板级/定向诊断保留|
|常量/无用节点删除|32位x0、固定0的id_alu_ctrl[4]、未使用tx_busy、eei_state_reg[2]等工具删除，完整数据通路/初态已核；不据常量剪枝宣称整体形式等价|
|B参数保护系统任务|$display/$finish被PDS忽略，B源码不改；当前CLKS_PER_BIT=16为合法固定参数，非法参数的仿真保护不当作硬件保护|
|板级差异|当前顶层CLKS_PER_BIT=16，N234仅有软件回归；不能称已提供27MHz/115200板级串口。没有核实体复位/异步输入时序、实际时钟和全部板级引脚，也没有ILA|

结论为**逻辑SoC有限可实现性通过、带未关闭警告/板级限制**，不作整板时序/实机验收。over_temp原因未闭环，硬件STOP继续。

## 7. 证据入口与复现

H下：APPROVAL、SOURCE_DIFF、equivalence、compile-plan/result、simulation-result/audit、memory-init-audit、pds-audit、timing-audit、postflight及SHA清单。compile-plan保存四个实际完整argv，logs/compile-*和run-*保留原stdout/stderr/process；runs各目录有新VCD、trace、bus、RF/RAM和check-result。普通PDS失败和外部单次结果分开。

PDS原报告：compile/run.log、synthesize/soc_top.snr及soc_top_syn.vm、device_map/soc_top.dmr、place_route/soc_top.prr、soc_top_pnr.netlist、早期timing_summary_after_hold_fix、report_timing/soc_top.rtr。专有模型未复制/分发，原始PDS日志/数据库只在本地；对外只给自有总结/脚本和选定结果。

H/audit_results.py首版把所有LUT输入误限定I2，bank6实际用I1；在任何审计结果产生前断言失败。纠正为I0–I5实际端口枚举后，128个连接用途成立，才输出审计结果。此为**新检查器静态解析错误**，无RTL/预期修改、无DUT或PDS重跑，旧诊断留audit-parser-correction.json。

## 8. 下一阶段建议与停止

唯一推荐：**A-BOARD-TOP-M1纯软件板级适配**。先复用已核板卡资料确定27MHz/复位/UART/有限GPIO实际引脚和极性，新增A板级顶层/真实UART参数/复位同步及有依据的约束，相关短C/接口验证与PDS复验；同步定位上述constant-probe诊断。CPU/B/存储功能和地址不改，无需队员重做核心或包装。

这是新板级RTL/约束/TB/PDS批范围，**尚未实施、待另行批准**；若发现需改CPU/存储协议，先给最小方案再确认，不以本建议自动扩范围。不得因此生成位流/接线/上电/ILA，不能解除过温STOP。B按F139原验证整改并行，10/27 18北京时间窗口不变，没有新B包/送达/承诺事实。

本M0在报告、记忆与工作单元Git同步后停止；正式CoreMark≥10秒、目标硬件运行/片上取证及有证据收益仍未完成。许可证需人工按官方途径及时续期，未擅自申请或修改配置。
