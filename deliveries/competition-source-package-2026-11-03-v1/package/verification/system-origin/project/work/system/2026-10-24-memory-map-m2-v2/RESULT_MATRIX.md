# 逐项实测

|项目|结果|证据|
|---|---|---|
|selftest-0 normal selftest|PASS|D:\A_FPGA_Comp\work\system\2026-10-24-memory-map-m2-v2\logs\selftest-0\stdout.log|
|selftest-1 explicit protocol rejection|PASS|D:\A_FPGA_Comp\work\system\2026-10-24-memory-map-m2-v2\logs\selftest-1\stdout.log|
|selftest-2 explicit protocol rejection|PASS|D:\A_FPGA_Comp\work\system\2026-10-24-memory-map-m2-v2\logs\selftest-2\stdout.log|
|selftest-3 explicit protocol rejection|PASS|D:\A_FPGA_Comp\work\system\2026-10-24-memory-map-m2-v2\logs\selftest-3\stdout.log|

|CPU程序|结果|物理沿|推进沿|stall/flush|墙时秒|
|---|---|---:|---:|---|---:|
|P01|PASS|23|11|1/0|0.657|
|P02|PASS|37|18|1/0|0.657|
|P03T|PASS|27|13|1/1|0.657|
|P03N|PASS|27|13|1/0|0.687|
|P04|PASS|27|13|0/1|0.672|
|P05|PASS|19|9|0/0|0.672|
|cboot|PASS|1285|642|2/97|0.781|
|performance|PASS|2202631|1101315|22483/155217|119.797|
|validation|PASS|2361451|1180725|23001/168293|126.609|
