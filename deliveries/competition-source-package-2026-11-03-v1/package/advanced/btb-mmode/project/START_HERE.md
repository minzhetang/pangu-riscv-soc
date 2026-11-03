# 高阶B有限软件候选交付

先读reports/verification/2026-11-03-taskB-software-closure.md。当前源为M3，M4没有再改RTL；M1/M2原源与前后反例保留。动态预测与所选M-mode范围的有限软件结果，不是完整高阶2，不替换生产板级基线，无新PDS/实机/ILA/CoreMark结论。

本包包含完整当前八模块RTL、C/启动/链接/ELF/bin/hex、冻结输入与参考、全部已选软件阶段结果/原事件日志及脚本。较大历史VVP和大多数旧VCD不随包；M4全部普通窗口VCD及四个前期关键代表波形随包，未带文件仍保留原项目。COPY_IDENTITY是实际源到副本SHA，不以历史SHA清单冒称全部历史产物已交。

来源：B原HL4基础，A主线最小修复/测试/集成核查；不能由提交者或目录推断为B全部交付已验。许可证/工具安装包/专有模型/凭据不包含。

先只读执行VERIFY_PACKAGE.py核材料。REPRODUCE_C.py能在明确的新目录复现当前C程序8运行；需已有合法Windows Python3与Icarus13，通过--iverilog-root指定现有ucrt64根，不安装/改PATH。需向普通软件阶段取得实际执行许可；本包不授权硬件/PDS。输出目录不得存在，包保持只读。

示例：python -X utf8 -B REPRODUCE_C.py --iverilog-root <已有ucrt64目录> --output <唯一不存在目录>

重放/静态检查不当新DUT；重编/新运行有独立结果。包内原audit.py检查历史89保护项/M3原全清单等，依赖原项目，不能当独立包一键审计。当前便携入口只复现C闭环，未声称重跑全部168历史运行。旧报告里的原始路径和COMMANDS属追溯信息，不要求另一台电脑具有A盘符。

剩余：全特权/S/U/PMP/Sv32、完整高阶2、候选CoreMark/综合频率资源/硬件均未验。先保护已验作品，不因deadline替换CPU或改标准。
