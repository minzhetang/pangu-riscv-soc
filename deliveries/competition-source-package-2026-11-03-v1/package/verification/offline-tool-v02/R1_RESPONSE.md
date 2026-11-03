# R1_RESPONSE / 补充 1.0.1 逐项对照

任务：`B-VERIFY-OFFLINE-M0-R1`，D158，2026-10-27。原 ABI 1.0.0 与冻结 API 未改；v01 原 37 例输入/预期保留在 `tests/history/`，v01 目录未被覆盖。

## 0. 接收与身份

- 实际接收：`2026-10-27T12:53:03+08:00`
- 输入包：`mainline-b-offline-r1-2026-10-27-v1`
- 输入 `SHA256SUMS.txt`：`D47564C58F043AF8E3599D23F157799C01A6BACF4B23C7F78CF53EA3E79A81F0`
- 合同：`1704CD79...5113C`；接口：`BEDB4492...C8C5`；验收计划：`80A9B2A2...B431`
- Python：3.12.10 / Windows 11 / `-B` / optimize=0
- 新冻结计划：`tests/PLAN.json`，SHA256 `82C42434FDE78495B6A3F9F945756F1ADE464EEEB6A5E9DC3D63E5C5F442AA4F`
- 结果：`tests/results.json`，54/54 PASS_LOCAL（原 37 + R1 17）
- 未安装软件、未运行 DUT/TB/仿真器/PDS、未操作硬件；无新 DUT。

## 1. A 四个 CLI 反例的新旧对照

| ID | 旧 v01 实测 | 新 v02 实测 | 结论 |
|---|---|---|---|
| C0-default | `MATCH/rc0`，result 3016B | `MATCH/rc0`，result 3308B，worker-result 1370B | 正常路径不退化 |
| C1-worker-memory | `MATCH/rc0`，worker 仍运行 | `LIMIT/rc5`，preflight 拒绝，worker_started=false，result 1492B | 1B 阈值不再 MATCH |
| C2-result-size | `TOOL_ERROR/rc7`，result 2184B、worker-result 1368B | `LIMIT/rc5`，**无 result、无 worker-result**，只有 command/log | 256B 上限不写超限结果 |
| C3-optimized-protected | `INVALID_INPUT/rc3`，但复制工具树内创建 945B 输出 | `INVALID_INPUT/rc3`，无输出目录；复制工具树前后哈希相同 | 保护树不被污染 |

旧 v01 实测副本在 `r1/old-v01/`；A 的原始反例在 `r1/task/COUNTEREXAMPLES.json`。旧 v01 目录本身未修改。

## 2. R1-1 资源/日志/结果

- **内存阈值**：阈值低于运行器最小开销 8MiB 时 preflight `LIMIT/rc5`，不启动 worker；正常阈值运行后取 parent 观测与 worker 自报峰值的较大值，超限即 `LIMIT/rc5`，`fully_consumed=false`，不 MATCH。`R1-MEM-OVER`：阈值 16MiB，实测约 20.6MiB → `LIMIT/rc5`。
- **测量失败**：固定 `no_peak_worker` fixture + 内部 runner，parent/worker 均无峰值 → `TOOL_ERROR/rc7`，不成功化。`R1-MEM-MEASURE` PASS（这是单元/固定fixture证据，不是新 DUT）。
- **stdout/stderr**：父进程轮询并在超过 `max_log_bytes_each` 时终止、wait、截断；`R1-LOG-FLOOD` 用固定 fixture 产出 5MiB，实际日志被限制到 4KiB，状态 `LIMIT/rc5`。
- **结果上限**：worker-result 和 result 均按本 case `max_result_bytes` 序列化；超过时原子发布不落盘。C2 256B：无结果文件，rc5；`R1-RESULT-ENOUGH` 4KiB：worker-result/result 均在 4096B 内，MATCH。
- 未使用全局 1MiB 常量覆盖本 case 限额。

## 3. R1-2 统一前置路径/输入/错误

- 输出已存在：先拒绝，不覆盖；`R1-EXISTING-OUT` 的 marker 保持。
- `-O/-OO`：在创建任何输出前返回 `INVALID_INPUT/rc3`；C3 在复制工具树内输出路径也不创建。
- 无效 CASE JSON、无效 input-root、CASE >1MiB、archive index >2MiB：先保护输出/先 stat，再读取或拒绝；`R1-INVALID-JSON`、`R1-INVALID-ROOT`、`R1-OVERSIZE-CASE`、`R1-OVERSIZE-INDEX` 均验证。
- raw 输入先核字节预算再计算 identity SHA；archive index 先核 <=2MiB、路径/链接，再进入冻结 codec；不再先无限读/完整哈希。
- 未修改 `frozen/offline_api.py`、`frozen/block_codec.py`；其 SHA 与 v01/输入包一致。

## 4. R1-3 单一时限与真实 rc

- 父 CLI 从 CASE 元数据准备开始使用单调时钟；worker 收到同一 case 剩余 deadline，identity、compare、诊断共用，不各自续期。
- 短超时：`R1-TIMEOUT-TOTAL` 1s 主预算 + 1s 清理，受控 `sleep_forever` worker，parent 终止并 wait，总实测约 2.015s（观测容差 <2.6s），`TIMEOUT/rc6`。
- 每个测试同时核对父 CLI rc、worker rc、result status/native_rc；F17/F18 仍保留为纯守卫单元证据，R1-WORKER-RC/MISSING/PASS 是实际父 runner 路径。
- `R1-WORKER-RC`：worker rc17 → parent `TOOL_ERROR/rc7`；`R1-MISSING-RESULT`、`R1-PASS-TEXT`：无有效 result/只有打印 PASS → `TOOL_ERROR/rc7`，绝不 MATCH。

## 5. 原 37 例回归

`tests/history/PLAN-v01.json`、`results-v01.json` 保留为 v01 历史。v02 原 37 例全部 PASS_LOCAL，P02 四流共 `9,378,498` 记录；P02 仍是旧观测重放，不是新 CPU/ISA 验证。

- P01 7/7
- P02 4/4，记录 `9,378,498`
- F01–F19 19/19（含预期拒绝/超时）
- D01/D02 2/2
- R01 1/1（中文空格独立目录）
- S01 3/3 + S02 1/1（1/16/128MiB，>2^32 周期）
- R1 新增 17/17

## 6. 未完成/局限

- A 的独立代码审阅、复现和分层验收：`PENDING_A`。
- P02 是旧记录重放，不是独立 ISA/CPU 语义验证；不是新 DUT、不是 CoreMark 正式成绩。
- 其他 OS 未实测；仅 Windows 11 + 现有 Python 3.12.10。
- 未操作硬件；`over_temp`/PDS/JTAG/供电/Flash/板级边界不变。
