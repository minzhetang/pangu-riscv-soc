# 实际命令与结果入口（不是要求再次执行）

工具：已核可信MSYS2便携Icarus/vvp13.0；D:\A_FPGA_Comp\tools\iverilog-13.0-msys2-ucrt64\ucrt64\bin\iverilog.exe / vvp.exe；-B及VPI目录为同根ucrt64\lib\ivl。Python使用已存在可信解释器绝对路径，均-B、不改PATH。

本次原生实跑完整argv/cwd/超时/rc/耗时、stdout/stderr路径在独立工作目录：
`D:\A_FPGA_Comp\work\peripheral-review\2026-10-25-increment-2335\plan.json、compile-result.json、resume-plan.json、compile-result-resume.json、run-result.json、w06-reset-plan.json、w06-reset-compile.json、w06-reset-run.json`及`logs/{compile,run}-*/process.json`。每编译60s、运行30s；正式RX预算5045/11319/110967，包装300000，A W0612000物理沿。实际执行过的清单优先于示例。临时源/新VVP/VCD都在该新目录，不执行收到的VVP/PYC/入口脚本。

总12编译进程：11成功、1因A额外-s选项顺序错误失败，原始诊断保留；11运行：5正式配置、2小负向、2 A首版W06（time0初始化X失败）、2修正A复位事件后的W06v2通过。不是11/11全功能通过。源路径UTF8准备错误在调用编译器前由guard截停，不算DUT；所有旧plan/失败未覆盖。全部原生运行正常$finish/rc0，无超时/日志截断；不能用它们替代逐信号判定。

只读解析命令使用本证据目录自己的intake/waves/new_runs/semantic_checks/coverage_close脚本；收到的Python只阅读，需控制验证时AST抽取已审纯函数，不执行其模块入口、安装/清树或系统调用。原5波形分析不算新DUT；new-run-summary/REVIEW_RESULTS分列新运行与严格账本失败。W06可转交副本含完整实际process参数，B无需重跑。

本轮无CPU/CoreMark/PDS/许可查询/硬件操作。新批外部工具执行逐批核工具权限，不把历史许可转永久授权；下轮执行仍按当轮授权判断。
