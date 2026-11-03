# B-UART-RX 状态与证据

> **2026-10-25 1.3.5 更新（真实事件沿 pre/post 快照修正）**：新计划 `tests/rx-plan-1.3.5.json`（SHA256 `979D6451D69A22B889FE564EF2E33CA4ECD0BCF65B0D3CE2E0356E6D94CE17E4`）。正式运行 `rx-20261025-211013`：N8/N16/N234 全 PASS，账本 **92/110/68**，功能计数 N8 41/41/4/7、N16 50/50/4/7、N234 29/29/4/7。内联账本在独立串行解码确定的真实 S/consume 沿保存 pre，NBA 后同一沿 +1 ps 保存 post；N16 seq0/edge170 pre_valid=0/post_valid=1，seq30/edge2618 pre_valid=0/post_valid=1；5e `edge=8081` 为 `pre_clear=1/pre_fe=1/post_clear=1/post_fe=0/OV=1`。新增 `RX_SNAPSHOT_CHECK_PASS` 逐条校验无 X/Z、无缺/重复；正式/负向仍共用 `rx_public_capture`，共享捕获逐笔有序 type/data/edge 全等。状态传播自检 `rx-status-selfcheck-20261025-211027 all_pass=true`。1.3.4/1.3.3 及更早内容保留为历史，不再是活动引用；不是主线复现或最终验收。

> **2026-10-24 1.3.0 更新（协议事件账本补正）**：新冻结计划 `tests/rx-plan-1.3.0.json`（SHA256 `8409561AA24E2DD21F0A24E68FC8EEDB660D69C170AC15DAF558598DA6326EE6`）。正式本地运行 `rx-20261024-002409`：N8/N16/N234 全 PASS，账本 **88/106/64**（旧 87/105/63 保留为历史），功能计数仍 40/39/4/7、49/48/4/7、28/27/4/7。RX-05 5e 在 OV 已 1、clear 与新帧同沿时补记一笔协议 DROP：N16 实记为 `edge=8081 type=3 data=0x44 pre_ov=1 post_ov=1`，数据来自独立串行解码而非 `stim_bytes[0]`。账本每条带 edge、pre/post 公开端口状态；CANCEL 由“复位时独立串行解码器仍在帧中”推导，已移除刺激后 `actual_cancel()` 调用。负向公开流捕获源已覆盖漏/多/错序/错字节与控制。日志/普通 VCD 在 `logs/rx-20261024-002409/`、`waves/rx-20261024-002409/`；不是主线复现或最终验收，旧 1.2.0 计划/日志保留。

> **2026-10-23 1.2.0 更新（review response）**：当前正式本地结果为 run `rx-20261023-192450`，计划 `tests/rx-plan-1.2.0.json`，**30 PASS + 1 预期 TIMEOUT**，schema PASS。新增逐笔 ACCEPT/CONSUME/DROP/CANCEL 有序账本（N8 87、N16 105、N234 63 项，TB 断言通过），各配置 `last_check_cycle + 32` 预算（N8 4883、N16 10997、N234 106285），共享 `rx_ledger_check.svh` 比较器，负向额外事件使用同一机制；watchdog 仅接受 TB 正常触发，进程超时记 FAIL。旧 1.1.0/1.0.0 结果保留为历史。

> **2026-10-23 1.1.0 更新（review response）**：当前正式本地结果改为 `results.json` / run `rx-20261023-180309`，计划 `tests/rx-plan-1.1.0.json`（`B-UART-RX-PLAN-1.1.0`，SHA256 `3CFED893…15E3`），**30 PASS + 1 预期 TIMEOUT**，schema PASS。新增 clear+new OV、DATA/START/STOP reset、额外 valid checker 控制、事件计数、硬上限和负向 watchdog。旧 `1.0.0` 计划/结果/日志/VCD 保留为历史，不作为当前最终本地结果。下面 1.0.0 段落保留原样，仅作历史记录；当前证据以 `work/B-RETURN/increment-20261023-1740/README.md`、`MODULE_STATUS.json` 和本文件顶部更新为准。

- **任务**：B-UART-RX（UART 8N1 接收核心）
- **模块**：`uart_rx`
- **模块版本**：`1.0.0`
- **合同**：`PERIPH-CORE-RX-1.0` / `1.0.0`，`APPROVED / RELEASED`
- **合同 SHA256**：`E1DA0CC3BC1E9F64285B5846369D910338FF2289652E297629DDA9F5BAEEA706`
- **收件回执**：`docs/MAINLINE-RX-RECEIPT-20261023.md`，实际收件 `2026-10-23T11:27:47+08:00`
- **执行计划**：`tests/rx-plan-1.0.0.json`，`B-UART-RX-PLAN-1.0.0`
- **计划 SHA256**：`D6C9604B9788DF28921D2351196701ABE8A8493301419DE5C611385CC49BCDA1`
- **最终本地 ACTUAL**：`results.json`，run_id `rx-20261023-115726`
- **结果**：30 PASS + 1 预期 TIMEOUT（COM-02 watchdog）；schema 机检 PASS
- **更新时间**：`2026-10-23T11:43:55+08:00`（Asia/Shanghai）
- **硬件状态**：未操作，保持 `STOPPED`；未启动 PDS、未扫描 JTAG、未供电/下载/Flash、未改 SCBV/跳线/温控。

## 1. 结论

- RX 合同已获主线书面批准；RX 实现、独立 TB、负向 checker、watchdog 和 N=8/16/234 有界仿真完成。
- 三个配置均 `PASS`：N8/N16/N234；`COM-02` 的 `TIMEOUT` 是故意 watchdog 负向能力，不是功能 FAIL。
- `N<8` 非法配置在仿真开始显式拒绝（`RX_ILLEGAL_CLKS_PER_BIT=4 minimum=8`）。
- 该结果是队员侧本地 ACTUAL；**不是**主线复现、最终验收、接口兼容、系统集成或硬件验证。
- `LOCAL-REGIF / B-REGIF` 本批明确未启动；未做地址/总线/MMIO/CPU/SoC。

## 2. 配置与验收矩阵

| 配置 | 结果 | 证据 |
|---|---|---|
| N=8 | PASS | `logs/rx-20261023-115726/run_N8.log`；`waves/rx-20261023-115726/uart_rx_N8.vcd`（243,103 B） |
| N=16 | PASS | `run_N16.log`；`uart_rx_N16.vcd`（562,716 B） |
| N=234 | PASS | `run_N234.log`；`uart_rx_N234.vcd`（5,549,812 B） |
| 负向 checker | PASS | `tb_uart_rx_neg.sv`；`NEG_CONTROL_PASS` + `NEG_CHECKER_PASS` |
| watchdog | TIMEOUT（预期） | `TB_WATCHDOG_TIMEOUT cycles=201 limit=200` |
| 非法 N=4 | PASS（拒绝） | `RX_ILLEGAL_CLKS_PER_BIT=4 minimum=8` |
| schema | PASS | `logs/rx-20261023-115726/schema_validate.log` |

| 验收项 | 结果 | 覆盖摘要 |
|---|---|---|
| RX-01 | PASS | 0x00/FF/55/AA/01/80/7E；S_postNBA 的 valid/data；消费后 data 保持 |
| RX-02 | PASS | N8/16 四相位（0.1/0.3/0.6/0.9T）× 0x55/AA；N234 代表帧 |
| RX-03 | PASS | N16 16 帧、N8 8 帧、N234 2 帧背靠背；raw 10NT；`d_next=d+10N`，无 +1/idle |
| RX-04 | PASS（N16） | 假 start L=7/8；随后好帧 0x5A |
| RX-05 | PASS | 坏 stop、旧邮箱保留/消费、持续低、满邮箱、clear/new-error 竞争 |
| RX-06 | PASS | S_postNBA；valid&&!ready 保持 24 周期；一次消费；data 保持 |
| RX-07 | PASS | 满邮箱丢新保旧、overrun sticky、clear、同字节不去重 |
| RX-08 | PASS | 同沿消费旧 + 新帧替换；valid 保持；无 overrun；S+1 消费 |
| RX-09 | PASS | 帧中复位、释放持续低→见高→好帧、clear 与新错误同沿 |
| RX-10/COM-05 | PASS | 独立负向 checker 故意期望 0xAA，DUT 0x55 被检出 |
| COM-01 | PASS | 计划/5 个 artifact 哈希在 DUT 前匹配 |
| COM-02 | TIMEOUT（预期） | 有界 watchdog 能力，不记功能 FAIL |
| COM-03 | PASS | compile 60s/run 30s；TB_MAX_CYCLES=200000；硬上限 1,000,000 |
| COM-04 | PASS | 新 run_id、新日志、新 VCD；未复用旧结果 |
| COM-06 | PASS | N<8 显式拒绝 |

## 3. 关键实现

- 8N1：1 start 低、8 data LSB-first、1 stop 高、空闲高；无 parity/FIFO/流控/BREAK。
- `CLKS_PER_BIT` 默认 16，`N>=8`；`N<8` 显式拒绝。
- 恰好两级同步器，异步复位置 1；主逻辑只读沿前第二级；`d=E2`。
- 采样：start `d+floor(N/2)`；data `d+N+floor(N/2)+k*N`；stop `S=d+9N+floor(N/2)`。
- 好 stop 在 `S` 沿 NBA 后发布，不额外推到 S+1。
- 背靠背 raw 严格 `10NT`；同相位 `d_next=d+10N`，不插入 idle。
- 单字节邮箱；同沿消费旧+新替换；满且未消费丢新保旧置 overrun；坏 stop 不写邮箱。
- `frame_error`/`overrun` 独立 sticky；clear 与 new error 同沿按每位新错优先。
- 复位取消在途帧；释放后预热、见高再武装；持续低不伪造帧/错误。

## 4. 文件

- `src/uart_rx.v`：SHA256 `BDCD02CA8CBA1CAE9D8A774D336B30B43E9457834856234BD7C2BA8AE1719F34`
- `tb/tb_uart_rx.sv`：SHA256 `8FC755C4124D45F565CBB06DF466813382B7057CD8EF537FF6BBB65858ADE0C5`
- `tb/tb_uart_rx_neg.sv`：SHA256 `33179167B6F5311A64DBEAB1F0C9A1EEDC155A33963D42761C0B7FCE252A4B59`
- `tb/tb_uart_rx_watchdog.sv`：SHA256 `0F9C2159F2FFD76F0D84A34C39721648AAFF7528B7B1604E48C6D16D299E2BD9`
- `tb/tb_uart_rx_illegal.sv`：SHA256 `5FF8F379FB5DAED06A07B51B2E902182CA806AB7D7CADCDDE3C3C5BCE10DC191`
- `tests/rx-plan-1.0.0.json`、`tests/rx-plan-1.0.0.sha256`
- `scripts/run_rx.py`
- `results.json`
- `logs/rx-20261023-115726/`、`waves/rx-20261023-115726/`
- `docs/MAINLINE-RX-RECEIPT-20261023.md`、`docs/MIGRATION-0.1.0-to-1.0.0.md`
- `docs/rx-design.md`、`docs/rx.diff`
- `docs/SHA256SUMS-BUARTRX-v1.txt`（104 项实际文件，含保留的旧运行证据；清单自身排除）

## 5. 保留的旧计划

- `tests/rx-plan.json`、`tests/rx-plan.sha256`、`docs/rx-sampling.md` 保留原样；旧计划 `B-UART-RX-PLAN-0.1.0-DRAFT`，SHA256 `19AC1882EE000F4DA74792081A43EE8D8E702A6E30C9F671AF5185F2D52C5864`。
- 旧计划中的 `d+10N+1`、`S+1` 等待确认项已由合同纠正；迁移见 `docs/MIGRATION-0.1.0-to-1.0.0.md`。
- 不把旧计划或模型迁移称为 DUT 回归。

## 6. 边界与下一步

- 未做：PDS 综合/布局布线/时序/资源/功耗、JTAG、上电/下载/Flash、板级环回/温控、物理 MTBF/噪声/任意 baud 容差。
- 未做：B-REGIF、地址/总线/MMIO、CPU/SoC/CoreMark/Timer/启动工具。
- 下一步：B-RETURN 阶段返回树净目录复现、文件清单/diff/ZIP 安全检查、主线复现/接收窗口复核。阶段返回前不得把本结果升级为最终验收。
- 硬件继续 `STOPPED`；未获单独授权前不操作设备。
