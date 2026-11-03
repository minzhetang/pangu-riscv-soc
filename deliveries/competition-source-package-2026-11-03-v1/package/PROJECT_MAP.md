# 工程总览与成果覆盖

作品围绕“小型设备可编程事件记录与故障回溯”构建：真正编译的裸机C运行在自研五级流水线CPU上，访问同步存储、64位Timer、UART发送与GPIO。采集状态变化、检查规则、保存故障前后上下文，采集完成后导出。板载按键用于模拟设备输入，不宣称工业现场部署。

```text
裸机C / CoreMark / 事件规则
          │ 启动、链接、ELF/bin、ROM初始化
          ▼
  IF → ID → EX → MEM → WB
  前推 / load-use / 控制冲刷 / 定义EEI
          │ 同一时钟、固定两相同步存储适配
          ├── 32KiB程序ROM与32KiB数据RAM
          ├── 64位物理拍Timer
          └── TX/GPIO包装 → UART与按键/LED

分立研究：Cache M0/M1/M2；BTB及所选M-mode；定点FC算子
```

## 全项目覆盖表

| 成果 | 随包位置与内容 | 已有证据层次与价值 |
|---|---|---|
| 基础CPU/SoC | baseline/sm2：performance/validation两套完整pds/source、约束、flow、固件 | SM2有限板级双种子256次；同CPU性能周期减少7.856%，+60B |
| 冒险/精确终止 | verification/cpu-regression：763例输入、预期、TB、两个模型、EEI对齐与旧源 | 默认组合模式历史763例；同步模式另有真实C/依赖/副作用证据，不谎称763同步全跑 |
| 存储与C启动 | verification/system-origin；基础与应用firmware | 一拍DRM读延迟、两相采样/推进、单次STORE、字节写、data/BSS/sp/gp |
| UART TX/GPIO/Timer | 基础及应用source、verification/peripherals-frozen-v02 | TX/GPIO已系统接入，Timer64计计算；GPIO真实输入、八灯/复位有现场证据 |
| UART RX | verification/peripherals-frozen-v02完整源码/TB/继承header/计划/日志 | 独立有限模块接收；没有RX SoC包装/双向命令或UART RX实机验收 |
| 真实片上分析 | baseline/o2-onchip：pre/build工程、FIC、dprj、4WDF/CSV/图及分析器 | 旧O2固定256程序，140通道×1024点四个不同窗口，分析load-use/冲刷及局部EX有效槽 |
| 设备事件记录应用 | application/event-recorder完整v2源码、软件构建/检查、TB与板级账本 | 正常/顺序错/超时三场景；采集期间不阻塞打印，故障后冻结并显式记录拒绝/覆盖 |
| 原始采样对照 | 同一app.c的DENSE参数、两个冻结bin；research-origin与evidence/application-m1 | 同口径正常输出1216→256字符、记录载荷384→128B，处理段3002→2722tick；不是全RAM/CPU占用下降 |
| Cache与准入演进 | advanced/cache-ai根M0、cache-m1-admission、cache-m2-two-ghost | 完整RTL、后端、TB、独立字节/替换参考；M2两行交替534→282拍，stream357拍；退化同时保留 |
| 动态预测/所选M-mode | advanced/btb-mmode/project/work/advanced各阶段 | 主线M1–M3最小修复，M4真C及M5严格CoreMark短测；旧源对照与错误副作用检查 |
| 高阶离线实现 | advanced/btb-mmode/project/work/fpga/.../pred0,pred1,pred32 | 同performance1镜像/27MHz条件，32项11299LUT/5088FF/16DRM36，STA估33.9006MHz，非板上Fmax |
| 定点AI | advanced/cache-ai：FC RTL、AI TB/参考/合成张量/协议负向 | 16×8/128MAC、40bit累加、舍入/饱和；136/148拍；不是实际模型识别率 |
| 流式验证 | verification/streaming：采集TB、流codec/参考/守卫/C++检查源、有限结果 | 无损分段和逐笔副作用检查；历史长跑守卫失败源码/诊断也保留，不伪称≥10秒候选完成 |
| 独立离线工具 | verification/offline-tool-v02与mainline-review | B工具及完整原计划/负向；A复现22P/3F与G1–G3限制，未用于生产通过门 |
| 镜像身份与实现结果 | evidence/STATIC_IDENTITY_BINDINGS、各工程程序和报告 | 本轮8处ROM/程序静态绑定、12组核心SHA核对；无新运行 |

## 不同方向如何相互支持

基础系统提供真实执行平台；片上窗口解释控制气泡和软乘开销，指导SM2局部软件优化；事件程序把CPU、时间、存储和外设组合为可演示用途。高阶分立实验研究新的性能机制，允许在不破坏基础版本的前提下形成收益、资源代价及反例分析。代码包保留的是这些不同层次的实际成果，没有将独立Cache/AI与BTB拼成一颗“最新板级核”。

基础与应用完整RTL/固件/初始化已随包。PDS专有原语、工具和许可证由复验者合法取得；相关仿真可使用随包memory_sim或候选TB数组模型，不能把它们当厂商物理模型。源程序不是以位流/截图替代。
