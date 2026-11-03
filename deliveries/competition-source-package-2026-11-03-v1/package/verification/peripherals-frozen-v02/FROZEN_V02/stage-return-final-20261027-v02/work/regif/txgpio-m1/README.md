# B-REGIF-TXGPIO-M1 独立包装

- 合同：`LOCAL-REGIF-TXGPIO-M1 / 1.0.0`
- 合同 SHA256：`F0E31602D008459B3E95901C0F533BC7FF4153F6B5A93859780EA8D2AD64E988`
- 质量补充 SHA256：`80DEBA901A0917E730CD14D98A08933274337588A1E2A31AFBAB6D91D700F476`
- 批准：D115 `APPROVED_TO_START_ON_RECEIPT`；实际接收 `2026-10-23T23:52:38+08:00`
- 包装 RTL：`src/local_regif_txgpio_m1.v`，SHA256 `5C81EE8F01372D33D4173A34BB095B3D6E649541E4716C933AF11A2390D264FA`
- 冻结计划：`tests/w01-w10-plan-1.0.5.json`，SHA256 `5A955CD36618C736A4060C4EF4804B77A3E802FFBA6145FA7C71F6B05BDD97A9`
- TB：`tb/tb_local_regif_txgpio_m1.sv`，SHA256 `7F0C1060ED9524B18965575CC3BE8DA1AE76D899521916F2D701976AEFAD793B`
- 公共 uart_tx 捕获：`tb/regif_tx_public_monitor.sv`，SHA256 `A7C857C1451B5C3960F6DA4A1CF90451E72D4D572815D806FA14B51ADE106CFB`
- 官方运行：`regif-m1-20261025-210743`
- 结果：N16 W01–W10 PASS（9 TX 接受、6 GPIO 接受、11 拒绝、6 完整帧、3 复位取消）；N234 W05/W06/W09 PASS；`results.json` schema PASS
- VCD：`waves/regif-m1-20261025-210743/regif_m1_N16.vcd`、`regif_m1_N234.vcd`
- 日志：`logs/regif-m1-20261025-210743/`

## 边界

只新增独立包装，不修改冻结 TX/GPIO 核心、CPU、公共模型或原测试；不包含 RX 包装、FIFO/中断、完整总线、正式计时、PDS/JTAG/供电/Flash/温控或硬件。A 已使用原包装/核心完成 N16/N234 有限复验及 GPIO+C 程序系统仿真；CPU 适配、存储和系统验证归 A，B 不承担，也不把 A 的使用写成 B 最终验收。

## 文档

- `docs/CONTRACT_RECEIPT.md`：合同/质量补充 SHA 与实际接收时间
- `docs/W01-W10.md`：逐项预期、结果、写语义
- `docs/RUNBOOK.md`：完整命令、计划 gate、预期 marker、schema
- `docs/SHA256SUMS.txt`：源/TB/计划/结果/日志/VCD 清单
- `scripts/run_regif_m1.py`：共享 runner 入口，先 gate 后 DUT；含逐项唯一 marker 与公共事件账本判定
- `scripts/regif_entry_selfcheck.py`：用正式 N16/N234 日志和 runner 同一判定路径跑正确控制及 marker/事件负例
- `scripts/regif_capture_selfcheck.py`：用同一 `regif_tx_public_monitor` 的合成公共 uart_tx，检好帧、坏 stop、额外/漏帧

## 历史

- 1.0.0 计划/运行 `regif-m1-20261024-000015` 保留；当时 TB 未生成 VCD，不作为最终含 VCD 证据。
- 1.0.1 仅补 `+WAVE_FILE` 普通 VCD。
- 1.0.2 修正 W01 首释放沿请求计数：N16 rejected 10→11；新增实际请求/TX/GPIO 账本和逐项唯一 marker 负例；wrapper/TX/GPIO 核心未改。
