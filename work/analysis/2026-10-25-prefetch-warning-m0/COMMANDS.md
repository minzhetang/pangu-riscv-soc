# F147实际分析入口与边界

工作目录D:\A_FPGA_Comp；既有Python绝对路径为C:\Users\tamii\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe，均加-B，不修改PATH。原生分析退出后才检查新JSON；无外部编译器/DUT/PDS执行。

以下是最终接受的只读分析命令，**不是要求覆盖当前输出重跑**。graph文件使用独占创建；新复查应另建目录。输入SHA、库方向和覆盖范围见INPUTS及各graph；PDS程序/模型仅被读取，没有执行。

```
python -B work\analysis\2026-10-25-prefetch-warning-m0\netlist_graph.py 2026-10-25-board-top-m1
python -B work\analysis\2026-10-25-prefetch-warning-m0\netlist_graph.py 2026-10-25-resolved-target-fetch-m1
python -B work\analysis\2026-10-25-prefetch-warning-m0\netlist_graph.py 2026-10-25-resolved-target-fetch-m1 precise
python -B work\analysis\2026-10-25-prefetch-warning-m0\netlist_graph.py 2026-10-25-board-top-m1 constrained
python -B work\analysis\2026-10-25-prefetch-warning-m0\netlist_graph.py 2026-10-25-resolved-target-fetch-m1 constrained
python -B work\analysis\2026-10-25-prefetch-warning-m0\collect_evidence.py
python -B work\analysis\2026-10-25-prefetch-warning-m0\verify_inputs.py
```

最终接受命令原生rc=0、各约0.5–1.3秒，进程上限由普通shell执行默认10秒管理；无无限仿真。自检只为静态解析器/布尔关系，不统计成DUT。

开发诊断保留：第一次graph严格拒绝未列GTP_INBUF（rc1），查当前官方端口后补明确INBUF/OUTBUF；最终粗略图仍有残余，原JSON保留。精化依次区分INIT/双输出、实际直接绑脚，接受两最终0残余图。collect_evidence前两次rc1分别是旧实例名字不同、33FF外另有同名LUT，改为真实端口定位并按DFF类型计数；无旧源/预期变化。只读终端输出曾遇GBK显示异常，使用UTF-8后读取成功，不是工具/CPU失败。

目录枚举/rg、sqlite3只读QCH并zlib解压HTML/TXT/XML、原VM结构读取使用Python标准库；不执行帮助内命令，不复制模型/完整帮助或日志信息头。官方域名两公开搜索无结果，不证明无勘误。硬件停止、候选不升级；PANGO_QUESTIONS只准备未发送。
