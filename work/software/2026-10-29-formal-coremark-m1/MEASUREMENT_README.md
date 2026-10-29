# A-FORMAL-COREMARK-SOFTWARE-M1（恢复D196）

本目录是独立软件候选，不是已转交B的固定8迭代包，也不是新位流。所有hardware_valid/formal_score_valid始终false。旧失败在reference_worker.py、logs/reference-performance2；r1只修ELF BSS预检，不把RAM预零。STAGE_CLOCK保留，RECOVERY_CLOCK复用原deadline，没有延长。

入口依次：FROZEN_PLAN.json、BUILD_RESULTS.json、oracles-recovery/*/expected.json、runs/*/functional-result.json（只有实际生成且PASS才算短程功能证据）。源码13份/算法/启动链接保持原件，PORT_DIFF只端口元数据/编译常量；PHASE_ADDR按实际ELF冻结。source/init旧数据不可直接当新程序，必须用cases/<case>/source/init_tables.svh；256初始化另在initialization下（若生成）。绝不把旧8位流当256位流。

全部命令实际argv/cwd/native rc与日志在logs/*/process.json；新四C未重编，N256只独立参考，不长RTL，不运行PDS。工具版本/已安装绝对路径由四build记录和原F179工具身份锚定。run_short_once.py每case只有一次编译/DUT，预算120秒/12M物理拍900秒/最终检查300秒；失败即停，不能直接重跑覆盖。

短case必须保留至少10秒错误，返回0不证明官方验证成功。N256的≥10秒是27000000编译设定和参考计数条件，不是实测频率/实机成绩。HAS_FLOAT=0合法，原整数秒不改；主机measurement_report.py用64位raw差和真实频率应另行审核，示例计算只输出nominal候选。实际计时窗不含UART输出；物理CPU时钟不得因两拍推进改为13.5MHz冒充提分。

正式测量仍需匹配新程序/INIT/实现身份、真实CPU时钟证据、两种子均≥10秒、完整CRC/原始输出与重复运行、A审核。任何实机动作、生成新位流、转包均不在本轮；over_temp停止不因软件通过解除。测量软件参考与短DUT通过也不证明256 DUT运行、完整ISA/异常/实机正确。

完整逐笔比较不去重。冻结独立先验再DUT；检查全RF/32KiB RAM、每笔合法EX/WB/READ/STORE各自顺序、独立stall/flush/phase/计时、实际UART引脚全时轴和窗口普通VCD。保留无真实退休PC、无统一WB/STORE提交顺序、固定内存与初态、窗口非全程波形等限制。普通VCD不是片上ILA。

本目录脚本都是本阶段一次性有界入口，不是随处重跑的通用包。不要执行prepare_and_build/prepare_reference/diagnose_static/resume_references来覆盖现有记录。diagnose_static旧版曾将两JSON写入项目根；已按字节复制回本目录，根副本保留为历史，不再重复运行。
