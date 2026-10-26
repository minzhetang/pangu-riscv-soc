from pathlib import Path
import json,hashlib,datetime,re,sys
P=Path('D:/A_FPGA_Comp');H=P/'work/fpga/2026-10-26-coremark-stream-evidence-m1';B=H.parent/'2026-10-25-coremark-iter2-m1';D=H/'runs/performance-N234'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest().upper()
def save(p,o):
    with p.open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
check=read(D/'check-result.json');strict=read(D/'strict-equality-result.json');capture=read(D/'capture-result.json');arc=read(D/'archive-receipt.json');neg=read(H/'controls/negative-results.json');guards=read(H/'controls/capture-guards.json');model=read(H/'controls/model-equivalence.json')
assert check['status']==strict['status']==neg['status']==guards['status']==model['status']=='PASS'
protected=read(H/'protected-originals.json')['files'];assert all(sha(Path(r['path']))==r['SHA256'] for r in protected)
live=read(H/'frozen-live-inputs.json')['files'];assert all(sha(Path(r['path']))==r['SHA256'] for r in live)
newwarn=(H/'logs/compile-performance-N234/stderr.log').read_text(encoding='utf-8-sig');oldwarn=(B/'logs/compile-performance-N234/stderr.log').read_text(encoding='utf-8-sig');same_warn=newwarn.replace(str(H),'<STAGE>')==oldwarn.replace(str(B),'<STAGE>')
(H/'compiler-warnings.txt').write_text(newwarn,encoding='utf-8')
archive_bytes=sum(p.stat().st_size for p in (D/'archive').rglob('*') if p.is_file());raw=sum(x['raw_bytes'] for x in arc['per_stream'].values())
assert not list((D/'spool').iterdir()) and archive_bytes<=256*1024*1024
compile=read(H/'logs/compile-performance-N234/process.json');run=read(H/'logs/run-performance-N234/process.json');final=read(H/'logs/final-functional-check/process.json');old_run=read(B/'logs/run-performance-N234/process.json')
receipts=[]
for root in ['source','cases/performance-N234/source']:
    for p in (H/root).iterdir():
        if p.is_file():receipts.append(dict(path=str(p.relative_to(H)),SHA256=sha(p),old_SHA256=sha(B/root/p.name),unchanged=sha(p)==sha(B/root/p.name)))
assert all(x['unchanged'] for x in receipts)
save(H/'SOURCE_RECEIPTS.json',dict(RTL_and_init=receipts,ISA_models=[dict(name=n,SHA256=sha(H/'models'/n),unchanged=sha(H/'models'/n)==sha(B/'models'/n)) for n in ['cpu_program_reference.py','peripheral_checker.py']],images=[dict(name=n,SHA256=sha(H/'build'/n/'program.bin'),unchanged=sha(H/'build'/n/'program.bin')==sha(B/'build'/n/'program.bin')) for n in ['performance','validation']],source_protected=len(protected),frozen_live_inputs=len(live),no_GCC=True,RTL_diff=[]))
summary=dict(stage='A-COREMARK-STREAM-EVIDENCE-M1',date_beijing='2026-10-26',decision_approval='D156',decision_result='D157',status='PASS_FINITE_PIPELINE_NOT_FORMAL_LONGRUN',old_replays={name:read(H/'replays'/(name+'-N234')/'replay-result.json')['status'] for name in ['performance','validation']},model_controls=model,pipeline_controls=dict(total=len(neg['rows']),positive=sum(x['status']=='PASS' for x in neg['rows']),expected_rejections=sum(x['status']=='EXPECTED_REJECT' for x in neg['rows']),host_seconds=neg['host_seconds']),capture_guard_rejections=len(guards['rows']),entry_policy=read(H/'controls/entry-policy.json')['status'],new_compiler_invocations=1,new_DUT_runs=1,compile=compile,DUT=run,final_functional_check=final,compiler_warning_groups=newwarn.count('warning:'),compiler_warnings_identical_after_path_normalization=same_warn,metrics=check['metrics'],raw_ticks=check['detail']['raw_ticks'],crcfinal=check['frozen_comparison']['crcfinal'],UART_bytes=check['UART_frames'],UART_pin_records=check['streaming']['pin']['records'],streaming=check['streaming'],raw_bytes=raw,raw_records=sum(x['records'] for x in arc['per_stream'].values()),segments=sum(x['segments'] for x in arc['per_stream'].values()),streams=arc['per_stream'],archive_bytes_including_metadata=archive_bytes,archive_ratio=archive_bytes/raw,spool_peak_bytes=capture['supervisor']['peak_spool'],archive_parent_peak_bytes=capture['supervisor']['peak_parent'],old_DUT_host_seconds=old_run['elapsed_seconds'],new_DUT_host_seconds=run['elapsed_seconds'],observed_host_time_ratio=run['elapsed_seconds']/old_run['elapsed_seconds'],host_time_comparison='Different executions; load not controlled, not a causal attribution or speedup claim',byte_for_byte_old_logs_and_pins=True,normal_stop_tail_cycles=32,reference_semantics_unchanged=True,source_protected=len(protected),frozen_live_inputs=len(live),problems_preserved=['adapter guard false substring before checker write','initial host ImportError before model execution','performance replay Python tuple-vs-JSON-array qualification failed after strict checker PASS; exact saved JSON independently qualified without rerun'],remaining_limits=['Only two-iteration performance new DUT; validation old replay only','512MiB raw/stream,1024 segments/stream,16M records/stream and5M ISA steps remain short-stage caps; not a >4GB/160-iteration production claim','MMIO observations and bounded UART transitions still retained; no claim all metadata memory is O(1)','Checks rely on nonoptimized Python; guarded_entry rejects -O/-OO, direct internal modules unsupported','No true retirement PC/unified WB-STORE stream, fixed GPIO0/input/state model','No valid CoreMark score, real FPGA temperature/timebase/ILA or hardware validation'],hardware='STOPPED',PDS_runs=0,GCC_runs=0,B_task='Independent offline scope remains; no presumed receipt/new deliverable')
save(H/'SUMMARY.json',summary)
(H/'STATUS.json').write_text(json.dumps(dict(status=summary['status'],decision='D157',compile_used=1,new_DUT_used=1,source_protected=len(protected),hardware='STOPPED'),indent=2)+'\n',encoding='utf-8')
# Exact native argument arrays retained locally; profile-specific Python executable is redacted in tracked commands.
commands=[]
for p in sorted((H/'logs').glob('*/process.json')):
    r=read(p);commands.append(dict(id=p.parent.name,**r))
save(H/'COMMANDS-exact-local.json',dict(commands=commands,Python=sys.version))
public=[]
for r in commands:
    r=dict(r);r['argv']=[('<EXISTING_PYTHON>' if i==0 and ('python' in str(x).lower()) else str(x)) for i,x in enumerate(r['argv'])];public.append(r)
(H/'COMMANDS.md').write_text('# Reproducible commands and native results\n\nD156 business scope; only compile-performance-N234 used the separately reviewed external tool route. All calls nonadministrator; existing tools only. JSON argv arrays are argument lists, not shell strings. Exact local arrays are in COMMANDS-exact-local.json; <EXISTING_PYTHON> denotes the already verified local Python runtime.\n\n'+''.join('## '+r['id']+'\n\n```json\n'+json.dumps(r,ensure_ascii=False,indent=2)+'\n```\n\n' for r in public)+'The initial model import and performance replay qualification failures are retained. They are not failed new CPU DUTs or silently rewritten PASS. guarded_entry.py is the required future nonoptimized launch boundary; its status/-O/-OO controls launch no compiler or DUT. Existing attempt/output directories prohibit reruns; use a separately authorized new directory for a reproduction.\n',encoding='utf-8')
report=f'''# 长测证据管道M1：有限验收通过，主机时间代价保留

2026-10-26，F157/D156–157。**保持13RTL和2迭代镜像不变，完成旧双种子等价重放、1次编译、1次新DUT及端到端严格核验。** CPU没有提速或增加ISA。它打通了“真实CPU运行→已关闭分段→无损回读归档→独立逐笔参考/全态/计时/实际串口→旧证据逐字节对照”；不是正式长测/硬件成绩。

## 实测与边界

|项|本次实际结果|
|---|---|
|旧性能/验证两种子|原严格结果除新增streaming统计外JSON逐字段一致，完整实际PIN时间线与字节解码PASS；各是旧记录重放，不计新DUT|
|模型/故障控制|N8/16/234逐拍旧模型与稀疏模型边界一致；管道{len(neg['rows'])}项（1正/{sum(x['status']=='EXPECTED_REJECT' for x in neg['rows'])}拒绝）、采集4拒绝、入口正常/-O/-OO三项符合预期；不计B通用套件|
|编译|1次，原生0，{compile['elapsed_seconds']:.3f}秒；3类warning（继承时间单位、部分模块无时间单位、厂商grsn隐式线），路径归一后同F151：{same_warn}|
|新DUT|仅performance-N234，2迭代，原生0，{run['elapsed_seconds']:.3f}秒，正常STOP/32拍尾，无第二次运行|
|架构/时序|全RF/32KiB RAM/每笔EX、WB、MEM/phase/独立计时PASS；物理5888943拍、stall173406、flush435221、计算4207378 ticks、crcfinal72be均同F151|
|真实UART/VCD|完整662字节、3838实际PIN变化；实际时间戳/中心采样及原生窗口VCD前后沿检查PASS。不是全算法VCD、退休PC或ILA|
|无损归档|142段（trace107/bus35），4602669条，194334829原始字节→{archive_bytes}归档及元数据字节；回读后逐行/字节同旧，两者不是只比SHA|
|临时空间|峰值{summary['spool_peak_bytes']}B，<32MiB；142段仅关闭、回读逐字节和身份核同后逐文件删除，失败测试的超限文件保留；旧原始日志未删|
|内存|归档父进程峰值{summary['archive_parent_peak_bytes']}B，VVP峰值{run['peak_working_set_bytes']}B，最终检查峰值{final['peak_working_set_bytes']}B；旧流重放峰值约252MB，均在本轮限制内|
|保护|{len(protected)}原件和{len(live)}执行冻结输入SHA核同；13RTL、初始镜像、ISA模型不变；0GCC/PDS/硬件|

## 不能隐去的代价与限制

旧同输入DUT记录为{old_run['elapsed_seconds']:.3f}秒，本次{run['elapsed_seconds']:.3f}秒（观测比值{summary['observed_host_time_ratio']:.4f}）。主机负载未受控，不能据此断言全部增量由日志封装造成；但当前没有仿真加速证据，不能只报告压缩收益。CPU物理拍和计算量保持完全相同，归档不是CPU创新或性能提升。

去掉逐物理拍samples列表后，GPIO0空闲仅在活动/完成边界核实后跳步，实际PIN独立解码。仍保留有限MMIO观测、UART变化与归档元数据，并非整个工具恒定内存。当前512MiB raw/流、1024段/流、16M记录/流、5M ISA步和8M DUT拍是本短阶段硬限，**不能直接开160迭代或>4GB流**。正式长跑还需流总量/分页索引/参考预算与主机耗时安排，不得静默放大上限。

准备期保留3个非DUT错误：生成器检查误匹配新统计关键字、host_worker多余save导入在模型执行前失败、性能重放比较Python元组与已序列化JSON数组而失败。最后一项严格检查已PASS，保存JSON与旧JSON逐字段一致后单独资格核验，未为修脚本重跑该CPU或改预期；完整原始日志及checkpoint收据均留存。

## 证据与复现

主目录`work/fpga/2026-10-26-coremark-stream-evidence-m1/`：SUMMARY、SOURCE_RECEIPTS、APPROVAL、TEST_PLAN、compile/DUT-attempt、compile-result、frozen-live-inputs、COMMANDS、各logs/process/stdout/stderr；准确TB_DIFF和4个checker输入改动patch。`runs/performance-N234/`含完整无损archive、全态、uart-pins、原生wave、check-result、strict-equality-result、UART/wave audits及capture-result；`replays/`明确旧重放，`controls/`真实拒绝/故障分列。

新源的关键变化只在采集TB、输入迭代和GPIO0/UART采样层。用`guarded_entry.py`作为正式调用边界；`-O/-OO`明确拒绝，不能直接以优化模式导入断言型内部库。本次实际命令均为非优化模式，入口负例未重跑DUT。

## 下一步技术排序

先依据这次实测做**只读采集开销归因和长跑资源预算**：分开VVP解释执行、分段归档、ISA检查和串口阶段；明确大流索引/记录总量、参考步数与可用主机时间。确认代价后再确定一项局部采集改进或正式长跑范围。新增TB改动/编译/DUT及数小时预算须另列范围，不能复用已用完的1+1许可，也不让B离线工具成为主线等待门槛。

B仍独立离线质量包，实际回执未确认，不重派核心。F143功能RTL稳定、F151校准保留、F146暂缓/F147告警，over_temp硬件STOP不变；软件通过不解除温度/供电/真实时基/片上波形缺口。
'''
(H/'REPRODUCE.md').write_text('''# Finite stage evidence and reproduction boundaries

Start with SUMMARY.json, TEST_PLAN.json, COMMANDS.md and the report. Historical output/attempt markers are immutable; do not rerun preparation/compile/capture scripts in this directory or remove the markers. Exact source/image/oracle identities are recorded; vendor GTP models remain external from the existing PDS installation and are not redistributed.

The ordinary Python guarded_entry.py status command reads state only. -O/-OO is unsupported and rejected. compile/capture/check actions are single-use and are not an authorization to repeat this completed stage. A new reproduction requires an independent new directory plus the appropriate compile/DUT scope and tool permission. No PATH or system changes are needed.

Git stores reviewed small code/metadata only, not vendor models, VVP, generated initialization, raw 32MiB overbudget fixture, compressed trace payloads, ELF/bin or native VCD. Full local evidence and old immutable inputs remain available; a Git clone alone does not include them.
''',encoding='utf-8')
with (P/'reports/verification/2026-10-26-coremark-stream-evidence-m1.md').open('x',encoding='utf-8') as f:f.write(report)
# Final manifest excludes itself, remains append-free.
entries=[(p.relative_to(H).as_posix(),sha(p)) for p in sorted(H.rglob('*')) if p.is_file()]
with (H/'SHA256SUMS.txt').open('x',encoding='utf-8') as f:
    for name,value in entries:f.write(value+'  '+name+'\n')
save(H/'postflight.json',dict(status='PASS_FINITE',source_protected=len(protected),frozen_live_inputs=len(live),manifest_SHA256=sha(H/'SHA256SUMS.txt'),manifest_entries=len(entries),source_RTL_unchanged=True,new_compile=1,new_DUT=1,PDS=0,hardware='STOPPED'))
print(json.dumps(dict(status=summary['status'],raw=raw,archive=archive_bytes,segments=summary['segments'],records=summary['raw_records'],peak_check=final['peak_working_set_bytes'],host_ratio=summary['observed_host_time_ratio'],protected=len(protected),frozen=len(live),manifest=len(entries)),ensure_ascii=False))
