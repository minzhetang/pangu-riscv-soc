# B离线R1 v02审收回复包 / 1.0.0

2026-10-27。先读TEAMMATE_REPLY.md，再读A_RESULTS.json、A_FROZEN_PLAN.json。总体**有条件接收**：C0–C3具体反例已关闭；主机25项独立复现22 PASS、3 FAIL，资源工具生产准入未通过。不是CPU/ISA/系统/硬件结论。

只需转交本整个目录，不必重发已有v02或65MB输入包。A未代发。剩余工作仍为已批D158的三组守卫差额，不是新功能/新核心任务。

复现三个有限反例（Windows、现有普通Python、无安装）：

```text
<EXISTING_PYTHON> -B REPRODUCE_GUARDS.py --tool-root <RETURN_V02> --input-root <ORIGINAL_A_INPUT_PACKAGE> --work <FRESH_WORK_OUTSIDE_INPUT_AND_TOOL>
```

默认核当前v02完整manifest SHA；新整改候选需先生成真实清单，再显式用 --manifest-sha 提供其SHA，不跳过校验。原件只读，新工作目录复制5MB工具及小型夹具。当前v02预期复现3个FAIL，退出1；修复后须全部PASS，不能改预期。两个资源夹具只测真实parent执行路径，不是记录比较/CPU证据。内存夹具仅申请并触摸32MiB，时间夹具沿用B固定sleep_forever，日志夹具沿用B固定5MiB flood；不接受任意外部命令。所有新产物只落独立work。

probes中的脚本为A实际复验代码同字节副本。完整独立25项结果附后；原压力/54自测仅作B证据，A没有重跑全54或128MiB压力。无需为了本次回复重跑外设、CPU、DUT或PDS。
