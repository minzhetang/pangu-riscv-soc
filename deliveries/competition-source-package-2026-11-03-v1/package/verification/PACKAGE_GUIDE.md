# 验证代码与证据

| 目录 | 内容与入口性质 |
|---|---|
| cpu-regression/project | 763例完整冻结输入/终态、两个模型、有序WB/STORE期望、14组TB与请求，及EEI对齐/复位源码与有限结果；run_regression763保留原R路径，需在新副本配置根与工具 |
| system-origin/project | 真实C启动、同步存储时序/字节写、SoC/Timer及独立参考源；保留代表性结果，不带全部旧DUT轨迹 |
| peripherals-frozen-v02 | 已接收UART TX/RX、GPIO、TX/GPIO包装与继承依赖；W06主线补验、计划/原日志/代表性VCD；大N234 RX波形省略，原日志/代码仍在 |
| offline-tool-v02 | B独立离线比较/差异诊断/压力与故障工具，不是在线ISA参考；原54项PASS_LOCAL与主线G1–G3失败分层 |
| offline-tool-mainline-review | A资源/期限/日志反例与复现入口、22P/3F审查结果；不把B工具直接作为生产通过门 |
| streaming/project | 主线分段采集、无损codec、独立比较/计时/UART与有界入口；本轮省略百万行大流，补齐代码级继承源 |
| streaming/historical-longrun | M6 C++/Python/TB/镜像源与失败诊断入口，仅历史，不得直接重启旧ATTEMPT |

全状态与每笔合法非x0 WB/STORE及其各自顺序都检查，不去重。没有统一真实退休PC；两类流不强行推成一个退休序列。部分历史stall/flush没有独立冻结期望（17/20项NOT_SPECIFIED），与历史计数一致是另一项检查，不能补写成独立预期。

模型、故障注入与负向输入也是代码成果。少数JSON文件故意无效，属于冻结拒绝测试，不应为让“所有JSON可解析”而修成合法输入。原包含全部历史大数据的SHA清单属于历史，不是本包完整性判据；以根MANIFEST/CHECK_STATIC为准。

本次只做材料审查和静态核验，不运行本目录任何项目程序。已有PASS、旧记录重放、工具测试和新DUT各自分开；SHA证明身份，不替代功能结论。
