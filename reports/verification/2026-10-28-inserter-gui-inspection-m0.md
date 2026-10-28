# Inserter只读界面诊断：启动到期提醒已确认

2026-10-28（北京时间），D171授权一次<=3分钟只读GUI，F167/D172结果。实际一次启动4.453秒后结束，没有进行插核/构建或修改许可。

- 自有新进程的可见窗口标题为 **Expiration Reminder**，窗口类Qt5152QWindowIcon。没有点击按钮或读取编辑框、文档/文件列表、许可内容/身份字段；结束先投递一次WM_CLOSE，再终止仍未退出的自有根进程。最终rc1是受控关闭结果，不当作工具自身错误。
- Windows UI Automation辅助入口rc1，未取得提醒正文或后续主界面，不能声称完整GUI阅读成功。该辅助入口的stderr未保留，原始错误细节无法追回；后续最小同类.ps1只读控制同样rc1/PSSecurityException、未输出标记，执行策略查询rc1不可用，**不能据此断言当前策略名称或原辅助失败完全由同一原因导致**。没有修改/绕过执行策略，没有安装或更改安全设置。
- 原生stdout222B，stderr0B。本次从软件实际提示解析出 **will invaild in 6 days**（工具原拼写），因此记录“本次Inserter提示6天后失效”，不是已经到期，也不宣称所有PDS特性已checkout通过。提醒正规续期，不按日期估计精确到期时刻，不读取许可证文件/机器标识。
- 回查F166不变的194B旧stdout，也确有相同6天提示，其SHA为35D4585D90D868C3DC1E396415C2C493B7AD0147E4BBA9976D71C142BEA39D07。旧解析只匹配expire/expired而漏掉invaild；F166“未解析出明确余期”的解析结论现被本证据补充取代，原日志/旧报告/JSON不回写。旧批处理窗口当时没有保存标题，不能反推其一定就是本次同一窗口。
- 46受保护原件前后SHA同；本次原生GUI1次、PDS构建0、编译/DUT0、控件调用0、硬件0。根进程已退出，剩余该进程可见窗口0；没有因此声称全后代快照验证。F160/F163功能与位流不变，over_temp STOP保持。

证据根目录：`D:/A_FPGA_Comp/work/analysis/2026-10-28-inserter-gui-inspection-m0/`。APPROVAL、FROZEN_INPUTS、RESULT、SAFE_LOG_SUMMARY、LICENSE_NOTICE、OLD_NOTICE_REPARSE、POLICY_DIAGNOSTIC及POSTFLIGHT/SHA清单分层留存；只读UI辅助脚本与一次性监督代码同目录。stdout/stderr/策略负例原日志仅本地，不把UIA失败或安全控制当DUT失败。

本轮任务已结束，不自动再次启动GUI、确认提醒或恢复构建。下一推荐把**仅确认纯信息到期提醒、GUI配置观察核及原纯软件构建**合并为一个清晰阶段授权，避免按按钮逐次审批；精确范围见`deliveries/mainline-local-debug-insert-r1-scope-2026-10-28-v1/IMPLEMENTATION_SCOPE.md`（1.1.0，PENDING）。只允许安全可核的本地业务操作，不改许可/安全策略、不安装、不接硬件；不能可靠操作界面则停止并只索取一项具体必要反馈。
