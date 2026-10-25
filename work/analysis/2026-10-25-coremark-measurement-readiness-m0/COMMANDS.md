# 本轮实际执行与复查方法

实际只运行现有可信Python解释器-B执行本目录自写audit.py：读取固定68输入，逐SHA及ELF PT_LOAD映射，完整流式遍历旧两例trace/bus，分计算窗口和外围计字节/事件，预算算术5边界自检。没有运行任何目标ELF、GCC/iverilog/vvp、参考模型、PDS或硬件。write_report.py只写本轮报告与下一有限范围，不实施C/TB改动。

权威输入/输出：INPUTS.json、STREAM_PARTITIONS.json、SUMMARY.json、CODE_ANCHORS.json、CALCULATOR_SELFTEST.json、postflight.json。反查旧动态结果在F143原process/check/trace/bus中，本轮只读复用，不能把它们重审写成新DUT。两个官方固定URL本轮实际打开，本地README/裸机指南/官方六源对可信归档已核同；没下载/执行新软件。早期source-receipt失败保留，用后来的source-integrity-review作SHA权威。

如需重跑本只读分析，须在新的独立目录保存输出或先调整输出位置；脚本open('x')保护已有证据，不覆盖旧结果。本轮没有安装或修改PATH/许可证，没有扫描整机/枚举设备。下一scope文件明确PENDING，不能看到文件就执行未经批准的实施/长跑。
