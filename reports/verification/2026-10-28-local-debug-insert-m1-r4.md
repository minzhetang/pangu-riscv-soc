# 本地观察核R4：调试位流已生成，保留关键告警验收门槛

日期2026-10-28，D179批准1.4.0；F171/D180。结果为**软件调试位流候选已生成，尚非最终实现/实机验收**。

## 交付和真实执行结果

工具：PDS 2022.2-SP6.4 build146967；目标PG2L100H-6IFBG676。新目录：
`D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1-r4/`。

| 层次 | 本次结果 |
|---|---|
| 第一次PDS | 只编译/综合，18.719秒/原生rc0；完全退出后检查新ADF/VM及其SHA，才允许GUI。 |
| 一次Inserter GUI | 275.828秒/原生rc0，正常退出；直接载入本轮新ADF，无旧网表参考、无等待循环。 |
| FIC | 单核/140数据位/1024点，nt_clk物理上升沿，Data Same As Trigger，无过滤/多窗口；每位顺序与新网络清单核对。 |
| 第二次PDS | 同一冻结输入完整编译、综合、实际插核、Map、PnR、时序和位流；105.078秒/原生rc0。不是中途日志或退出0单独判定。 |
| 新位流 | `build/generate_bitstream/board_top.sbit`，3,791,112字节；新鲜mtime、大小和SHA均在进程退出后核对，与旧位流SHA不同。 |
| 27MHz内部时序 | Slow/Fast的setup、hold、recovery、removal均正裕量/0 failing；最小setup **24.876ns**，最小hold **0.113ns**。工具其他已报告调试时钟行亦0 failing，但不代替实际JTAG/CDC验证。 |
| 功能初始化 | 原28 DRM18/1792 INIT与F163逐片相同，另从原ROM/RAM字节独立映射核对；15912B程序、ROM32KiB补零/RAM32KiB A5保持。 |
| 最终门槛 | **新增4条调试/JTAG时钟Critical Warning未关闭**；停止最终验收，不再构建或改约束掩盖。 |

位流SHA256：
`139DD52013B6C3A9ADA50B92D72F1479ED488DE2C70D024284A27AEC573EFC03`

FIC：`debug.fic`，8977字节；SHA256：
`B4799B1A379A6D023E8B2A5AC19A283D48EF5484A3773A774F60F8F214CB8CFF`

## 源码、映射和证据边界

本轮只新增获批的eei_hold保留注释，合计3文件7处PAP_MARK_DEBUG；完整13源去掉这些注释后逐字节等F163。准确diff和每文件SHA在DEBUG_METADATA.patch/SOURCE_RECEIPTS.json。未修改ISA、控制/数据路径、存储协议、外设、时钟边沿或程序；没有新GCC/Icarus/DUT运行，不把本次构建当新CPU功能验证。

第一次和第二次综合的**完整VM**仅归一阶段路径及生成日期后逐字相同；FIC从本轮第一次新ADF得到，而非历史ADF。实际清单4899网，全部140位映射，flush_if使用已核直接别名flush_id，顶层停止/错误线使用冻结RTL的直接连线别名。保存FIC逐位顺序核对，实际Map调用并成功编译Pango debug core；布局后库存含完整0..139数据一级采样寄存器。

上述为“有序FIC＋原生插核执行＋完整采样寄存器库存”证据，**没有独立反解位流每条物理路由或全部后布局引脚连接**。内存INIT审计在综合网表层；没有硬件读回、布局后功能仿真或形式等价。不能宣称140路实际采样及CPU实机已通过。

## 复位字段差异的结论

`ins_set_net -reset`虽返回成功，最终FIC没有用户Reset Port。已视觉核对安装版官方《Fabric Inserter用户手册》V1.0（2022.07.12），实际PDF **13页**说明Reset Port可选且示例不使用；**39页**说明Use Reset Port默认不启用，关闭时不显示该端口。当前GUI也无Reset Port节点，符合这一默认状态，不是已完成板级复位连接。

本版**保持可选用户Reset Port未启用**，没有改全局偏好或重开GUI重构；sys_rst_n作为数据通道38被观察。生成核库存存在conf_rst/resetn等内部线，但没有独立还原其完整fanin；不宣称板上复位键会清空或重新武装ILA。需要这种行为时应在后续明确配置/验证，不把采样复位线与CPU复位混同。

文档原路径：`D:/PDS/PDS_2022.2-SP6.4/doc/Fabric_Inserter_User_Guide.pdf`，SHA见RESET_REVIEW.json；两个原页渲染已视觉检查。渲染工具报Symbol/ArialUnicode显示字体提示，但关键中文与选项可读，未安装字体/软件。

## 资源、时序与剩余告警

| 资源 | F163无调试版 | 本版 | 差值 |
|---|---:|---:|---:|
| LUT | 1805 | 2931 | +1126 |
| FF | 1519 | 3838 | +2319 |
| DRM36资源单位 | 14 | 18 | +4 |
| IO | 15 | 15 | 0 |

实际布局库存为28个功能gopDRM18K加4个调试全36Kb gopDRM，不能把4个全块误记为8个物理半块；合计32个RAM原语、等效36个18Kb。该增量含保留标记和整体插核实施，不冒称纯IP净开销或CPU效率收益。主机审计初稿误按全半块同类计数触发断言，修正解析后复核，未重跑PDS/改输入或预期。

引脚、3.3V普通IO标准与94约束核同；14个外部IO时序未约束、实际CDC未验证，静态估计Fmax不是实测或性能提升。SCBV沿High Voltage工程假设，Bitstream-2001未出现，不证明板上实际配置供电正确。

新增Critical共4条：

- Place-2028一条：SCANCHAIN固定位置与全局时钟缓冲布局不理想。
- Route-2036三条：TCK1、CAPTUREDR及后续调试配置时钟路径使用SRB。

路径均包含工具插入的u_CORES/JTAG控制域；dmr记录工具生成的`u_CORES/drck_o PAP_CLOCK_DEDICATED_ROUTE=FALSE`，不是本轮修改用户FDC。**来源可定位不等可以豁免**；即使声明时钟下All Constraints Met，仍保留物理实现/实际采样验收门槛，未添加false path或降低频率凑通。

原7条constant-probe警告仍在，根因未闭。Public-4008数量14→49，净增35；逐字新增37/移除2，其中34条属于调试命名空间，3条CPU停止输出清理对应原总线/单元类型变化，不能自动按“全是调试噪声”关闭。DANGLING_REVIEW记录归类；用于分析前仍需核实实际采样源驱动，不只看FIC或寄存器名。

## 复现入口、保护及下一步

实际命令由现有Python `-B run_phase.py pre`、`-B gui_control.py`、`-B run_phase.py build`驱动；两次原生PDS argv均为固定绝对路径`D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe -file <本阶段pre或build/flow.tcl>`。准确argv/cwd/时长/rc见PRE_EXIT_RECEIPT/BUILD_EXIT_RECEIPT及logs/*/process.json；GUI原生argv/动作在OWN_GUI_PROCESS/GUI_ACTIONS，仅本地。历史入口有独占计数，不直接重复运行。

关键结果：FIC_AUDIT、SYNTHESIS_IDENTITY、MEMORY_INIT_AUDIT、INSERTION_AUDIT、TIMING_RESOURCE_AUDIT、WARNINGS_AUDIT、WARNING_DETAIL、DANGLING_REVIEW、CRITICAL_TRIAGE、RESET_REVIEW、AUDIT_RESULT、SUMMARY、POSTFLIGHT、SHA256SUMS。

148保护条目、预综合52/完整构建54个冻结文件核同；两PDS和唯一GUI正常退出、无额外原生命令帮助查询。许可证本次实际提示6天，需留意正规续期，不推算精确失效时刻或改许可。

下一最有价值的是**只读复核4条生成调试时钟关键告警和采样源完整性**，先利用现有报告/映射产物及官方资料；不自动重建、改约束、改复位或进入硬件。作品仍缺真实FPGA/ILA及正式CoreMark证据；本次0硬件、未起服务器/JTAG、未下载/Flash，over_temp STOP不变。Git外发既有系统阻塞保持，本轮仅审查本地提交，不改通道绕过。
