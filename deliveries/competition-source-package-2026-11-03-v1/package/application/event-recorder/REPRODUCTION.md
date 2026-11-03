# 复现入口与依赖

本目录先以STATUS.json/START_HERE为准，SHA只证明材料身份，不代表执行通过。没有工具、许可证、专有仿真模型、安装包、凭据或机器ID。

1. 离线原始报告复查：在有Python3的普通目录运行
   `python -B verification/recheck_reports.py --output <全新结果目录>`。
   解析全部逐笔原始E行及header/END，不拿摘要哈希代替比较；旧预期FAIL仍应被拒绝。此入口不打开串口或运行DUT。结果明确new_DUT_runs=0。
2. 软件重建：已有合法xPack RISC-V GCC15.2.0-1，在包目录运行
   `python -B build_software.py --gcc-dir <工具bin目录> --output <全新输出目录>`。
   默认固定生产事件程序，可加`--dense 1`生成相同配置原始采样对照。每个编译进程60秒上限，保留命令/原生rc/日志；新bin必须与随包冻结bin逐字节一致才接收，不自动更新FPGA ROM。本轮已用此便携入口各重建一次event/dense，均与冻结bin逐字节一致（1836B/2164B）；证据见evidence/reproduction。该结果只证明软件可重建，不是新DUT或FPGA验证。
3. RTL复验资料：simulation/含M2参数化TB、无厂商模型的memory_sim、冻结输入和预期；fpga/source为实际板级原件。仿真要用memory_sim替换memory_model，并排除board_top/board_reset_sync；TEST顶层tb，Icarus13.0 `-g2012 -s tb`。TB通过真实CPU执行程序、同步GPIO、timer读、UART串行解码、RAM、返回与错误副作用检查。历史脚本在historical-scripts，仅供准确运行方法追溯，带旧A工作区依赖，不能在本包直接执行或宣称开箱可跑。尤其frozen_tb_validation依赖旧M1已编译平台，execute的source目录/工具路径需配置；包不含旧VVP，当前也不拿它伪装新编译。
4. FPGA重建：fpga/flow.tcl为已执行的相对源码入口，使用合法PDS2022.2-SP6.4 build146967、PG2L100H-6 FBG676。它会综合/布局布线/生成配置文件，**不是本包默认动作**；需要独立确认执行范围、工具许可与新输出目录。源码ROM绑定当前event1836B，软件另行重建不会自动换ROM_BITS。不要拿dense程序bin与event位流混用。原High Voltage属性作为已有工程配置保留，不是修改板上SCBV/供电的指令。
5. images/为已核固定event sbit及官方完整CRAM SVF，完整命令含ID/DONE校验；不是Flash文件，不是安装程序。下载需要当前授权/现场条件和有界控制器，**不在此包提供自动硬件入口**。本轮不复制已消费ATTEMPT假装可复用。

依赖均从本机已有合法工具取得，不自动下载/安装。Windows/Icarus此前有0xC0000005代码生成异常，普通用户受控外部一次编译成功不等全部环境问题根因已解；工具错误与DUT失败分开记录，不能运行不完整VVP。历史CRLF是Verilog Windows文本文件行为；实际UART物理字节为LF，离线报告检查按真实协议处理。
