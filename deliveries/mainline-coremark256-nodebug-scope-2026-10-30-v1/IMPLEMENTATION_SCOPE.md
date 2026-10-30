# A-BOARD-COREMARK256-NODEBUG-M1 /1.0.0（待批准）

2026-10-30；依据F182/D199及F181软件证据，目标是在两个独立工程把既有performance256/validation256镜像实现成非调试位流，取得新INIT/资源/内部时序证据。不是恢复硬件，不是正式跑分，不是256 RTL仿真。

## 输入和唯一允许变化

- 使用`work/software/2026-10-29-formal-coremark-m1`已构建ELF/bin、初始化表、两种子独立参考及短DUT证据；不重编C、不变种子/256迭代/27MHz/2000B/flags。实际完整SHA锚定`work/analysis/2026-10-30-board-readiness-m0/SOURCE_AND_IMAGE_IDENTITY.json`。
- 生产模板为`work/fpga/2026-10-27-board-coremark8-bitstream-m1`的13功能源、生产memory_model、build.tcl及两约束；12文件逐字节不变。memory_model沿原有M0_VERIFY排除和INIT内联方法，只更新两程序的ROM内容，RAM继续A5；不可预清零掩盖CRT问题，不改端口/延迟/时钟/控制/存储映射。
- 唯一新根目录`work/fpga/2026-10-30-coremark256-nodebug-m1`，若已有则选唯一后缀；两个case完全隔离，保留source-before/生产模板快照、输入SHA、准确diff。不得覆盖F163/F181、R4或旧交接包。
- 只允许新本阶段脚本/元数据/审计适配、生产INIT及源路径/输出目录变化；基于已验F163审计修改case/期望镜像身份，不保留“8与1只差1字节/只有1个INIT变化”的过时期望。新程序必须完整从原bin独立算全1792段，不按DUT/综合实际值回填预期。

## 原生执行/预算

固定已装PDS2022.2-SP6.4 build146967，用绝对路径`D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe -file <case/pds/build.tcl>`，工作目录同case/pds。最多两次CLI、两case各一次且串行；每次1800秒，同一阶段绝对4800秒，不重试/重置。先冻结输入、脚本和预期，再运行。

各次build.tcl只允许set_arch Logos2/PG2L100H/-6/FBG676和board_top的compile→synthesize ADS→dev_map→pnr→report_timing→gen_bit_stream -scbv "High Voltage"。High仅既有D010工程决定，不改变温控/下载/Flash等配置。没有新帮助查询、-project/-run或-force_to_run、调试插入/导出、GUI。旧1.3.0导出继续待批，不包含在本阶段。

监督器/直接PDS入口各限512MiB/1GiB；内部阶段工具pool若有报告仅独立列出（警戒2GiB），不得冒称已测全后代内存。每stdout/stderr16MiB、各case新产物512MiB、总新证据2GiB；审计每case300秒。先离线核阶段状态/路径竞争处理；日志禁止打印许可/host字段，只提取正常checkout与本次实际到期提示。授权异常保存并停，不配置/申请许可。若需要沙箱外运行，工具权限独立申请，不是管理员许可。

## 验收和停止

1. 原生退出后再核新鲜位流mtime/size/SHA，阶段日志与实际产物对应，不能只用rc0或旧文件存在。每阶段完成、无错误/截断/超限且受保护原件同。
2. ELF种子4=256、ROM32KiB=image+零/RAM32KiB=A5，全部保留DRM原语/1792个INIT与原bin独立映射核同；不反解专有位流，不称硬件读回/布局后仿真。
3. 目标/顶层/两约束/94条引脚约束及15针位置/标准不变；slow/fast setup/hold/recovery/removal八类内部27MHz报告正裕量、TNS0/失败端点0。外部5输入/9输出无delay及实际CDC仍未验证，不能升为全系统时序PASS。
4. 按类别和具体消息对比F163警告；既有7条constant-probe保持OPEN，不推定无害。出现新增Critical/错误、时序失败或新增告警，保存产物及诊断，停止相关后续运行，不为过关改RTL/约束/预期。若需扩大范围，先说明。
5. 分别输出两case的bin→INIT→来源功能源→新综合INIT→位流SHA、资源与内部时序；禁止混用performance/validation或旧8位流。hardware_valid/formal_score_valid=false。256独立参考不升级为256 DUT通过。

本阶段仅解决“已有长程序但无对应FPGA实现”的缺口；不解决温度/实际供电/电源开关未知、调试4Critical/采样驱动/CDC、片上波形与真实跑分。0新GCC/参考/仿真，0安装/驱动/许可修改/环境/重启/外发，0硬件服务器/设备枚举/JTAG/上电/下载/Flash。over_temp STOP保持；本阶段结束报告后停止，不自动进入实机。
