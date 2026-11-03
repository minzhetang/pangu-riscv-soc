# 高阶B软件候选：真实C与BTB收益证据

当前源码与M3八模块同SHA，不替换D300/SM2，不是完整高阶任务2。先读项目报告 `reports/verification/2026-11-03-taskB-software-closure.md` 与AUDIT.json。

- `program.c/start.S/link.ld`、ELF/bin/hex及反汇编：真正编译的RV32I/ILP32裸机程序，排序、CRC、64次交替函数指针调用。
- `FROZEN_REFERENCE.json`、`expected`：DUT运行前由独立算法＋逐指令模型互校并冻结，两个输入。逐笔WB/STORE和全寄存器/32KiB内存预期均保存，不用摘要哈希代替逐笔检查。
- `first-RESULTS.json`：四配置×两输入8次实际DUT运行；runs中完整WB/STORE/state和起始/末尾普通VCD窗口。
- `IRQ_PLAN.json`、`irq-final-RESULTS.json`：MRET后pending响应及中断前STORE抑制/重执行，2程序×4配置8次通过。
- `AUDIT.json`：独立逐行比较、CRC32交叉验证、10个负向控制、VCD时序限定和生产/M3保护SHA。
- `COMMANDS.json`、logs：完整编译/运行命令、native rc/时长/Job清理。预冻结前链接脚本语法错误、CRC常量表初始化缺口和补测生成器求值错误保留为诊断，不当DUT失败。

## 执行环境

独立Harvard取指/数据测试平台，ROM8KiB，同时映射同字节镜像到数据口以支持编译器生成的CRC只读查表。数据RAM32KiB，seed在0x2000；BSS0x4000、stack0x8000。软件签名0x3000–0x3020仅为本测试平台地址，不是生产SoC新接口。采集开始标记后才计算，完成前检查main返回0；无UART打印，不能称外设集成或正式CoreMark测量。

程序实测生成了CRC优化表，初参考模型只初始化取指ROM而未初始化数据可读ROM，独立高层算法在DUT前拒绝CRC不符。明确测试平台读写模型后，双模型先互校再冻结。不能称CPU因此被修复。普通VCD只含前2048周期及完成附近窗口，全程副作用用完整账本验证。

已有合法Python3、Icarus13、OwnedJob可用的原项目树内，`run.py <未使用stage名>`可复现；build.py只用于新输出目录，已有bin拒绝覆盖。reference.py已有冻结参考时拒绝覆盖。新运行不自动改变已冻结验收。audit.py还依赖M1纯VCD解析函数与M3历史清单，单独移走本目录不代表全历史审计可运行。

本轮紧凑交付包提供只读VERIFY_PACKAGE.py及独立REPRODUCE_C.py入口，需显式提供合法Icarus根和未存在的工作目录；原包不改。其性能为确定性RTL周期，非真实时间/正式CoreMark/FPGA收益。频率/资源/完整特权/PMP/Sv32/硬件/ILA未验。
