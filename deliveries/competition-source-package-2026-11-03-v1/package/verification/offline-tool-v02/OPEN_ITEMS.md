# OPEN_ITEMS / 未完成项（R1 v02）

- B 实现与冻结测试：`COMPLETE_LOCAL`，54/54 PASS_LOCAL。
- A 独立代码审阅、复现、ABI 兼容与分层验收：`PENDING_A`。
- 原 v01 37 例：全部回归通过；原输入/预期未改，v01 只读保留。
- P02 是四份旧观测记录的重放，不是独立 ISA/CPU 验证，不是新 DUT。
- C2 的 `result.json`/`worker-result.json` 在 256B 限额下**故意不存在**；这是 `LIMIT/rc5` 的正确结果，不是缺结果。
- F15/R1-TIMEOUT 的 `TIMEOUT` 与 C1/C2/R1-LOG/R1-MEM 的 `LIMIT` 是预期负向结果；测试 PASS 与被测 CLI 退出码分开。
- R1-MEM-MEASURE 是固定 fixture + 内部 runner 的测量失败单元证据，不是新 DUT/DUT 失败。
- 未安装软件、未运行 DUT/TB/仿真器/PDS、未操作硬件；PDS/JTAG/供电/Flash/板级/温控仍未授权。
- 其他 OS 未实测；仅 Windows 11 + 现有 Python 3.12.10。
- 旧根 `OPEN_PREEXISTING`、外设 10/27 18:00 窗口和 v02 外设任务均不在本 R1 内。
