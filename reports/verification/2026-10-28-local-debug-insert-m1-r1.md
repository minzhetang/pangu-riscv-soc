# 本地观察核R1：部分配置已保存，未完成插核构建

日期2026-10-28；D173批准范围1.1.0，F168/D174。本报告明确记录部分结果和A自动化失误，不升级F160/F163验收。

| 层次 | 实际结果 |
|---|---|
| 工具/许可 | 两次普通用户Inserter启动；现有fabric_inserter checkout成功，均实际提示6天后失效。不是全部PDS特性checkout或精确到期时刻。 |
| 原设计载入 | 第二次GUI成功解析独立复制的旧ADF；原生输出“All signals have been recovered”，ins_list_nets实际列出4793个网络。 |
| 新配置 | GUI内官方Tcl设置单核、1024点、上升沿、无存储过滤/多窗口，保存partial.fic。**没有数据、时钟或复位连接，不能用于完整验收。** |
| 观察对象 | 140计划位中126个精确名称在实际网络清单匹配；14位仍未映射。名称匹配不等连接成功，未匹配也不等逻辑不存在。 |
| 补救候选 | 新13源副本仅cpu.v、soc_top.sv、board_top.sv共6处新增PAP_MARK_DEBUG注释；移除新增标记13文件逐字节等原件。未重新综合，标记效果未验。 |
| 构建/硬件 | 0新PDS、0新DUT、无新调试位流/时序/INIT审计，无硬件操作；over_temp STOP。 |

## 原因与预算

第一次19.141秒：监督脚本预期Expiration Reminder，但实际为主窗口，精确标题保护停止；无控件操作，应用正常rc0退出。保存为gui-attempt1，不当工具错误。

第二次365.844秒：已视觉核对主界面；还原/最大化、输入新ADF路径、Next解析成功、创建一核、进入配置并通过GUI Tcl设置参数/列网络/保存新FIC。保存使标题加入新FIC路径，A监督仍以旧固定标题查找下一截图，因而退出；原生rc0。之后准备的连接命令未执行（ui_text StopIteration），不能称126位已接线。监督错误是A自身实现问题，不能归因CPU、许可或PDS。未更改任何执行策略、许可证、系统配置。

累计2次/384.985秒，低于600秒但已耗完两次启动额度；不把剩余时间或未用PDS额度解释为第三次GUI许可。两自有根正常退出，退出后各自可见窗口0；未独立证明所有潜在后代进程树。标题截图顶部已脱敏，原日志/ADF/完整源/位流只本地。

## 未映射对象与候选差异

- soc/cpu_core/branch_taken：1位。
- soc/address[0..7]：8位；[8..31]名称已匹配。
- soc/wren：1位。
- soc/stopped、soc/stop_kind[0..1]、soc/write_error：4位。

仅此名称查找不能区分优化、别名或命名保留问题。官方《Fabric Inserter用户手册》V1.0（2022.07.12）实际PDF40页已视觉回看，支持信号旁添加`/* synthesis PAP_MARK_DEBUG="true" */`；41–42页说明保留/自动连接，但本轮未动态验证候选。标记branch_taken、address、wren、顶层stopped/stop_kind/write_error，不新增逻辑、端口或改变功能表达式。准确差异及每文件前后SHA见下列入口。

## 证据与复现边界

根目录：`D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1-r1/`。

- `APPROVAL.json`、`STAGE_CLOCK.json`：独立批准/总预算，旧阶段不重置。
- `GUI_START.json`、`GUI_RESULT.json`、`GUI_ACTIONS.json`及`gui-attempt1/`：两次实际会话、动作、原生rc和保护停止。
- `gui_session.py`、`ui_text.py`：本次实际执行脚本；保留缺陷，不当未来可重跑入口。命令见`COMMANDS.md`。
- `partial.fic`：940字节，SHA256 **8E985383663B4A56837A736036AFB30D733427EF0C60CC4F86FF3CA540AFEA93**；单核1024点，无任何数据/钟/复位连接，未核新FIC完整器件字段。
- `NET_MAPPING.json`：逐对象/逐位索引及缺口，未宣称成功连接。
- `SOURCE_RECEIPTS.json`、`DEBUG_METADATA.patch`、`prepare_marked_candidate.py`：13原件/候选、3文件/6注释、准确diff；仅候选未构建。
- `SAFE_TOOL_RESULT.json`、`POSTFLIGHT.json`、`SUMMARY.json`、`SHA256SUMS.json`：安全解析/46保护原件核同/独立本地全清单。

不重跑本次历史脚本、不用旧位流替代新产物；无CPU实机、真实片上采样或正式CoreMark验收。下一先修正自有监督的稳定PID/窗口类定位、保存后标题变化及截图脱敏；新GUI额度须另有批准，原预算不静默扩张。无需用户连接硬件、提供日志或联系厂家。
