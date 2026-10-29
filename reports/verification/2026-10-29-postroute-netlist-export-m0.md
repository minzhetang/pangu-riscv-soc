# 后布局网表导出M0：实际接口已核，尚未导出

2026-10-29，D184批准1.0.0（SHA E1A3CC9105AA708E12361710D9089A8F98E370AA0B947B4DC235CC90F10316A1），F174/D185。

实际仅1个PDS2022.2-SP6.4 build146967进程，79.922秒、rc0、无监督错误，实测峰值100077568B。执行`gen_netlist -help`成功，明确支持：`-input_db_file file string`（指定输入DB）、`-func_sim_only`、`-sdf_annotate TRUE/FALSE`，另列-of_flow/-force_to_run；本轮未使用强制或追跑选项。帮助已取得并保留，不能把rc0说成网表导出通过。

Tcl标准命令表先生成，但原生gen_netlist帮助在脚本等待结束后才输出；A的单进程“先查帮助再继续”控制方式未能动态衔接。显式STOP后正常退出，没有猜加载接口或追加原生进程。初次主机准备遗漏logs父目录，Popen前失败，HOST_ERROR与原POSTFLIGHT保留；补目录后真正的原生调用只有一次，NATIVE_EXIT及POSTFLIGHT_FINAL取代初版预执行快照，不静默改写旧证据。

260保护条目、4份DB副本后验SHA同。实际导出0、新sim.v零、连接核验仍0/140；0编译/综合/Map/PnR/重跑时序/位流/新DUT/GUI/硬件。原生许可提示剩余5天（仅此次提示，不推算精确到期、不保存授权内容）。原始stdout仅本地，帮助节单独脱敏保存，不打印/纳管授权路径。

现已具备不猜参数的精确下一命令：`gen_netlist -input_db_file <同字节pnr.adf副本> -func_sim_only -sdf_annotate FALSE`，目标元数据沿PG2L100H/-6/FBG676。推荐一个额外180秒CLI范围1.1.0；原1.0.0明确只有一个进程，不能把新导出当仍有次数。不得因本次适配不足扩成重新实现/新GUI。

入口`work/analysis/2026-10-29-postroute-netlist-export-m0/`：APPROVAL、COPY_RECEIPT、NATIVE_ATTEMPT、NATIVE_EXIT、HELP_SANITIZED.txt、SUMMARY、POSTFLIGHT_FINAL，原始logs与错误保留。完整可复现argv见NATIVE_EXIT；本轮未运行后仿或CPU，4Critical/CDC及over_temp STOP未闭。
