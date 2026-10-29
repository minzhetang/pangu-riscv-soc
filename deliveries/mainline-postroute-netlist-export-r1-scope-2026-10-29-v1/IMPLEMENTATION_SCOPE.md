# A-POSTROUTE-NETLIST-EXPORT-M0-R1 /1.1.0

2026-10-29，待批准。前轮唯一CLI已正常退出，只获得实际帮助，未导出；不复用已消耗进程次数。

允许新独立目录复制并核SHA已有R4 board_top_pnr.adf；一次普通权限pds_shell.exe -file export.tcl，最长180秒、阶段900秒，0GUI/帮助追加。仅设置已有目标元数据并执行一次已由本机帮助证实的命令：

```tcl
set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676
gen_netlist -input_db_file {独立目录/inputs/board_top_pnr.adf} -func_sim_only -sdf_annotate FALSE
```

不在Tcl内等待原生动作、不使用-run/-force_to_run；输入新副本、cwd新目录，不接触原工程。禁止compile/synthesize/dev_map/pnr/report_timing/gen_bit_stream、仿真/安装/GUI/硬件或设计修改。若独立输入DB仍不被接受，保留原始诊断并停止，不补跑前置。

退出后核新sim.v等网表、mtime/大小/SHA及真实阶段；解析采样D/CLK→网络→驱动，优先136–139/34/38，再全140；未知/常量/多驱动如实保留，不执行模型。日志16MiB/输出128MiB/总磁盘256MiB/内存1GiB，超限即停。原件及冻结输入前后核SHA。

输出与连接核验分层，不以rc0代替功能通过；4Critical/CDC/over_temp STOP仍保持，无Debugger/服务器/JTAG/上电/下载/Flash/SCBV/供电/温控变更。完成或新错误即停，不追加进程。
