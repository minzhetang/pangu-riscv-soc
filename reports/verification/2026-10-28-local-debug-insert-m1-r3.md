# 本地观察核R3：工具操作恢复，必需测点尚缺1位，未生成调试位流

2026-10-28；D177批准1.3.0，F170/D178。主线F160/F163有限成果保持，本次不升级实机或正式CoreMark验收。

## 本次确实打通的部分

- 13项窗口策略、6项窗口分类、16项PDS启动门禁主机检查通过；这些是自有控制程序检查，不是新DUT测试。
- PDS PID/创建时间/存活两次实查通过后，才消耗本轮唯一GUI会话。Expiration Reminder已视觉读明：仅6天到期信息和OK按钮；明确点击OK，未改许可/勾选选项或进入注册。
- 主界面、设计载入、配置及列表操作均在同一次会话完成，保存后标题变化正确处理；实际511.125秒，正常原生rc0退出/自有可见窗口0。截图落盘前遮主机标题，截图和原日志仅本地。
- 新综合网表的96保护原件/52冻结输入后验核同；28 DRM18/1792功能INIT与F163一致，只有既定3文件6处非功能标记，没有第7处。

## 原生流程边界的新证据

PDS进程存活且SYNTH_READY已存在时，compile/synthesize目录及目标ADF仍不存在；第一次GUI载入因此真实报Inserter-0001文件不存在。不能把“已提交综合命令”或“PDS还活着”当产物已就绪。

在同次GUI额度内，改读**显式登记的R2配置参考副本**（ins-input/configuration-reference.adf），不是冒充本轮新产物。该参考与当前13生产源逐字节相同；最终PDS停止并实际产生R3综合网表后，剔除已列明的阶段根路径/生成日期，两份**完整VM规范化文本完全一致**，不是只匹配摘要或若干名字。REFERENCE_BINDING_AUDIT保留两SHA和规范化范围。参考读取在最终核同前仅为工程假设，本次后验核实，不作为位流或实机证据。

本次现象支持CLI动作排程与Tcl等待循环互相阻塞的判断；不宣称已证明PDS所有命令普遍异步。下一采用明确进程边界：只综合并退出后核ADF，再GUI配置，再带FIC完整构建，避免依赖未核的脚本内等待语义。

## 140位中还缺什么

实际参考输入列出4898网络（并已后验绑定到本次R3相同规范化VM）：

| 项目 | 结果 |
|---|---|
| 精确名称匹配 | 138位，逐位见NET_MAPPING.json；尚未写入FIC连接。 |
| flush_if | 1位直接别名：冻结RTL中flush_if和flush_id都直接赋值control_flush，原生有soc/cpu_core/flush_id。MAPPING_GATE记录实际索引与源SHA，可确认逻辑等价，未称已连接。 |
| eei_hold | 1位未找到可信映射；新优化未保留该原名。1072个LUT局部静态查找未找到所检模式的直接/反相输出，仅为有限辅助排查，不证明全网表不存在任何等价节点。 |
| 最终连接 | 0位；不以139/140、未知别名或推算值通过验收。 |

此前缺的branch_taken、address低8位、wren、stopped、stop_kind、write_error这14位本次均找到；新增未匹配的flush_if已用直接别名闭合，只剩eei_hold。冻结board_top把soc的stopped/stop_kind/write_error直接接同名顶层线，所选顶层同名别名依据一并记录。

本轮严格只允许旧6处标记，因此**没有擅加eei_hold第7处**。最小提议为在原声明旁加入一个PAP_MARK_DEBUG注释，不改表达式/端口/流水线；准确提议在待批1.4.0包中，尚未修改源码。

## 停止及验收状态

发现缺测点后写GUI_ABORT、未写FIC_READY，不放行Map。GUI正常退出；PDS最终退出rc1，原生明确A_GUI_ABORT，实际560.265秒、无超时/资源上限故障；随后保留的R3综合产物已审。没有重跑PDS或重开GUI，也没有新增帮助查询。

partial debug.fic仅1024点参数，**0数据/clock/reset连接**，SHA256 **4EC70EC2B013C49552EF4AADF5FC39AC69F122D1338C8D0240657F22C8222BEE**。不当成可用调试配置。无新sbit、Map/PnR/最终27MHz时序/插核资源结果；本次许可原生提示6天，非精确到期时间或续期成功。

## 证据及下一步

根目录`D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1-r3/`：

- APPROVAL、PDS-attempt、GUI-attempt、FROZEN_INPUTS、GUI_LAUNCH_GATE：范围/预算/输入/进程活性。
- GUI_ACTIONS、GUI_RESULT、01.png/04.png及原生gui-stdout（截图与日志只本地）：可靠读取/确认提醒和同会话原生操作。
- CONFIGURATION_INPUT_RECEIPT、REFERENCE_BINDING_AUDIT：参考输入身份、完整新旧VM后验核同。
- NET_MAPPING、MAPPING_GATE、HOLD_MAPPING_SEARCH：138精确+1直接别名+1待映射，有限搜索范围明确。
- MEMORY_INIT_AUDIT、POSTFLIGHT、SUMMARY、SHA256SUMS：96原件/52冻结核同、1792 INIT、预算及最终状态。
- source/source-before、DEBUG_METADATA.patch及实际控制脚本/新旧Tcl/原始process收据全部保留；原生日志/厂商ADF/完整源/程序/位流不上传。

下一仅推荐`deliveries/mainline-local-debug-insert-r4-scope-2026-10-28-v1/IMPLEMENTATION_SCOPE.md`1.4.0：额外1个非功能注释，分两次PDS入口（只综合＋完整构建）消除等待耦合，仍1GUI，原功能/程序/约束不变；**待批准，不是已实施**。无需B重派、用户研究信号或无渠道咨询；不执行新DUT/GCC/Icarus，不安装、不操作PDS硬件服务器/JTAG/Flash/供电。over_temp STOP保持。

Git外发仍因已有系统审核拒绝而阻塞，不改通道绕过；本次按长期规则仅审查本地提交，不能记为远端同步。
