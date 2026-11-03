# 实际命令与复现入口

2026-10-23，阶段A-COREMARK-CORRECTNESS-M1。以下是实际执行历史，不要原地复跑或覆盖。复现应使用新输出目录，按所列request.json的固定argv/输入SHA执行，并保留相同预期；目录守卫会拒绝覆盖。

```powershell
Set-Location -LiteralPath 'D:\A_FPGA_Comp'
# 下列脚本均由本项目编写；不是下载包内程序。普通权限，均使用此Python绝对路径及-B。
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'work/system/2026-10-23-coremark-correctness-m1/prepare_and_build.py' prepare
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'work/system/2026-10-23-coremark-correctness-m1/prepare_and_build.py' build
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'work/system/2026-10-23-coremark-correctness-m1/reference_coremark.py'
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'work/system/2026-10-23-coremark-correctness-m1/check_and_run.py' freeze
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'work/system/2026-10-23-coremark-correctness-m1/check_and_run.py' compile
# 上一步普通编译真实0xC0000005，残留VVP未执行。
```

独立获批固定一次、非管理员、沙箱外编译（仅编译，60秒）后，回到普通环境运行：

```powershell
# 此命令是已消费的单次外部许可，不代表今后可自动在沙箱外复用。
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'D:\A_FPGA_Comp\work\system\2026-10-23-coremark-correctness-m1\check_and_run.py' compile-external
# 以下普通权限，每参数1次；分别180秒、1000万周期限。
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'work/system/2026-10-23-coremark-correctness-m1/check_and_run.py' run
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'work/system/2026-10-23-coremark-correctness-m1/review_windows.py'
```

独立VCD复核定位只采初始窗口。保持原冻结TB、输入、期望和双参数结果不动，新增`tb_coremark_wave_v2.sv`，唯一行为差异为采集条件`holds==0`改`holds<=1`，加解释注释。`wave-v2-frozen.json`核精确diff并冻结v2输入。

```powershell
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'work/system/2026-10-23-coremark-correctness-m1/wave_v2.py' prepare
# 以下另获一次非管理员外部编译许可，60秒；原CPU不变。
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'D:\A_FPGA_Comp\work\system\2026-10-23-coremark-correctness-m1\wave_v2.py' compile-external
# 普通权限只复跑performance，同原镜像/原预期，180秒/1000万周期限。
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'work/system/2026-10-23-coremark-correctness-m1/wave_v2.py' run
& 'C:\Users\ANON_USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'work/system/2026-10-23-coremark-correctness-m1/finalize_evidence.py'
```

每个目标工具的**完整argv、cwd、超时**：

- GCC/ELF检查：`performance`、`validation`下`compile/readelf/objdump/undefined/objcopy/request.json`及各自process/stdout/stderr。
- Icarus：`compile-ordinary-01/request.json`（失败保留）、`compile-external-01/request.json`、`compile-wave-v2-external-01/request.json`。
- vvp：两个参数下`dut-run-01/run/request.json`及performance下`dut-wave-v2-01/run/request.json`。
- Icarus绝对路径`D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe`，带`-B D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl -g2012 -Wall -s tb_coremark`；四RTL加memory_model及指定TB。
- vvp同目录`vvp.exe`，带`-N -M- -MD:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\lib\ivl`，指定成功VVP及`+IMAGE=../image.hex +WORDS=3792`或`3794`。不改PATH。

源码取得另有实际网络记录：普通PowerShell socket权限错误；`fetch_official.py`经网络许可后API403限流；经另一限定网络许可执行`fetch_direct.py`，archive/raw12文件同、五C MD5同，但上游header MD5过期导致保存错误停止。随后只读核固定官方commit差异及内存还原注释MD5，`source-integrity-review.json`登记来源完整性结论，未重下载/修改header/执行包内脚本。下载函数不会执行安装器或源码自带命令。

`get_time/time_in_secs`在本CRC专用port明确标为无计时实现并返回0，不是实测时间，官方不足10秒提示保持。不能将本阶段日志用于正式CoreMark成绩或FPGA性能。
