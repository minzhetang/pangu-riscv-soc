# 来源与提交副本处理

MANIFEST.json逐文件记录实际包路径、源项目相对位置、源SHA、包SHA及处理类型。源位置用于追溯，并非要求评委有A电脑D盘：主要代码已实际复制到包中，不能用本地路径假装交付。

复制时先逐字节核源SHA→副本SHA，再仅对文档、日志、JSON、patch和链接map等元数据中的C:/Users或C:\Users本地账号目录改为ANON_USER。原件不改，功能RTL、TB、C/汇编、冻结输入/预期及二进制保持原字节；具体哪些元数据改变可由manifest的changes字段识别。匿名化会使部分原“历史总清单”不能直接校验本提交副本，不能因此静默改写旧SHA。当前包完整性用根SHA256SUMS与MANIFEST。

一个明确例外是verification/streaming/project/work/fpga/2026-10-25-compile-quality-m1/finalize_evidence.py：仅将其历史COMMANDS.md生成文字中Python程序位置的用户目录匿名化，未改变可执行逻辑、运行路径配置或检查规则。静态审查逐字符确认该副本恰好只有这一处替换；它属于历史证据整理入口，不作为本包便携执行入口。全部其他项目Python脚本与原件同字节。

同字节继承材料可有多个源位置，equivalent_sources说明来源一致，不混为新版本。RX共享账本头只补了已冻结同字节依赖副本，没有修订RX实现。CoreMark完整许可保留，未改第三方文件。

本次没有编辑源码修“可跑性”、重建算法预期或删掉失败判定。代码有旧BASE/一次性门或缺全量历史产物时，按REPRODUCIBILITY注明范围，而不宣称全部开箱可复现。历史工具和候选失败保留准确表述，原始工作区证据不删除。
