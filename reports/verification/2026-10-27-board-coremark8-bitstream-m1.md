# CoreMark8 CPU软件位流：单次构建与退出后核验

2026-10-27；授权D164，事实F163，有限验收D165。仅软件生成；不解除over_temp硬件停止。

本次把F160已经在仿真中验证的8迭代程序，连同原CPU/SoC/存储/外设，形成了目标FPGA的可下载格式文件。它消除了“已有程序但没有对应CPU位流”的缺口；不证明CPU已在开发板执行、正式CoreMark成绩或片上ILA已完成。

## 实际结果

|检查|结果与边界|
|---|---|
|工具/目标|PDS2022.2-SP6.4 build146967；Logos2 PG2L100H / -6 / FBG676；board_top|
|调用|唯一1次CLI，81.547秒/native rc0，无超时/日志截断；退出后独立检查新产物|
|许可|本次正常checkout成功；实际提示剩余7天，应及时正规续期；未读取许可内容/机器标识，未更改配置|
|功能源|F160整组13文件、source-before及原件SHA一致；不混入F146候选，不重新GCC/Icarus/仿真|
|生产绑定|12文件逐字节同源；memory_model仅排除M0_VERIFY观测视图并内联同一初始化表；与F142相同转换后的模型规范化核同|
|镜像|15912B原8迭代bin；ROM32768B=image+零，RAM32768B保持A5；不复用旧1迭代ROM|
|INIT|28个保留DRM18原语、1792个INIT片段全部由原始ROM/RAM独立计算核同；旧1迭代也同法校准。仅bank[3]/halfword[0]/INIT_38变化，对应镜像offset15904的1→8|
|内部时序|27MHz；slow/fast的setup、hold、recovery、removal八项均正裕量、TNS0、失败端点0。最差setup23.279ns、hold0.129ns|
|资源|1805 LUT、1519 FF、14 DRM36（28 DRM18）、15 IO、0 latch|
|约束|原27MHz及94条引脚约束不改，15针位置/标准核同；5个异步输入及9个输出无外部delay，不能声称外部IO或物理CDC通过|
|SCBV|High Voltage仅沿D010已接受的工程假设；工程及生成数据库核同，Bitstream-2001未出现；不证明实际配置供电匹配|
|警告|与F142逐类别计数相同，无新增类别/计数。7条constant-probe根因仍OPEN，不能宣称无害或零警告|
|保护|41原件、48冻结输入退出后及最终后验核同；旧工程、位流、初始化和失败证据未覆盖|

位流完整路径：
`D:\A_FPGA_Comp\work\fpga\2026-10-27-board-coremark8-bitstream-m1\pds\generate_bitstream\board_top.sbit`

大小：3791112B；SHA-256：
`F548BC8BAA3DDFB5E2EB3158AE108F5A9DFCE7FE6C08919DB8DB245187C8D7A4`

原镜像SHA-256：`EC365839FEA1111CB365763322E2FA99C3C3B3F6B74A5884C5B0EB30593486F0`。逐源、约束、初始化完整SHA见下列收据。

## 命令、产物及复查入口

工作目录：`D:\A_FPGA_Comp\work\fpga\2026-10-27-board-coremark8-bitstream-m1\pds`

```powershell
& 'D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe' -file 'D:/A_FPGA_Comp/work/fpga/2026-10-27-board-coremark8-bitstream-m1/pds/build.tcl'
```

实际通过同目录外层`run_once.py`监督启动，普通用户/独立工具审批，非管理员；绝对总deadline、1800秒原生限时、stdout/stderr各32MiB，旧attempt不允许重置。Tcl完整列在`pds/build.tcl`，依次compile、ADS synthesize、dev_map、pnr、report_timing、gen_bit_stream -scbv "High Voltage"。**这次调用已用完；本报告不是重新执行或下载授权。**

下列均相对独立工作目录`work/fpga/2026-10-27-board-coremark8-bitstream-m1/`：

- `APPROVAL.json、SOURCE_RECEIPTS.json、INIT_RECEIPT.json、SOURCE_CHANGE_SUMMARY.json、FLOW_DIFF.patch`：授权、整组源/实际变化、约束与镜像。
- `PDS-attempt.json、BUILD_EXIT_RECEIPT.json、COMMAND_RECEIPT.json、COMMANDS.md`：一次调用/进程退出/实际参数；`logs/pds-flow-once/`保留完整原生stdout/stderr及进程数据，仅本地。
- `pds/compile、synthesize、device_map、place_route、constraint_check、report_timing、generate_bitstream`：原始工程/网表/时序/生成证据，仅本地。
- `CONFIGURATION_AUDIT.json、MEMORY_INIT_AUDIT.json、TIMING_RESOURCE_AUDIT.json、WARNINGS_LICENSE_AUDIT.json、AUDIT_RESULT.json`：真实解析结果；审计逻辑`audit_build_v3.py`。
- `SUMMARY.json、STATUS.json、REPRODUCE.md、SHA256SUMS.json、POSTFLIGHT.json`：分层结论、复现边界、逐文件清单/最终预算与保护核验。Git只纳入已审小型脚本/脱敏收据；原日志、网表/DB、厂商模型、镜像、初始化大表、位流及工具不上传。

入口PDS shell峰103264256B、监督父峰64360448B；工具自行报告内存池最大1247MB。没有独立测得整个内部工具进程树峰值，不把入口峰当整体内存。

警告逐类及旧计数均保留在WARNINGS_LICENSE_AUDIT；包括Verilog-2008、Sdm-2000、constant-probe、Public-4008、移除常量寄存器提示、Timing-4086/4087，不能只报告目标告警消失。

## 保留的纠错与限制

1. 旧scope状态把UTF8/LF规范化SHA `BB1D768F…6753B9D`写成文件SHA；实际CRLF文件SHA为`6BE782B91E2670510E9A47FC1233B51FC89CFC5B7DDE9911D4D9E4C234BE4B08`。已与审查Git blob逐字节核同，授权内容未变。原scope及状态不覆盖，纠错在其目录`SCOPE_IDENTITY_CORRECTION.json`；D163/F162的旧SHA含义由本记录更正。
2. 首版产物审计在flow.log查找本应在stdout的Tcl成功标志；第二版将字符串INIT_MODE误作数字INIT片段。均保留原代码/诊断；第三版修正记录位置和精确INIT_00..3F键过滤，其他参数照旧核同。**没有重新调用PDS，没有改DUT或放宽数值预期。**
3. INIT核验到合成原语，不是专有位流二进制反解、硬件读回或布局后功能仿真。8迭代程序仍是有限短测，不满足正式至少10秒测量；名义估频72.685MHz不等实测时钟/Fmax或效率提升。
4. 本轮0新C构建/0仿真编译/0新DUT/0硬件调用。历史JTAG PG2L100H识别单独保留；本轮未扫描、未下载。CPU实机、片上ILA、物理配置供电及过温原因均未验证，停止条件不变。

下一最有价值的阶段是明确安全可用FPGA平台与真实CPU/时基/ILA取证范围；不能仅因位流生成成功而恢复本板供电/连接，也不自动启动双160长跑或插入ILA。本阶段到此停止。B工具差额继续独立，不改变外设窗口或代其重写。
