# Diagnostics 说明

本目录保存从冻结测试结果导出的首错/邻域/错误证据，不重新定义期望。

- `P01-S00-duplicates-kept.json`、`P01-S04-empty-explicit.json`、`P01-S06-bus-format.json`、`P02-*.json`、`F04.json`、`R01.json`、`S01-*.json`、`S02.json`：无差异或规模匹配，`no_difference=true`。
- `P01-S01-wrong-field.json`、`P01-S02-missing-tail.json`、`F01`–`F06`、`D01`：首错序号、类别、字段/值及 ±2 邻域。
- `D02.json`：在第二个 4MiB 存档块范围内插入的合法 EDGE 字段差异；首错序号 44269，邻域 ±2，证明比较跨块仍逐笔核对。
- `F07`/`F08`/`F13`：格式/尾行/超长行错误；`F09`：complete 收据缺失；`F10`/`F11`：存档 payload/index 损坏；`F12`：越界路径；`F14`：字节限额；`F15`：deadline；`F16`：输出已存在。
- 所有诊断均来自 RUN 的实际结果；测试预期的 `PASS/FAIL` 与功能状态 `MATCH/MISMATCH/...` 分开记录。
