# CoreMark256实机长测：性能两轮通过，验证配置失败

日期：2026-11-01；D272/D273，实测事实F244/F245、处置D274。所有路径相对项目根D:\A_FPGA_Comp。

## 已取得的真实结果

|阶段|实际方法|结果|目标ticks|标称27MHz时间|
|---|---|---|---:|---:|
|H30 performance256|先开COM22，再一次易失Program，自动输出|1123字节全匹配，五CRC通过|538539600|19.945911111s|
|H31 performance重复接收|180秒窗口到期，0字节；用户回执已晚|采集缺口，不判CPU失败|未取得|不适用|
|H32 performance256|新接收窗口、明确KEY0重复|1123字节全匹配，五CRC通过|538539600|19.945911111s|
|H33 validation256|先开COM22，一次易失Program|100%后官方DONE错误，0字节|未取得|不得拿先验21.4602s当实测|
|H34/H35|未启动|因配置失败阻断|未取得|未取得|

性能两轮均为五级CPU实际执行256迭代后由物理UART输出，主机逐字节匹配冻结报告；并非旧数据重放、宿主仿真耗时或文件存在判PASS。CRC：seed e9f5/list e714/matrix1fd7/state8e3a/final b40f。原始start=0x0000f20f，end=0x201a685f，64位差=0x20197650=538539600。每轮均超270000000目标ticks。完整raw SHA=73425EECBAB76C9DDE20D58A7F1E85014F346B3242C995C9B6F64B1DCDC0679E。

准确换算：256×27000000/538539600=12.834710762216929迭代/秒；除27MHz=0.47535965785988626/MHz。固件打印整数秒19、整数速率13，不能将13作为精确成绩。串口输出位于stop_time之后，不计入算法计算时间；源port/core_portme.c的64位高低高读取及差值溢出守卫已核。硬件计时器直接接板载系统clk，不因CPU同步存储两相而把频率减半。

## 版本与证据

稳定输入：work/fpga/2026-10-30-coremark256-nodebug-m1，两例分别保存源码、初始化、PDS工程/约束、报告和位流；软件依赖work/software/2026-10-29-formal-coremark-m1。无新GCC编译、RTL仿真、RTL修改或PDS构建。12功能RTL、引脚/27MHz及65位流设置与既有8迭代基线核同，程序和存储初始化单独固定。237项历史SHA与10项新冻结输入执行前后全部一致，见本阶段INPUT_MANIFEST_RECHECK和POST_SOURCE_HASH_CHECK。

performance位流SHA A86C7ECB6EF98CC2DDFD3CEFB67D8027BD66EFA5B136FADEC3F558B7FF644CC4；ELF FA9822A21D61AE72E807541CFB9676EE308D3F247EF7180F84E74151AD7B0D1C；bin 0160BF311C70A8CCDDDF1B4F19B96C4F5B7357CB2E4BD04E69DB9A87DBC8C21E。validation位流SHA 992EA6D9FBCD1990E07A1F46EA86F13DBD41E7CBA1941AD42DA96612E86D3F10，复制原件及执行副本均3791112字节/同SHA，排除复制损坏，不证明位流/下载路径整体无误。

独立CoreMark算法来源字节核对ALGORITHM_SOURCE_IDENTITY（6项均同；起初选择的历史GitHub审查目录仅含子集，缺项不当源码差异，已改查既存upstream-direct完整源码）。16/16新主机解析正负控只证明检查器，不是新CPU测试。未新联网下载或安装。

时钟原件：盘古100Pro+开发板（MES2L676-100HP）配套资料/教程1_硬件实验指导手册_盘古676系列100Pro开发板.pdf，实际PDF22–23页/印刷18–19页，已渲染视觉核对U11 27MHz与D18。CLOCK_BASIS记录原件SHA及RTL/约束链；不是实物测频校准。当前只报按厂家标称27MHz换算结果，不称EEMBC认证，也不把双种子未完成阶段包装为正式全验收。

## H33失败及停止边界

官方报错：JtagServer-0312: DONE pin did not go high；Configuration-0008: The command 'Program' execute fail。控制器184.734秒结束，未到400秒Program/480秒控制器限额。配置前STATUS081ffca0/DONE1/GOUTEN1/CRC-ID错误0/OT1；失败后未读回STATUS，不能将前值当后值。当前FPGA驻留/输出状态未知，不能称仍在运行已成功的性能镜像。0字节是配置失败背景下的采集结果，不是验证算法CRC失败。

客户端/服务器因官方错误由所属Job强制清理，原生1；串口正常停止关闭/原生0，所有Job为空。Python最外层捕获异常后进程0不等成功：以RESULT=FAILED及官方原文判定，保留全部原件。H30/H32均原生0、Job空、无强制清理。

原定2次Program额度已消费，不追加第三次，不启动H34/H35旧按键窗口。下一建议只做一次有界ID/STATUS读取，0 Program/0寄存器写/0reset/0Flash，先定位配置状态，再决定是否另批单次有证据的恢复；此建议未实施、非既成授权。无新断电回执；实际温度/通电起点未知，不将OT1视为已解释，按D237记录且不独立停止，未修改芯片保护/供电/SCBV。

## 可复查入口和命令

总目录work/pds-jtag/2026-11-01-coremark256-measurement-m1：PLAN、STAGES、RESULTS、CLOCK_BASIS、POST_SOURCE_HASH_CHECK、CHECKER_SELFTEST及EVIDENCE_SHA256。有限基线work/hardware-baselines/2026-11-01-coremark256-performance-v1/BASELINE.json。

原始命令由各H30/H33的RESULT.commands、run.py和configuration_tcl.log保存，明确500kHz、program3。原执行入口为Python绝对路径（C:/Users/tamii/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe）-X utf8 -B <对应H阶段/run.py> --run；所有ATTEMPT已消费，不能盲目重跑。H31/H32仅capture.ps1/COM22 115200 8N1、无流控、0串口写；H34/H35的执行前窗口调整留CAPTURE_WINDOW_REVISION，但本次均未执行。

新离线检查原命令：同一Python -X utf8 -B work/pds-jtag/2026-11-01-coremark256-measurement-m1/check_measurement.py performance256 <H30或H32/uart-raw.bin绝对路径>；MEASUREMENT_CHECK独占创建，不覆盖重跑。各H阶段保留SERIAL_RESULT、RESULT、uart-raw.bin、MEASUREMENT_CHECK（仅实际通过的H30/H32有）。底层旧parser中的hardware_valid=false为历史候选类型，未篡改为true；本轮实际物理证据在独立外层检查中明确记录。

尚未验证：validation256实际运行及重复、同版本ILA、独立实物测频、完整ISA/长程序所有退休副作用、热电安全。既有无退休PC、WB/STORE分流、固定存储/初态、IO/CDC等限制保留。原8迭代和短仿真结论不倒改；长256 RTL仿真仍NOT_RUN。本轮不提交推送D245待审文档。
