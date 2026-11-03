# 复现方法与入口分级

本轮只做复制/静态核验和RAR归档，不执行下面的项目入口。复验请在新输出目录/包外工作副本进行，保留冻结输入和本包只读状态；不要为让新构建通过去改旧预期。安装、许可证、硬件等须由使用者依法依规准备，代码包不自动授权。

## 1 材料检查 无工具链

在解包package根用Python3：`python -B CHECK_STATIC.py --root .`。仅标准库、逐SHA、文件覆盖、路径/链接和静态身份；不运行任何项目脚本。结果不是构建/仿真或板级通过。

## 2 事件应用 已有便携入口

```text
python -B application/event-recorder/verification/recheck_reports.py --output <全新包外目录>
python -B application/event-recorder/build_software.py --gcc-dir <已有xPack工具bin> --output <另一个全新包外目录>
python -B application/event-recorder/build_software.py --gcc-dir <已有xPack工具bin> --output <另一个全新包外目录> --dense 1
```

第一条只逐笔重读既有板级字节，旧错误应被拒绝，不开串口；后两条真正编译event/dense并与1836B/2164B冻结bin逐字节核对，不自动写ROM。已有历史便携重建同bin证据随包；本轮没有重做。

RTL输入：simulation/tb.sv、memory_sim.sv、fpga/source中的cpu/alu/control/regfile/soc_data_adapter/soc_top/cycle_counter64/local_regif_txgpio_m1/uart_tx/gpio_core；用memory_sim替代memory_model，不混用两种同名module，不纳board_top/board_reset_sync。Icarus `-g2012 -s tb`，具体宏、ROM、FROZEN_PLAN/EXTENDED_PLAN/OVERLOAD_PLAN与TB公开plusargs须一并采用。原execute/frozen_tb_validation等位于historical-scripts，依赖旧M1编译平台，不能直接在本包运行；包内research-origin提供其源码/计划用于适配，不提供旧VVP。先核TB端口/参数，再在新副本配置入口，不能用宿主结果伪造CPU执行。

## 3 基础SM2 软件与FPGA

performance与validation均从其software目录作为工作目录。准确gcc参数和命令见各software/build-evidence/COMPILE_RESULT.json的jobs[0].argv；将首元素替换为本机已有GCC路径，保持其余参数及源文件顺序：纯RV32I/ILP32、O2、2000B、ITERATIONS=256、BOARD_QA_M2=1、PROJECT_MULSI3_SM2=1、对应PERFORMANCE_RUN/VALIDATION_RUN、-lgcc。上游算法文件已位于software/upstream，build_identity.h在对应build/<mode>256。必须在包外可写副本构建，比较bin/ELF段/初始化，不能覆盖本包冻结文件。若改变工具/flags，报告变化而非套用旧实机成绩。

PDS相对入口为各pds/flow.tcl，顶层board_top，Logos2/PG2L100H/-6/FBG676、27MHz、三约束。memory_model和init_tables中可能有两处ROM常量，必须同同一bin；本包已经静态核对应身份。流程包含生成配置，不是当前可执行授权，也不含下载/Flash；厂商IP由合法PDS取得。

## 4 独立高阶 真C便携复验

```text
python -X utf8 -B advanced/btb-mmode/project/REPRODUCE_C.py --iverilog-root <已有ucrt64根> --output <唯一不存在的包外目录>
```

既有入口复制冻结M4源/预期，设置输出副本的Icarus路径，编译并执行8条配置运行，检查全态、有序WB/STORE和周期。它复现真C闭环，不是CoreMark或硬件。基础CPU不因此被替换。普通Windows工具所需`-B`及VPI路径由入口配置，不改变PATH。

## 5 M5 CoreMark及三配置离线实现

M5在advanced/btb-mmode/project/work/advanced/2026-11-03-coremark-strict-m5：build.py、reference.py、tb.sv/tb-timed.sv/tb-timed32.sv、run.py/run-timed.py/run-timed32.py、fault计划和程序已完整提供。源与8模块/PDS一致。推荐32项走tb-timed32及run-timed32，不能拿默认64项脚本结果贴32项标签。

execute.py按H.parents[2]确定候选project根并从其tools/iverilog-13.0-msys2-ucrt64/ucrt64取工具；OwnedJob源码已在该project的原相对位置。build.py指向同根tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin。包内没有这些工具；可在包外副本配置I/G指向已有合法安装，记录准确diff；不要改CPU、输入、预期、计时方程。原日志/ATTEMPT/TIMED32_PLAN是一次性门，复验只在全新执行目录准备同一源、镜像与冻结规则，不删原门硬跑。完整CoreMark WB/STORE长流由新执行和独立参考在新目录产生，本包只保留必要短输入和代表证据，不能在本包直接运行audit.py冒充全量重放。

真实时钟规则：第N拍计数N−1，一级同步口返回low=N−2；每次12读按独立指令地址顺序核验。检查CRC/错误/返回/签名/32RF/测试内存/每笔WB与STORE/UART及计时，计算窗与初始化/打印分开。ITERATIONS=1不足10秒；M6未完成前缀不补足资格。

离线PDS在同候选project/work/fpga/...offline-m1下pred0/pred1/pred32的flow.tcl。顶层board_top_hl4，三工程同program/performance1、同27MHz和约束，仅预测参数不同。build-pred*.py是历史一次性入口且含原工具位置，复验应新目录配置工具；只需合法PDS和随包相对flow/源，无厂商数据库随包。此处没有生成位流/实机/ILA证据。

## 6 Cache与定点AI

M0根有cache.sv/backend.sv/cache_tb.sv、AI RTL/TB/reference_ai及vectors；M1/M2有各自baseline/candidate/m1.sv、backend、TB、冻结PLAN/EXPECTED/参考。M2的experiment.py准确列出3种RTL与宏：M0 baseline.sv无策略宏，M1 m1.sv -DADMISSION_M1，M2 candidate.sv -DADMISSION_M1 -DTWO_GHOST；顶层cache_tb，-g2012。输入+RO/+BYPASS/+DELAY/+VEC及协议+MODE必须按原EXPECTED/PLAN，不只挑最好一组。

原run.py通过祖先目录查找tools/...UCRT64，并拒绝覆盖已有logs；原check_delivery/audit还核其历史VVP/清单。本包省略编译物且只做元数据匿名，不应直接执行原全历史audit。复验用新目录复制源码/冻结向量/参考，配置已有Icarus；保留输入，重新生成输出并逐数据与统计比，不修改预期。AI同样分开配置、计算和输出背压，合成数据不等真实模型。

## 7 历史基础回归/系统/RX/工具

763回归入口、14组TB、完整cases、plan与两个模型均随包；原run_regression763中的R和编译请求为旧绝对路径。包外新副本先把根/工具及每个请求文件映射到本包对应project位置，当前CPU源在quality/.../source，不能把10/21旧source替代11/01源；仅配置路径，不改冻结预期。同步存储与新EEI另按其TB/PLAN运行，不称763同步全覆盖。

RX/包装冻结依赖完整提供（除明确省略的大波形），原runner含B工作区布局/已执行日志，按SOURCE_INDEX及DEPENDENCIES映射到新目录；账本header已补同字节到tb目录。GPIO/TX已有系统接入，RX仍独立。B离线工具入口为RUN.py --case-file ... --input-root ... --out <新目录>，其G1/G2/G3未闭，只作独立工具研究/故障复现，不用其结果取代主线CPU判定。

流式和片上分析脚本保留原数据位置，属于按需适配的历史入口；外部数据及M6不自动运行。全部适配须留下入口diff、实际命令和新结果，不能把本轮静态材料检查写成复现成功。
