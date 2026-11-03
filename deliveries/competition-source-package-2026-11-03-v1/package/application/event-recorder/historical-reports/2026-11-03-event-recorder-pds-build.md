# 事件记录应用M3：PDS构建、ROM身份与内部时序审计

日期2026-11-03，北京时间；D313/F273。用户批准独立PDS构建，不含硬件。**本阶段成功生成新位流，尚未下载或验收板级应用。**

## 固定输入与修改范围

基于D300恢复快照 `deliveries/accepted-basic-sm2-2026-11-02-v1/performance/pds` 创建独立目录 `work/fpga/2026-11-03-event-recorder-m3/build`。仅替换memory_model.sv和init_tables.svh两处ROM_BITS载荷，1836B生产事件程序后补零至32768B；两处均逐字节重建核对。其余CPU、SoC、外设、复位/同步级保留、存储接口、RAM A5初始化、引脚、27MHz、closure_io窄域约束和流程脚本全部同原件。89项原输入SHA后验保持。

程序来自M2 `build/production0-r1/program.bin`，SHA **CBB37E60674713CCFBB0E603BA774ECB82E2460FA7D2DD2707AF34D4175E3D30**。默认period2700000tick/count128/WAIT20、AUDIT0、DENSE0；名义27MHz下100ms采样/12.8秒一批。完整该批次仍未运行，不能用PDS构建代替M2未完成的动态项。

SCBV沿用已接受的High Voltage工程决定；没有修改硬件供电或证明配置域接线。不是新的调试/ILA镜像，不继承O2波形。

## 实际构建与许可

工具Pango PDS/Fabric Compiler **2022.2-SP6.4 build146967**，执行文件SHA631FFD8F14D6246872873C72025CBC2734C9F8C388075B7AFB0B042F3A684E6F，普通用户无管理员。

实际命令：`D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe -file D:/A_FPGA_Comp/work/fpga/2026-11-03-event-recorder-m3/build/flow.tcl`，cwd为该build目录；完整argv/预算/结束见ATTEMPT及BUILD_EXIT。一次构建约86.31秒，原生rc0，所属Job空，无强清。通过综合→映射→布局布线→时序→位流日志及新产物交叉确认，不仅依赖exit0或旧文件存在。

本次许可可支持上述实际流程，没有安装、改许可证、环境或读取授权文件。没有解析到新的剩余天数提示，因此不沿用11/2的“剩1天”作为今天实际有效期，也不推断长期有效/准确到期日；后续如失效需通过合法途径处理。

## 新产物

位流：`work/fpga/2026-11-03-event-recorder-m3/build/generate_bitstream/board_top.sbit`，3791112B。

SHA-256：**D43E4E419CC2F3656F92BCA2AF7BB23EFBE48B3EEC74A019A1D04FAABD60CEDE**。

新综合网表25个DRM18K参数对象的1600个INIT逐片核对：ROM匹配固定程序+零填充，RAM匹配原A5。未因常量区被裁剪就跳过存在对象的核查。未独立解码sbit全部内部数据，位流身份链以输入冻结、综合INIT、完成阶段、时间及新SHA共同建立。

## 时序、资源及警告

目标PG2L100H-6IFBG676；主时钟37.037037ns/27MHz。

|项目|结果|
|---|---:|
|最终LUT（CLMA1288+CLMS490）|1778|
|最终FF（1184+343）|1527|
|PDS最终DRM36口径|12.5|
|IO|15|
|Slow Setup / Hold WNS|22.238ns /0.173ns|
|Fast Setup / Hold WNS|28.170ns /0.123ns|
|Setup/Hold/Recovery/Removal × Slow/Fast|8组0 failing|
|约束检查|97项，0错误/0Critical/0 warning|
|总流程错误/Critical|0/0|

27MHz是当前设计约束，不是本轮独立测频；工具估算Fmax不能当板上可运行频率或作品性能。新程序和原CoreMark不同，资源差异也不能宣传为相同计算任务的优化收益。

流程保留76条警告：忽略$display/$finish2、x0常量寄存器裁剪32、constant probe loop7、悬空输出清理6、另1条控制位常量裁剪、Timing-4087输出提示18和Timing-4086按键输入提示10。后两类含不同分析阶段重复，不能当独立端口数。closure_io已应用窄域异步入口与输出datapath预算，但没有外部接收时钟/同步input/output-delay预算，故不认全面I/O或CDC/MTBF签核；没有屏蔽日志去换PASS。旧O2调试版4Critical也未被本非调试版结果关闭。

## 资源报告纠正

复用的旧解析器用整数正则读取DRM，曾把本次12.5读为12；复查原表后修正为完整小数并要求右侧表分隔符。原AUDIT_RESULT.json保留为被取代历史，**权威为AUDIT_RESULT_v2.json**，RESOURCE_PARSER_CORRECTION记录原因。

同样回查原SM2性能/验证最终.prr，均为14.5，旧报告/海报材料中的14来自该截断，应在后续提交文案改为14.5；冻结旧包不改SHA，原CPU/程序/CRC/周期验收不因资源文字纠正而撤销。不把少半块资源的错误继续传播。

首次宿主审计还因编码别名utf8-sig错误中止；已保留原脚本/错误，改为utf-8-sig后只重跑只读审计，没有重建PDS或放宽判定。

## 证据与恢复

入口 `work/fpga/2026-11-03-event-recorder-m3/README.md`；SCOPE/PRECHECK、PROTECTED_INPUTS/FROZEN_INPUTS、ATTEMPT/BUILD_EXIT、AUDIT_RESULT_v2、RESOURCE_PARSER_CORRECTION、原生已脱敏日志、完整原报告、软件与新位流留在独立目录。原D300恢复快照和全部失败保持。日志仅过滤许可/机器标识等私人字段，错误/警告保留。

本轮没有启动硬件服务器、枚举设备、扫描JTAG、配置FPGA或操作Flash，没有读取COM或要求实体动作。完成后停止于此；原已消费配置额度不复用，不推定目前板上供电/驻留镜像。

下一最有价值的是另获授权后，用该固定应用镜像做一次易失性下载及正常/顺序错误/超时三场景板级验收，核完整串口账本、时间和LED/按键现象，保留首次失败。不以软件通过/新位流存在自动恢复硬件。
