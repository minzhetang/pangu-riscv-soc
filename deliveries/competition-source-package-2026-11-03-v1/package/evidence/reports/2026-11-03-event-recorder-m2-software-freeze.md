# 应用M2：慢速参数、真实RAM占用与可复现软件候选

日期2026-11-03；D312/F272。原D300已验CPU/SoC不改；本轮没有PDS、GUI、硬件服务器、JTAG、下载、串口硬件接收、电源或保护修改。沿用户已授权的软件应用范围推进。

## 阶段结论

1. 编译出AUDIT0的慢速事件版候选：2700000tick采样、128样本、WAIT20，按27MHz标称对应100ms/12.8秒/约2秒等待超时。ROM/bin1836B、链接.bss196B。
2. 同配置dense对照为2164B/1220B .bss，多出的1024B对应128×8B原始采样。共同预留8KB栈不包含在.bss数字中，也未独立量栈水位；FPGA仍是原32KB RAM接口，不能说物理RAM资源减少。
3. 新固件在原M1已编译平台完成8组快速32样本测试，每组两次复位：7类event场景及normal dense，完整GPIO/timer观测、事件顺序/时间/原因、UART引脚解码与main返回核对通过。移除了审核数组，没有用宿主生成结果。
4. 故意period32过载，两轮CPU均采到17样本后出现late1/fault3/frozen1；记录[index17,state0,reason3]并终止采样。预先标准是首次超1000tick预算、done<32、GPIO计数相符、唯一故障记录、无后续采样和完整UART，不是事后把17填成预期。
5. 新参数化TB普通环境-tnull展开rc0、VVP生成异常；经一次受控普通用户沙箱外编译实际rc0后，同一TB正常运行。原四种有界诊断及日志保留；没有据此认定所有旧工具异常根因已解决。
6. 同270万tick周期的**2样本见证**通过，采样输入1/1，在索引1记录状态1；窗口5400244目标tick。实际跑了CPU等待循环，没有强制timer或模拟主机结果。按TB时基实际54ms模拟时间，不冒称已经物理运行200ms；100ms是目标27MHz换算。
7. count128/wait20的normal128、wrap_fault128、timeout20三组缩短周期（12000tick）测试通过；包括20个等待样本在索引23触发超时、满窗口前5+故障+后2保持及后续显式拒绝。

完整“270万tick×128样本”的12.8秒配置仍是**编译候选/运行NOT_RUN**，没有板级应用验收。上述见证和缩短周期测试不能合称全时长通过，也不继承原CoreMark实机或ILA。

## 当前程序身份

工作入口：`work/application/2026-11-03-event-recorder-m2/README.md`。

|候选|ROM/bin|.bss|程序bin SHA-256|
|---|---:|---:|---|
|production0-r1，event|1836B|196B|CBB37E60674713CCFBB0E603BA774ECB82E2460FA7D2DD2707AF34D4175E3D30|
|production1-r1，dense|2164B|1220B|CE394C50FF735F55422DFD3BADC6843C130DE7004521F5AE3049EB9BE2DC591C|

每项ELF/bin/8192字ROMhex/map/BUILD.json均在build目录；活动源码firmware/app.c及start.S/link.ld。APP_DIFF为对M1的准确应用差异，14份基础RTL与M1逐文件同SHA。首次dense编译的声明作用域错误与源保存，修复仅发生本副本；旧M1/预期无变。

## 证据与命令

- FROZEN_PLAN：沿原7场景手工预期，加编译前冻结的slow witness参数；OVERLOAD_PLAN为过载条件；EXTENDED_PLAN为3个128样本预期。没有以DUT结果回填。
- FAST_RESULTS、OVERLOAD_RESULT、SLOW_WITNESS_RESULT、EXTENDED_RESULTS分别记录四类不同层级结果，不把模块/文件存在当运行。
- logs/*.json和runs/*/COMMAND.json有完整argv、cwd、rc、超时和墙钟；TOOL版本沿M1已核GCC15.2.0/Icarus13.0，无安装/PATH或系统环境修改。
- 仅一次沙箱外编译，EXTERNAL_COMPILE_RESULT有准确命令和rc0；NEXT_EXECUTION_SCOPE保留执行前状态，不作未来可重复授权。
- M2新TB实际运行使用external-diagnostic-1.vvp；fast旧平台用M1/app0.vvp，身份独立记录。两者不混淆，不把旧VVP当新编译。
- 进程局部IVERILOG_DUMPER=none关闭波形输出，实际保留GPIO/timer日志、RAM和串行引脚解码；没有新VCD，不拿旧图作新应用波形。新增证据为有界几十MB，避免M1约783MB级的重复全时钟记录。

## 真实使用边界

原板顶层把KEY1–4反相映到GPIO低四位；应用只用低三位，KEY4未使用。第一版合法输入累计0→1→3→7→0，对应依次累计保持KEY1、KEY1+2、KEY1+2+3，最后一起松开；不是旧GPIO QA的逐键按松顺序。这里只做静态映射与待验证方案，不指导当前实体操作。

8条上下文、2连续样本滤波、故障后2个变化事件冻结；若后续无变化则批次结束导出，不保证永远收足两条。无采集中UART打印，导出期停止监测，仍忙轮询；无RX命令、中断、外部传感器或工业认证。32位时间戳代表软件观察时刻；短脉冲/跨回绕/全相位最坏延迟未穷尽。调度预算超限主动冻结，不静默补采。

## 推荐下一项及真实门槛

应用软件已具备进入**独立PDS镜像绑定与实现审计**的依据。建议只复制D300恢复工程，绑定production0-r1事件程序，保留原CPU/SoC/引脚/27MHz/可靠性约束；核对ROM初始化、资源/时序、全部新警告和位流身份。此阶段不得自动下载或操作硬件，需用户另批PDS构建范围。实际板级输入、全时长批次及UART输出再另以准确范围授权，不复用旧配置额度。

高阶候选维持D311：原BTB模块有限通过，整核尚未新复验；本轮不顺便叠加高阶修复或认定其工具阻塞已关闭。提交临近，优先保护软件应用及原可信基础成果，有限高阶如实交付。
