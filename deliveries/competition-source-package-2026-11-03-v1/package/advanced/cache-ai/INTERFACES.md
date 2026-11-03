# 接口与实施边界

所有接口为同一时钟域、同步高有效 reset，ready/valid 在上升沿握手。
数据在 valid=1/ready=0 时必须稳定；接收后上游可立即更换请求。

## Cache

`cache_m0`：`qvalid/qready/qaddr[31:0]/qwrite/qdata[31:0]/qstrb[3:0]`；
`pvalid/pready/pdata[31:0]/perror`，写成功 pdata=0；完整32位读，按little endian字节使能写。
`READ_ONLY=1` 写请求返回错误；地址必须4字节对齐，错误请求不访问后端。
`bypass` 每个请求接受时采样其效果。切换 bypass 不自动失效旧行，模式切换前须复位。

`mvalid/mready/maddr/mwrite/mdata/mstrb/mlen` 发单一命令。
读填充4 beat且16B对齐，非缓存读1 beat；写命令单beat带strb。
`rvalid/rready/rdata/rlast` 回传按序读beat或单写应答；
后端必须满足预告长度，无错误/重排/事务ID/超时恢复。无响应将阻塞，TB有watchdog。

写穿透在命令握手提交；命中行在请求接受时更新，但端口阻塞直到写应答消费，
同端口不能观察未完成的写。reset 同时清 Cache 与后端协议，已提交写不回滚。
fill最后beat才设valid；仅清valid/LRU，不物理清数据阵列。无脏行无需writeback。

`cache_subsystem_m0`：两个打包通道，低位通道0为I，高位通道1为D。
例如 qaddr[31:0] 是I、[63:32] 是D，其余向量同规则。
各自128B/2way/4set/16B，组合读数组，单端口单请求，无流水接受。
后端通道独立，没有仲裁器/CPU适配器；仿真是两份独立内存，不是共享存储一致性验证。
不支持一致性、DMA/别名更新、自修改代码、flush指令或多核；使用不可缓存别名写后，
读取旧缓存别名可能陈旧。使用者不得混用cacheable/uncacheable别名，或须统一reset失效。

bit31=1全不可缓存，bit31=0可缓存；这是独立原型映射，未套用当前CPU/SoC映射。
`backend_m0`低12位索引4KiB数据，0x80000ffc读为读增计数器。
delay_cycles可调，每beat插入该等待，再叠加固定command/beat停顿；rvalid等待时保持数据。
仅模拟后端可控延迟；无真实AXI/AHB/DDR协议宣称。

## FC

`cfg_valid/cfg_ready/cfg_kind[1:0]/cfg_addr[7:0]/cfg_data[31:0]`：
kind0的addr0..15写input，kind1的addr0..127写row-major权重，kind2的addr0..7写bias。
权重/输入取低8位有符号数，bias取有符号32位。无效配置被接收但忽略。
`cfg_valid`优先，阻止同拍start。只在idle可配置；阵列支持原型组合读取，未综合RAM映射。

`start_valid/start_ready` 接受一份矩阵计算；输入/权重/bias每项须自reset后写过，
否则产生一个out_error=1、out_last=1、index0/raw0/y0的响应，不执行MAC。
完整配置可多次start；调用者遵守握手，持续valid可在回idle后接受下一任务。

`out_valid/out_ready/out_index[2:0]/out_last/out_error/out_acc signed[39:0]/out_y signed[7:0]`。
8个有序输出，row7 last；等待时暂停下一行，不改变当前结果。
reset取消任务及挂起输出、清所有初始化位，需要重载，未承诺清物理阵列。
数值细节及可复查公式见 ai_plan.md、AI_REPORT.md、reference_ai.py。
