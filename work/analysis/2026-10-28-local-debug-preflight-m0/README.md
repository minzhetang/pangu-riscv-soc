# 本地插核只读预检

2026-10-28，F165/D168。执行`check.py`只读取安装程序/帮助/三个历史FIC及F163 ADF等10个输入，前后SHA一致，没有启动PDS、Inserter或Debugger，没有新DUT或硬件操作。

- 安装版入口是`D:/PDS/PDS_2022.2-SP6.4/bin/cdt_ins.exe`；文件SHA为`B526DA86DA96B84A591F63D1E35F3B4CA50433F14DA9D136F7BF10DD50F07D94`。
- 程序静态可见`-batch、-version、ins_set_file、ins_list_nets、ins_set_net、ins_save`。这些是接口线索，**不证明命令行语法、许可或执行可用**；官方QCH有18个HTML条目，其中Inserter章节明确按网络索引连接，未说明外层无GUI启动参数。
- 安装示例中存在精确目标PG2L100H/-6/FBG676的LVDS FIC，44个序列化通道、1024深度；ADC示例同100H/FBG676但-5、33通道，不照搬其等级或温度行为。PGL25G另系列/另一封装/145通道，不能拿来替代目标规则。
- 三示例都指向已不存在的旧开发路径，仅用于格式/配置参考，不作为活动工程或直接运行入口；本轮没有执行示例。旧F163功能网表ADF存在。
- `PREFLIGHT.json`保留实际解析字段，`INPUTS.json`保留10输入SHA，`POSTFLIGHT.json`为后验保护。初期查找不存在的tcl/scripts目录已更正为安装实际目录，不将失败搜索当无接口。

唯一推荐的新实施范围为`deliveries/mainline-local-debug-insert-scope-2026-10-28-v1/IMPLEMENTATION_SCOPE.md`（1.0.0，PENDING）。先有限验证CLI及信号映射，再最多1次调试插核构建。旧D164只允许已完成的1次无调试位流；本次新的调试网表/保留元数据和构建尚未获批。无需咨询渠道，不恢复硬件。
