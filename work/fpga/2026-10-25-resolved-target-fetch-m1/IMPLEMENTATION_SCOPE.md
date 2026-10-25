# A-RESOLVED-TARGET-FETCH-M1：已批准实施

2026-10-25，D139。用户对D138具体两处RTL/新验证/收益后PDS范围明确“批准 继续推进！”。原提案`work/analysis/2026-10-25-control-flow-quality-m0/NEXT_IMPLEMENTATION_SCOPE.md`保留原件，本文件承接批准，不将旧未批状态当当前门槛。

独立source-before/models-before；仅cpu.v新增默认0参数RESOLVED_TARGET_FETCH，以及同步模式已决目标请求/valid-PC标签/匹配与IFID/PC选择；soc_top.sv仅绑定1。ALU/control/regfile、数据存储/前推/load-use/时钟边沿/软件/所有B源不改。

为保持未映射返回的旧路径，命中还要求返回inst非0；物理ROM未映射返回0，合法RV32I指令不会是全0。此保守回退也适用于映射内0字，不扩CPU地址接口或硬编码ROM容量；相应请求/回退须按独立程序映像核验。非对齐/无效/EEI/复位不发合格请求。新增valid和PC标签是取指标签，不是退休PC。

允许独立定向TB/时序检查适配，不改ISA参考语义/旧763预期。先冻结人工用例与参考结果，再编译运行；默认参数原763回归、新模式定向、原两O2 CoreMark真实程序及公开输出。每步首个设计失败停止保留诊断，不为跑通扩RTL/预期。固定编译清单完成后单独申请外部工具权限；新权限不复用旧许可。

两个CoreMark仍2K/各1迭代/N234/27MHz，原镜像逐SHA不变，各600万物理拍/360s。功能和可信计算收益成立后，才同F142器件/引脚/27MHz约束跑PDS compile/synthesis/map/pnr/timing代价，无位流。新CPU路径不能用旧STA保证。

任一正确性/重复副作用/X-Z/时序失败、无收益或须改数据存储/握手/全局结构即停候选保留F143/O2。B原任务/10月27日18北京时间窗口、over_temp STOP保持；不硬件/服务器/JTAG/Flash/供电SCBV温控/安装/改许可证环境，不承诺正式成绩/首创或理想14%收益。
