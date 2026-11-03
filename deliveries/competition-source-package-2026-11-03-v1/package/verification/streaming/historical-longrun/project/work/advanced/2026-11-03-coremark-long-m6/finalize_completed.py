"""Run only after all four bounded long simulations and complete replays finish."""
from native import *
from run_fast import frozen_check
import datetime,re
if not(H/'CONTROLLER_EXIT.json').exists():raise SystemExit('Long campaign still incomplete; no report or PASS written')
controller=json.loads((H/'CONTROLLER_EXIT.json').read_text())
if controller['status']!='LONG_RUNS_AND_REPLAYS_PASS':raise SystemExit('Campaign not accepted')
frozen_check()
for manifest in ['TERMINAL_CAPTURE.json','EXECUTION_FROZEN.json']:
 for p,digest in json.loads((H/'plans'/manifest).read_text())['sha256'].items():
  p=Path(p);p=p if p.is_absolute()else H/p
  if sha(p)!=digest:raise RuntimeError('Input changed '+str(p))
results=[]
for pred in [1,0]:
 for mode in ['performance','validation']:
  d=H/'runs'/f'long-{mode}-p{pred}';r=json.loads((d/'RESULT.json').read_text());x=json.loads((d/'MEASUREMENT.json').read_text());audit=json.loads((d/'AUDIT-full.json').read_text())
  if r['status']!='PASS'or not audit['pass_']or x['mtime_ticks']<270000000 or x['iterations']!=192:raise RuntimeError('Incomplete long proof')
  if r['native']['rc']!=0 or r['native']['forced_cleanup']or r['native']['remaining_before_close']:raise RuntimeError('Process did not finish normally')
  for fn in ['program.bin','program.hex']:
   if sha(d/fn)!=sha(H/'build'/f'{mode}-192'/fn):raise RuntimeError('Program copy mismatch')
  results.append(dict(mode=mode,pred=pred,iterations=192,mtime_ticks=x['mtime_ticks'],phase_cycles=x['phase_cycles'],target_seconds=x['target_seconds'],full_cycles=x['full_cycles'],host_seconds=r['native']['seconds'],Icarus_and_VPI_peak_bytes=r['native']['peak_bytes'],log_bytes=r['native']['log_bytes'],raw_trace_bytes=r['raw_bytes'],gzip_trace_bytes=r['compressed_bytes'],WB=x['checker']['wb'],STORE=x['checker']['stores'],instructions=x['checker']['instructions'],algorithm_crc=x['oracle'],program_sha256=sha(d/'program.bin'),status='PASS',replay='MATCH'))
comparisons=[]
for mode in ['performance','validation']:
 a=next(x for x in results if x['mode']==mode and x['pred']==1);b=next(x for x in results if x['mode']==mode and x['pred']==0)
 if a['program_sha256']!=b['program_sha256']:raise RuntimeError('Different comparison image')
 comparisons.append(dict(mode=mode,off_ticks=b['mtime_ticks'],on_ticks=a['mtime_ticks'],cycle_reduction_percent=100*(b['mtime_ticks']-a['mtime_ticks'])/b['mtime_ticks'],same_image=True,speedup=b['mtime_ticks']/a['mtime_ticks']))
P=H.parent/'2026-11-03-coremark-strict-m5';identity=[]
for p in (H/'source').glob('*.v'):
 identity.append(dict(file=p.name,same_as_M5=sha(p)==sha(P/'source'/p.name),sha256=sha(p)))
protected=json.loads((R/'work/fpga/2026-11-03-event-recorder-m3/PROTECTED_INPUTS.json').read_text())
if not all(sha(R/x['path']).upper()==x['sha256'].upper()for x in protected)or not all(x['same_as_M5']for x in identity):raise RuntimeError('Protected source changed')
date=datetime.datetime.now().date().isoformat();summary=dict(completed=date,status='192_ITERATION_DUAL_SEED_SIMULATION_LONG_RUN_AND_OFF_COMPARISON_PASS',results=results,comparisons=comparisons,clock_hz=27000000,simulator_half_period_fs=18518518519,source_identity=identity,protected_files_unchanged=len(protected),hardware_calls=0,PDS_builds=0,formal_FPGA_CoreMark_score=False,limits=['Finite RV32I/CoreMark execution under fixed memory and initial state; no complete ISA/privilege proof','Separate ordered WB/STORE streams, no real retirement PC','Timer clock response checked by fixed N-2 rule; reference consumes oracle values, never DUT data','UART accepted byte-write model; no wire-level UART or board test','Memory peak is measured Icarus plus in-process VPI; Python compressor/controller peak not continuously measured','Prior M5 resource/frequency reports use one-iteration ROM, not a new 192-iteration PDS result'])
save(H/'SUMMARY.json',summary)
report=R/'reports/verification'/f'{date}-coremark-long-simulation-m6.md'
lines=[f'# CoreMark 192次双种子仿真长测与同条件预测对照\n\n{date}完成；源自D328–D329。固定32项BTB，已验CPU/SoC和M5保持。以下均为软件RTL仿真，不是FPGA实机正式成绩。\n',
       '## 实际结果\n\n名义时钟27MHz，TB半周期18518518519fs。mtime由每个实际仿真上升沿递增；所有12笔读取按同步口第N拍应为N−2独立核查。计算时间只取真实end_ticks−start_ticks，不用宿主耗时或迭代倍乘。phase接受沿差另核固定4拍标记开销。\n',
       '|种子组|预测|mtime计算周期|目标计算秒数|phase周期|合法WB|合法STORE|结果|\n|---|---|---:|---:|---:|---:|---:|---|\n']
for x in results:lines.append(f'|{x["mode"]}|{"32项开启"if x["pred"]else"关闭"}|{x["mtime_ticks"]:,}|{x["target_seconds"]:.9f}|{x["phase_cycles"]:,}|{x["WB"]:,}|{x["STORE"]:,}|PASS / 完整重放MATCH|\n')
lines.append('\n计算与初始化、格式化及UART输出分开。四例都由实际模拟计数达到>=270000000拍；没有增添延时空转、减少算法、降低采样或按宿主墙钟凑时间。\n\n')
for c in comparisons:lines.append(f'- {c["mode"]}：同一192次程序/种子/编译条件/同步存储，开启预测减少{c["cycle_reduction_percent"]:.6f}%计算周期，吞吐比{c["speedup"]:.6f}。\n')
lines.append('''
## 正确性和参考独立性

CoreMark上游文件保持原SHA。GCC RV32I/ILP32 O2、TOTAL_DATA_SIZE=2000、ITERATIONS=192及完整命令在plans/FROZEN-v2和commands。两种种子分别0/0/0x66与0x3415/0x3415/0x66；本机不变算法在DUT前给出最终CRC9BA8/9555，与一组已知首轮CRC一同冻结。本机oracle的固定计时只服务算法输出，不是任何性能证据。

顺序RV32I参考维护自己的PC、寄存器和内存，按自己的指令决定地址、结果和控制路径；实际WB与STORE分别有序即时比较、无去重。mtime期望来自冻结时钟方程及参考自身读地址顺序，不用实际DUT返回值回填。动态时间数值不冒称事前全部固定。终态32寄存器/24576个测试内存word、完整UART、种子/迭代、错误/溢出0、timer start/stop各1、portable结束、main返回0及done600D600D均核查；由于上游返回固定0，返回值不单独作为正确性判据。CRCfinal192及原输出不得有ERROR/Errors detected。

每笔原始观测以20B记录保存，含类型、沿、地址/寄存器、数据和掩码；各段gzip均完整解压核SHA后才移除新raw段。轨迹未抽样、未用摘要替代逐笔检查。所有完整压缩流又经独立进程重新执行原生参考、核所有事件/终态/输出，结果与运行中核验相符。原生参考此前已完整匹配10份M5旧流（旧数据重放，不是新DUT）；六项实时错误控制及六项完整原始流变异均明确拒绝，单独保留。

资格阶段原VPI链接缺stack-check运行库、CRLF文本重放、强加WB/STORE交错顺序等准备/检查器失败保留。v1第一轮control5未到达预期计时错误点，不算关闭；v2明确核每项具体拒绝原因。完整192长测采用冻结v2。终端VCD只有完成前6拍，以免bulk阶段VCD回调拖慢，完整事件/全程X和非法副作用检查不减；不能将终端短VCD说成全程内部波形或片上ILA。

## 宿主资源与停止边界

宿主墙钟仅表示验证成本，不代表目标执行时间。每例6小时/整个阶段18小时、每进程1GiB/日志1MiB、raw8GiB/gzip4GiB/待压96MiB、9亿拍；有界所属Job清理、输入身份守卫和不覆盖尝试记录。Python压缩器/controller峰值未持续测量，下面内存峰值只指Icarus及其同进程VPI，不冒称全验证链总峰值。

|种子组|预测|宿主秒数|Icarus+VPI峰值MiB|完整raw MiB|gzip MiB|日志B|
|---|---|---:|---:|---:|---:|---:|
''')
for x in results:lines.append(f'|{x["mode"]}|{x["pred"]}|{x["host_seconds"]:.3f}|{x["Icarus_and_VPI_peak_bytes"]/1048576:.2f}|{x["raw_trace_bytes"]/1048576:.2f}|{x["gzip_trace_bytes"]/1048576:.2f}|{x["log_bytes"]}|\n')
lines.append('''
## 资源频率身份与剩余限制

本轮没有PDS构建、位流、硬件、安装或生产替换。M5旧32项PDS为11299 LUT/5088 FF/16 DRM36，27MHz内部约束通过、STA估算33.9006MHz；对应**旧一次迭代ROM**。八CPU模块相同不等于192次镜像已经新实现或实机测频，不能把旧报告换标签用于本轮ROM。完整S/U/PMP/Sv32、任意ISA/异常组合、真实退休PC、完整物理IO/CDC和实机/ILA仍不在本次验收范围。

## 复查入口

work/advanced/2026-11-03-coremark-long-m6/：START_HERE、SUMMARY、plans/FROZEN-v2/TERMINAL_CAPTURE/EXECUTION_FROZEN、commands与logs；runs/long-{performance,validation}-p{0,1}/中RESULT、MEASUREMENT、TRACE_INDEX、AUDIT-full、state、完整uart、timer读账本及普通终端VCD；trace目录为完整压缩事件。controller/worker/campaign入口是已消费的一次阶段，不原地重启；复现应另建独立目录与新尝试身份，保留冻结输入和旧失败。89生产保护文件和M5源同SHA，SHA清单仅材料完整性，不提升功能结论。

这组结果可补入作品报告的“仿真长测/动态预测周期收益”部分，和旧离线资源时序、生产实机材料分别标识。当前继续保护已验作品；不为完整性扩大高阶范围或上板。
''')
with report.open('x',encoding='utf-8')as out:out.write(''.join(lines))
save(H/'REPORT_IDENTITY.json',dict(path=str(report.relative_to(R)),sha256=sha(report),completed=date))
print(json.dumps(dict(report=str(report),comparisons=comparisons,results=results),indent=2))
