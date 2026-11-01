# 固定CPU/CoreMark8真实片上CRC与64位计时复验

日期：2026-11-01（北京时间）。本轮由用户恢复暂停并批准当前阶段必要权限，报告供电、下载器及UART已连接；真实温度和通电起点未知。没有重新构建CPU/程序，没有修改RTL、冻结预期、SCBV、供电或保护，没有Flash操作。D245文档不提交推送保持。

## 已实际完成

1. H20在沙箱中因CIM不可访问而结束，串口未打开，0服务器/Program。独立H20-r1在普通用户宿主环境成功打开COM22，再核PG2L100H/公开ID00602899并完成**一次**固定R4易失性下载；168.718秒。位流SHA256：139DD52013B6C3A9ADA50B92D72F1479ED488DE2C70D024284A27AEC573EFC03。
2. 配置前STATUS=00180c80；两次后STATUS=081efca0，DONE/DONE_I=1，CRC/ID/timeout/rbcrc/aut错误均0，GOUTEN=0，over_temp=1照录，不作为独立软件停止或温度安全证明。H20-r1客户端/服务器/串口均原生退出0，无强制清理，Job均空。
3. H20-r1串口在Program前打开，115200/8N1、DTR/RTS关闭、0发送，实际监听194.195秒，0字节，错误事件队列空。**外部UART完整输出未通过**，不是CRC计算失败。
4. H21不再Program，载入同一FIC，分5次用户KEY0复跑，分别按地址触发。五个新WDF均1024点/140通道，原生dbg_run及自动保存成功；使用此前已与PDS原生VCD全位交叉核对的限定读取器解析。全部触发值均逐位原生回读Bin一致。

| 新采样 | 目标写地址 | 实测 | 冻结期望 | 结果 |
|---|---|---|---|---|
| seedcrc | 0x109b1–0x109b4 | e9f5 | e9f5 | MATCH |
| crclist | 0x109cb–0x109ce | e714 | e714 | MATCH |
| crcmatrix | 0x109e5–0x109e8 | 1fd7 | 1fd7 | MATCH |
| crcstate | 0x109ff–0x10a02 | 8e3a | 8e3a | MATCH |
| elapsed_ticks64 | 0x10810/0x10814 | 0x000000000100cc0c = 16829452 | 16829452 | MATCH |

最终CRC ccd1为此前H18真实片上证据，本轮未重复采样，不混称五CRC在同一新运行内验证。各CRC窗口在样本512/546/580/614出现四个依次非零字符写；相邻零终止符写完整保留，各目标恰一次非零，未通过去重隐藏重复。所有新窗口write_error样本计数0。原始有序写、完整CSV、WDF SHA在每个*-result.json及ALL_FIELDS_RESULT.json。

计时窗口：样本512在0x10810写16829452，样本516在0x10814写0；真实ID级PC分别0x3308/0x3310，与固定ELF在0x3304/0x330c的SW一致。两次写均rst1/phase0/wren1。高低字各一次、保留顺序；不将ID级PC称退休PC。

## 测量方法与限制

CRC谓词只限实际地址/wren/rst/阶段和ASCII共有bit5以排除先前零终止符，未筛期望CRC。计时谓词对wdata全不关心；实施前发现旧H19只筛地址会先命中.bss清零，因此在H21冻结细化为ID级PC处于stop_time所在0x3xxx代码区，排除启动清零；旧计划保存在CASE_PLAN-v1-before-timer-refinement.json，期望未改变。实际SW来自固定ELF反汇编，未运行或修改程序。

这些是**真实FPGA程序打印缓冲及计时写事务观察**，不是宿主仿真/旧波形重放。5个窗口来自独立复跑，不是完整连续轨迹；没有真实退休PC、全部WB/STORE统一提交或错误路径全程证明。timer64写值匹配有限参考；实际27MHz没有独立测频，不能由导出时间单位证明。8迭代仍不足10秒，不是正式CoreMark成绩，不能用宿主墙钟替代目标时间或删掉原固件的短测错误标签。

H21额外COM采集从所有KEY0前打开，raw文件0字节，但复制的旧接收脚本缺少STOP_SERIAL循环检查，收尾被Job强制终止，未生成SERIAL_RESULT，不能称正常串口收尾/错误队列已核。GUI及服务器原生0/无强制关闭，5个波形均在关闭前完整保存，不受串口清理缺陷影响。SERIAL_CLEANUP_REVIEW.json保留原缺陷，下一接收器先做普通宿主有界取消自检；不为此重跑已完成CPU采样。

## 外部输出的专项检查

- 回查实际构建的board_top.sv、soc_top.sv、soc_data_adapter.sv、local_regif_txgpio_m1.v：TX寄存器路由、全字写、CLKS_PER_BIT=234、GPIO/TX连接仍存在。综合board_top_syn.vm中nt_uart_tx确接GTP_OUTBUF；布局布线prr.db把uart_tx放在C24/BANKL3/LVCMOS33/3.3，驱动8/SLOW/约束YES。这是工具文件证据，不是管脚电压测量。
- 已保存硬件手册43页为CP2102/USB-UART说明（图示CP端TX/RX箭头标签存在可疑表达，不仅凭该示意推断线路），板级详细网络与实际电平仍需进一步闭环。没有改接线或跳线。
- H22新只读得到STATUS081efca0、RDDEBUGR=00000001、指令寄存器=00000071；主机将debug mode3误送STATUS解析而停止，原始日志及失败保留。修正为精确命令分类，仅补剩余mode4；原生明确当前器件不支持此操作，未反复重试。
- H23按官方Fabric Configuration用户手册V1.0实际87页视觉核的mode5只读边界输出尝试，原生参数检查先要求-value，补唯一结果文件路径后又要求十六进制。两次均未取得引脚数据；此版本具体mode5参数语义尚未确认，不猜测HEX来尝试，不宣称边界扫描或实测IO通过。厂内BSDL FBG676头部自身标为preliminary/not verified on silicon，仅作线索，不能当已证实引脚电平。
- 最后各次有效STATUS仍081efca0/GOUTEN0，内部CPU可运行与外部输出未正常使能并存。GOUTEN0按已核Logos2手册为用户IO高阻；**为什么仍为0尚未确定**，不把它改写成UART核心错误、芯片损坏或过温已经证明/排除。旧H6通用寄存器读0矛盾及H7 BYPASS无LED恢复保留，不原样重复这些路径。

## 当前状态与下一工作

新片上四CRC/64位计时取证已完成；整个CPU外部输出阶段尚未全部验收。当前唯一主问题收敛为外部输出使能/管脚路径，需要可信的pad/OE观察或有证据的工具适配，不能靠再刷同位流、未知控制位写入或改保护凑通。优先确认原生只读接口的确切参数/支持范围或准备不改CPU功能的针对性TX/OE调试方案；不自动声称新候选获验收。已有CRC窗口不重复，正式长测/优化仍未由本次小样本取代。

全部已启动工具结束，Job均空。开发板当前仍供电只是用户恢复时报告，没有收到新的断电回执；本轮不称已断电、不承诺后台监测/代切电。原始记录：work/pds-jtag/2026-11-01-cpu-resume-h20[-r1]、2026-11-01-cpu-crc-fields-h21、2026-11-01-cpu-output-status-h22[-r1]、2026-11-01-cpu-output-boundary-h23[-r1]。未提交推送。
