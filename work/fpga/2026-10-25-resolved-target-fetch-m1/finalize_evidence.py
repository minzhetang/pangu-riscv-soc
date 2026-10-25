"""Close D139 results with explicit new-warning hold; no further tool execution."""
from pathlib import Path
import json,hashlib,re,sys,csv
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_redirect as s;import core_stage
def main():
    core_stage.protect();initial=s.read(H/'initial-compile-result.json');comp=s.read(H/'core-compile-result.json')
    small=s.read(H/'small-result-v2.json');reg=s.read(H/'regression-result.json');core=s.read(H/'core-result.json');quality=s.read(H/'quality-compare.json');pds=s.read(H/'pds-audit.json');cost=s.read(H/'pds-feature-cost.json')
    assert initial['status']==comp['status']==small['status']==reg['status']==core['status']=='PASS'
    assert len(small['cases'])==67 and len(reg['cases'])==763 and len(core['rows'])==2
    for n in ['small-wave-audit.json','prefetch-wave-audit.json','wave-audit.json','uart-audit.json','checker-negative-result.json']:assert s.read(H/n)['status']=='PASS'
    assert quality['all_seeds_benefit'] and pds['constant_probe_count']==8
    sources=[]
    for row in s.read(s.B/'postflight.json')['source']:
        n=row['file'];before=s.sha(H/'source-before'/n);after=s.sha(H/'source'/n)
        assert before==row['sha256'] and (before!=after)==(n in ['cpu.v','soc_top.sv'])
        sources.append(dict(file=n,before_SHA256=before,after_SHA256=after,changed=before!=after))
    warning_scope=[];oldflow=(s.P/'work/fpga/2026-10-25-board-top-m1/pds/flow.log');newflow=H/'pds/flow.log'
    for base in [oldflow,newflow]:
        t=s.log(base);lines=t.splitlines();hits=[i+1 for i,l in enumerate(lines) if 'constant probe' in l]
        warning_scope.append(dict(path=str(base),sha256=s.sha(base),constant_probe_count=len(hits),line_numbers=hits,
            named_net_in_warning=False,stage='sdm2adm',other_loop_lines=[l for l in lines if 'loop' in l.lower() and 'constant probe' not in l.lower()]))
    reports=[];other=[];large=[]
    for f in (H/'pds').rglob('*'):
        if f.is_file() and f.suffix.lower() in ['.rtr','.ccr','.rpt','.log']:
            if f.stat().st_size>=2000000:large.append(str(f));continue
            reports.append(str(f));lines=[l for l in s.log(f).splitlines() if re.search(r'combinational.*loop|loop.*combinational|loop.*net|loop.*path',l,re.I)]
            if lines:other.append(dict(path=str(f),lines=lines))
    s.save(H/'constant-probe-review.json',dict(status='OPEN_NEW_WARNING_HOLD',old_and_new=warning_scope,reports_read=reports,skipped_large=large,other_named_loop_results=other,
        own_source_observation='redirect_request depends on registered EX/forwarding state; hit drives registered PC/IFID, ROM response is one-edge. This does not prove all mapped combinational SCCs absent.',
        conclusion='8 vs 7, one additional unnamed constant-probe warning; not classified as harmless or proven physical loop; keep F143 stable baseline',new_PDS_runs=0,hardware='STOPPED'))
    with (H/'CASE_RESULTS.csv').open('x',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['group','id','verdict','new_DUT_processes','evidence'])
        for group,rows in [('directed',small['cases']),('default-regression',reg['cases']),('coremark',core['rows'])]:
            for row in rows:w.writerow([group,row['id'],row['status'],1,row['process']['stdout']])
    s.save(H/'RESULTS.json',dict(date_beijing='2026-10-25',fact='F146',decision='D139/D140',stage='COMPLETE_WITH_OPEN_FINDING',
        outcome='FINITE_FUNCTION_PERFORMANCE_PASS_INTERNAL_STA_PASS_NEW_CONSTANT_PROBE_WARNING_OPEN',stable_baseline='F143 O2 unchanged',candidate_promoted=False,
        source=sources,initial_compiles=16,core_compiles=2,new_DUT_processes=dict(directed=67,default_regression=763,coremark=2,total=832),
        directed_status=small['status'],default_regression_status=reg['status'],coremark_status=core['status'],quality=quality,PDS=pds,cost=cost,
        checker_v1_failure_preserved=s.read(H/'checker-v2-correction.json'),PDS_parser_v1_failure_preserved=True,
        no_extra_DUT_for_checker_fix=True,no_extra_PDS_for_parser_fix=True,default_unspecified_counters=s.read(H/'regression-count-compare.json'),
        native_VCD_audits=dict(directed=67,core_unique=2,default763_VCDs_preserved_but_not_fully_reparsed=True),
        UART_bytes=[r['check']['UART_frames'] for r in core['rows']],original_protection=s.protect(),core_frozen_entries=len(s.read(H/'core-frozen.json')['files']),
        GCC_runs=0,PDS_runs=1,no_bitstream=True,hardware='STOPPED',formal_score=False,
        limitations=['finite functional/performance evidence, not full ISA/official score/FPGA/ILA','EX not retirement, WB/MEM separately ordered','mapped internal timing only; 14 external IO without delay and CDC remain open','tool estimated maximum clock decreased; not measured Fmax','8 constant-probe warnings vs old7; root cause not closed, candidate not promoted']))
    commands=['# D139本轮命令和原生结果\n','Python绝对路径`C:/Users/tamii/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`，均用`-B`，无安装/PATH/系统环境修改。\n',
        '执行顺序：stage_redirect prepare/freeze → compile-initial（固定16目标、非管理员外部权限、用完）→ small（首个检查器格式误报停止）→ resume_validation prepare/run（同输出复核1次，接续66个新DUT）→ regression（763）→ core_stage prepare/compile（固定2目标另批、用完）/run（2）→各独立审计/质量统计 → cost_stage prepare/run（1次非管理员PDS另批、用完）→ v1审计网名假设失败 → cost_stage_v2 audit（0新PDS）。\n',
        '每次完整argv/cwd/returncode/timeout/cap/耗时见以下记录；18编译各120s，定向/回归每进程30s，CoreMark600万拍/360s，各trace/bus/fetch/VCD256MiB、stdout/stderr8MiB。实际无超时/截断/强杀，不认证通用清理机制。定向10ns时钟、CoreMark37037ps周期（名义27MHz），显式1ns/1ps TB；不把旧未声明延时猜为ns。\n']
    for row in initial['rows']+comp['rows']+small['cases']+reg['cases']+core['rows']:
        commands.append('```json\n'+json.dumps(row['process'],ensure_ascii=False,separators=(',',':'))+'\n```\n')
    commands.append('```json\n'+json.dumps(s.read(H/'pds-process.json'),ensure_ascii=False,indent=2)+'\n```\n')
    (H/'COMMANDS.md').write_text('\n'.join(commands),encoding='utf-8')
    report=s.P/'reports/verification/2026-10-25-resolved-target-fetch-m1.md'
    lines=['# 已决目标取指实验：有限性能收益成立，新增告警待闭\n',
        '2026-10-25（北京时间）；D139批准，F146实测/D140技术取舍。**候选功能/计算收益及内部27MHz时序通过，但constant-probe由7增8，暂不替换F143/O2稳定基线。**无位流或硬件操作。\n',
        '## 1. 源码、输入与范围\n',
        'H=`D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-resolved-target-fetch-m1`，13源来自F143；Git起点f28794776cf559d910d168954bd0209ae5e9233a。仅新cpu.v默认关闭的RESOLVED_TARGET_FETCH参数/请求-PC标签/IFID-PC选择及新soc_top.sv一处显式开启绑定；另外11源、原两个O2 ELF/bin和完整INIT表不改，source-before/models-before保留。CPU_DIFF/SOC_DIFF、RESULTS的13项SHA及最终清单提供准确差异/字节证据。\n',
        '同样的EX比较/跳转目标先进入ROM采样相位，下一推进沿核标签和非零返回才保留目标IF/ID，仍清错误路径ID/EX。无效/复位/EEI/非对齐及零/未映射返回保守回旧路径；不硬编码CPU ROM容量，不改比较/前推/load-use、数据存储、时钟边沿、ISA/异常、启动链接、算法、外设或B接口。pc仍是取指请求，不是退休PC。\n',
        '## 2. 实际验证\n',
        '|层级|本次真实结果|边界|\n|---|---|---|\n|编译|16快速目标+2官方存储CoreMark目标，18/18通过|固定两批非管理员外部权限，均已用完|\n|定向|34程序、67新DUT，功能/终态/每笔EX-WB-MEM/物理计数/完整请求账本通过|PF0/PF1对照，复位案例仅PF1，非完整ISA|\n|原回归|参数0下原763例严格PASS|原输入/预期不改；stall17/flush20项仍NOT_SPECIFIED|\n|CoreMark|两原O2镜像、官方primitive模型、N234，两新DUT严格PASS|2K/各1迭代，不足10秒|\n|负控/波形|检查器1正4负、UART解析器合成1正4负及4真实日志损坏拒绝；67完整定向VCD和2窗口CoreMark VCD逐配置核验|都不是新增DUT或ILA|\n|PDS|仅一次compile/synthesis/map/pnr/report_timing通过，退出后检查新产物|内部27MHz，不生成位流|\n',
        '总计832个新DUT进程，不把同输出复核、解析器负控/波形再分析或重复解析计入。默认763原波形保留，没有把它们宣称本轮逐VCD完整解析；其原严格日志/RF/RAM/专用LOAD-STORE-EEI等检查保持。显式独立stall/flush期望746/743项通过，17/20项仅NOT_SPECIFIED，并另核全部763历史计数一致（不是补成独立期望）。\n',
        '定向覆盖六分支、正负/PC+4/连续目标、JAL/JALR rd=rs1/返回/链接首条消费、跨4K银行/合法NOP、两源前推/WB→ID与load依赖、load写x0、旧MEM STORE及新目标LOAD、错误路径STORE/ECALL/EBREAK清除、目标ECALL排空、零字/未映射/非对齐回退和请求后复位。复位真实REQ→SAMPLE→RESET取消→重启REQ→SAMPLE→REDIR→APPLY，全账本不去重；首个中断尝试没有合法EX/WB/STORE被隐藏。\n',
        '## 3. 同条件计算收益与代价\n',
        '|种子|原O2 ticks|候选O2 ticks|少tick|计算时间减少|同频吞吐比|\n|---|---:|---:|---:|---:|---:|\n']
    for r in quality['rows']:lines.append(f"|{r['id']}|{r['O2_before_ticks']}|{r['O2_candidate_ticks']}|{r['ticks_saved']}|{100*r['time_reduction']:.4f}%|{r['speedup']:.6f}×|\n")
    lines += ['\n两个镜像逐字节同旧。计算窗口EX序列SHA、EX/LOAD/STORE/WB数量同旧，load-use20714/21220不变，重定向149422/162524均按独立参考预测命中。新构成2×EX+2×load-use+2×redirect，残差0；测得少tick恰等于2×这些重定向数。不是少做工作、去重写回或改算法。\n',
        '全RF/32K RAM与独立ISA模型一致，每笔EX/WB/MEM各自有序无去重；MMIO样本来自独立外设/物理计数模型而非DUT返回值反填，12实际timer LOAD、阶段0–4含启动BSS零写、返回0/SP0x18000/正常EBREAK和尾32均通过。全程请求/标签/命中/返回与每笔独立参考重定向及目标EX间隔对应，不能仅凭最终答案正确验收。\n',
        '|种子|实际全程命中|目标EX间隔4拍|UART字节|格式化ticks 前→后|UART阶段ticks 前→后|\n|---|---:|---:|---:|---|---|\n']
    for r,run in zip(quality['rows'],core['rows']):
        pf=run['check']['prefetch_audit'];lines.append(f"|{r['id']}|{pf['hits']}|{pf['successor_EX_gaps'].get('4',0)}（另1笔目标停止）|{run['check']['UART_frames']}|{r['formatting_ticks_before']}→{r['formatting_ticks_after']}|{r['UART_phase_ticks_before']}→{r['UART_phase_ticks_after']}|\n")
    lines += ['\n空读窗口仍26，不直接从raw扣除。最低观测SP0x17e20，有限栈深480B，8K预留未越界；不是最坏栈证明。完整UART实际引脚时间线/中心解码逐字节匹配独立参考报告；N234和字节数不变，UART阶段仅+2tick。CPU更快导致串口轮询读/停顿/分支次数增多，不能用全程stall/flush增长否定计算区收益或把主机秒当FPGA速度。普通原生VCD明确窗口，另连续PIN及完整fetch账本，不冒充完整算法/ILA。\n',
        '|PDS指标|原F142|候选|变化|\n|---|---:|---:|---|\n',
        f"|LUT|1805|{pds['resources']['LUT']}|+108（{108/1805*100:.3f}%）|\n",
        f"|FF|1519|{pds['resources']['FF']}|+33（{33/1519*100:.3f}%）|\n",
        '|DRM36 / IO|14 / 15|14 / 15|无增加|\n|内部最差setup / hold|23.279 / 0.129ns|20.524 / 0.116ns|27MHz均正裕量|\n|工具估算最高频率|72.6850MHz|60.5583MHz|降低，非实测板级Fmax|\n',
        '新增33个标签/valid FF的INIT0、RF992 INIT0、板级复位3级和15针位/原94约束均实际核对；28个DRM18/1792 INIT片与候选完整O2表核同，ROM零半字共享连接与PnR身份核对。不能以约束零warning或全部internal约束满足替代外部时序/CDC；5异步输入/9输出仍无外部delay。\n',
        '收益仅在相同27MHz条件下成立；工具估算最高频率下降表明新取指路径有真实时序代价，不能宣传Fmax、最高频率下吞吐或能效优化。板卡实测频率/温度/功耗/片上波形均无。\n',
        '## 4. 失败、解析修正与未闭问题\n',
        '首个PF0定向v1检查误报all RAM：预期用2位hex，vvp32位表达式输出8位hex。32768字节逐值完全相同，仅文本表示不同。原small-result.json和首个check-result FAIL/原checker原样保留；新check_redirect_v2只按字节比较，在同输出上复核通过，未改RTL/TB/预期也未重跑该DUT。后续66个新进程正常接续，small-result-v2为本层权威，1正4负另证字节损坏/重复WB/错标签/漏RESET不能通过。\n',
        'PDS v1审计假定扁平storage/网名前缀，当前综合网表改为局部bank/及soc/storage/，在同一新产物上失败。原脚本保留，新v2只扩已核别名，仍严格要求每位两处半字消费者，128项通过；未放宽INIT/时序/接口检查，未重跑PDS。修正记录含原/新脚本SHA和实际别名消费者明细。\n',
        '**constant-probe由原7变8**，均在sdm2adm阶段，未给网名；新增告警原因未闭，不能解释为无害或宣称真实组合环。已读本次.rtr/.ccr/.rpt/.log中小于2MB的相关报告，未找到其他命名组合环信息，覆盖/跳过范围见constant-probe-review.json。源码上新请求依赖寄存EX/前推状态、hit写寄存PC/IFID、ROM一沿响应，这不等于证明整个映射网表无组合SCC。\n',
        f"本次许可证成功使用，实际提示余{pds['license_days_remaining']}天，请及时按官方渠道续期；未读取/保存许可证内容、机器码，未配置授权。其他原regfile继承/缺少时间单位和官方grsn模型告警保留，18编译0错误；PDS其他警告逐类计数见pds-audit，不静默消除。\n",
        '## 5. 当前结论、入口与下一步\n',
        '有限软件功能/计算收益和内部STA通过，候选保留；因新增未定位告警，暂不替换F143稳定集成源。原默认参数/原镜像/全部历史证据保护，3912初始保护项及core-frozen条目结束核同。最终SHA/精确命令/逐例CASE_RESULTS.csv、RESULTS、postflight为入口；各原始日志/全态/trace/bus/fetch/PIN/普通波形、错误和修正分层保留。专有模型/工具/大产物只留本地，不随Git分发，也不声称干净克隆一键复现。\n',
        '新方案是有限输入下有实证的工程效率改进候选，不证明学术首创、完整RV32I/所有程序正确或正式CoreMark成绩；不足10秒与Errors detected原文仍在。EX非退休、WB/MEM分流、固定存储/初态限制保持。无GCC/新软件安装/环境修改/位流/硬件，over_temp STOP保持。B原F139整改/10月27日18北京时间窗口不变，无新B包/任务/外发，A不替队员重复实现。\n',
        '唯一下一建议A-PREFETCH-WARNING-M0：仅只读对照新旧综合网表/层级与constant-probe上下文，定位新增告警是否能归属具体路径；不足时准备最小官方咨询材料，不改RTL、不重构/重新构建、不操作硬件或代发。不能为消警告盲改功能或降低检查标准，也不因性能收益自动恢复硬件。\n']
    with report.open('x',encoding='utf-8') as f:f.write('\n'.join(lines))
    s.save(H/'postflight.json',dict(status='COMPLETE_WITH_NEW_WARNING_OPEN',date_beijing='2026-10-25',source=sources,protected=s.protect(),core_frozen_entries=len(s.read(H/'core-frozen.json')['files']),
        report_SHA256=s.sha(report),RESULTS_SHA256=s.sha(H/'RESULTS.json'),new_DUT_runs=832,PDS_runs=1,hardware='STOPPED',candidate_promoted=False,stable_baseline='F143 O2'))
    print('Recorded832 actual DUT/18compile/1PDS; finite benefit+STA pass, new warning hold; report',report)
if __name__=='__main__':main()
