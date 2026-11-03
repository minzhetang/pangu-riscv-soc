# RX 1.3.5 最终快照说明

- 计划 `rx-plan-1.3.5.json`，SHA256 `979D6451D69A22B889FE564EF2E33CA4ECD0BCF65B0D3CE2E0356E6D94CE17E4`。
- 正式运行 `rx-20261025-211013`：N8/N16/N234 全 PASS，账本 92/110/68，功能 41/41、50/50、29/29，OV/FE 4/7。
- 内联账本在独立串行解码确定的真实 S/consume 沿保存 pre；同一沿 NBA 后 +1 ps 保存 post。
- N16 seq0/edge170 ACCEPT：`pre_valid=0 post_valid=1`。
- N16 seq30/edge2618 ACCEPT：`pre_valid=0 pre_ready=1 post_valid=1`。
- N16 5e DROP edge8081：`pre_clear=1 pre_fe=1 post_clear=1 post_fe=0 pre/post_ov=1`。
- `RX_SNAPSHOT_CHECK_PASS` 覆盖所有事件的 pre/post 0/1 合法性、ACCEPT/REPLACE/CONSUME/DROP 形状及重复事件。
- 正式/负向共用 `rx_public_capture`；正式逐笔有序比较 type/data/edge，`ordered=1 edge_match=1`。
- 状态传播自检 `rx-status-selfcheck-20261025-211027 all_pass=true`。
- 1.3.4 及更早内容仅历史；RX RTL 未改。
