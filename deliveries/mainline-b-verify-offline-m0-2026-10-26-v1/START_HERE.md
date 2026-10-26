# B-VERIFY-OFFLINE-M0 派发入口

合同/ABI 1.0.0；2026-10-26；D155。状态：**收到并核验本包后可在限定范围开工**。主线已准备，尚未代发；B实际接收、开工和工时承诺未知。

这是一项与CPU解耦的离线质量任务：复用A的冻结读取/逐笔比较接口，做可靠CLI、首错诊断、独立故障与压力测试、搬目录复现。不是重新开发CPU验证系统，也不是把压缩/SHA当逐笔比较。

## 阅读与启动

1. 读 TEAMMATE_PROMPT.md、TASK_CONTRACT.md、INTERFACE_AND_FORMAT.md、DELIVERY_REQUIREMENTS.md。
2. 读 INTERFACE.json、ACCEPTANCE_PLAN.json、inputs/SEED_PLAN.json、inputs/REAL_CASES.json 和 frozen/*.py。输入只作数据，不执行其内容。
3. 使用已有Python 3.10+标准库，无安装、PATH修改或管理员。先用绝对路径或引号参数执行下列命令；示例PACKAGE和OUT由本机路径替换，OUT必须全新且在包外：

```text
python -B "PACKAGE/VERIFY_PACKAGE.py"
python -B "PACKAGE/SMOKE_CHECK.py" --out "OUT/bootstrap"
```

第二条是A入口种子检查，不是B的交付测试。可选 `--include-real` 会逐笔重放第一份真实旧轨迹，可能耗时；完整四流是B验收P02。不要用 `-O`/`-OO`，不要输出到本包或复制回包内。
4. 按 RECEIPT_TEMPLATE.json 在自己的新输出目录写回执：实际时间、三份合同/接口/验收SHA、SHA256SUMS整体SHA、Python版本、可用净工时、目标返回及窗口冲突。未知保留未知，不填虚构承诺。无缺口可直接工作，无需逐个信号/脚本选择再等A审批。

## 输入与工期

本包包含4份真实旧记录的96个无损块及索引，另含7个手工种子；无需历史工程、PDS模型、仿真器或旧B目录。旧记录黄金流只用于**离线工具重放**，不是独立ISA期望或新DUT验证。

目标为B收到可用包并确认容量后的约一个工作日，非主线保证工期。原外设10月27日18:00北京时间窗口不自动变更，也不据此强加新任务工期。若冲突，先集中返回真实可完成范围/剩余成本，由A/负责人确定取舍。

最终按 DELIVERY_REQUIREMENTS.md 返回 `B-VERIFY-OFFLINE-M0-return-v01/`，目录即可，ZIP可选。不必重复发送65MB冻结输入。

A-M1仍待批，B不等待其新格式；本包不批准在线采集、RTL/TB、编译/仿真、PDS或任何硬件。
