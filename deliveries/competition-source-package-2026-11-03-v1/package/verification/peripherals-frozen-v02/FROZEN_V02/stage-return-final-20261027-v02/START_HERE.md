# 最终阶段 v02：START HERE

- stage：`stage-return-final-20261027-v02`
- 基线：`stage-return-final-20261027-v01` / `increment-20261024-2335`
- 本轮只做 R1/R2/R3；旧 v01、核心、包装 RTL、W06/GPIO 历史包均保留。
- 性质：最终阶段候选，`PASS_LOCAL`；不是主线复现或最终验收。
- 硬件：`STOPPED`。

## R1/R2 结果

- **R1 RX**：计划 `rx-plan-1.3.5`，SHA `979D6451...17E4`；run `rx-20261025-211013`。真实 S/consume 沿 pre + 同沿 NBA 后 +1 ps post；N8/N16/N234 账本 92/110/68，功能 41/41、50/50、29/29；seq0 edge170 和 seq30 edge2618 的 pre/post 已修正；5e post_clear=1/post_fe=0；`RX_SNAPSHOT_CHECK_PASS`。
- **R2 TX**：计划 `w01-w10-plan-1.0.5`，SHA `5A955CD3...97A9`；run `regif-m1-20261025-210743`。START event_edge=真实接受沿，COMPLETE event_edge=START+10N；observed_edge=event_edge+1。N16 首帧 37→197，N234 6→2346；6 完整/3 取消/0 bad stop。

## R3 索引

- `SOURCE_INDEX.json`、`CHANGED_FILES.json`、`DIFF.patch`、`SHA256SUMS.txt` 从冻结后的当前文件重新生成；不再对 `SOURCE_INDEX` 用旧哈希。
- 五个元数据块（DEPENDENCIES/HISTORY_ALIASES/MODULE_STATUS/SOURCE_INDEX/delivery）在 diff 前稳定生成，主 SHA 最后生成。
- 活动计划/说明已统一到 1.3.5 / 1.0.5；旧 1.3.4/1.0.4 仅历史别名。

## 阅读顺序

1. `delivery.json`
2. `MODULE_STATUS.json`
3. `OPEN_ITEMS.md`
4. `coverage_map.json`
5. `CHANGED_FILES.json` / `DIFF.patch`
6. `SOURCE_INDEX.json` / `DEPENDENCIES.json` / `HISTORY_ALIASES.json`
7. `SHA256SUMS.txt`
8. `work/` 下 R1/R2 最终源/计划/日志/VCD/results

W06 引用 `A-W06-SUPPLEMENT`；GPIO 1.0.2 沿用已有接收结论；旧根 `OPEN_PREEXISTING` 未改写。ZIP 可选，本目录未生成 ZIP。
