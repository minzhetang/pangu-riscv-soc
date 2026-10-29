# A-PROJECT-CONTEXT-EXPORT-M1 /1.2.0

2026-10-29，推荐待批。F176静态镜像准备完成，不等原生载入/导出通过。

## 精确范围

- 在新独立执行目录从F176已核镜像复制完整上下文（copy2/逐SHA与mtime核对），不改原件或已核镜像。保留FIC原件路径作为已核只读依赖，保护其原预综合ADF；不重新插核。
- 仅在新执行副本flow.pds的cmd_gen_netlist任务添加func_sim_only ON、sdf_annotate FALSE两个导出选项。保留所有_gci_state、输入/输出引用、时间记录及其他选项；提交前准确diff，只允许这两个选项，绝不把状态0改2或伪造时间。
- 一次普通权限进程，cwd为执行副本build：

  `D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe -project <执行副本/build/flow.pds> -run gen_netlist`

- 本范围**显式仅允许以上-run gen_netlist**，取代此前范围内对-run的一概禁止；不允许其他-run、-force_to_run、Rerun All、source impl.tcl/flow.tcl或新-file实现脚本。没有第二次进程或GUI兜底，参数不兼容即停止。
- 进程<=180秒/阶段<=900秒，内存1GiB、单日志16MiB、导出128MiB、总磁盘256MiB；新原生帮助0/GUI0。监督执行日志，若实际进入任何上游实现或位流动作，立即停止并如实记录已发生阶段，不能掩盖为0。前置检查拒绝则保留错误，不改状态/补跑。
- 退出后核新网表mtime/大小/SHA、命令/阶段及所有原件与既有镜像不变。主机只读解析D/CLK→net→驱动，优先136–139/34/38再全140；未知/常量/多驱动如实列出，不执行模型/仿真。导出和连接核验分层。

## 不授权

不主动运行compile/synthesize/dev_map/pnr/report_timing/gen_bit_stream，不修改任何功能RTL/TB、程序、INIT、引脚/时钟/FDC、FIC、复位配置或B接口。除上述新副本导出选项外不改变设计设置，不安装/管理员/许可证/系统环境修改。

0 GCC/Icarus/DUT/后仿、Debugger/服务器/设备枚举/JTAG/上电/下载/Flash。不改SCBV、供电、跳线或温控，over_temp STOP保持。网表连接通过也不能豁免4Critical、CDC或硬件准入。

完成或新错误即停；若需要其他原生入口、重建或新实施，再列明真实范围，不无限追加尝试。
