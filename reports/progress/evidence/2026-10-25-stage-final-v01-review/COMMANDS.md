# 本机实际命令入口

现有工具`D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe/vvp.exe`，实际版本13.0沿既有验证；-B及-M库为同根lib/ivl。普通用户；没有安装/环境/授权修改或破解软件。

7次固定新编译（60s/项）完整argv/cwd在`work/peripheral-review/2026-10-25-stage-final-v01/plan.json、compile.json、logs/compile-*/process.json`；本批外部工具许可已用完。7次普通vvp新运行（30s/项）在run.json及logs/run-*/process.json，原始stdout/stderr和新VVP/VCD在同目录。源码11项原/副本SHA和只读observer SHA在plan。没有运行接收包内脚本/VVP/PYC。

审阅解析入口为本目录review.py（安全清单/继承/结构/diff）、final_waves.py（原5配置）、correlate.py（新7运行、共享数组与纯函数变异）、close_checks.py（字段一致性/覆盖/原件保护）。原重审、模型解析/负控不计新DUT。所有7原生编译/运行0、无警告错误/超时并正常finish，只证明进程和限定功能；R1快照/R2原事件沿严格FAIL单列。

自己的首版解析器曾把diff的空白context当分隔，v1结果保留parser-history；v2修正后全代码9文件准确重建，仅5实际元数据块不同。不据解析器初版误报源差异，更未修改任何收到的文件或期望。所有15JSON完整解析，活动矛盾逐项报告。
