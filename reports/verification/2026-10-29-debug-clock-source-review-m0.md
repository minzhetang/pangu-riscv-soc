# R4调试时钟与采样源：只读复核

2026-10-29，F172/D181；基线为F171/R4，Git基线00d16739。本轮没有启动PDS、GUI、仿真、Debugger或任何硬件工具，没有重建或改变输入。

## 结论及新增证据

1. **采样时钟链已进一步核实**：原生`report_timing/rtr.db`的Slow/Fast Clock Network树中，140个`trig0_d1[0..139]`的CLK端点均经`clkbufg_3`归属`clk_27mhz`，没有落在JTAG时钟树。它是原生产物的新解析，不是新运行或实机证明；也不证明140个D输入接线正确。
2. **4条Critical不是可以靠隐藏检查消除的提示**：PDS安装版UCE手册V1.7 §2.3.4.9实际PDF97–98页（印刷96–97页）说明，`PAP_CLOCK_DEDICATED_ROUTE=FALSE`允许SRB互连，并可将Place-0084降为Place-2028。PDS手册V1.5实际115页（印刷114页）说明Route-2036检测非时钟树走线。R4生成的`u_CORES/drck_o`已有FALSE属性；用户FDC未新增此设置。来源确定不等工程风险消除，不改属性、关检查或盲目换种子。
3. **CPU/调试域的时序通过声明必须限界**：Clock Interaction中JCLK→27MHz、CAPTURE→27MHz、27MHz→JCLK分别是Asynchronous Groups，原报告端点计数474、1、239，没有对应setup/hold裕量。这些数是报告统计，不能当独立CDC路径数；没有做同步器/握手证明，不能把“All Constraints Met”解释成CDC验证通过。声明的JCLK20MHz/CAPTURE10MHz也不是实测下载器频率。
4. **数据连接仍缺原生后布局证据**：FIC数据136/137/138/139分别选择stopped、stop_kind[0]、stop_kind[1]、write_error。综合网表中CPU→SoC→板级命名端口连线支持原别名；但Public-4008清理发生在后续映射阶段，不能用此前连线证明之后驱动一定存在。布局库存只有Port/Inst/Pin/Net/Clock的名称/方向/类型，没有net-to-pin边；dmr/prr/rtr XML报告也未提供全部数据引脚的连接表。未逆向解析二进制ADF或解密IP。既不判定“被清理就丢信号”，也不判定“只是重复信号”。

## 4条告警逐项状态

|告警|R4实际对象|本轮可确定的内容|尚未关闭的内容|
|---|---|---|---|
|Place-2028|SCANCHAIN固定SCANCHAIN_88_312→时钟缓冲|源属于工具插入JTAG域；clock_utilization列出buffer为USCM_215_576|此放置是否满足最终调试可靠性，不能由降级属性判定|
|Route-2036|SCANCHAIN:TCK1→clkbufg_4:CLK|原生日志明确SRB；不是27MHz外部时钟入口|实际路由/边界及可接受条件|
|Route-2036|CAPTUREDR→id_sample.conf_id[1]时钟|属于调试配置采样域|实际负载及路径情况|
|Route-2036|clkbufg_4:CLKOUT→conf_reg[188]时钟|属于调试配置域，非trig0_d1一级采样CLK|该分支使用SRB的实际关系及风险|

原7条constant-probe仍开放；34条调试内部清理和3条CPU停止输出清理消息不自动豁免。本轮没有新证据解除over_temp、配置供电、外部IO时序或硬件停止条件。

## 官方原件与视觉核对

原件均在`D:/PDS/PDS_2022.2-SP6.4/doc/`：

|文件|版本|实际PDF页|用途|
|---|---|---|---|
|User_Constraint_Editor_User_Guide.pdf|1.7|97–98|属性与告警降级规则；已视觉核对|
|Pango_Design_Suite_User_Guide.pdf|1.5|115|Route-2036含义；已视觉核对|
|Fabric_Inserter_User_Guide.pdf|1.0|7|Data/Clock Port含义；已视觉核对|
|Design_Editor_User_Guide.pdf|2.0|12–13|de.exe独立打开及加载已有pnr.adf/可选timing；已视觉核对|

PDF渲染只使用现有Poppler；部分页面有Symbol/ArialUnicode字体提示，关键正文可读。未安装字体/软件，未创建或修改PDF原件。线上精确查询SCANCHAIN/Place-2028/Route-2036及该属性，没有取得适用本版本的Pango官方豁免说明；第三方搜索结果不作为技术验收依据，不写成“官方没有勘误”。

## 最小下一阶段，尚未批准/执行

推荐**A-DEBUG-CONNECTIVITY-M1 /1.0.0**：只打开一次安装版`de.exe`（GUI<=600秒，阶段<=1200秒），在新独立目录使用R4已有后布局数据库的同字节副本，查询实际采样输入/驱动以及4条时钟告警涉及的网络与负载；同一GUI内只读帮助最多6项，不另开PDS命令行或重建。优先查136–139、34及38通道；若有官方原生批量只读接口，再导出全140通道。无法可靠取得则记录有限覆盖/停止，不猜命令、不逐次追加预算。

成果是连接报告/只读截图和可复查源路径，不是修复告警、形式等价、CDC认证、硬件准入或采样成功。没有必要改CPU、FIC、时钟/引脚约束或B接口。独立GUI权限是项目规则的真实门槛，不能把R4已用额度或本轮一般“继续”当作新GUI批准。

准确待批范围：`deliveries/mainline-debug-connectivity-scope-2026-10-29-v1/IMPLEMENTATION_SCOPE.md`。

## 可复现分析及保护

入口：`work/analysis/2026-10-29-debug-clock-source-review-m0/review.py`，使用现有Python绝对路径加`-B`执行；代码不实现任何PDS/仿真/硬件调用。输出INPUTS、SAMPLER_CLOCKS、CLOCK_INTERACTIONS、WARNING_FINDINGS、DATA_SOURCE_LIMITS、SUMMARY。输出为独占创建，不盲目重跑覆盖。

全部20个直接输入、148保护条目、预综合52/完整构建54冻结文件后验SHA核同。PDF页图仅本地保存；专有网表/报告原件、位流、完整帮助、截图、许可及机器信息不纳入Git。本轮没有新增DUT、CoreMark或硬件测试，F160/F163/F171的层次与限制保持。
