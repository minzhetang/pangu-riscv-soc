# M6：当前32项BTB候选的双种子CoreMark仿真长测

本阶段只普通用户软件构建/RTL仿真。CPU八模块继承M5同SHA，生产D300/SM2、D320应用和历史结果不改；不做PDS、位流、服务器或硬件。

状态必须读各`runs/*/RESULT.json`、`MEASUREMENT.json`和`CAMPAIGN_*_EXIT.json`，不能从计划或文件存在推断长测完成。

## 冻结输入与独立性

- `plans/FROZEN-v2.json`冻结源码、程序、GCC参数、192迭代、两组种子、27MHz计时规则、CRC和判定；v1保留为检查器相对时序错误的历史。
- `HOST_CRC_ORACLE.json`：不改上游算法的本机C运行给出192次最终CRC：性能9BA8、验证9555；本机指针宽度单独适配。host_port的固定时间只满足宿主算法运行/打印，绝不是计时证据。实际DUT必须自己读时钟计数。
- `engine.hpp`独立顺序RV32I参考有自己的PC、寄存器、ROM/RAM。每笔合法WB/STORE分别有序比较，不能去重；参考不能使用DUT写回值驱动自己。有限32项队列只适配流水WB/STORE相对时序，不冒称真实退休流。
- `qualify.py`/`replay.exe`完整逐笔重放上一轮10份M5记录及全终态；这是旧观测重放，不是10次新DUT。
- 六项新实时VPI错误控制及双参数一次迭代资格运行，身份/结果与192次长测分开。

## 时间与完整事件证据

每上升沿mtime递增1，同步数据读口于第N拍使用的low值必须为N−2；12笔hi/lo/hi读取均校验。TB半周期18518518519fs，名义27MHz（离散时间舍入误差约2.6e-11相对量）。计算区为start_time到stop_time的真实mtime差，phase标记差另核4拍开销；初始化、格式化和UART输出均排除。192次运行只有实际mtime差>=270000000、全部CRC/端口状态/返回与有序副作用正确才能通过。

`tb-terminal.sv`仅将VCD注册移到结束前6拍，避免bulk仿真期间无效的波形回调开销。所有WB/STORE、计时读取和全程X/非法副作用检查保持；每笔原始观测仍保存为20B小端二进制事件并分段gzip，逐段解压SHA核同后才移除新生成的raw分段。`TRACE_INDEX.json`和全部`.bin.gz`可以逐笔恢复，不以hash代替检查。

## 预算和入口

单例6小时、总阶段18小时、最多同时两例；单进程1GiB、日志1MiB、每例原始流8GiB/压缩流4GiB、待压缩96MiB、9亿仿真拍。先完成32项双种子，再根据剩余预算对同两镜像关闭预测。`campaign.py on/off`各只一次ATTEMPT，不自动重试。普通入口需已有合法Python/Icarus/GCC/MinGW及原OwnedJob helper，不是任意电脑一键环境。

通过VPI插件在DUT运行中逐笔比对。此前失败的VPI链接、CRLF重放和WB/STORE相对时序检查器问题及旧代码/二进制保留，不当CPU缺陷；正式负向控制必须核对具体拒绝原因，不能任意失败就算通过。

本阶段>=10秒也只叫**仿真长测**。旧M5 PDS资源/频率对应旧一次迭代ROM，不能写成本轮192次镜像新PDS报告；完整S/U/PMP/Sv32、物理IO/CDC、实机/ILA及完整高阶2仍未验收。
