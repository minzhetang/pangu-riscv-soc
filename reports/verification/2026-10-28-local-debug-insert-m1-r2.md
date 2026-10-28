# 本地观察核R2：综合通过，控制脚本失败，未完成插核

日期2026-10-28；D175批准范围1.2.0，F169/D176。本报告不把阶段候选或部分成功记作完整验收。

| 检查层次 | 本次真实结果 |
|---|---|
| 输入保护 | F163完整13源基线；新副本仍仅3文件6处非功能PAP_MARK_DEBUG注释。46保护原件及50个执行前冻结文件后验核同。 |
| 编译/综合 | PDS2022.2-SP6.4 build146967在PG2L100H/-6/FBG676配置完成compile、ADS synthesize；产生新ADF/VM。 |
| 功能初始化 | 28个综合网表DRM18块的1792个INIT_00..INIT_3F逐片数值与F163相同。仅综合网表层，不是新位流、读回或实机验证。 |
| 完整构建 | 1次调用、18.546秒、原生rc1。综合后等待脚本调用`clock`失败，未进入add_fic/Map/PnR/最终时序/位流生成。 |
| GUI | 唯一会话17.625秒；仅出现Expiration Reminder。A把主窗口命令提前入队，角色保护停止；无控件调用、无新FIC，rc1是监督终止，不等许可失败。 |
| 限额内诊断 | 2次PDS只读帮助/能力查询，1.219及1.328秒，均rc0；共6项额度用完，无新综合或GUI。clock不存在，after/vwait/incr可用，add_fic帮助正常；两次1ms计数等待实际运行得2。 |
| 许可/安全 | 本次原生实际提示6天；未改许可证、安全策略或系统环境。0GCC/Icarus/新DUT/硬件/Flash，over_temp STOP保持。 |

## 两个独立的A自身问题

1. PDS的`clock`不可用。仅凭标准Tcl经验写暂停脚本是错误；SYNTH_READY在错误前已经落盘，文件存在不能证明PDS仍存活。下次启动GUI前必须核自有PDS进程仍在运行且等待协议有效，不能只看标志文件。已通过原生只读查询验证的替代方法为固定次数`while`/`after`/`incr`，外层主机仍保留绝对超时。
2. GUI分类器虽能识别提醒，调度器却把“当前没有主窗口”当错误。必须在提醒存在时阻止向主窗口输入，等待角色出现，再执行；不能盲点提醒或额外重开。prepared/window_policy.py以13项合成元数据及启动序列检查通过，修正GUI副本和Tcl副本已准备，但**未再运行**。

本轮两项失败都不归因CPU、过温、许可已失效或PDS设计错误。完整构建及唯一GUI额度已消耗，不静默延长或重启。

## 证据入口

根目录`D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1-r2/`：

- `APPROVAL.json`、`STAGE_CLOCK.json`、`PDS-attempt.json`、`GUI-attempt.json`、`FROZEN_INPUTS.json`：批准、独立计数、输入冻结。
- `pds/build.tcl`、`run_pds.py`、`logs/pds-flow-once/process.json`及原始stdout：真实失败脚本/rc/时长；原生日志仅本地。
- `GUI_RESULT.json`、`GUI_WINDOWS.json`、`gui_control.py`、`gui-commands/`：真实窗口/角色错误；未执行主窗口动作。
- `READONLY_HELP_RESULT.json`、`WAIT_QUERY_RESULT.json`、两查询process.json及脚本：原生能力验证，与综合调用分开。
- `SYNTHESIS_MEMORY_AUDIT.json`、`MARKER_OBSERVATIONS.json`、`SOURCE_RECEIPTS.json`：1792片一致及实际属性观察。VM中属性出现不等140位可连接性；总线声明未显示属性也不能单独证明标记失效。
- `prepared/POLICY_SELFTEST.json`、`prepared/PREPARATION_RECEIPT.json`：仅主机离线控制策略测试及未执行恢复代码，不是DUT测试。
- **当前结果读`SUMMARY_FINAL.json`**、`POSTFLIGHT_FINAL.json`；初稿SUMMARY的许可解析为空、查询计数4被`LICENSE_NOTICE_CORRECTION.json`及最终结果取代，原件保留。初稿INIT审计过宽匹配INIT_FORMAT触发断言，仅修改主机解析为64项INIT数据后复核，无RTL或期望修改。

新FIC、调试位流、最终27MHz时序及片上采样均未完成；原F160/F163有限软件成果保持。下一只推荐修复后的同范围恢复，须新执行额度；不联系厂家或让用户代研究接口。

## Git状态

用户本轮明确批准前20项同步，系统自动审核仍拒绝外发，未换通道上传。更安全的本地提交已获系统审核并实际完成：`cffee7362fc9fe805ef96a980577b83afbdd4da1`，精确20项、757已跟踪路径、当时工作区干净，**未推送/0网络命令**。收据`reports/repository-local-debug-r1-partial-sync-2026-10-28-v1/LOCAL_COMMIT_ONLY.json`。R2新成果随后另审本地纳管，不能把本地提交当远端同步或功能验收。
