# 已验SM2基础系统

performance与validation分别保存同CPU/SoC、不同种子固定256次的完整实现源码、三类约束、flow.tcl、软件启动/链接/端口及ELF/bin。upstream六算法文件及许可已补入两套软件目录，均与原上游SHA相同。

- 顶层：pds/source/board_top.sv；SoC：soc_top.sv；流水线：cpu.v；复位：board_reset_sync.sv；存储：memory_model.sv与init_tables.svh；Timer：cycle_counter64.sv；外设：local_regif_txgpio_m1.v、uart_tx.v、gpio_core.v。
- CPU五级，EX/MEM优先前推、WB旁路、真实源load-use、控制冲刷与定义EEI。生产不提供完整特权CSR/OS环境；异常式停止与高阶trap不是同一机制。
- 同一个27MHz时钟下固定两相使能：采样沿读写存储，推进沿消费响应；STORE只在采样资格下写一次。32KiB程序ROM和32KiB数据RAM，初始化与内嵌ROM常量必须成套匹配。
- 软件：firmware/start.S、link.ld、board_qa.c、mul_sm2.S；port/core_portme.*；upstream算法不改。build_identity.h保留实际编译参数与计时频率。软件重编不会自动更新RTL内ROM。

原完整编译命令在software/build-evidence/COMPILE_RESULT.json，准确过程在下文总包REPRODUCIBILITY。PDS flow为相对路径，工具自备。configuration中的sbit/SVF本次不随代码包，原SHA与配置史仍在历史清单；这不缺源码，不是让人执行未核下载文件。需要配置必须重新按明确权限/现场条件及完整身份门处理，不能拿旧ATTEMPT重用。

既有实机双种子五CRC/完整UART/重复运行与计时见evidence/RESULTS及REPORT。性能周期下降7.855984%、同频吞吐增加8.525767%，二者分母不同；+60B而非新增硬件乘法。DRM36实际14.5，原文字14是截断历史。UART断接后恢复不等唯一根因或长期可靠性已证。

本次只打包/静态绑定，未重编、重跑、重新实现或板测。旧O2片上数据请看另一个独立目录，不移植到本版。
