# 独立高阶BTB / 有限M-mode候选

2026-11-03。当前仅有限RTL仿真接受，**不替换D300/SM2板级基线，不是完整高阶2完成**。

先读 `SUMMARY.json`，再读仓库 `reports/verification/2026-11-03-btb-mmode-independent-candidate.md`。

- `source-before/`：B原八模块精确副本；`source/`：独立修复版，只有cpu_hl4.v不同。`RTL_DIFF.patch`为准确对照。
- `FROZEN_PLAN.json`：19程序及手工WB/STORE/trap预期；`FROZEN_EXTRA_PLAN.json`：两条定向补充。不要改预期求PASS。
- `final-r2-RESULTS.json`、`final-r2-sync-RESULTS.json`、`final-extra-r2-RESULTS.json`、`final-extra-r2-sync-RESULTS.json`：最终统一TB、编译/运行输入SHA绑定的84次运行；`before-RESULTS-rechecked.json`：原源38次对照的修正检查器离线重判。先前final等为历史中间运行，不再重复累计为最终84次。
- `logs/`、`runs/`：全部旧/新原始证据；每例events.txt、program.hex、普通trace.vcd。旧失败/检查器错误保留，不能把所有历史FAIL混算成最终DUT失败。
- `AUDIT.json`：独立账本、负向控制、VCD前后沿、周期对照和89保护原件核验。
- `BTB_UNIT_RESULT.json`：当前源码新运行12单元检查；不是84条CPU程序中的一部分。
- `COMMANDS.json`：实际命令、墙钟时间、rc及Job清理；`SANDBOX_TOOL_ERROR.json`：最初工具失败和证据留存缺口。

## 可复现入口及依赖

本目录仍按项目工作树布局使用；依赖Python3（标准库）、已有合法Icarus13、`work/pds-jtag/2026-10-30-led-official-batch-h4/owned_job.py`。execute.py通过本文件位置定位工作树根，无旧M0 BASE。不包含/不安装工具；移到其他主机需先合法提供对应依赖并调整明确的工具根，不能宣称任意目录即直接运行。

在已配置工作树，用已有Python运行：

```text
python -X utf8 -B work/advanced/2026-11-03-btb-mmode-m1/suite.py final-repro
python -X utf8 -B work/advanced/2026-11-03-btb-mmode-m1/suite.py final-repro-sync
python -X utf8 -B work/advanced/2026-11-03-btb-mmode-m1/suite.py final-extra-repro --extra
python -X utf8 -B work/advanced/2026-11-03-btb-mmode-m1/suite.py final-extra-repro-sync --extra
```

每个stage名称必须未使用，否则明确拒绝覆盖。新运行结果用该stage名保存，audit.py默认分析本次冻结的final四配置，不会自动把重跑混入验收。prepare*.py为生成史，已有冻结计划时拒绝覆盖，不是重跑前必须执行的步骤。原tb.sv/execute.py初始主入口只用于工具问题历史隔离，正式使用suite.py/tb-check.sv；不要拿初始TB的linkwrites常量作有效证据。

本次已批准独立软件阶段，不含新硬件/PDS/Flash。不要运行失败或历史vvp充当当前源码结果。保留S/U/Sv32/PMP已知缺口，详细剩余范围见报告。材料哈希通过不等于功能通过。
