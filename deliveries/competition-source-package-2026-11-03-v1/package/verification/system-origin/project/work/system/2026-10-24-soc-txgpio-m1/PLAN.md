# A-SOC-TXGPIO-M1 当前实施与事前预期（D120）

2026-10-24用户明确批准，B包装包稍后提供。新CPU侧/系统范围已批，不含CPU修改、B包装代写/合同变更、RX包装、Timer/正式计时、PDS/硬件或新工具。旧合同及scope保留，以下只更新A实现候选：CPU四源F130原SHA、存储F131官方模型，两拍模式/32K ROM+32K RAM@10000/SP18000，IO20000000–ff，B LOCAL-REGIF-TXGPIO-M1/1.0.0不改。

## 当前可独立验证

- 新main.c/start.S/link.ld用既有纯RV32I工具普通编译链接，ELF/反汇编/bin/hex/容量/数据与BSS/栈检查；这不是CPU执行。
- 仅CPU侧soc_data_adapter单元，核ROM/RAM/IO边界、写互斥、低位完整偏移、字节strobe传递/IO写不漏进RAM、无效写观察；其fixture只驱动测试向量，不实现B外设或伪报集成。
- 独立外设模型/检查器的合成输入自检，明确不是DUT覆盖。完整系统top作为候选只连接合同模块名，B未收前不造stub凑展开。

## 固定软件意图

启动复用原机制，真正复制.data、清.bss、建立sp/gp后调用main；main验证cookie13579bdf、原BSS0、volatile栈数组checksum126（x=15，8*x+6）；GPIO依次5a、5a、a5并读回；等GPIO_IN=3c后记录；轮询发送12字节`PG100 M1\r\nAA`，等最后ready再等GPIO_IN=c3、保存签名534f4331，正常main返回0后EBREAK。results[0..11]手工期望为[13579bdf,0,126,5a,5a,a5,3c,c3,12,a5,0,0]（数字混合口径以manual-expectations.json机器字段为准，最后项仍BSS0）。不插NOP、不force内部、不预置最终结果。

## 完整系统执行前门槛与验收

B包到后先安全列包/核SHA、读合同/入口/测试/原日志，不执行包内脚本，分层复现再连接原件或核SHA副本；未收/未验不宣称B通过。N16完整/N234同序列有界，固定GPIO外部刺激（候选：释放后物理16拍前置3c、4096拍前置c3，须在DUT前由独立模型核启动至首读界限并冻结；尚未冻结最终系统时序）；TX按物理钟N，不按CPU推进钟。

记录全RF/RAM、每笔WB和内存/IO事件、实际TX串行位与GPIO变化/实际接受使能（包审后确认可观察网名）、stall/flush、X/Z与停止后无新副作用。动态GPIO/ready预期由先冻结的独立逐物理时钟模型给出，不把DUT返回值喂回当预期；参考CPU无退休PC/统一提交序局限保持。轮询次数可变时依据经独立验证的环境读事件，而非无条件接受任意DUT输入。

CPU不改不重复763全回归；风险回归集中存储/IO互斥、真实load/store、重复GPIO请求/重复A帧、复位和停止尾窗。CPU缺陷/接口改动需越界时停；错误不降预期。普通编译/仿真许可与沙箱外门槛分开，所有新外部编译另固定命令/次数请求，旧批用完。

阶段当前是PREPARING，完整SoC COMPILE/LOAD/RUN均NOT_RUN，原件/冻结测试/历史结果保留；B等待只挂接入，不使软件/检查器准备停滞。over_tempSTOP保持。
