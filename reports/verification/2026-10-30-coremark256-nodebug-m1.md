# 双种子256迭代非调试位流生成及有限核验

2026-10-30；批准D200、结果F183/D201。对应scope1.0.0真实字节SHA `4C6E5A61DFFB882F378883926D098364EDF8FB16C6150A01B193DE47A67C0A46`。本轮只实现既有软件镜像，不是256 DUT/实机/正式成绩，不解除过温停止。

|case|原生PDS/时长|新位流SHA256|INIT核验|
|---|---|---|---|
|performance256|rc0，83.360秒|A86C7ECB6EF98CC2DDFD3CEFB67D8027BD66EFA5B136FADEC3F558B7FF644CC4|1792段核同，相对旧8变134段|
|validation256|rc0，82.609秒|992EA6D9FBCD1990E07A1F46EA86F13DBD41E7CBA1941AD42DA96612E86D3F10|1792段核同，相对旧8变148段|

两位流各3791112B，位于`D:/A_FPGA_Comp/work/fpga/2026-10-30-coremark256-nodebug-m1/<case>/pds/generate_bitstream/board_top.sbit`。每case完整实际命令为`D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe -file <case>/pds/build.tcl`，cwd为case/pds；argv/native rc/时长/资源收据在`logs/pds-<case>/process.json`，退出时间与新位流mtime、size和SHA均核同。没有第二版PDS重跑，原生实际总2次。

PDS2022.2-SP6.4 build146967；目标Logos2 PG2L100H/-6/FBG676、board_top。compile、ADS synthesize、dev_map、pnr、report_timing、gen_bit_stream全部完成；SCBV沿既有High Voltage工程决定，工程/生成数据库同、无Bitstream-2001，不当实际供电测量。

两例内部27MHz八类时序（slow/fast setup/hold/recovery/removal）均正裕量、TNS0/失败端点0，最差setup23.279ns、hold0.129ns；资源均1805LUT/1519FF/28DRM18（14DRM36）/15IO/0latch。原94约束、15针位置/方向/Bank/VCCIO/标准核同。5个输入和9个输出无外部delay、实体CDC未验，不报全系统时序通过。资源/裕量与旧8相同不说明吞吐优化，本轮不是性能优化。

12生产功能文件逐字节同F181/F163；memory_model沿原生产绑定，只内联新ROM/RAM INIT，逻辑规范化同旧模板，准确INIT_DIFF保留。ROM32768B=原bin+零，RAM32768B保持A5；保留28个DRM原语，每64段INIT从原bin独立计算，1792段全部逐数核对，非INIT参数/保留集合与旧模板一致。没有专有位流反解、硬件读回或布局后功能仿真。bin/ELF/INIT/生产memory/位流/期望报告身份在TARGET_IDENTITIES.json；不混用两个seed或旧8位流。

告警比较仅规范化变更的工程根路径，其余完整消息/行号及计数保持；两例无新增告警，7条constant-probe根因仍OPEN；未以生成成功宣称无害。PDS两次正常checkout，实际提示剩余4天（非新增查询或到期时刻证明），应预留正规续期。未读取许可文件/机器标识，原始工具日志只本地，不纳Git。直接shell峰值约103/102MB、父监督约65/68MB；内部pool工具报告1248/1249MB，非独立测全后代，均在范围。

首入口run_stage.py因漏建logs父目录于supervisor.mkdir报FileNotFound，发生于Popen之前/PDS0。保留STOPPED.json、原入口及尝试标记；prepare_recovery.py只补目录，r1使用新元数据路径，原输入与4800秒时钟不变。HOST_PREFLIGHT-r1检查完成标志与可变输出消失分支，仅FileNotFound可忽略/PermissionError仍失败；不对受保护输入忽略错误。此处不是原生PDS失败或额度增加，也不隐瞒A准备错误。

108受保护条目、112冻结输入在退出后及最终后验SHA核同。完整过程/源码表/两约束/基线快照保留。封存237文件/36360220B（不含新SHA清单自身），低于2GiB；SHA256SUMS-FINAL.txt存逐文件哈希。若后续仅新增Git组织文件，将另列不覆盖本清单。

入口：`work/fpga/2026-10-30-coremark256-nodebug-m1/RESULTS.json、TARGET_IDENTITIES.json、POSTFLIGHT.json、PLAN.json、FROZEN_INPUTS-r1.json`，以及每case的AUDIT_RESULT/BUILD_EXIT_RECEIPT/INIT_DIFF。原生日志路径和完整命令在process.json，不复制许可相关日志正文。0新GCC/独立参考/仿真编译/DUT；无GUI、安装、驱动、许可修改、硬件服务器、设备枚举、JTAG、供电、下载或Flash。

本轮消除“已有长程序但没有对应FPGA实现”的缺口。F181的256参考约19.946/21.460秒只以27MHz设定折算，不是本轮新实机成绩。CPU实机/实际频率/双种子重复运行/正式CoreMark/片上波形仍未取得；over_temp、配置供电、外部IO/CDC、R4调试4Critical及采样驱动未知仍保留。下一关键门槛是有依据的硬件诊断/准入，不能因新位流存在直接上电下载。阶段完成即停，不自动进入硬件或旧调试导出。
