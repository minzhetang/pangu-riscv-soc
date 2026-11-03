"""Generate explanatory tables from checked measurements, never modify frozen inputs."""
import csv,json,math,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parent
def main():
    rows=json.loads((R/'CACHE_RESULTS.json').read_text())+json.loads((R/'CACHE_SUPPLEMENT_RESULTS.json').read_text())
    indexed={(x['key'],x['delay']):x for x in rows};comparison=[]
    for c in rows:
        if not c['key'].endswith('_0'):continue
        base=indexed[(c['key'][:-1]+'1',c['delay'])];ro,name,_=c['key'].split('_')
        comparison.append(dict(channel='I' if ro=='1' else 'D',workload=name,delay=c['delay'],requests=c['requests'],
            no_cache_cycles=base['cycles'],cache_cycles=c['cycles'],cycle_change_percent=100*(c['cycles']/base['cycles']-1),
            read_hits=c['hits'],eligible_reads=c['eligible_reads'],hit_rate=c['hits']/c['eligible_reads'] if c['eligible_reads'] else 0,
            no_cache_transactions=base['transactions'],cache_transactions=c['transactions'],no_cache_bytes=base['bytes'],cache_bytes=c['bytes']))
    with (R/'CACHE_COMPARISON.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=comparison[0]);w.writeheader();w.writerows(comparison)
    report=['# Cache 独立仿真结果','',
      '44 组配置全部通过独立字节内存及独立 Cache 行/LRU 事务预期检查。包含 I/D、缓存/直通、延迟 0/3；每次后端还叠加确定性命令及 beat 等待。',
      '以下周期包含同一 TB 的请求驱动、响应消费、0..3 拍背压及固定收尾开销；不是 CPU 周期或物理时钟实测。延迟参数是每 beat 准备等待数，不是总内存延迟。',
      '命中率分母为可缓存且合法的读请求；写命中不计入统计。无 Cache 命中率为 0。字节数仅为 payload：读 beat 每拍 4 B，写按有效字节；不计地址/控制总线开销。','',
      '|通道/序列|延迟|请求|无Cache→有Cache周期|周期变化|读命中|后端事务|传输B|',
      '|---|---:|---:|---:|---:|---:|---:|---:|']
    for x in comparison:
        report.append(f"|{x['channel']}/{x['workload']}|{x['delay']}|{x['requests']}|{x['no_cache_cycles']}→{x['cache_cycles']}|{x['cycle_change_percent']:+.2f}%|{x['read_hits']}/{x['eligible_reads']} ({x['hit_rate']:.2%})|{x['no_cache_transactions']}→{x['cache_transactions']}|{x['no_cache_bytes']}→{x['cache_bytes']}|")
    report+=['','|检查|结果及证据|','|---|---|',
      '|命中/缺失/冲突替换|locality/stream/conflict，全响应及 hit/事务/字节统计精确相等；conflict 的 A,B,A,C,B 区分 LRU 与 FIFO|',
      '|字节写/零掩码/写缺失|bytes 原测试 + lanes 补测，16 种掩码每次写后立即读；命中与冷行写分别覆盖|',
      '|等待与背压|两延迟和确定性命令/beat 停顿；每个响应 0..3 拍等待；逐拍检查响应与命令有效载荷稳定|',
      '|相同请求/副作用/锁存|protocol 序列及 MODE2；valid 连续保持跨两次接收，阻塞期间不重复接收，MMIO 正好返回 0/1，修改已接受的输入不影响事务|',
      '|复位|MODE1：填充中取消、响应挂起取消、已提交写后取消；无幽灵响应、计数复位、已提交写保留；I/D 并发分别得到独立内存结果|',
      '|非法请求|非对齐读/I 写 error，后端无对应命令；无完整异常/总线错误协议|',
      '|检查器负向|只改派生向量第一期望字，RTL 仿真 exit1 且 data mismatch；原预期 SHA 未变|','',
      '收益依访问序列而异。局部性有收益；stream 的每行仅用一个字仍取整行，读传输扩大 4 倍且周期增加；不接受“Cache 一定提速”。',
      '原字节测试最后才读，可能掩盖中间 lane 错误，已以先冻结的独立补测收敛；原结果保留。没有修改原冻结计划/预期。',
      '接口与限制见 cache_plan.md / INTERFACES.md；原始日志在 logs；逐项机器数据在 CACHE_RESULTS.json 和 CACHE_SUPPLEMENT_RESULTS.json。']
    (R/'CACHE_REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    cases=json.loads((R/'ai_vectors/cases.json').read_text());ai=json.loads((R/'AI_RESULTS.json').read_text())
    errors=[]
    for c in cases:
        e=c['final_quantization_error'];pre=c['pre_output_quantization_error']
        errors.append(dict(case=c['name'],max_abs_pre_output_error=max(map(abs,pre)),max_abs_final_error=max(map(abs,e)),
            rmse=math.sqrt(sum(v*v for v in e)/8),saturated_outputs=sum(nearest_raw(v)>127 or nearest_raw(v)<-128 for v in c['raw'])))
    (R/'AI_QUANTIZATION.json').write_text(json.dumps(errors,indent=2))
    report=['# AI 独立全连接算子结果（仅合成数据）','',
      '未移植真实训练模型。模型来源：无；权重/输入来源：本目录 reference_ai.py 确定性数学函数及人工边界值；无第三方模型使用许可依赖。',
      '文件名检索未找到 .onnx/.tflite/.pt/.pth/.npz/.npy（排除 tools 和本交付目录）；未解包遍历归档、未宣称项目绝无真实模型。用户没有提供已核验合法模型，本轮按允许的合成算子分支完成。',
      '这是具备配置、矩阵存储、128 次 MAC 调度、8 行输出和背压控制的 FC 原型；无 CPU 接入、激活/网络拼接、识别率、端到端 AI 系统或 CPU 加速比。','',
      '|用例|无背压/有背压周期|配置周期|量化前最大绝对误差|最终最大绝对误差|最终RMSE|饱和输出|',
      '|---|---:|---:|---:|---:|---:|---:|']
    for k,e in enumerate(errors):
        report.append(f"|{e['case']}|{ai[k*2]['compute_cycles']}/{ai[k*2+1]['compute_cycles']}|{ai[k*2]['config_cycles']}|{e['max_abs_pre_output_error']:.9g}|{e['max_abs_final_error']:.9g}|{e['rmse']:.9g}|{e['saturated_outputs']}/8|")
    report+=['','误差单位为实数输出值。non_grid 三组以未量化 float 输入、权重和 bias 的 Python 点积为参考；边界用例以精确可表示整数张量的实数点积为参考。大范围/极端 bias 的巨大误差来自规定的输出饱和，不作模型精度结论。',
      '所有 raw40 与 Python 任意精度整数点积逐行精确相等，所有 int8 与独立 divmod 舍入/饱和预期相等。输出 16 组×8=128 项（含背压重复），另有协议复跑。',
      '计算周期从 start 接受边沿到最后结果接受边沿；16 MAC+1 响应/行，无等待136拍，固定背压合计12拍后148拍。',
      '配置152个握手，当前简单 TB 每项驱动占2拍，计304拍；这是驱动开销，不是硬件要求的最低配置时间。配置与计算合计440/452拍（不含 start 驱动间隔和复位）。',
      '有符号 int8/64，bias/4096；raw40/4096。累加数学边界 [-2147743744,2147745791]，40位无溢出；输出最近舍入、半值远离零、限幅[-128,127]。',
      '零、正负乘积、极值、±32/±96半值、饱和边界、int32 bias极限均覆盖。协议测试：非法配置无初始化效果、缺失初始化错误、忙时不接受配置/start、保留配置重复启动、MAC中/结果挂起复位、复位后必须重载。',
      '负向控制把派生向量最后一个输出期望改1，得到 mismatch/exit1；原冻结材料不改。',
      '原始日志 logs/ai_*，波形 ai_rounding.vcd、ai_reset.vcd；逐项实际输出见 AI_RESULTS.json；原始浮点和定点张量/预期 ai_vectors/cases.json。']
    (R/'AI_REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
def nearest_raw(v):
    a,rem=divmod(abs(v),64);a+=rem>=32;return a if v>=0 else -a
if __name__=='__main__':main()
