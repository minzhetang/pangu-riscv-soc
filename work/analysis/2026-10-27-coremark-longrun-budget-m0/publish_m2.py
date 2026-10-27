from pathlib import Path
import sys,json,time,hashlib
P=Path('D:/A_FPGA_Comp');H=P/'work/fpga/2026-10-27-coremark-longrun-ready-m2';D=H/'runs/performance8-N234';M=P/'.project-memory';sys.path.insert(0,str(H))
from stage_coremark import read,save,sha
from stage_budget import check
from preserve import protect
if __name__=='__main__':
 check();s=read(H/'SUMMARY.json');assert s['status']=='PASS_FINITE_8_ITERATIONS_NOT_FORMAL_LONGRUN';assert '## F-160' not in (M/'FACTS.md').read_text(encoding='utf-8-sig');assert '## D-161' not in (M/'DECISIONS.md').read_text(encoding='utf-8-sig')
 q=H/'oracles/performance8/expected.json';o=read(q);a=s['archive_timings'];ticks=s['raw_ticks'];stage=read(H/'STAGE_CLOCK.json');elapsed=time.monotonic()-stage['started_monotonic']
 report=f'''# CoreMark长跑准入M2：8迭代有限实测

2026-10-27，F160/D160–161。**保持13功能RTL和算法不变，完成可信8迭代执行及大流主机守卫验证。** 不是完整RV32I验证、正式CoreMark成绩、160迭代或FPGA实机验收。

## 已打通的真实流程

同一O2/RV32I/ILP32程序仅将ITERATIONS=2改8 → 单次GNU构建/ELF与单字节镜像检查 → 预先独立ISA及MMIO时序参考 → 单次Icarus编译 → 单次有界8迭代DUT → 分段无损归档 → 全RF/RAM、逐笔EX/WB/MEM、计时、串口及窗口VCD核验。

|层次|实际证据与结果|
|---|---|
|主机容器规模|真实逐笔消费571018176字节/5898240条bus记录，1025个实际trace小段；每行重新生成核对、回读字节/SHA/数量一致。13项含一正及拒绝控制通过，另3项容量/实际回调期限控制与-O明确拒绝；不是CPU或>4GB测试|
|旧双种子重放|新检查器全严格结果与F151 JSON核同，完整PIN串口审核通过；原2迭代输入/期望保留，0旧DUT重跑|
|新C程序|仅一次GCC及必要辅助命令，各原生0；实际ELF seed4=8，二进制与旧性能2迭代仅一字节2→8。算法/port/启动/链接不改|
|独立先验|{o['steps']}ISA步，预期物理{o['expected_physical']}，计算{o['raw_ticks']}ticks，crcfinal={o['crcfinal']}，{o['report_bytes']}报告字节，在DUT前冻结；与旧线性估计不同，未用估计替代oracle|
|编译|1次，原生0，{s['compile_host_seconds']:.3f}秒；{s['compile_warning_groups']}类warning，路径归一同旧={s['warnings_identical_normalized']}|
|新DUT|1次performance8-N234/GPIO0，原生0，{s['DUT_host_seconds']:.3f}主机秒；正常STOP及32拍尾，无额外运行|
|功能|完整RF/32KiB RAM、每笔合法EX/WB/MEM及各自顺序/数量不去重、独立stall/flush/计时、BSS/phase及副作用一致；物理{s['metrics']['physical']}，stall{s['metrics']['stall']}，flush{s['metrics']['flush']}|
|输出/波形|{s['UART_bytes']}完整实际UART字节及每次PIN变化核同，原生窗口VCD前后沿/计数采样通过；不是全算法波形、统一提交/退休PC或ILA|
|实际容器|{s['segments']}段、{s['raw_records']}条、{s['raw_bytes']}原始字节→{s['archive_bytes_including_metadata']}含元数据归档字节；本轮各已关闭段逐字节回读并核身份后删除spool，失败夹具和历史输入保留|
|资源|spool峰{s['spool_peak_bytes']}B；归档父峰{s['parent_archive_peak_bytes']}B；最终检查峰{s['check_peak_bytes']}B；参考峰{s['reference_peak_bytes']}B。实际VVP峰见logs/run-performance8-N234/process.json；各工作集<512MiB|
|保护|{s['protected']}原件及{s['frozen_inputs']}执行冻结输入SHA核同；13RTL/外设/官方C及参考ISA语义不改，无PDS或硬件动作|

## 代价、观测和真实限制

参考{s['reference_host_seconds']:.3f}秒，最终检查{s['check_host_seconds']:.3f}秒。归档编码{a['encode_s']:.3f}、解码逐字节核验{a['decode_verify_s']:.3f}、源身份复核与删除{a['source_verify_delete_s']:.3f}秒，这些父进程片段与VVP并行/等待有重叠，**不能直接相加为串行总耗时或因果比例**。VVP及父CPU时间见SUMMARY/原process；不同长度/负载的执行不构成受控提速实验。TB把冗余total逐笔累加移到闭段汇总，字段/时刻/事件谓词未变，未声明收益比例。

每流raw16GiB/500M条/16384段/index16MiB、整例归档4GiB是明确硬上限，不是所有上限已实测；主机规模仅>512MiB和1025段。内存测量缺失、绝对期限、超限均失败；stage_clock同一绝对7200秒未重置。直接子进程和父进程测峰，GNU/Icarus内部孙进程峰没有独立测量，不夸大观测范围。CLOSED-SEGMENTS为新验证路径，raw/F153兼容读取不是所有最大规模均已验证。

独立参考25M步/900秒、DUT32M拍/2400秒、最终检查1800秒等均在批准范围。本次计算{ticks}/27000000约{ticks/27000000:.6f}名义秒，报告保留SIM ONLY和不足10秒警告；不等真实FPGA频率或正式分数。无真实退休PC/统一WB-STORE顺序、固定内存及初态限制保留。

准备顺序曾导致一次旧重放找不到尚未完成的build-result.json，原始stderr/rc保留；诊断为元数据未就绪，在构建完成后用唯一新日志目录重放通过。该次未跑DUT、未获得/篡改功能结果；C/RTL/DUT均未重试。附加回调期限负控的首个辅助包装曾因错误文本大小写断言失败，实际守卫正确抛出ABSOLUTE_DEADLINE；原脚本/夹具保留，独立新回调与精确错误码复核通过，记录在controls/extra-guards.json。

## 入口、复现和下一步

`work/fpga/2026-10-27-coremark-longrun-ready-m2/`：SUMMARY、SOURCE_RECEIPTS、APPROVAL、TEST_PLAN、oracle-freeze、frozen-inputs、IMAGE_DIFF、EXACT_DIFF、COMMANDS、REPRODUCE、SHA256SUMS及postflight；build/compile/DUT-attempt各1。oracles为先验；replays明确旧数据；controls明确主机；runs/performance8-N234含新archive、全态、实际PIN/VCD和functional/check/UART/wave结果；logs含所有真实命令/rc/资源。

下一优先完成**正式测量路径与初赛证据缺口的只读决策**：以本次实际时间/容量更新长跑成本，判断名义160迭代的证据收益；CPU/系统已有闭环，不再自动追加数十小时仿真来冒充FPGA成绩。新长跑/优化/工具/远程或本地硬件均须明确范围/权限，不能复用这次已用完1+1。B R1独立、不重派外设、不等待其整包；原10/27 18窗口保持。over_temp STOP及F146候选/F147告警保持。
'''
 with (P/'reports/verification/2026-10-27-coremark-longrun-ready-m2.md').open('x',encoding='utf-8') as f:f.write(report)
 fact=f'''## F-160：M2真实8迭代与大流主机准入有限通过

- 2026-10-27，D160具体授权后，`reports/verification/2026-10-27-coremark-longrun-ready-m2.md`和`work/fpga/2026-10-27-coremark-longrun-ready-m2/`SUMMARY/SOURCE_RECEIPTS/COMMANDS/原始分层证据。571018176B/5898240条真实主机逐笔/1025小段及拒绝控制通过；不是CPU大规模或>4GB证据。旧双2重放严格JSON和完整UART同F151。
- 仅1次C构建/1次RTL编译/1次性能8迭代DUT，13RTL/算法/port/启动链接/ISA语义不改，模型仅预算5M→25M；实际镜像仅2→8一字节。独立先验{o['steps']}步/{o['expected_physical']}物理拍/计算{ticks}/CRC{o['crcfinal']}，与DUT全RF/RAM、逐笔有序EX/WB/MEM、stall/flush/计时、{s['UART_bytes']}真实UART及窗口VCD一致。{s['segments']}段/{s['raw_records']}条/{s['raw_bytes']}rawB→{s['archive_bytes_including_metadata']}归档B；spool峰{s['spool_peak_bytes']}B，参考/最终检查峰值等见SUMMARY；各已测工作集<512MiB。
- 新DUT{s['DUT_host_seconds']:.3f}秒、参考{s['reference_host_seconds']:.3f}、最终检查{s['check_host_seconds']:.3f}，分项编码/核验与CPU时间保留，非受控加速结论。编译{s['compile_warning_groups']}警告类、归一路径同旧={s['warnings_identical_normalized']}。{s['protected']}原件/{s['frozen_inputs']}冻结输入核同；准备缺元数据的host重放失败保留，非额外DUT/期望修改。
- 仍有限性能8、旧验证2重放，非160/正式CoreMark/真实频率/ILA/FPGA。无真实退休PC/统一提交，固定模型/初态及直接进程测量边界保留；4GiB/最大容量未实际覆盖。原F159 PENDING由D160授权和本次实测取代，旧提案SHA/失败不改；B R1新回执未知，硬件STOP/候选告警不变。

'''
 decision='''## D-161：接受8迭代准入有限结果，不自动扩大名义正式长跑

- 2026-10-27，F160实测支持采用新的有界分段/绝对deadline与fail-closed监督候选，保持CPU/算法不变；旧双2等价和单8独立全态/逐笔/计时/真实串口证据充分，仅作已测范围验收。未采用以摘要代逐笔、预期回填、反复跑到通过或把实际未测容量写为通过。
- D160本阶段1C/1编译/1DUT已用完；不转为160迭代/正式成绩/CPU优化或PDS/硬件许可。下一只读收敛正式测量与初赛关键证据路径，使用这次实际代价，避免先消耗十多小时模拟名义分数；新实施范围另外明确。
- 原13RTL/B外设/冻结历史保持，F143稳定/F151校准、F146暂缓/F147告警、over_temp STOP不变。A仍拥有采集/模型/计量与最终集成，B资源守卫R1独立；未代发或推定B回执/改窗口。

'''
 for name,head,entry in [('FACTS.md','# 已验证事实与约束',fact),('DECISIONS.md','# 重要决策记录',decision)]:
  p=M/name;s0=p.read_text(encoding='utf-8-sig');assert s0.startswith(head);p.write_text(s0.replace(head,head+'\n\n'+entry,1),encoding='utf-8')
 hist=M/'history/2026-10-27-m2-completed';hist.mkdir()
 for name in ['CURRENT.md','INDEX.md','TODO.md','COLLABORATION.md']:(hist/name).write_bytes((M/name).read_bytes())
 current=f'''# 当前阶段与入口

更新：2026-10-27，F160/D160–161；恢复完整读WORKING_POLICY v1.3。

- **主线**：M2已有限完成：旧双2严格等价、主机>512MiB/1025段控制、1新C/1编译/1性能8迭代DUT与全态/逐笔/计时/{s['UART_bytes']}UART/窗口VCD通过。13RTL/算法不变，物理{o['expected_physical']}、计算{ticks}ticks、CRC{o['crcfinal']}；不是正式分数/160/FPGA验收。
- **当前阶段**：1+1许可已用完，进入正式测量路径/初赛证据缺口只读收敛，新增长跑/优化/硬件须另列范围；不重复运行本阶段。
- **协作/安全**：B R1 F158/D158新回执未知、原10/27 18窗口不改；A不等B整包。F143稳定/F151校准，F146暂缓/F147告警、over_temp STOP及真实时基/FPGA/ILA缺口保持。

入口：`reports/verification/2026-10-27-coremark-longrun-ready-m2.md`；`work/fpga/2026-10-27-coremark-longrun-ready-m2/SUMMARY.json、SOURCE_RECEIPTS.json、COMMANDS.md、postflight.json`及分层logs/runs/replays/controls。历史/协作按INDEX/COLLAB v1.88/TODO。

Git：本单元待按D126精确同步；前单元6a022107/513路径已核，不能以Git升级功能/硬件验收。
'''
 (M/'CURRENT.md').write_text(current,encoding='utf-8')
 p=M/'INDEX.md';s0=p.read_text(encoding='utf-8-sig');start=s0.index('最近更新：');end=s0.index('\n',start);s0=s0[:start]+'最近更新：2026-10-27，F160/D160–161：M2单8迭代及主机规模控制有限通过；13RTL不改、1+1已用完，非正式长跑/FPGA，B R1独立、硬件STOP。'+s0[end:];marker='|任务|最小读取入口与权威证据|';pos=s0.index('\n',s0.index('|---|---|',s0.index(marker)))+1;s0=s0[:pos]+'|当前M2真实8迭代/生产有界准入|F160/D160–161；`../reports/verification/2026-10-27-coremark-longrun-ready-m2.md`及`../work/fpga/2026-10-27-coremark-longrun-ready-m2/SUMMARY.json、SOURCE_RECEIPTS.json、COMMANDS.md、postflight.json`。旧双2重放、真实host>512MiB/1025段与单8新DUT分列；全态/逐笔/计时/实际PIN/窗口VCD有限通过。1C/1编译/1DUT已用完，未自动160/正式成绩/硬件；旧PENDING按D160取代|\n'+s0[pos:];p.write_text(s0,encoding='utf-8')
 p=M/'TODO.md';s0=p.read_text(encoding='utf-8-sig');s0=s0.replace('# 待办事项','# 待办事项\n\n## 当前M2 F160/D160–161（2026-10-27）\n\n- [x] 生产有界守卫、主机真实>512MiB/1025段、旧双2严格等价、单新C/1编译/1性能8迭代及全态/逐笔/计时/实际串口/窗口VCD有限通过；证据按INDEX。\n- [ ] 下一只读决策正式测量/初赛证据与实测长跑成本，不自动追加160或新CPU优化；真实FPGA/时基/ILA仍阻塞在安全及独立授权。\n- [ ] B R1新回执/候选v02审收按原任务，不重派核心，不等待整包阻主线。\n\n### 以下M2待批/执行中为历史，已由D160批准及F160结果取代\n',1);p.write_text(s0,encoding='utf-8')
 p=M/'COLLABORATION.md';s0=p.read_text(encoding='utf-8-sig');pos=s0.index('版本：COLLAB');s0=s0[:pos]+'''版本：COLLAB v1.88；2026-10-27，F160/D160–161。A-M2单8迭代及旧双2/主机规模分层有限验收，13RTL/算法不改，1+1范围用完；下一仅只读收敛正式测量/交付证据。A继续采集/模型/计量/集成，不代B重写资源工具。B R1新回执未知、原10/27 18窗口保持；不重复派核心。硬件STOP、F146暂缓/F147告警不变。

### 历史v1.87（执行中由F160完成结果取代）

'''+s0[pos:];p.write_text(s0,encoding='utf-8')
 # Immutable manifest after all stage products exist, excludes itself and final postflight.
 entries=[(p.relative_to(H).as_posix(),sha(p)) for p in sorted(H.rglob('*')) if p.is_file()]
 with (H/'SHA256SUMS.txt').open('x',encoding='utf-8') as f:
  for name,value in entries:f.write(value+'  '+name+'\n')
 check();protect();save(H/'postflight.json',dict(status='PASS_FINITE_8',manifest_entries=len(entries),manifest_SHA256=sha(H/'SHA256SUMS.txt'),protected=s['protected'],frozen=s['frozen_inputs'],stage_elapsed_total_seconds=time.monotonic()-stage['started_monotonic'],stage_clock_not_reset=True,C_builds=1,RTL_compiles=1,DUT=1,hardware='STOPPED'))
 for n in ['CURRENT.md','INDEX.md','FACTS.md','DECISIONS.md','TODO.md','COLLABORATION.md']:assert 'F160' in (M/n).read_text(encoding='utf-8-sig') or 'F-160' in (M/n).read_text(encoding='utf-8-sig')
 print('Report and six memory files written and reread; historical states retained; no new implementation')
