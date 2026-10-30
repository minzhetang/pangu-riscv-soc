# 配置前后过温状态对照：只读方案核查

2026-10-30；F187/D206。当前12V和下载器USB由用户报告均断开。此次没有启动PDS/硬件服务器、扫描或下载，也没有修改RTL/位流/SCBV。

## 回查结果

| 已核证据 | 结论与边界 |
|---|---|
| `reports/hardware/2026-10-14-led-volatile-result.json`完整命令/状态；`work/pds-jtag/2026-10-14-led-volatile/configuration_tcl.log` | 官方Program命令168.5秒；服务端cfg_program succeed记录169.1秒。两者计时边界不同但一致指向配置命令耗时，不是聊天等待。未记录足够内部阶段/USB吞吐信息，不能定因。 |
| `scripts/environment/Invoke-PdsVolatileLed.ps1`完整源码，仅阅读 | 实际1MHz、program3、仅一次cfg_program；命令超时180秒。旧脚本不读下载前状态；异常时未证明停止服务器中的配置动作，不能原样重跑当新安全控制器。未执行该脚本。 |
| 原LED位流 | 3791112字节，SHA256 `5CBE55491613F163BBDC372F2F5226F1D0E1C1A95A508A02ED54BF150704F307`，与旧配置前后SHA相同。没有重新生成。 |
| F186真实冷启动只读原RESULT | PG2L100H/ID00602899，STATUSR00180c80/flag0/DONE0，仅一个样本；对照旧配置后081efca0/flag1/DONE1不构成同条件因果证明。 |
| 本机官方 `D:/PDS/PDS_2022.2-SP6.4/doc/Fabric_Configuration_User_Guide.pdf` V1.0，实际/页脚81–85 | 81列支持100kHz至15MHz及1MHz；82–83说明program位0/1适用于Logos2，值3；84说明cfg_program，85区分公开ID、状态与其他读取。工具支持某频率不等本板/本下载器线缆实测通过。 |
| 同手册实际13/30 | 13的Cancel是连接参数设置取消；30的可中止说明针对verify。不能拿来证明cfg_program可安全即时取消或断电后保留完整配置。 |

PDF实际81–83三页已新渲染完整视觉核对；13/30/84/85完整相关页文字核对。关键位表/频率列表以81–83可视原页为准。Poppler缺Symbol/ArialUnicode字体警告保留，但关键中文、数值及Logos2行可读。无`help`目录，已读现存`doc`官方手册，不把不存在的路径写成检查成功。

源身份/提取页/渲染文件：`work/analysis/2026-10-30-configured-status-review-m0/`，`SOURCE_RECHECK.json`保留PDF/LED哈希、旧时长和本轮0硬件。没有读取设备序列号、许可或机器标识。

## 技术判断

1. 旧168.5秒的原因**未定**。频率、文件体积和单一耗时不能分离USB传输、协议开销、等待和配置处理。没有依据宣称提频必然解决，也不把软件timeout当停止硬件配置的保证。
2. 推荐保持同一LED位流/1MHz/program3，在一次启动中取得配置前及配置后状态。避免同时换CPU程序、时钟、SCBV或配置选项，降低解释歧义。
3. 该对照能回答“本次配置前后标志是否变化、DONE是否完成”，仍不能凭变化确认实际温度、供电正确或温控因果。采样不是测温，配置期间不能保证持续监视bit27。
4. 60秒范围已完成且不够容纳旧配置，不通过脚本延长偷偷复用。建议新阶段通电硬限300秒、控制器240秒、单配置命令200秒，各为工程操作预算，**不是热安全时长**。此风险和范围扩大需用户单独批准。
5. 不推荐先提高TCK、换多个High/Low档、反复上电或直接CPU/CoreMark：增加变量、扩大未验证活动。正式CPU运行仍是后续独立门槛。

## 待批的最小下一阶段

范围`deliveries/mainline-led-configured-status-scope-2026-10-30-v1/EXECUTION_SCOPE.md`，状态PENDING_USER_APPROVAL。仅准备范围，尚未编写/执行新硬件控制器。批准后在独立目录准备控制器及离线守卫验证，再逐步确认实体条件；不是让用户立刻接电。

停止条件：配置前flag1/身份不符则不下载；配置错误/超时则不重试、不追加其他位流；配置后flag1立即结束；即使flag0/DONE1也只接受本轮配置和短时状态，不自动进入CPU实跑。供电上限或明显异常优先用户断电，软件无法保证远程切断电源。
