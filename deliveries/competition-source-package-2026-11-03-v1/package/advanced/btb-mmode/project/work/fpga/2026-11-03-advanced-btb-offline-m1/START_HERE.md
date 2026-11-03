# 独立离线PDS：关闭 / 64项 / 32项BTB

用户明确不板，本阶段仅已有合法PDS普通用户compile/synthesize/dev_map/pnr/report_timing。无gen_bit_stream、服务器、JTAG、下载、Flash、许可证或系统环境更改。

先读项目报告reports/verification/2026-11-03-coremark-resource-no-board.md及AUDIT.json。推荐pred32：32项，内部STA估算33.9006MHz，11299 LUT/5088 FF/16 DRM36；不称板上Fmax。

三独立工程pred0/pred1/pred32：同芯片PG2L100H/-6/FBG676，同27MHz、引脚及窄域异步入口约束、同程序ROM，只变BTB_ENABLE/INDEX_BITS。source里的同步级syn_preserve沿用已核主线修复，未改原B或生产源。原始BUILD_EXIT/flow/资源/STA/constraint_check及网表按各配置保留。1792段存活ROM/RAM primitive INIT已逐值核对。

constraint_check零Critical不等整个流程无warning；未约束原始异步IO、常量探测、最大扇出等告警保留。内部时钟八检查通过不等全IO/CDC签核，也不关闭旧ILA版四Critical。无新位流或实机运行，程序镜像不是已验可安全下载版本。

build-pred*.py为已消费的一次构建入口，检测ATTEMPT已存在会拒绝复用。复现须新独立副本、合法同版本工具及明确软件阶段范围。audit.py核本次三组报告和原89保护项；这些外部依赖未满足时不能把静态文件存在称为复现通过。
