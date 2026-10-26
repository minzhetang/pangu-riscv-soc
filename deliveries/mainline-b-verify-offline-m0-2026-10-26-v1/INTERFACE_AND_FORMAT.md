# ABI 1.0.0 / 离线格式和完成规则

机器可读常量以INTERFACE.json为准；函数源为frozen/offline_api.py。仅离线固定快照；不提供stdin实时流协议或在线背压。每输入<=512MiB、600万记录、每行512B；冻结codec为4MiB块。更大流须新版本，不把虚拟偏移当>4GB真实I/O。

## B的生产入口

```text
python -B RUN.py --case-file CASE.json --input-root INPUT_ROOT --out NEW_OUTDIR
```

CASE是UTF-8 JSON，示例（允许空流默认false，limits可降低但不高于INTERFACE上限）：

```json
{"id":"demo","expected":{"storage":"raw","stream":"trace","path":"inputs/seeds/S00-duplicates-kept/expected.log","complete":true},"actual":{"storage":"raw","stream":"trace","path":"inputs/seeds/S00-duplicates-kept/actual.log","complete":true},"allow_empty":false,"limits":{}}
```

archive模式将path设为归档目录，并给固定外部 `index_SHA256`，例如REAL_CASES中的input。CASE **不读取测试标签expected_status来决定运行结果**；真正测试标签只存在冻结测试计划。输入根与返回代码根独立，可移动；输入相对路径不许越界、链接/reparse或绝对路径。输出必须包外全新目录，已有目录拒绝，不能覆盖/递归删除。B返回代码可用`--input-root`引用这份独立包，不许引用A历史绝对路径。

## 文本记录

ASCII正文，`|`分隔；LF或CRLF完整行，十六进制字段宽度固定且不区分大小写；无符号十进制周期1..2^64-1。非法字符/X/Z、缺尾换行、错误宽度不放行。

```text
EX|cycle|pc[8hex]
WB|cycle|rd[decimal1..31]|data[8hex]
READ|cycle|pc[8hex]|addr[8hex]|raw[8hex]|loaded[8hex]
STORE|cycle|pc[8hex]|addr[8hex]|data[8hex]|mask[1hex]
EDGE|cycle|gpio_async[2hex]|addr[8hex]|write[0/1]|data[8hex]|mask[1hex]|read[8hex]|error[0/1]|pre_tx[0/1]|pre_gpio[2hex]|post_tx[0/1]|post_gpio[2hex]|accept[0/1]|stop[0/1]|pre_ticks[16hex]|post_ticks[16hex]
```

trace保留EX/WB/READ/STORE交织文件顺序，周期不递减；bus每行周期严格递增。**每个类型化字段包括物理周期/PC全部相等**才MATCH；同值多次合法WB/STORE保留，绝不去重。EX不是退休PC，不把bus/trace拼成统一退休流，不由B重新解释UART/采样沿或CPU合法行为。

乱序故障须区分：如交换同周期的不同trace事件，格式仍合法，应MISMATCH；跨周期交换破坏单调性则INVALID_INPUT。合法重复故障只用允许同周期/后续合法周期的trace；bus重复周期本身INVALID_INPUT。精确写在B冻结计划，不能按输出临时改判。

## 完成与错误

spec.complete必须字面true，表示提供方冻结快照已关闭；不是从字节相等推导真实DUT成功。必须完整耗尽两个迭代器并校验容器索引、每块与全流完整性。早退/只比前缀、缺关闭证据、空流未授权、尾损坏都不得MATCH。空流仅allow_empty显式true可作为格式测试通过，不代表CPU完成。

保留全量逐笔核对，但诊断最多16差异、邻域各2条，日志各<=4MiB、结果<=1MiB。超过差异上限只截诊断，不停止消费；结尾坏块不得因先发现差异而漏检。两流均完整后才可fully_consumed=true。

原生退出码：MATCH0，MISMATCH2，INVALID_INPUT3，INCOMPLETE4，LIMIT5，TIMEOUT6，TOOL_ERROR7。异常/未知rc、日志/结果截断不能升级成功。RUN至少输出status/native_rc、两流检查数量/字节、fully_consumed、差异及其首序号、实际时间/资源、CPU_function_proven=false、所用ABI/输入及代码SHA；不可用项null并说明。测试汇总另写预期/实际/测试PASS，避免与功能MATCH混淆。

Windows现有Python3.10+是必测平台；优化`-O/-OO`必须在冻结assert codec前拒绝。压力以真实消费字节/记录数计，1/16/128MiB档、峰值worker<=256MiB、每case180秒+8秒清理、全套<=1800秒。父进程也流式读写/限额，不能把内存搬到父进程；分别报告父/worker峰值与测量方法。未实测其他OS不宣称跨OS通过。
