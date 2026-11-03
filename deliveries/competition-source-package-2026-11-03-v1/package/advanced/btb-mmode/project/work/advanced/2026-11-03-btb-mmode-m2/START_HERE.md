# 高阶独立候选M2：自然取指停顿与跳转重叠

2026-11-03。**有限仿真候选，不替换D300/SM2生产基线，不是完整高阶任务2验收。**

1. 先读 `SUMMARY.json` 及项目报告 `reports/verification/2026-11-03-btb-ifstall-candidate-m2.md`。
2. 再读 `RTL_DIFF.patch`、`PLAN-v2.json`、`AUDIT.json`。
3. `after-v2-RESULTS.json` 是4程序×4配置的16次最终新用例；`after-trap-RESULTS.json`另有两条异常重叠程序×4配置=8次；`final-*-RESULTS.json` 是21个原冻结程序的84次相关回归。总计108次最终运行，不把中间试验叠加成完成率。
4. `before-v2-RESULTS.json` 为同一v2用例在M1前源的对照；`original-v2-RESULTS.json` 是B原始HL4对照。三组不同，不混称。
5. 每次 `runs/<stage>/<case>/` 保存程序、原事件日志、普通VCD；命令/输入SHA/native rc/时间/Job清理见 `COMMANDS.json`。

## 版本与保留

- `source-original-hl4/`：B原八模块，继承M1 source-before，原成果不修改。
- `source-before/`：M1最终候选精确副本。
- `source/`：M2独立候选，仅cpu_hl4.v新增stall期控制转移门控；八模块中其余七个同字节。
- `source-first-fix/`：首次修复快照，与最终RTL同字节；留下测试纠错时的身份。
- M1全部1410项清单、本阶段89保护原件均回查同SHA，详AUDIT。
- `PLAN.json` / `prepare.py` / `before*` / `after-RESULTS.json`：原测试设计和历史失败。原BEQ偏移0x1008超出范围，被编码成负偏移；不能将它的跑错路径称CPU缺陷。`PLAN-v2.json`以合法+8替换该程序，保持手工期望不变并重新冻结。`prepare-v2.py`有独立立即数字段解码核验。
- 初版 `tb-initial.sv` 把miss期无效PA中的X当有效控制失败；保留原日志。正式TB仅对真正被接受的取指地址/指令检查未知，同时继续检查PC、有效控制及WB/STORE数据，不屏蔽有效错误。

## 复现

依赖项目工作树中的既有合法Icarus13/Python3和 `work/pds-jtag/2026-10-30-led-official-batch-h4/owned_job.py`。路径以execute.py位置解析工作树根，无旧M1 BASE。未捆绑工具、无安装或新硬件操作。

```text
python -X utf8 -B work/advanced/2026-11-03-btb-mmode-m2/run.py after-v2-repro
python -X utf8 -B work/advanced/2026-11-03-btb-mmode-m2/regression.py final-repro
python -X utf8 -B work/advanced/2026-11-03-btb-mmode-m2/regression.py final-repro-sync
python -X utf8 -B work/advanced/2026-11-03-btb-mmode-m2/regression.py final-extra-repro --extra
python -X utf8 -B work/advanced/2026-11-03-btb-mmode-m2/regression.py final-extra-repro-sync --extra
```

使用未存在的stage名，禁止覆写旧运行。审计默认核本次固定验收stage，重跑不自动升级既有结论。prepare*.py为生成史，冻结文件存在时拒绝重建。

`audit.py`依赖原M1审计函数，采用AST仅提取纯函数，不执行原M1整脚本或写回；该依赖已核SHA，跨主机移植须同时保留M1所需audit.py及保护清单/生产文件或另建合法、明确的验证依赖，不能声称本目录单独任意搬移即完整复现。

所有新用例真实取指执行；使用既有MRET进入S态开启翻译，以固定superpage夹具自然制造I-TLB miss。没有force、没有新增S/U/MMU实现；这不是完整S态/PMP/Sv32验证。无本候选PDS/位流/实机/ILA/CoreMark成绩。硬件与公共基线不因本包存在获得授权或替换。
