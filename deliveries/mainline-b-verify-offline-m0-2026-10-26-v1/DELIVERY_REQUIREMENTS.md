# 一次集中返回 / 最低交付

目录 `B-VERIFY-OFFLINE-M0-return-v01/`；不需ZIP，不重发原冻结65MB输入。若压缩，另算ZIP SHA且保留目录。只写自己新目录，原v02/旧根失败保持。

- START_HERE.md：入口、依赖、局限、PASS_LOCAL/PARTIAL及未测项；RECEIPT.json填写实际接收和工时/返回容量，不推定A验收。
- RUN.py及所有新源码；frozen依赖可带同字节副本并核SHA，或明确依赖本任务包根；不得依赖主工程/旧B绝对路径、PDS或新安装。
- tests/PLAN.json：在执行前冻结每例输入生成规则/种子、人工预期/首错、退出码/限额，引用ACCEPTANCE_PLAN的25类；交计划冻结SHA及时间。
- tests/results.json：逐例目的/输入/预期/实际/status/原生rc/PASS/FAIL/TIMEOUT/终止原因/是否完整消费、实际字节/记录、输出诊断与资源；列全配置，不只总PASS。P02四流逐笔重放9378498记录，不称CPU新验证。
- COMMANDS.md与有界原日志：完整可复现参数、cwd、Python版本、rc、时间、是否截断和清理结果；日志截断的功能证据不得PASS。
- diagnostics/：首错序号/类别/字段/期望实际、邻域；保留无差异、首/中/尾、跨4MiB块边界以及后续坏尾部的明确正负例。新增生成器不得通过调用被测判定器生成预期。
- pressure/results.json：真实1/16/128MiB每侧消费、记录数、耗时、父与worker峰值/测法和预算判断；>2^31/>2^32周期字段另列，不冒称>4GB实际文件。生成器可确定重建，不把所有压力文件塞进返回包。
- 独立空目录/中文空格路径：只带返回目录+本任务输入包，实际运行同一命令，说明如何验证无历史BASE/环境依赖。
- OPEN_ITEMS.md、CHANGED_FILES.json、SHA256SUMS.txt、来源与冻结依赖SHA；返回<=128MiB，无缓存/PYC/VVP/工具/许可/机器标识。保留真实失败而非只拷贝PASS。

B交完整可审脚本，A先读再按权限复现。外部命令执行、内核修复、格式变更、安装/硬件不在本包；集中问题单交A处理。新增任务不要求修改旧根OPEN_PREEXISTING，也不要求重跑UART/GPIO/RX DUT或重新封v02。

阶段结束交真实完成部分，未完标NOT_RUN/FAIL/PARTIAL与最小剩余，不把约一天目标变成降标准。既有10/27 18:00外设窗口保持；如新任务容量冲突需回报，不自行改承诺。
