# A-DIRECT-NETLIST-EXPORT-M1 /1.3.0（待批）

2026-10-29。F177表明-project/-run会启动前置Compile，停止该路线。

只允许新独立目录、已有R4 pnR ADF同字节副本，一次普通PDS CLI -file运行180秒/阶段900秒，脚本仅：

```tcl
set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676
gen_netlist -input_db_file {同字节副本/board_top_pnr.adf} -func_sim_only -sdf_annotate FALSE -force_to_run
```

**本范围明确申请仅对gen_netlist允许-force_to_run**，改变此前对此选项的禁止；依据本机帮助“运行该动作而不检查状态”，不篡改完成状态，不用于硬件/位流动作。不允许其他-force、-project、-run或执行旧脚本，不重新实现；若任何上游动作启动，立即终止并如实报告。

先离线核监督器识别Executing与Process started两类日志，修正动态输出枚举竞争；不放松原件/输入SHA保护。单日志16MiB/输出128MiB/总256MiB/内存1GiB，0新增帮助/GUI/第二进程。失败即停，不补跑前置。

退出后核新网表、来源DB、阶段/命令/SHA，再只读解析D/CLK/net/驱动，优先136–139/34/38，再全140，未知不判PASS。不执行模型/仿真，不改RTL/TB/程序/INIT/约束/FIC/B接口。

0安装/管理员/许可或环境修改，0Debugger/服务器/设备枚举/JTAG/上电/下载/Flash，不改SCBV/供电/温控，over_temp STOP保持。导出或连接核查不豁免4Critical/CDC/实机证据。
