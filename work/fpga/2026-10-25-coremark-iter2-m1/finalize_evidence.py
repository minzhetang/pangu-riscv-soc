"""Collect completed calibration evidence; refuses to publish before both pass."""
from stage_coremark import *
def run():
    protect();frozen=read(H/'frozen.json')['files']
    for row in frozen:assert sha(row['path'])==row['SHA256']
    for row in read(H/'audit-scripts-frozen.json')['files']:assert sha(row['path'])==row['SHA256']
    rows=[];source=[];oracles=[];cost=[]
    for p in sorted((H/'source').iterdir()):
        assert sha(p)==sha(H/'source-before'/p.name)==sha(B/'source'/p.name)
        source.append(dict(file=p.name,SHA256=sha(p),unchanged=True))
    for name in ['performance','validation']:
        tid=name+'-N234';d=H/'runs'/tid;result=read(d/'check-result.json');assert result['status']=='PASS' and result['frozen_comparison']['status']=='PASS'
        ref=read(H/'oracles'/name/'expected.json');old=read(B/'runs'/tid/'check-result.json');proc=read(d/'process.json');assert proc['returncode']==0 and not proc['timed_out'] and not proc['cap']
        for p in [d/'trace.log',d/'bus.log',d/'wave.vcd']:assert p.stat().st_size<=256*1024*1024
        assert ref['report_SHA256']==sha(d/'ram-output.txt') and ref['RAM_SHA256']==sha(H/'oracles'/name/'expected-ram.bin')
        row=dict(id=tid,status='PASS_LIMITED_ITER2',iterations=2,process=proc,metrics=result['metrics'],trace_counts=result['trace_counts'],streams=result['streams'],timer_reads=result['timer_reads'],detail=result['detail'],UART_frames=result['UART_frames'],frozen_comparison=result['frozen_comparison'],files={p.name:dict(bytes=p.stat().st_size,SHA256=sha(p)) for p in d.iterdir() if p.is_file()})
        rows.append(row);before=old['detail']['raw_ticks'];after=result['detail']['raw_ticks']
        cost.append(dict(id=tid,C1=before,C2=after,second_iteration_increment=after-before,delta_from_two_times_C1=after-2*before,old_full_physical=old['metrics']['physical'],new_full_physical=result['metrics']['physical'],old_UART_bytes=old['UART_frames'],new_UART_bytes=result['UART_frames'],new_nominal_compute_seconds=after/27000000,new_DUT_host_seconds=proc['elapsed_seconds'],old_files={n:(B/'runs'/tid/n).stat().st_size for n in ['trace.log','bus.log','wave.vcd']},new_files={n:(d/n).stat().st_size for n in ['trace.log','bus.log','wave.vcd']},fit_is_only_two_points=True,not_a_speedup_claim=True))
        small={k:v for k,v in ref.items() if k not in ['io_reads','io_writes']};small['full_oracle_SHA256']=sha(H/'oracles'/name/'expected.json');oracles.append(small)
    UART=read(H/'uart-audit.json');wave=read(H/'wave-audit.json');assert UART['status']==wave['status']=='PASS'
    save(H/'ORACLE_SUMMARIES.json',dict(rows=oracles,old_calibration=[{k:v for k,v in read(H/'oracles'/('old-'+n)/'expected.json').items() if k not in ['io_reads','io_writes']} for n in ['performance','validation']],new_DUT_runs=0,expected_before_DUT=True))
    save(H/'SOURCE_RECEIPTS.json',dict(source=source,official_six_SHA=[dict(name=p.name,SHA256=sha(p),unchanged=sha(p)==sha(T/'upstream'/p.name)) for p in sorted((H/'upstream').iterdir()) if p.is_file()],port_header_unchanged=sha(H/'port/core_portme.h')==sha(H/'port-before/core_portme.h'),firmware_unchanged=[dict(name=p.name,SHA256=sha(p),unchanged=sha(p)==sha(T/'firmware'/p.name)) for p in sorted((H/'firmware').iterdir())],frozen_inputs=len(frozen),original_inputs=protect()))
    save(H/'quality-compare.json',dict(rows=cost,stable='F143/O2',candidate_F146_enabled=False,method='actual raw compute difference, actual file sizes/host duration and same code-image one-byte iteration input change',formal_score=False,limitations=['two iteration points do not prove all later costs are affine','nominal27MHz is not a hardware frequency measurement','DUT host seconds are resource cost, not FPGA speed','WB/MEM separate, no retirementPC','no new PDS/bitstream/FPGA/ILA']))
    refdiff=''.join(difflib.unified_diff((H/'models-before/cpu_program_reference.py').read_text().splitlines(True),(H/'models/cpu_program_reference.py').read_text().splitlines(True),fromfile='models-before/cpu_program_reference.py',tofile='models/cpu_program_reference.py'))
    (H/'REFERENCE_BUDGET_DIFF.patch').write_text(refdiff,encoding='utf-8');(H/'PORT_DIFF.patch').write_text(read(H/'SOURCE_DIFFS.json')['port'],encoding='utf-8');(H/'TB_DIFF.patch').write_text(read(H/'SOURCE_DIFFS.json')['TB'],encoding='utf-8')
    result=dict(date_beijing='2026-10-25',fact='F151',approval='D149',acceptance='D150',stage='A-COREMARK-ITER2-M1',outcome='PASS_LIMITED_DOUBLE_ITERATION_CALIBRATION',source=source,build=read(H/'build-result.json'),compile=read(H/'compile-result.json'),new_DUT_runs=2,rows=rows,oracles_pre_DUT=True,oracle_calibration_old_programs=2,oracle_new_programs=2,checker_controls=read(H/'checker-negative.json'),UART=UART,wave=wave,quality=cost,ports_changed=['core_portme.c ITERATIONS initializer and positive guard'],CPU_RTL_changed=False,official_algorithm_changed=False,reference_change='budget2M->5M only; new pre-DUT independent schedule in precompute.py',old_inputs_unchanged=protect(),frozen_inputs_unchanged=len(frozen),PDS_runs=0,new_install_environment_license_changes=False,stable='F143/O2',candidate='F146_HELD',formal_score=False,hardware='STOPPED',B='R1-R3 original tasks; user reported relay sent; no new reply inferred')
    save(H/'RESULTS.json',result)
    # Human-readable exact commands are generated from actual completed process records.
    commands=['# 实际可复查命令与原生结果','','每例编译120s、DUT600s/8M拍、每trace/bus/VCD256MiB；现有工具、绝对路径/B/VPI、不改PATH。外部编译仅本批2项、已用完。原生退出后才检查新产物，退出0不是功能证明。完整参数为JSON argv，按数组分词，不把它拼接当shell命令。','','GCC build/objcopy/objdump/readelf/nm共10调用；RTL编译2；新DUT2。独立参考旧2校准/新2预计算、1+7纯检查器控制、UART/VCD重审和日志负例均不计DUT。','']
    procs=[]
    for x in read(H/'build-result.json')['artifacts']:procs += [('build '+x['id'],p) for p in x['commands']]
    procs += [('RTL '+x['id'],x['process']) for x in read(H/'compile-result.json')['rows']]
    procs += [('DUT '+x['id'],x['process']) for x in rows]
    for label,p in procs:commands += ['## '+label,'','```json',json.dumps(p,ensure_ascii=False,indent=2),'```','']
    (H/'COMMANDS.md').write_text('\n'.join(commands),encoding='utf-8')
    report=r'''# 双种子各2迭代：真实程序校准有限通过

日期2026-10-25，北京时间；授权D149、实测F151/结论D150。**稳定F143/O2的同一CPU/同步存储/板级top下，性能与验证种子各2迭代真实执行、全状态/逐笔副作用/计时及完整UART有限通过**。CPU与官方算法不改；这是重复执行校准，不是正式≥10秒成绩、CPU完整正确性、优化收益或实机验收。

## 1. 修改、基线和冻结顺序

独立`work/fpga/2026-10-25-coremark-iter2-m1`保留source-before、port-before、models-before。只把新port/core_portme.c的seed4硬编码1接入ITERATIONS（默认1、正32位保护、禁0自动校准），构建只用2；port头/计时/启动/链接、官方六源、F143整组13RTL及B核心/包装不变。新TB只将6M上限改8M；新参考副本只将2M步预算改5M，ISA语义不变。准确PORT_DIFF/TB_DIFF/REFERENCE_BUDGET_DIFF/CHECKER_DIFF及SOURCE_RECEIPTS/IMAGE_DIFF.json给实物证据。

两个新bin与旧版分别同15912/15920字节，均只在offset15904把迭代初值01改02，执行代码不变；ELF PT_LOAD与运行报告均证2。GCC15.2.0-1、RV32I/ILP32、统一O2及其他选项不改，无新工具/float/M/LTO或全ISA补齐。新初始化逐字节反解匹配新镜像和RAM A5；没有把旧PDS的INIT/位流当新双迭代工程已映射。

先复制SHA/构建，再在DUT前独立校准固定两拍同步内存时序参考：EX首拍6、普通后继+2、load-use另+2、重定向另+4、READ为EX+2、STORE为EX+1。此模型先重放两个旧F143程序，逐逻辑EX/WB/MEM digest、所有RF/RAM、12计时LOAD/完整报告/物理拍均同原证据，**不是重跑旧DUT**。再为新2迭代镜像预计算并冻结每笔有序流/全态/计时/UART报告及crcfinal，未借用新DUT数据回填，也未按旧值乘2。

预计性能raw4207378/crcfinal72be、验证4526490/fe8c在新DUT启动前已落盘；80项pre-DUT冻结及原件保护收据核同。验证程序真实2005976架构步超过旧2M限制，预先按已批5M调整的是验证预算，未修改CPU/功能语义。模型仍受5M步/600秒限制。

## 2. 实际执行和严格判定

现有合法Icarus/vvp13.0显式绝对路径/-B/VPI；仅本批固定2次非管理员外部编译、每次120秒，许可用完。两个普通vvp各最多8M拍/600秒，各trace/bus/nativeVCD256MiB，stdout/stderr受限；真实完成后核新产物。完整命令/原生rc/日志在COMMANDS、compile-result和runs各process/stdout/stderr。编译原继承时间单位/官方模型隐式grsn等警告如实保留，不改RTL消警告。

逐项实测见下表（自动从本次真实结果填入）：
'''
    report+='\n|事项|性能种子|验证种子|\n|---|---:|---:|\n'
    for label,fun in [('迭代数',lambda r:2),('计算raw ticks',lambda r:r['detail']['raw_ticks']),('完整物理拍',lambda r:r['metrics']['physical']),('架构EX观察',lambda r:r['trace_counts']['EX']),('stall',lambda r:r['metrics']['stall']),('flush',lambda r:r['metrics']['flush']),('最终CRC',lambda r:r['frozen_comparison']['crcfinal']),('完整UART帧/字节',lambda r:r['UART_frames']),('DUT主机秒，仅资源成本',lambda r:r['process']['elapsed_seconds'])]:report+='|'+label+'|'+'|'.join(str(fun(r)) for r in rows)+'|\n'
    report+=r'''
全32RF/32K RAM、每笔合法EX/WB/MEM及各自顺序不去重、stall/flush/总物理拍均通过独立模型，精确计时与先冻结参考一致；真实Iterations2/seed4=2/迭代相关CRCfinal/全部报告SHA匹配。BSS零写的phase0保留，完整相位0/1/2/3/4；一次start/stop、12实际高低高LOAD与沿前计数一致、timer/port/overflow错误0，main返回0/SP恢复18000，正常EBREAK及尾32拍无副作用；关键数据/控制X-Z会失败。

新检查器沿用逐笔比较，又用frozen_checks同一路径核前置参考所有RF/RAM/流摘要/计时/报告/预算。1正确控制+7篡改（Iterations1、crcfinal错、缺WB、多MEM、raw错、漏BSS相位、超预算）均拒绝，只有host判据自查不是新DUT。不会因最终答案正确忽略重复写回。

算法窗口内无UART或其它MMIO写，完整输出都在phase3之后。实际UART pin连续变化独立时间/位宽/中心解码全部报告，与先冻结报告和实际合法TX STORE一一核对；普通原生VCD只采明确窗口，12计时LOAD/相位与沿后计数检查通过。UART真实日志四类损坏副本被拒绝，原证据不改；重审/合成负例不记新DUT。详uart-audit/wave-audit，不把窗口VCD或文本pin观察当片上ILA。

## 3. 校准结果、代价与限制

'''
    report+='|计算指标|性能|验证|\n|---|---:|---:|\n'
    for label,key in [('原1迭代C1','C1'),('新2迭代C2','C2'),('实际第二次增量C2−C1','second_iteration_increment'),('C2−2×C1','delta_from_two_times_C1')]:report+='|'+label+'|'+'|'.join(str(x[key]) for x in cost)+'|\n'
    report+=r'''
两点显示重复计算基本同量级但不精确线性；不能将C2乘任意倍当正式长测或保证129/120次足够，后续数据/CRC影响分支路径。主机秒/日志大小是仿真资源成本，不是FPGA速度。UART字节量保持，未少打印/缩工作量制造性能收益；2迭代不是优化实验。

两组仍不足10个名义秒，官方不足10秒/Errors detected提示与SIM ONLY, NO VALID SCORE保留。PASS含义是这些有限程序正确执行/计时/输出校准通过，不改上游判据来宣称有效成绩。27MHz仍配置名义值，未实测时基；64位进位重试/回绕不在本程序动态覆盖内。WB/MEM分流、无退休PC、固定RF/RAM初态限制保留。

本轮0PDS/位流/服务器/设备枚举/JTAG/上电/Flash/供电/SCBV/跳线/温控/新安装/系统环境/许可查询，over_temp STOP不变。F146候选仍因F147告警未闭暂缓；这项只对稳定F143校准，不让B承担A任务。B已报告人工转交回复、当前R1–R3/10月27日18北京时间窗口保持，无新B回执或外发事实。

## 4. 下一唯一建议

下一应先完成**正式长测验证与资源方案**：用本次实际增量/输出量选择迭代及有界运行策略，保留每笔合法副作用的检查，解决长原始轨迹超过256MiB/主机数小时的预算，不直接把上限改成无限或删关键证据。当前两迭代阶段完成后停止；没有自动实施≥10秒、CPU优化/PDS或恢复硬件。官方频率/实物取证仍需安全条件及独立授权。

入口：RESULTS/ORACLE_SUMMARIES/quality-compare/SOURCE_RECEIPTS/COMMANDS与postflight/SHA；旧原件/冻结预期及错误历史保持。工具/官方模型/算法副本、初始化大表和原日志波形留本地，Git仅审过的普通代码/测试/紧凑证据，不声称干净克隆一键复现。
'''
    (P/'reports/verification/2026-10-25-coremark-iter2-m1.md').write_text(report,encoding='utf-8')
    save(H/'postflight.json',dict(status='PASS_INPUTS_UNCHANGED',old_originals=protect(),pre_DUT_frozen=len(frozen),source13_unchanged=True,official6_unchanged=True,new_DUT=2,report_SHA256=sha(P/'reports/verification/2026-10-25-coremark-iter2-m1.md'),formal_score=False,hardware='STOPPED',candidate_promoted=False))
    print(json.dumps(dict(status=result['outcome'],rows=[dict(id=r['id'],ticks=r['detail']['raw_ticks'],UART=r['UART_frames']) for r in rows],hardware='STOPPED')))
if __name__=='__main__':run()
