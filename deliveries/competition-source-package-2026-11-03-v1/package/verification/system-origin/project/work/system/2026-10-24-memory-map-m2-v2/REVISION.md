# v2：仅初始化字面量词法修正

2026-10-24。v1首次固定编译rc2，stderr为“input buffer overflow, can't enlarge buffer because scanner uses REJECT”，0DUT；原目录/日志/初始化表/冻结状态完整保留。

本副本仅改自有生成器：单个262144bit十六进制字面量拆为64个4096bit块拼接；每块1024hex字符。拼接位值及源镜像、CPU/存储绑定/TB/期望不改。不重装或改工具。不把初版0DUT写成功。

新增固定最多10目标编译需另经工具权限审批，原批首错停已结束，不复用原许可。准备时核v1/v2初始化表等值。
