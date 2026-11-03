# 随包与外部依赖

## 已随包

完整项目RTL/TB、主要C/汇编/启动/链接/移植层、独立参考、冻结输入/预期、必要程序bin/ELF/hex/ROM常量、项目自编OwnedJob源、流式检查器/C++源、代表性原日志/结果/普通波形、PDS流程/约束和调试配置。CoreMark六上游算法文件与完整LICENSE（包含CoreMark acceptable-use及Apache-2.0）已随包；源码头版权不删除。

CoreMark上游固定提交为1f483d5b8316753a742cbf5590caf5bd0a4e4777，来源是本地既有官方GitHub下载归档，非本轮下载。六文件与基础恢复快照的UPSTREAM_DEPENDENCIES及M5都逐SHA一致。不存在用网上“最新版”替代固定算法。

project-verify-headers内三个原有M0_VERIFY观测头供历史存储验证按原宏配置使用；默认PDS不启用该宏，候选M5的数组TB也不使用厂商存储模型。RX共享账本头来自已冻结1930依赖，已在RX TB旁补同字节副本以关闭直接include。

## 合法外部依赖

| 工具/资源 | 已核版本 | 取得/配置与适用范围 |
|---|---|---|
| Python | 3.12系列；项目部分本机记录3.12.10 | python.org官方渠道；大多数校验只用标准库；原断言型检查不可-O/-OO |
| Icarus Verilog/vvp | 13.0，MSYS2 UCRT64现有发行 | Icarus官方源码/发行说明及合法MSYS2发行；Windows通常需-B指向lib/ivl、vvp的-M路径；不随包带安装程序或VVP |
| xPack GNU RISC-V GCC | 15.2.0-1（GCC15.2.0），RV32I/ILP32 | xpack-dev-tools/riscv-none-elf-gcc-xpack官方GitHub Releases；必须用匹配纯I multilib/软运算，不借M/C扩展库凑构建 |
| Pango PDS | 2022.2-SP6.4 build146967 | 紫光同创官方支持/合法竞赛或板卡资料渠道，按厂商授权自备；不分发许可证、工具数据库或私有模型 |
| GTP_DRM等原语/调试核 | 与上述PDS、Logos2/PG2L100H匹配 | 仅PDS合法安装提供；代码中保留原语绑定，不复制原语实现；软件仿真用独立memory_sim/TB数组或合法模型 |
| C++编译器 | 项目原有MSYS2 UCRT64 g++，仅流式C++辅助 | 需复验者已有合法工具链；M6为历史失败源，不因有编译器自动重跑 |
| Pillow | 仅可选片上图片重绘 | 并非CPU构建依赖；已有CSV/PNG可直接阅读，本轮不安装 |

不要求安装Vivado。其它板卡/FPGA家族或工具版本的约束/模型不能直接替用。外部依赖缺失时，相关构建/物理仿真步骤保持未执行，不把工具错误计作CPU失败。

## 明确没有随包的内容

工具/安装包/许可证密钥/机器标识/专有模型及DB/ADF/生成网表；旧位流/SVF；大部分逐笔长轨迹和大N234 RX VCD。它们不是项目源码，省略不意味着曾不存在。固定镜像身份由原清单与静态绑定记录保留。需要板级重建时按源码流程合法生成，不把旧下载器/板卡串号作为依赖。

对历史审计器所需全量旧轨迹/旧归档，参见HISTORICAL_REFERENCES，不宣称随包所有历史审计可一键运行。常规应用软件便携入口和真C候选隔离入口已经实际交付，根REPRODUCIBILITY给出准确使用方式。
