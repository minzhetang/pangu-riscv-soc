"""Close a tested compiler candidate; no new DUT/build/hardware operations."""
from pathlib import Path
import difflib,json,subprocess,sys
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8')
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import stage_coremark as s
def main():
    simulation=s.read(H/'simulation-result.json');q=s.read(H/'quality-compare.json');u=s.read(H/'uart-audit.json');w=s.read(H/'wave-audit.json')
    assert simulation['status']==u['status']==w['status']=='PASS'
    assert q['decision']=='STOP_O3_KEEP_O2_NO_PDS' and not q['all_seeds_benefit']
    assert not (H/'pds').exists() and not (H/'pds-process.json').exists()
    integrity=[]
    for row in s.read(s.B/'postflight.json')['source']:
        f=row['file'];assert s.sha(H/'source'/f)==s.sha(H/'source-before'/f)==s.sha(s.B/'source'/f)==row['sha256']
        integrity.append(dict(file=f,sha256=row['sha256'],unchanged=True))
    for sub in ['firmware','upstream']:
        for f in (H/sub).iterdir():assert s.sha(f)==s.sha(s.T/sub/f.name)
    assert s.sha(H/'port/core_portme.c')==s.sha(s.T/'port/core_portme.c')
    assert s.sha(H/'tests/tb_board_coremark.sv')==s.sha(s.B/'tests/tb_board_coremark.sv')
    assert all(s.sha(H/'models'/n)==s.sha(s.B/'models'/n) for n in ['cpu_program_reference.py','peripheral_checker.py'])
    old=s.read(s.T/'build-result.json')['artifacts'];new=s.read(H/'build-result.json')['artifacts'];flags=[]
    for name in ['performance','validation']:
        before=next(a for a in old if a['id']==name)['commands'][0]['argv'];after=next(a for a in new if a['id']==name)['commands'][0]['argv']
        norm=[v.replace(str(H),str(s.T)) for v in after];assert norm.count('-O3')==1;norm[norm.index('-O3')]='-O2';assert norm==before
        flags.append(dict(id=name,only_flag_change='-O2 -> -O3',all_sources_one_command=True))
    s.save(H/'consistency-receipt.json',dict(status='PASS',source=integrity,unchanged_TB=True,unchanged_two_models=True,unchanged_start_link_port_C=True,
        compiler_flag_comparison=flags,port_header_only_truthful_O3_metadata=True,protected=s.protect(),old_O2_not_rerun=True))
    scripts=['check_coremark.py','audit_uart.py','audit_wave.py','stage_coremark.py']
    for n in ['check_coremark.py','audit_uart.py','audit_wave.py']:
        with (H/(n+'.diff')).open('x',encoding='utf-8') as f:f.writelines(difflib.unified_diff((s.B/n).read_text().splitlines(True),(H/n).read_text().splitlines(True),fromfile='F143/'+n,tofile='O3/'+n))
    result=dict(date_beijing='2026-10-25',decision='D135/D136',fact='F144',stage='COMPLETE_STOP',
        outcome='O3_FUNCTIONAL_SHORT_TEST_PASS_BUT_REJECTED_FOR_COMPUTE_REGRESSION_AND_CODE_GROWTH',
        selected_baseline='F143 O2 board top (F142 PDS remains applicable)',candidate_default=False,
        rule_review=s.read(H/'rule-review.json'),compile=s.read(H/'compile-result.json'),simulation=simulation,quality=q,uart=u,wave=w,
        protected=s.protect(),RTL_changes=0,GCC_images=2,new_DUT_runs=2,old_DUT_reruns=0,PDS_runs=0,hardware='STOPPED',formal_score=False,
        cost_stage_script_status='NOT_EXECUTED; condition failed; no PDS project generated or license queried',
        tool_versions='same frozen xPack GCC15.2.0-1 and Icarus/vvp13.0 binaries; no reinstall or PATH change',
        limitations=['finite seeds/data/initial state; no entire ISA guarantee','EX not retirement, WB/MEM separately ordered','VCD windows not full algorithm waveform or ILA','no new frequency/resource measurement for rejected O3','no innovation or efficiency benefit claim from O3'])
    s.save(H/'RESULTS.json',result)
    # Full command vectors and native exit evidence, without proprietary contents.
    commands=['# A-COMPILE-QUALITY-M1 可复现命令与本次执行记录\n','2026-10-25，D135。原O2不重跑；所有路径为本机证据，不保证干净克隆一键复现。\n',
        'Python：`C:/Users/ANON_USER/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`；启动使用`-B`。无PATH/安装/系统环境修改。\n',
        '顺序：stage_coremark.py prepare → build → freeze → compile（固定2目标，非管理员外部许可一次，用完）→ run（普通权限2新DUT）→ audit_uart.py → audit_wave.py → quality_compare.py → finalize_evidence.py。\n',
        '编译各120s，DUT各600万物理拍/360s，trace/bus/VCD各256MiB；TB显式1ns/1ps、物理37037ps周期。当前无超时/清树/截断，不能据此认证通用runner清理机制。\n']
    for a in new:
        for p in a['commands']:commands.append('```json\n'+json.dumps(p,ensure_ascii=False,indent=2)+'\n```\n')
    for r in s.read(H/'compile-result.json')['rows']+simulation['rows']:commands.append('```json\n'+json.dumps(r['process'],ensure_ascii=False,indent=2)+'\n```\n')
    (H/'COMMANDS.md').write_text('\n'.join(commands),encoding='utf-8')
    report=s.P/'reports/verification/2026-10-25-compile-quality-m1.md'
    lines=['# O2→O3质量对照：功能短测通过，但拒绝O3候选\n',
        '日期2026-10-25（北京时间）；D135批准，F144实测/D136技术取舍。**保留O2，不把O3作为当前基线。**两个新DUT均通过严格检查，但两组计算都没有收益，代码均增加3080B；到此停止，不启动PDS。\n',
        '## 1. 范围、规则与真实性\n',
        'H=`D:\\A_FPGA_Comp\\work\\fpga\\2026-10-25-compile-quality-m1`。O2对照来自F143实际板级顶层/N234运行，代码/工具来自F136/F142；Git起点6d1ec32aacdfa728174c868a9fd35f491c57a7b9。原件、历史失败、O2输入与预期均保留，当前保护726项核同。\n',
        '官方固定commit1f483d5b8316753a742cbf5590caf5bd0a4e4777 [Run Rules](https://github.com/eembc/coremark/blob/1f483d5b8316753a742cbf5590caf5bd0a4e4777/README.md#run-rules)允许改变构建选项，但须统一编译选项、不改算法，正式报告须至少10秒。已实际打开官网及固定README，并核本地规则章节、6份源码SHA与既有官方固定归档一致；旧头文件注释/MD5清单问题及失败收据原样保留，不重下、不执行网页命令。GitHub commits API访问失败不影响已固定原件核对，未冒称查到新版本。\n',
        '只改新副本GCC选项-O2→-O3与core_portme.h的真实编译描述；PORT_DIFF.patch及consistency-receipt逐项证明。13RTL、冻结TB、两独立模型、启动、链接、端口C、算法、种子/2000字节/各1迭代、27MHz、N234及GPIO全释放保持；GCC命令路径归一后唯一开关差异得到核验。没有LTO/PGO、改算法/少计算或降低预期。\n',
        '## 2. 实测与取舍\n',
        '|种子|O2计算ticks|O3计算ticks|计算时间变化|O2→O3镜像B|功能|\n|---|---:|---:|---:|---|---|\n']
    for row in q['rows']:
        lines.append(f"|{row['id']}|{row['O2_ticks']}|{row['O3_ticks']}|{(-row['tick_reduction'])*100:+.4f}%（正数为变慢）|{row['O2_bytes']}→{row['O3_bytes']}|PASS|\n")
    lines.extend(['\n原始计算ticks不扣空读开销，两组empty窗口均26。仍在ROM32K、RAM32K/静态8K栈边界内，ELF为RV32I/ILP32、无未定义符号；代码增长不自动等于映射资源增加，O3未运行PDS，不能编造新LUT/FF/DRM数或时序。\n',
        '|种子|主机运行秒|物理拍/推进|stall/flush|UART字节|最低SP/有限观测深度|\n|---|---:|---|---|---:|---|\n'])
    for row,run in zip(q['rows'],simulation['rows']):
        m=row['total_metrics'];lines.append(f"|{row['id']}|{run['process']['elapsed_seconds']:.3f}|{m['physical']}/{m['advances']}|{m['stall']}/{m['flush']}|{row['UART_bytes_O3']}|0x{row['stack_min_SP']:x}/{row['observed_stack_depth']}B|\n")
    lines.extend(['\n每笔x2合法WB均核在0x16000–0x18000；这是本次有限执行的SP观测，不是所有输入/中断/递归的最坏栈证明。每种子EX/WB/READ/STORE计数、每笔有序摘要、阶段0/1/2/3/4、12笔timer LOAD及全过程结果详RESULTS与原始check-result。\n',
        '全RF/32K RAM与独立顺序模型一致，每笔EX/WB/MEM无去重，独立外设计时模型核真实MMIO，正常main返回0/SP恢复0x18000/EBREAK、尾32拍无副作用。原三算法/种子CRC、错误标志、timer调用次数、实际高低字时间戳及差值通过。新镜像布局/PC/编译描述变化，不能强求与O2全RF/RAM字节相同；使用同样严格的独立模型标准，不根据DUT反填。\n',
        '## 3. 输出、波形与质量解释\n',
        '完整连续UART引脚记录由独立中心采样和精确跳变时刻双重核验，逐字节对应独立模型生成的RAM报告，未用DUT未核数据作预期。4种实际引脚日志损坏被拒绝；合成1正4负仅检查解析器，不增加DUT次数。原生普通VCD仅明确窗口，逐配置解析pre/post计数/相位和全部12笔timer LOAD捕获，不宣称完整算法波形、退休PC或ILA。\n',
        '|种子|格式化等 O2→O3 ticks|UART阶段 O2→O3 ticks|\n|---|---|---|\n'])
    for row in q['rows']:lines.append(f"|{row['id']}|{row['formatting_ticks_O2']}→{row['formatting_ticks_O3']}|{row['UART_phase_ticks_O2']}→{row['UART_phase_ticks_O3']}|\n")
    lines.extend(['\n全程序结束稍早不能替代算法计算更快；启动/格式化与计算/输出分列。当前编译器优化没有提供目标计算收益，且ROM空间消耗更高，因此不继续参数搜索，也不将它包装成创新。O2/F143仍是后续工作的基线，F142原资源/27MHz证据继续只适用于原O2镜像。\n',
        '## 4. 告警、未执行项与交付\n',
        '两次GCC构建/工具检查及两次Icarus编译无错误；继承regfile时间单位、部分模块未显式单位与官方模型grsn隐式线网告警保持，没有为消告警改源码。编译43.313/43.515秒；两个仿真均未超时/截断/强杀，主机秒不冒称FPGA计时。\n',
        '仍是短实验，上游不足10秒和Errors detected原文保留，不是正式成绩。0PDS/0位流/0硬件，未查询或更改许可证；F142最后提示余9天仅历史，需人工官方续期。原7个constant-probe根因、14个外部IO时序/CDC及over_temp STOP保持，纯软件通过不能解除。\n',
        'B沿F139既有整改/最终包与10/27 18:00北京时间窗口，不重索已有材料、不派新核心任务；当前有限系统TX证据不关闭B整包/RX条件。无本轮新包/送达/承诺事实。\n',
        'H/COMMANDS.md提供完整命令/退出/预算；RESULTS、consistency-receipt、postflight及最终SHA、compile/build/simulation结果、各真实日志/全态/trace/bus/连续PIN/普通窗口VCD与审计提供本次证据。旧失败与SHA不覆盖。专有模型/工具/大型产物留本地；Git同步不是干净克隆一键复现保证。\n',
        '唯一下一建议：A-CONTROL-FLOW-QUALITY-M0，仅只读现有O2源码与已验轨迹，对JAL/条件分支/返回重定向分别量化，再收敛一项能独立验收的最小减泡方案与风险/回归范围；不自动开始RTL/TB/模型修改或新仿真，不预设预测器/Cache/M，也不承诺提升。现有软件/内存/外设基线保护，硬件仍停止。\n'])
    with report.open('x',encoding='utf-8') as f:f.writelines(lines)
    s.save(H/'postflight.json',dict(stage='COMPLETE_STOP',date_beijing='2026-10-25',source=integrity,protected=s.protect(),
        report_SHA256=s.sha(report),result_SHA256=s.sha(H/'RESULTS.json'),selected='F143 O2',O3='REJECTED_NO_COMPUTE_BENEFIT',PDS_runs=0,hardware='STOPPED'))
    print(json.dumps(dict(status=result['outcome'],report=str(report),protected=result['protected'])))
if __name__=='__main__':main()
