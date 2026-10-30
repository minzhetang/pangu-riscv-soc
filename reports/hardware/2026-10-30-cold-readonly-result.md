# 冷启动只读诊断结果

2026-10-30，F186/D205；D204执行收尾，无重新构建、下载位流或Flash操作。

## 实际证据

入口`work/pds-jtag/2026-10-30-cold-readonly-m0/read_status.py --run`，PDS2022.2-SP6.4官方工具，获批普通用户沙箱外执行。原会话同目录`RESULT.json`、单次执行`ATTEMPT.json`、身份`OFFLINE_CHECK-v3.json`、实体门控`PHYSICAL_GATE.json`。

- index0、TCK1MHz；一次扫描PG2L100H，公开ID00602899。未独立验证封装/速度等级或当前驱动版本。
- 一次STATUSR **0x00180c80**；官方hex、32位binary、逐位输出一致。over_temp27=0，done12=0，done_i13=0；timeout/rbcrc_err/aut_err/crc_err/id_err均0，init_n/init_complete均1。
- set_tcl_break → connect → set_cable_property → scan_chain → mode0公开ID → mode3状态 → disconnect，七条都有官方successfully输出；没有assign/program/reset/verify/readback/Flash命令。
- 首命令距控制器起点0.328秒；状态请求8.500秒，断连请求10.032秒。客户端和本轮服务器rc0、exited=true。控制器rc0结合实际输出证明只读流程完成，不能单靠rc验收。
- 剩余预算不足主动放弃第二读；结果ONE_FLAG0_SAMPLE_TIME_BUDGET_NOT_SAFETY_CLEARANCE。只有一个样本，不能声称两次稳定。

## 时间与实体局限

旧POWER-INSTRUCTION未执行，用户明确12V未接，CORRECTION保留作废原因；r1才是本次实际指令。r1指令前保守时间界至ATTEMPT **39.303秒**，含消息和工具审批延迟，不等实际通电时长。脚本按剩余预算提前结束。用户随后先报已断12V、再报USB已断；未独立测电或取得实际断电时间戳，不能把60秒操作目标写成实测满足。

## 历史对比与解释

`reports/hardware/2026-10-14-led-volatile-result.json`：LED配置后081efca0、flag1、DONE1；本次冷启动00180c80、flag0、DONE0。

已证明当前接线/官方工具可重新JTAG通信，且本次标志未置位。未证明实际温度、旧1的原因、下载后状态或长期运行安全。配置状态与观察时间不同，不能归因为锁存、误报或真实过热；DONE0只说明没有配置完成证据，不证明Flash空白/完全无活动。本轮未改变SCBV/供电/温控，CPU实机、正式CoreMark、ILA仍未验收。

## 结束与下一项

用户已顺序报告断12V/USB；D204一次启动/扫描额度用完，硬件恢复停止，不自动下载。下一仅只读收敛配置前后对照的最小诊断与预算：历史cfg_program报告168.5秒，不能将完整下载塞入本次60秒窗口；新硬件范围必须另批。不能因本次0直接放行。
