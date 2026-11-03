# 包装运行与复现命令

工作目录：`work/regif/txgpio-m1`；工具显式路径，未修改 PATH。

## 1. 计划/hash gate

```
C:\Users\ANON_USER\AppData\Local\Programs\Python\Python312-embed\python.exe -X utf8 scripts/run_regif_m1.py
```

runner 先核对：

- `tests/w01-w10-plan-1.0.5.json` 与 `.sha256`
- `src/local_regif_txgpio_m1.v` SHA `5C81EE8F...64FA`
- `../../peripherals/src/uart_tx.v` SHA `21044928...988C`
- `tb/regif_tx_public_monitor.sv` SHA `A7C857C1...6CFB`
- `../../peripherals/gpio/src/gpio_core.v` SHA `03380919...F95E`
- `tb/tb_local_regif_txgpio_m1.sv` SHA `7F0C1060...793B`

任一不符时不编译、不运行 DUT。

## 2. N16 编译/运行

在 `work/regif/txgpio-m1`：

```
D:\iverilog\bin\iverilog.exe -B D:\iverilog\lib\ivl -g2012 -Wall \
  -s tb_local_regif_txgpio_m1 -DCLKS_PER_BIT=16 -DTB_MAX_CYCLES=300000 \
  -o waves/<run>/regif_m1_N16.vvp \
  src/local_regif_txgpio_m1.v ../../peripherals/src/uart_tx.v \
  ../../peripherals/gpio/src/gpio_core.v tb/regif_tx_public_monitor.sv \
  tb/tb_local_regif_txgpio_m1.sv

D:\iverilog\bin\vvp.exe -N -M- -MD:\iverilog\lib\ivl \
  waves/<run>/regif_m1_N16.vvp +WAVE_FILE=waves/<run>/regif_m1_N16.vcd
```

## 3. N234 最小 smoke

同 N16，将 `-DCLKS_PER_BIT=16` 改为 `-DCLKS_PER_BIT=234`；TB 只运行 W05/W06/W09-N234。

## 4. 预期 marker

- N16：`REGIF_M1_SELFCHECK_PASS accepted_tx=9 accepted_gpio=6 rejected=11 frames=6 requests=26 complete=6 cancel=3 bad_stop=0`；首请求 edge=9
- N234：`... accepted_tx=9 accepted_gpio=0 rejected=1 frames=6 requests=10 complete=6 cancel=3 bad_stop=0`；首请求 edge=6
- W10：`W10_CONTROL_PASS`、`W10_NEGATIVE_DETECTED wrong-byte`、`W10_COUNT_PASS`
- 任何 `CHK_FAIL`/`TEST_FAIL`/watchdog 均为 FAIL。

## 5. schema

在包根目录：

```
C:\Users\ANON_USER\AppData\Local\Programs\Python\Python312-embed\python.exe -X utf8 \
  scripts/schema_validate.py --schema templates/results.schema.json \
  --data work/regif/txgpio-m1/results.json
```

结果：`schema_check: PASS`。

## 6. 官方证据

- 1.0.5 正式运行：`regif-m1-20261025-210743`；N16/N234 PASS，VCD 非空，schema PASS；`results.json` 13 行。
- 1.0.2/1.0.1/1.0.0 运行保留为历史；1.0.0 无 VCD，不作为最终证据。
- 原始日志：`logs/regif-m1-20261025-210743/`；普通 VCD：`waves/regif-m1-20261025-210743/`（N16 131109 B、N234 1930509 B）。
- runner 日志包含原生 rc、超时、日志截断、cleanup 状态/耗时。共享 runner 只用自身测试进程，cleanup ≤8 s、总 ≤15 s。

## 7. 未运行/未声称

- N8 包装全矩阵、PDS/时序/资源/功耗、JTAG/供电/Flash/板级、CPU/SoC 集成、RX 包装均未做；硬件 STOPPED。
