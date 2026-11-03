# 独立M3：有限M-mode向量/CSR响应检查点

先读SUMMARY.json及项目报告 `reports/verification/2026-11-03-mmode-vector-m3.md`，再读PLAN-v2.json、RTL_DIFF.patch和AUDIT.json。

- `source-before`：M2八模块精确副本；`source`：仅cpu_hl4.v两行修复。不是已验生产CPU替换。
- `PLAN-v2.json`：正式11程序、手工预期与响应门；`after-v2-RESULTS.json`44最终运行；`before-v2-RESULTS.json`40PASS/4FAIL对照。
- `final-regression*`/`final-extra-regression*`结果：84旧用例；`after-if-v2`/`after-if-trap`结果：24旧取指停顿用例；正式共152运行。
- 旧PLAN/first/final/AUDIT-initial-expectation为测试夹具错误或过宽预期的历史，全部保留，不能作正式验收。新预期按规范重新冻结，详报告。
- `logs`、`runs`含新旧完整日志/普通VCD/程序；COMMANDS包含每次输入SHA/native rc/耗时/Job清理；AUDIT是独立账本、负向控制、VCD前后沿和保护SHA检查。

已有项目Python3、Icarus13、OwnedJob依赖与M2一致，execute.py按脚本位置定位项目根，无旧BASE。没有捆绑/安装工具或启动硬件。依赖 `work/pds-jtag/2026-10-30-led-official-batch-h4/owned_job.py`；audit.py还按AST只读取M1/audit.py中的纯VCD解析函数，不执行其整脚本。跨机需合法提供依赖，不能宣称单目录任意搬移即完整复现。

```text
python -X utf8 -B work/advanced/2026-11-03-mmode-vector-m3/run.py after-v2-repro
```

使用未存在的stage名，输出存在则拒绝覆盖。prepare*.py属生成史，已有冻结计划时拒绝覆盖。正式回归入口regression.py及ifstall.py；其冻结输入/预期按复制来源保留，IF_PLAN*与本轮PLAN-v2区分。审计固定核本次stage，重跑不自动升级旧结论。

本版尚无CoreMark/综合/频率/资源/位流/实机或ILA结果，不是完整高阶2。D300/SM2生产版和D320应用保持，B不新增工单，硬件不操作。
