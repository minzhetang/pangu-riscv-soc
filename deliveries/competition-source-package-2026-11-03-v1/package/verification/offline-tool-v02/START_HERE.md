# B-VERIFY-OFFLINE-M0-R1 交付入口（v02）

## 结论

B 已完成补充 1.0.1 的资源/路径/失败守卫整改：C0 正常路径保持 MATCH；C1 为 `LIMIT/rc5` 且不启动 worker；C2 为 `LIMIT/rc5` 且不写超限 result/worker-result；C3 为 `INVALID_INPUT/rc3` 且复制工具树无新增输出。原 v01 37 例输入/预期未改，v02 共 54/54 PASS_LOCAL。

这是 B 侧 `PASS_LOCAL`，不是 A 的独立复验、CPU/ISA 验证或最终系统/硬件验收。P02 仅为旧观测记录重放。

## 关键身份

- 输入包：`mainline-b-offline-r1-2026-10-27-v1`
- 输入 manifest SHA256：`D47564C58F043AF8E3599D23F157799C01A6BACF4B23C7F78CF53EA3E79A81F0`
- 合同/接口/验收：`1704CD79...5113C` / `BEDB4492...C8C5` / `80A9B2A2...B431`
- v01 原计划 SHA：`9F74BDEFADC8981A55F0443855A0549F79A4FE1118E8D3EDBC330618355352BD`
- v02 冻结计划 SHA：`82C42434FDE78495B6A3F9F945756F1ADE464EEEB6A5E9DC3D63E5C5F442AA4F`
- Python：3.12.10 / Windows 11 / `-B` / optimize=0

## 入口

正常使用（输出目录必须不存在且在输入/工具树之外）：

```text
python -B RUN.py --case-file CASE.json --input-root INPUT_ROOT --out NEW_OUTDIR
```

固定白名单 fixture 只用于测试资源/失败守卫，不是通用命令入口：

```text
python -B RUN.py ... --fixture-worker log_flood
```

## 阅读顺序

1. `R1_RESPONSE.md`：C0/C1/C2/C3 新旧对照、R1-1/R1-2/R1-3 逐项。
2. `RECEIPT.json`：实际接收、版本/SHA、工时、返回时间。
3. `tests/PLAN.json` / `.sha256`：执行前冻结的 54 例计划。
4. `tests/results.json`：逐例状态、父/worker rc、完整消费、资源、首错、结果大小。
5. `COMMANDS.md` / `logs/<case>/`：完整命令、原生日志、rc、终止。
6. `pressure/results.json`：1/16/128MiB 压力与资源。
7. `diagnostics/`：首错/邻域/无差异/4MiB 块边界/坏尾部。
8. `CHANGED_FILES.json` / `DIFF.patch` / `SHA256SUMS.txt`。
9. `r1/old-v01/`：旧 v01 C0–C3 反例副本；`r1/task/`：A 的任务/反例文档。
10. `tests/history/`：v01 原计划/结果，原 37 例保留。

## 文件与边界

- 返回目录不含 65MB 原输入、不含大压力文件；压力输入由 `tests/generate.py` 在包外确定性生成。
- 未修改 frozen API、ABI、旧 v01、外设 v02、旧根或公共记忆。
- 未安装软件/未运行 DUT/TB/仿真器/PDS/硬件；硬件 `STOPPED`。
- 其他 OS 未实测；P02 是旧记录重放，不是独立 ISA 参考。
