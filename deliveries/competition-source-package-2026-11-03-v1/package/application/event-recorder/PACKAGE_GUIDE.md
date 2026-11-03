# 事件记录与故障回溯应用

完整v2代码及依赖位于本目录，研究与快速定量对照的源码另在application/research-origin。firmware/app.c是真正编译并由CPU执行的C程序；DENSE参数选择原始采样对照，不用宿主Python产生板级答案。

规则：GPIO低三位表示0→1→3→7→0；连续两个相同观察才接受状态；stable=1持续20样本触发超时。8条×16B环形事件包含tick/index/state/reason，保留故障前文、触发及2条后文后冻结。满环覆盖、冻结后拒绝、调度过载reason3均有明确计数。记录完成后UART导出，期间停止监测；时间为软件观察时刻，不是输入硬件边沿。

生产参数：SAMPLE_PERIOD=2700000、SAMPLE_COUNT=128、WAIT_SAMPLES=20、AUDIT=0。27MHz标称下100ms采样、12.8s批次。低于采样周期的脉冲可能漏掉，两样本规则还可能过滤较短变化；不是高速逻辑分析仪。板载KEY1–3模拟输入，KEY0复位；LED6采集中，正常末态0xA5，故障0x81。

已有便携入口：build_software.py（明确--gcc-dir和新--output；默认event，可--dense 1）、verification/recheck_reports.py（离线重查原始板级文本）、simulation/tb.sv与memory_sim.sv（真实CPU RTL测试资料）。完整固定bin/ELF/hex、冻结计划、手工预期及检查器均随包；历史脚本没有伪装为新便携入口。

三场景正常/顺序错/超时的实际UART原字节及有限LED观察，见evidence/board。旧失败也留作检查器拒绝控制。误截Codex前台的历史演示图片未用于本代码包。BOARD结果不直接验证快速32样本dense比较，量化仅按各自相同输入/口径解释。

复现说明、工具依赖和哪些入口需要适配见根REPRODUCIBILITY；本轮未执行这些脚本。应用位流/SVF本包省略，程序与ROM静态绑定已核，不能把省略配置文件当作获准硬件下载。
