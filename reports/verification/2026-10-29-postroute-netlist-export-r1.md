# 后布局文字导出R1：前置状态检查拒绝，未导出

2026-10-29，用户批准1.1.0（SHA DB2B53DF7EBFF0E8531C705281FC5A811A6603F1CA514396824E20EBAB5F40A3）；D186/F175/D187。

实际唯一PDS2022.2-SP6.4进程1.109秒，原生rc1、监督器无超时/资源错误；执行已核参数的set_arch和gen_netlist -input_db_file <pnr.adf副本> -func_sim_only -sdf_annotate FALSE。原生拒绝：

> E: Flow-0044: Place & Route hasn't been run, it's not allowed to run Generate Netlist..

没有导出网表，没有补跑前置，没有-force_to_run/-run或追加进程。260保护条目与同字节pnr.adf副本后验SHA相同；输出网表列表为空，实际生成sim.v零、连接验收仍0/140。0compile/synthesize/dev_map/pnr/report_timing/gen_bit_stream、新DUT、GUI、硬件。许可实际提示5天；不记录授权路径或内容。

## 静态诊断的新证据

旧R4 `build/flow.pds`与本次新`export.pds`顶层都写_status initial，因此不能再仅看顶层状态。准确差异位于tsk_pnr/cmd_pnr：旧工程_gci_state=2，并有place_route/board_top_pnr.adf及真实生成时间的_db_output；新工程_gci_state=0。原生错误与此相符，**工程推断**是新建上下文未承接布局任务状态，而非指定DB即可绕过流程检查。没有独立测试证明只复制.pds必然足够，也不推断DB损坏。

官方安装版PDS用户手册V1.5 §5.3实际166页说明-file默认按脚本名创建工程，-project用于打开已有工程，-run表示运行到某步骤。此前只查gen_netlist参数，遗漏了工程上下文，是A预检不足。不能将“参数存在”写成“独立导出已验证”；F174记录的参数事实保留，其可直接完成导出的建议被本次失败证据收窄。

## 下一步与边界

先**只读核验完整已完成工程的元数据、关联文件、路径和实际任务输出**，判断能否在新副本保留真实上下文。不得手工把_gci_state从0改成2、伪造时间戳或强制绕过前置。不得直接-project/-run触发可能的前置重跑。

本轮唯一CLI额度已用完；不马上再派一个猜测命令。离线准备不需要用户操作；可靠载入/单独导出方案尚未核清时，不生成已批准实施结论或承诺下一次成功。需要新原生进程/GUI/实现时再明确范围。4Critical/CDC/真实取证与over_temp STOP保持。

证据`work/analysis/2026-10-29-postroute-netlist-export-r1/`：export.tcl、APPROVAL、COPY_RECEIPT、logs/export-once/process.json与本地原日志、HOST_ERROR、POSTFLIGHT、SUMMARY、DIAGNOSTIC。原错误不覆盖，不把rc1当CPU功能失败；无新网表可供连接解析。
