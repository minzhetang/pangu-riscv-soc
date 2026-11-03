# 固定版本及证据归属

| 版本ID | 主要位置 | 状态 | 结果与不能混用的证据 |
|---|---|---|---|
| PROD-SM2-256 | baseline/sm2 | 已验有限板级、非调试运行基线 | 性能496232016tick/18.378963556s，验证522673286tick/19.358269852s；27MHz标称；1810LUT/1527FF/**14.5**DRM36等效；旧整数14被原报告纠正 |
| DBG-O2-256 | baseline/o2-onchip | 真实片上有限窗口，旧O2程序 | 4个不同WDF；并非SM2新采样；4调试时钟Critical、完整连接/CDC/IO签核限制保留 |
| APP-EVENT-v2 | application/event-recorder | 事件应用三场景板级有限通过 | M2固件/M3实现/M4–M5板级；1836B/.bss196B，1778LUT/1527FF/12.5DRM36 |
| BTB-M3/M4 | advanced/btb-mmode/project | 主线修复后的独立RTL/真C候选 | 八模块与M5同SHA，保留B原HL4来源与前源对照；不代替PROD |
| BTB-M5-32 | 同上work/advanced/...strict-m5 | 推荐独立32项同步参数候选；软件短测+离线实现 | 性能/验证计算周期1730128/1849336；比关预测减少17.7560%/18.2796%；未完成候选≥10s/板级/ILA |
| BTB-M5-off/64 | 同上及work/fpga/...offline-m1 | 同条件参数对照 | 同程序/编译/输入/存储时序；32项较64少611LUT/1888FF，多约0.6%周期 |
| CACHE-M0/M1/M2 | advanced/cache-ai | 三代独立原型有限仿真 | I/D各128B两路；M2修复M1交替访问退化，但M0在部分模式更快；未CPU集成/综合/板测 |
| AI-FC-M0 | advanced/cache-ai | 合成定点算子有限仿真 | 16×8，136/148拍；无真实模型/网络/识别率或CPU提速结论 |
| PERIPHERALS-v02 | verification/peripherals-frozen-v02 | F152/D151活动有限软件交付 | R1/R2/R3已关闭；W06引用主线补验；GPIO沿有限接收；RX仍独立 |
| OFFLINE-TOOL-v02 | verification/offline-tool-v02 | 有条件材料/比较功能接收 | PASS_LOCAL54不等A验收；A22P/3F，G1内存/G2日志/G3deadline未闭，未入生产 |
| M6-192-history | verification/streaming/historical-longrun | 已结束的失败长跑源码与诊断 | 两种子各16252928事件前缀匹配，宿主积压误计归档gzip退出；没有整例CRC/≥10s，不重启 |

各树的旧START_HERE/RESULT/AUDIT是当时阶段记录，可能写“等待/未开始/建议”。本表和项目总包说明用于解释当前完成层次；不改写旧文件使其看起来从未失败。原SHA清单只描述原交付，不替代本包MANIFEST。
