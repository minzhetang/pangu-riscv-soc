# 执行与复查入口（F146，不是新授权或一键复现）

工作目录D:\A_FPGA_Comp，Python为既有`C:\Users\tamii\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`，均`-B`。Icarus/vvp 13.0使用tools目录绝对路径及-B/VPI库，不改PATH。源13项SHA见RESULTS，手工冻结计划manual-plan、core-manual-plan，编译参数initial-compile-plan、core-compile-plan，PDS完整调用pds-plan。程序/初始化与F143原O2相同。外部工具审批已消费，不由本文件延展。

本地`COMMANDS.md`保存18个编译、832个DUT和1次PDS的**完整参数数组、cwd、进程超时、原生rc和实际耗时**（约794KB，未随Git分发）。每个原始process.json与stdout/stderr也保留，CASE_RESULTS.csv逐例指向它们。不得无检查地重跑准备/冻结脚本或覆盖既有目录。

16个快速编译按initial-compile-plan固定目标（14组默认+PF0/PF1）。首个定向v1仅RAM文本格式误判，check_redirect_v2在同输出复查，resume_validation接续其余66真实运行及763回归。两官方primitive CoreMark编译按core-compile-plan；core_stage执行两旧O2程序，6000000物理拍/每进程360秒上限。定向4000拍/30秒上限。实际18编译/832DUT总数不得再加同输出复核/负控。

依次记录的检查/解析入口为check_redirect_v2、check_coremark、fetch_audit、audit_prefetch_wave、audit_uart、audit_wave、checker_negatives、quality_compare；它们依赖既有冻结数据和本机合法模型，不是通用安装器。PDS仅cost_stage固定计划实际跑一次；cost_stage_v2仅在同产物修正已核网名层级别名、128连接计数仍严格。两原失败和v1脚本保留。RESULTS/CASE_RESULTS/报告是分层结果入口。

PDS仅compile/synthesize/map/place-route/report_timing，无bitstream；内部27MHz通过而constant-probe7→8根因未知，候选不替换F143。所有硬件/授权/工具边界保持。专有模型、工具、授权、镜像和大型产物不入仓，不宣称干净克隆可直接复现。
