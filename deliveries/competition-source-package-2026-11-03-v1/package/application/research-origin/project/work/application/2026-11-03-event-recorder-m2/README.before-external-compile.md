# 事件记录应用M2：参数化与真实全局RAM定型

2026-11-03。状态分开：`FAST_RESULTS.json`为新固件快速32样本的有限CPU仿真通过；`OVERLOAD_RESULT.json`为真实调度过载反例通过；`build/production0-r1`和`production1-r1`为慢速128样本**编译候选，运行NOT_RUN**。不要用前两项替代后者。

## 已完成

- 不改CPU/SoC/外设RTL；source与M1逐文件相同。只新增独立应用、参数/声明修复、测试/验证入口。
- 将周期、批次、等待超时阈值和AUDIT/DENSE编译参数化。默认period2700000tick、count128、wait20；按27MHz标称是100ms采样/12.8s批次/状态1等待约2s。无时钟独立校准或板级实测。
- 正式事件版AUDIT=0/DENSE=0，无samples审核数组、无raw数组；链接map实测ROM/bin1836B、.bss196B。相同慢速配置dense版ROM/bin2164B、.bss1220B。差额1024B来自128×8B原始采样数组。196B/1220B不含共同预留8KB栈，更不代表FPGA物理32KB数据RAM资源被缩小。
- 保持8条事件、2样本过滤、顺序检测与两条故障后上下文；新增明确调度过载reason3，late=1、冻结、停止批次，不再在漏deadline后无限补采。
- 新固件以period12000/count32/wait6/AUDIT0在**已成功编译的M1 CPU/SoC/TB**实际运行：7种event场景加normal dense对照，8组各两次复位；外部GPIO load、timer观察、完整有序事件、原始RAM（dense）、UART接受与串行引脚解码、main返回0/EEI2和终态匹配。FROZEN_PLAN沿原人工预期，未根据新DUT回填。
- period32过载对照在实际CPU执行，两个复位均done_samples17、late1/fault3/frozen1，单事件[index17,state0,reason3]，且时间戳对应第一个越出1000tick预算的begin、无后续GPIO采样、UART完整账本。精确17为实测结果，不是预先冻结的数字；预先标准是GPIO次数等于done、done<32、原因/时间条件/停止与副作用全部满足。

## 工具问题与证据

新参数化TB在`-tnull`语法/展开rc0，但VVP生成0xC0000005。已保留首次、常量dump名、scope dump以及timer判断移到宿主的四种有界诊断；没有反复执行完全相同命令，没有删掉检查迁就通过，但根因尚未定位。当前M2 tb.sv不能称编译可用。

因此本轮8组新固件使用M1已编译app0.vvp；源码/编译平台身份见FROZEN_TB_IDENTITY.json，ROM运行时重新装入本轮ELF生成的program.hex，既不是重放旧UART，也不是旧固件代跑。此平台固定12000/32/两次复位，不能用于证明production2700000/128的实际运行。

进程级环境变量IVERILOG_DUMPER=none本轮实测无VCD生成，仅关闭波形记录，不改系统环境/模拟时间/CPU。仍保留完整GPIO/timer读取、RAM及UART原文、串行引脚解码。没有新波形，不拿M1旧波形冒本轮新采样。

首次dense C编译发现raw声明作用域错误（gcc原日志和app-before-dense-declaration-fix.c保留），已在本副本改为条件全局声明，新production0-r1/1-r1及fast0/1均编译成功。没有改原M1或任何预期。

## 如何使用与下一步

`firmware/app.c`为活动源码；启动/链接沿既有32KB ROM、32KB RAM，链接器预留8KB栈并检查不重叠；尚未测完整慢速批次或独立栈水位。`build/production0-r1/program.elf/bin/hex/map/BUILD.json`为事件版候选，不是位流，不自动下载。

KEY0将来沿现有板顶层作为复位，KEY1–3对应三位累计状态，KEY4不参与第一版；板卡映射仅已验RTL静态核对。正常状态0→1→3→7→0需要累计按住而非逐个独立按松。故障可由非法顺序或状态1超时模拟。这只是待板级验证流程，不是本轮让用户进行实体操作。

采集不打印；结束导出并停止。32位低tick/有界批次，时间为软件观察时刻；不能记录任意短脉冲、不能连续无限监测、无RX或中断。2样本过滤的慢速接受延迟和WAIT20完整行为仍需慢速运行验证。

最小下一门槛是对同一参数化TB做**一次普通用户沙箱外编译诊断**，不是管理员/安装或硬件；当前仅准备准确命令，未执行，见NEXT_EXECUTION_SCOPE.json。若仍异常，不盲试，继续已有冻结平台可用的软件工作；若编译成功，再用现有普通用户软件授权运行有界慢速见证，不冒充完整128样本验收。PDS/板级另批，不能复用D300旧额度。

复现：先读execute.py/frozen_tb_validation.py/overload_check.py。所有输出目录及日志拒绝覆盖；每次新执行使用唯一副本。完整命令逐项在logs/*.json和runs/*/COMMAND.json；M1冻结VVP依赖需要按FROZEN_TB_IDENTITY核SHA。工具用已有GCC15.2.0/Icarus13.0，不安装、不执行破解软件。
