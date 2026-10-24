# 外部依赖与首提边界

2026-10-24；这里只记录来源和已核实的用途，不执行下载或安装。

|依赖|既有版本/固定来源|首提处理|
|---|---|---|
|Icarus/vvp|本地已验证MSYS2构建13.0|不收二进制、DLL、安装包；计时单元可用现有工具编译|
|RISC-V GNU工具链|本地已验证xPack15.2.0-1，rv32i/ilp32|不收工具/库/安装包或生成ELF/BIN；源码不因工具迁就而扩ISA|
|Pango Design Suite|2022.2-SP6.4|不收任何授权、机器识别信息、安装文件和专有模型|
|Pango primitive|本机PDS中的GTP_DRM18K_E1/GTP_GRS|绑定代码仅实例化外部模型；专有实现留在合法PDS安装中，不复制到私有仓库|
|CoreMark算法|[固定官方提交1f483d5b8316753a742cbf5590caf5bd0a4e4777](https://github.com/eembc/coremark/tree/1f483d5b8316753a742cbf5590caf5bd0a4e4777)|上游五C/coremark.h、归档及许可/使用说明不复制进本次首提，作为明确的外部依赖；本仓库只含项目平台适配及有限结果|

已只读核对本地CoreMark源文件头标注Apache License 2.0；上游`LICENSE.md`标题为COREMARK ACCEPTABLE USE AGREEMENT，不能把它误称为Apache全文。将来如纳入第三方源码，应保留其实际版权及许可/使用说明，不用“.gitignore排除授权文件”删掉源码应随附的声明。本轮不变更上游源、不做新的项目授权声明。

原`run_stage.py`等阶段入口依赖D盘本地布局、历史系统/ELF检查助手、保护清单和初始化材料。首次清单不递归收集历史树，因此完整系统“干净克隆后一键复现”尚未完成，不能把选定结果JSON当作本次运行。后续可迁移化需要另作有界技术工作，保持原基线及预期。

当前PG2L100H目标的实际综合映射/资源/Fmax、正式计时及FPGA/片上取证未通过；现有硬件停止条件不因Git归档解除。
