# CoreMark256完整SVF加载身份闭环与实机长测

日期：2026-11-01；授权D285；本轮实测及原件核对，不重新构建/仿真。

## 验收结论

接受固定双种子、原厂完整CRAM SVF加载路径下的有限实机测量与身份对应：两种指定镜像均自动输出正确全文；验证同镜像KEY0重复一致；性能镜像在用户报告全供电断接后独立恢复并自动输出一致。3次完整配置均为真实写入，不因原生cfg_program计数为0而称0配置。4份新硬件报告，非旧数据重放。

此前H44指定PERF却出现VAL的事实保留。当前完整SVF是已见证的有效替代流程；尚未证明旧原生加载路径的具体根因，不把ISC、缓存、DRM保留或板卡缺陷写成确定原因。

## 本轮逐项结果

|阶段|内容及启动|配置秒数|报告字节|目标ticks|标称27MHz秒|结论|
|---|---|---:|---:|---:|---:|---|
|h48|performance256 / automatic_after_warm_full_SVF|311.5620000001509|1123|538539600|19.945911111|全文/5CRC/计时匹配|
|h49|validation256 / automatic_after_full_SVF_PERF_to_VAL|311.5620000001509|1119|579425414|21.460200519|全文/5CRC/计时匹配|
|h50|validation256 / user_KEY0_no_new_config|无新配置|1119|579425414|21.460200519|全文/5CRC/计时匹配|
|h51|performance256 / automatic_after_user_reported_full_power_cycle_and_full_SVF|311.51499999989755|1123|538539600|19.945911111|全文/5CRC/计时匹配|

H48/H49/H51：每次完整SVF含原厂JRST、CFGI、整个配置数据、唤醒和DONE核验。100kHz原厂频率与等待原样保留，600秒配置/700秒控制器守卫；每次正常原生退出、无强清、所属Job均空，UART0写/无错误。H50仅只读串口和用户一次KEY0，不含新配置。H51用户回执明确先12V、再两USB断开，约10秒后先USB后原12V重接，JTAG不动；这是用户报告的完整断接，未实测所有电源轨归零或温度。

H51初始STATUS00180c80：DONE0/GOUTEN0/OT0，其余错误0；配置后两次081ffca0：DONE1/GOUTEN1/OT1，CRC/ID/timeout等0。H48/H49前后081ffca0。bit27照录，不独立阻断、不改镜像原有保护设置，也不据工作正常推断温度安全。

## 配置流和源码身份

- 官方UG040005 Logos2 Configuration V1.3（2023-04-24），实际PDF52/60、印刷51/59，表3-7/3-16均视觉复核：ADRR地址11，[26:25]=01为DRM；实际镜像先ADRR0、2960512B非DRM，再ADRR02000000、827392B DRM。原调查脚本的FDRI称呼在Logos2手册中对应CMEMIR。两镜像非DRM相同，DRM有1255字节不同；不因此直接宣称硬件内存已读回逐字核验。
- 原厂SVF大SDR30328896bit；将TDI完整位序反转回配置顺序后，与对应sbit从同步字2084到末尾逐字节相同。生成器规范化了同步前头部141字节，故不能说含头部全文件字节相同。两SVF非bulk命令完全相同，未手工改写数据/等待。
- SOURCE_BUILD_IDENTITY.json重新核ELF/bin、冻结软件输入、全部PDS源码/初始化、约束、工程和位流身份；237历史构建文件、21旧冻结输入、4固定原件均SHA不变，另6份本次输入副本SHA匹配。未改CPU/SoC/外设RTL、固件、参考模型、预期或SCBV；没有新设计构建/CPU仿真。

|种子|sbit SHA-256|完整原厂SVF SHA-256|
|---|---|---|
|performance256|A86C7ECB6EF98CC2DDFD3CEFB67D8027BD66EFA5B136FADEC3F558B7FF644CC4|F177A37FA89D92BC678E89E3DF8CE48FD30FA70675774EDD4F68E0308D514C7E|
|validation256|992EA6D9FBCD1990E07A1F46EA86F13DBD41E7CBA1941AD42DA96612E86D3F10|00E74B45A3443ADC186D75518A9C441B74C7D4A5C39691DFEB072E120BC6F123|

完整来源：本地官方手册[UG040005](2026-10-14-over-temp-evidence/UG040005_Logos2_Configuration_V1.3_EN.pdf)，实际页图见本阶段official-registers-PDF52.png、official-ADRR-PDF60.png。PDS Fabric Configuration User Guide V1.0实际PDF81列100KHz为支持频率，94–95说明SVF生成/执行；仅使用已安装官方工具。

## 性能含义与限制

- 性能种子256迭代：538539600ticks；19.945911111标称秒；12.834710762迭代/秒，0.475359658/MHz。不把固件整数打印的13当精确值。
- 验证种子256迭代：579425414ticks；21.460200519标称秒；验证用，不将其11.9291直接混作性能种子成绩。两种子各两份新报告超过标称10秒且重复一致。
- 只使用目标64位计时器差值/文档27MHz，计算与UART输出分离；不使用主机仿真或传输墙钟冒充计算时间。27MHz未独立仪器校准，未声称EEMBC认证。
- 完整SVF配置约311.5秒，比之前原生模式约165秒慢；这是正确加载/恢复流程的改进，CPU计算周期未改善，不能当性能优化收益。
- 共享冻结主机解析器保留其通用软件候选/内层hardware_valid=false标签；它本身不判物理来源。当前外层physical_uart_capture_complete及正常退出/全新原始采集/阶段审查组成硬件证据，不改旧解析器来凑通过。
- 无完整活体ROM逐字回读，本版无ILA、无真正退休PC或统一WB/STORE提交序；有限工作负载通过不等完整RV32I、CPU整体正确或作品最终验收。既有IO延迟未完整约束、CDC、SCBV实际接线/过温原因等限制没有被本次成功消除。

## 完整命令及证据入口

工具：已安装Pango PDS2022.2-SP6.4；本轮CLI/硬件服务器配置链路可用，未改许可证/驱动/系统环境。Python版本保存在RESULTS.json。

实际执行入口为以下各独立目录的run.py --run（普通用户Python -X utf8 -B）；每个入口都有一次性ATTEMPT，切勿重跑旧入口。完整Tcl命令保存在各RESULT.json.commands及总RESULTS.json.rows.commands；包括connect、100kHz、scan、publicID、STATUS、固定sbit assign、固定完整SVF execute、STATUS两次、disconnect。

```tcl
cfg_execute_svf -svf_file_name <本次唯一目录>/inputs/configuration.svf -device_index 0
```

配置前先打开只读COM22/115200/8N1、DTR/RTSfalse；随后完整配置及接收。0串口写、64KiB上限；H50接收300秒、父320秒。主机检查：

```powershell
& '<已验证Python>' -X utf8 -B 'D:/A_FPGA_Comp/work/pds-jtag/2026-11-01-coremark256-measurement-m1/check_measurement.py' <performance256或validation256> '<本次唯一目录>/uart-raw.bin'
```

检查器输出为各MEASUREMENT_CHECK.json，原始报告uart-raw.bin，所有原生公开技术日志native-sanitized.jsonl，退出/清理RESULT.json、串口来源SERIAL_RESULT.json，用户按键及全断接回执分别原样记录。它检查冻结全文/CRC/计时及采集来源，不仅看exit0。

总结果：[RESULTS.json](../../work/pds-jtag/2026-11-01-coremark256-identity-m3/RESULTS.json)。源码链、SVF映射、历史输入保护和证据SHA均在同目录。新有限恢复基线：[BASELINE.json](../../work/hardware-baselines/2026-11-01-coremark256-full-svf-v1/BASELINE.json)。旧H33失败、F247不符、H41部分回读等全部保留。

## 阶段停止与下一步

本阶段3次配置额度已用完，所有工具已退出、无后台监听，不再追加配置/按键/Flash。当前最后驻留为H51性能256易失性镜像，未取得新断电报告。下次恢复须新阶段/新唯一目录与实际状态，不复用ATTEMPT或旧实体回执。

唯一下一建议：以本次可恢复固定基线为参照，进入同程序片上流水线效率/关键算法取证及报告深化；先冻结观察目标与可比条件，不自动修改CPU或开始新调试构建。D245待审Git文档5项保持本地，未提交/推送。
