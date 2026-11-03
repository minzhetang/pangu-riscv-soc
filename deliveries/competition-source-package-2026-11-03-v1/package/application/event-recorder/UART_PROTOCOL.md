# UART账本怎样读

115200 baud，8N1，无流控。程序启动后采集约12.8秒，期间不输出；结束后发送ASCII，LF换行，每个数是8位小写十六进制，后面有空格。

`REC2 period count wait done dense start end work late retained evicted rejected fault frozen`

|字段|解释|
|---|---|
|period/count/wait|2700000tick/128样本/20样本等待|
|done|实际完成的样本数，正常批次128|
|dense|当前板级固定event镜像为0|
|start/end|本批采集起止目标timer低32位|
|work|采样处理段累计tick，不包括忙轮询等待/串口导出|
|late|超过调度迟到预算次数；本轮接受条件0|
|retained|实际随后E行数量，最多8|
|evicted|环满淘汰旧前文条数，不能把它藏为“无丢失”|
|rejected|冻结后不再保存的变化条数，明确报告|
|fault|0无故障/1顺序错/2等待超时/3调度过载|
|frozen|故障后上下文已冻结；无后续事件时可能仍0|

每条`E tick index state reason`，严格按事件发生顺序导出，最后一行`END`。state是三个输入位，不是故障码。reason0合法变化，1非法顺序，2等待超时，3调度过载。超时E行可以重复state1，因为记录的是“等太久”事件，不是重复误提交；index仍应晚20个样本。所有条目不去重。

比如state `00000003`表示KEY1和KEY2都被采到按下。合法完整流程为0→1→3→7→0；state2（只按KEY2）首先即非法。完整记录包含tick和index，可区分错误顺序与等待超时，并保留有限故障上下文；不完整报告、额外行、字段错误和串口错误都不能当通过。

LED6为采集中；正常结束0xa5对应LED0/2/5/7，故障结束0x81对应LED0/7。全灭不是本应用正常结束图样：先检查是否复位保持或配置有效，不能仅凭POWER亮推定CPU在执行。原M4配置状态变化仍未查明，保留为可靠性未闭项。

主机只能解码CPU真实输出，不能代造事件或改预期。`verification/recheck_reports.py`用于原始字节复查；不通过哈希摘要代替逐条比较，不把旧报告重放记为新板级运行。
