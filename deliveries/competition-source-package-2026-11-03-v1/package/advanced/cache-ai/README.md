# 独立 Cache / AI M0 交付

本目录为本轮唯一新增根；不与CPU/SoC集成，不改变主线CoreMark长测。
结论仅为独立模块原型及有限RTL仿真。AI使用合成数据，未移植真实模型。

- 主线审核结论与分层状态：MAINLINE_HANDOFF.md。
- 设计/实现接口：INTERFACES.md、cache.sv、backend.sv、fc.sv。
- 先冻结计划/预期：cache_plan.md、cache_supplement_plan.md、ai_plan.md；
  vectors/、ai_vectors/及三个冻结SHA清单；参考生成器reference_*.py。
- 逐项结果与量化对照：CACHE_REPORT.md、CACHE_COMPARISON.csv、CACHE*_RESULTS.json、
  AI_REPORT.md、AI_RESULTS.json、AI_QUANTIZATION.json。
- 原始进程输出与资源回执：logs/*.log、*.json；负向测试预期exit1，未混作正向PASS。
- 波形：cache_protocol.vcd、cache_reset.vcd、cache_held.vcd、ai_rounding.vcd、ai_reset.vcd。
- 独立新副本复跑：recheck-001/，含相同测试完整新日志、回执、结果、波形及自动检查入口。
- SHA256SUMS.txt覆盖全目录文件（清单自身除外）；不是Git提交状态证明。

在此目录普通PowerShell运行：

```powershell
python check_delivery.py
```

此入口重新核验冻结SHA、逐项预期/实际数据、原始日志、协议标记、资源回执和交付SHA。
不启动仿真，不触碰主线。正常Python运行，不使用-O关闭断言。

若需另一次复跑，应复制本交付至**同一项目内的新独立目录**，排除既有logs、结果、
波形、*.vvp、recheck-001及SHA256SUMS.txt，然后依次 `python run.py cache`、
`python run.py cache-supplement`、`python run.py ai`、`python check_delivery.py`。
运行器拒绝覆盖既有日志，避免历史失败/结果被静默替换；不要重新生成冻结向量覆盖原件。
check_delivery.py --replay为一次性新建recheck-001的入口，本交付已经使用，重复调用会拒绝。

每个编译/仿真最长20秒，BELOW_NORMAL优先级；Job Object每进程256MiB、全Job384MiB、
最多4个编译子进程，结束关闭Job仅清本任务进程树。最终运行器在受限Job中恢复挂起子进程。
目录64MiB、单日志1MiB由20ms轮询守卫，属于软件预算而非文件系统硬配额，极端瞬时写入
可能超过采样阈值；有限TB还有100000/30000拍watchdog，波形只在指定五个短用例生成。
没有全局kill/进程调优，不能用本报告推断主线实时运行或温度状态。

既有工具：项目内Icarus Verilog13.0便携版及既有Python；没有安装、环境修改或PDS调用。
编译器数组敏感性提示原样保留于Cache编译日志；AI编译无输出诊断。
初始cache_compile_v1.log为空：运行器工具路径错误导致CreateProcess前WinError2，
未编译/仿真；修正后cache_compile_v2及后续通过，未用失败产物运行。
