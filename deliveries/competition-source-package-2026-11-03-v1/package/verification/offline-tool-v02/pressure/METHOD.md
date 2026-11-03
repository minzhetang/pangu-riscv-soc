# Pressure / 资源实测说明

- 生成器：`tests/generate.py`，确定性生成 1/16/128MiB 的合法 EDGE 流，expected/actual 各一份；运行在包外临时目录，不进入返回包。
- S01 记录数：1MiB 11,155；16MiB 175,921；128MiB 1,395,143（每流，均 <6,000,000）。
- 实际字节：1MiB 1,048,619；16MiB 16,777,311；128MiB 134,217,767（每流，均 <512MiB）。
- S02：cycle `4294967301` 等 >2^32 的十进制字段，3 条；不代表 >4GB 实际文件 I/O。
- 峰值测量：父进程轮询 Windows `GetProcessMemoryInfo(...).PeakWorkingSetSize`，worker 自身也报告同一 API；父/worker 分别记录。父进程只读 case/结果/日志，不流式读取 record 文件。
- 限额：worker 峰值 <=268,435,456 B；单 case 180s + 8s cleanup；全 suite <=1800s；本次 worker 峰值约 21.4MiB，远低于限额。
- `pressure/results.json` 为最终实测；`S01-*.json`、`S02.json` 为逐例原始结果副本。
