# 首次提交范围（已完成的历史快照）

完成记录：用户已批准下面53项；2026-10-24已创建并推送`cac9f87aedef4879a3dc2893dc16f32fed8c849b`，未强推。名称/Private由用户在已登录官网确认，空引用及推送结果由原生Git核实。下面的未初始化/待提交措辞保留为**首次准备阶段描述**，不是当前Git状态；原SHA清单对应首提交，不用当前已更新文档去冒充原始字节。

首次成功后，既定项目已获按工作单元自动审查/提交/非强制推送的长期委托；普通源码/测试/文档可审后扩白名单，重大/敏感/冲突/破坏仍停，不扩硬件权限。初始源码及有限验收边界不因后续文档同步改变。

日期：2026-10-24。远端由用户提供：`https://github.com/minzhetang/pangu-riscv-soc`。
用户报告私有空仓库；本轮没有访问验证、登录或关联远端。Git 2.55.0.windows.3可用，项目不是Git仓库，没有可报告的本地分支/提交/暂存区。

拟提交 **53个明确路径**。保留原工作路径，不移动/改写RTL；逐文件原始SHA-256见first-commit-files.json，自清单不自哈希。

## 分层状态

当前软件依据F136，CPU/B/官方存储模型未改；有限C/计时/双种子短CoreMark及UART通过。非完整RV32I、正式CoreMark、PDS映射或FPGA验收；B整包条件保持。
首次只保存源码/检查器/少量结果，不承诺干净克隆完整SoC可运行。计时单元独立入口见README，未在本轮重跑。

## 排除范围

- 全部工具、安装包、专有primitive实现、授权/凭据/机器标识、资料压缩包、照片/历史参赛文件和完整队员交付包。
- CoreMark上游源/许可使用说明作为外部依赖，本次不复制；自有平台适配保留。不要把源码版权声明与PDS机器授权混为一谈。
- 本地AGENTS与.project-memory全历史不入首提，避免未审查的历史个人/环境资料；新公开协作规则需另整理，原件仍在本机。
- build/compile/logs/cases/source-before/port-before/models-before/旧工作目录、安装路径清单、完整波形/原始轨迹/镜像/生成初始化常量不入仓。

## 逐文件清单

|路径|类别|证据/限制|
|---|---|---|
|`.gitattributes`|repository|本轮新准备；尚未暂存/提交/推送|
|`.gitignore`|repository|本轮新准备；尚未暂存/提交/推送|
|`README.md`|repository|本轮新准备；尚未暂存/提交/推送|
|`docs/repository/EXTERNAL_DEPENDENCIES.md`|repository|本轮新准备；尚未暂存/提交/推送|
|`docs/repository/FIRST_COMMIT_SCOPE.md`|repository|本轮新准备；尚未暂存/提交/推送|
|`docs/repository/first-commit-files.json`|repository|本轮新准备；尚未暂存/提交/推送|
|`docs/repository/verify_first_commit.py`|repository|本轮新准备；尚未暂存/提交/推送|
|`reports/verification/2026-10-24-soc-txgpio-m1-system.md`|report|有限软件验收报告；本地引用不代表文件已随仓分发|
|`reports/verification/2026-10-24-timed-coremark-m1.md`|report|有限软件验收报告；本地引用不代表文件已随仓分发|
|`work/system/2026-10-24-timed-coremark-m1/analyze_windows.py`|workflow|原阶段工具；依赖本地历史/模型，未完成干净克隆移植|
|`work/system/2026-10-24-timed-coremark-m1/check_timed_v2.py`|workflow|原阶段工具；依赖本地历史/模型，未完成干净克隆移植|
|`work/system/2026-10-24-timed-coremark-m1/checker-negative-result-v2.json`|evidence|F136选定有限证据；本次未重跑|
|`work/system/2026-10-24-timed-coremark-m1/checker_negative_tests_v2.py`|workflow|原阶段工具；依赖本地历史/模型，未完成干净克隆移植|
|`work/system/2026-10-24-timed-coremark-m1/cpu_program_reference.py`|workflow|原阶段工具；依赖本地历史/模型，未完成干净克隆移植|
|`work/system/2026-10-24-timed-coremark-m1/firmware/link.ld`|firmware|F136关联输入；原件不改|
|`work/system/2026-10-24-timed-coremark-m1/firmware/start.S`|firmware|F136关联输入；原件不改|
|`work/system/2026-10-24-timed-coremark-m1/firmware/timer.h`|firmware|F136关联输入；原件不改|
|`work/system/2026-10-24-timed-coremark-m1/firmware/timer_smoke.c`|firmware|F136关联输入；原件不改|
|`work/system/2026-10-24-timed-coremark-m1/manual-plan.json`|expectations|执行前冻结计划；不是新测试结果|
|`work/system/2026-10-24-timed-coremark-m1/peripheral_checker.py`|workflow|原阶段工具；依赖本地历史/模型，未完成干净克隆移植|
|`work/system/2026-10-24-timed-coremark-m1/port/core_portme.c`|platform|F136短运行平台适配；非正式成绩|
|`work/system/2026-10-24-timed-coremark-m1/port/core_portme.h`|platform|F136短运行平台适配；非正式成绩|
|`work/system/2026-10-24-timed-coremark-m1/postflight.json`|evidence|F136选定有限证据；本次未重跑|
|`work/system/2026-10-24-timed-coremark-m1/quality-window-analysis.json`|evidence|F136选定有限证据；本次未重跑|
|`work/system/2026-10-24-timed-coremark-m1/run_stage.py`|workflow|原阶段工具；依赖本地历史/模型，未完成干净克隆移植|
|`work/system/2026-10-24-timed-coremark-m1/runs/baseline-N16/check-result.json`|evidence|F136有限PASS；非硬件|
|`work/system/2026-10-24-timed-coremark-m1/runs/baseline-N234/check-result.json`|evidence|F136有限PASS；非硬件|
|`work/system/2026-10-24-timed-coremark-m1/runs/performance-N16/check-result-v2.json`|evidence|F136最终检查器v2有限PASS；非正式成绩|
|`work/system/2026-10-24-timed-coremark-m1/runs/performance-N16/check-result.json`|historical-failure|旧检查器漏BSS阶段0导致FAIL；保留，不覆盖v2当前结论|
|`work/system/2026-10-24-timed-coremark-m1/runs/performance-N16/ram-output.txt`|evidence|实际RAM报告；不足10秒与Errors detected原样保留|
|`work/system/2026-10-24-timed-coremark-m1/runs/performance-N16/wave-review.json`|evidence|原VCD窗口检查结果；VCD本体不入仓/非ILA|
|`work/system/2026-10-24-timed-coremark-m1/runs/smoke-N16/check-result.json`|evidence|F136有限PASS；非硬件|
|`work/system/2026-10-24-timed-coremark-m1/runs/smoke-N16/wave-review.json`|evidence|原VCD窗口检查结果；VCD本体不入仓/非ILA|
|`work/system/2026-10-24-timed-coremark-m1/runs/validation-N16/check-result-v2.json`|evidence|F136最终检查器v2有限PASS；非正式成绩|
|`work/system/2026-10-24-timed-coremark-m1/runs/validation-N16/ram-output.txt`|evidence|实际RAM报告；不足10秒与Errors detected原样保留|
|`work/system/2026-10-24-timed-coremark-m1/runs/validation-N16/wave-review.json`|evidence|原VCD窗口检查结果；VCD本体不入仓/非ILA|
|`work/system/2026-10-24-timed-coremark-m1/source/alu.v`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/source/control.v`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/source/cpu.v`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/source/cycle_counter64.sv`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/source/gpio_core.v`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/source/local_regif_txgpio_m1.v`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/source/memory_model.sv`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/source/regfile.v`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/source/soc_data_adapter.sv`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/source/soc_top.sv`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/source/uart_tx.v`|rtl|F136有限软件基线；非PDS/FPGA验收；B整包条件保持|
|`work/system/2026-10-24-timed-coremark-m1/tests/tb_timed_system.sv`|tests|F136测试源；unit初版保留，v2为增强版|
|`work/system/2026-10-24-timed-coremark-m1/tests/tb_timer_unit.sv`|tests|F136测试源；unit初版保留，v2为增强版|
|`work/system/2026-10-24-timed-coremark-m1/tests/tb_timer_unit_v2.sv`|tests|F136测试源；unit初版保留，v2为增强版|
|`work/system/2026-10-24-timed-coremark-m1/unit-v2-result.json`|evidence|F136选定有限证据；本次未重跑|
|`work/system/2026-10-24-timed-coremark-m1/unit_boundary.py`|workflow|原阶段工具；依赖本地历史/模型，未完成干净克隆移植|
|`work/system/2026-10-24-timed-coremark-m1/wave_review.py`|workflow|原阶段工具；依赖本地历史/模型，未完成干净克隆移植|

## 本轮动作边界

仅准备文件和清单；不在项目根初始化Git，不暂存/提交/设置远端/推送，不读取Git用户名邮箱、凭据库、SSH私钥或授权文件。
审计可在忽略的tmp内创建一次性空Git仓库，只调用Git自身的ignore解析/未跟踪清单，不进行任何网络访问或提交。
首推前重新展示精确暂存范围并由用户确认；禁止git add -f或笼统将整个工作树强行纳入。ignore不保护已经跟踪的文件。
本轮无需登录；未来如GitHub确实要求认证，使用官方交互式登录，由用户在官方页面完成，不向聊天提供密码、令牌或验证码。
over_temp停止保持。
