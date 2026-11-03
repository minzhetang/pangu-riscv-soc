import pathlib,json,csv,hashlib,shutil,difflib
R=pathlib.Path(__file__).resolve().parent
def main():
    rows=json.loads((R/'RESULTS.json').read_text());index={(r['key'],r['policy'],r['delay']):r for r in rows}
    comparisons=[]
    for key in json.loads((R/'EXPECTED.json').read_text()):
        for delay in [0,3]:
            group=[index[(key,p,delay)] for p in ['bypass','baseline','admission']];b,m,a=group
            comparisons.append(dict(key=key,delay=delay,bypass_cycles=b['cycles'],baseline_cycles=m['cycles'],admission_cycles=a['cycles'],
                cycle_change_vs_m0=100*(a['cycles']/m['cycles']-1),
                bypass_bytes=b['bytes'],baseline_bytes=m['bytes'],admission_bytes=a['bytes'],
                baseline_transactions=m['transactions'],admission_transactions=a['transactions'],
                baseline_hits=m['hits'],admission_hits=a['hits'],eligible_reads=a['eligible_reads']))
    with (R/'COMPARISON.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=comparisons[0]);w.writeheader();w.writerows(comparisons)
    report=['# Cache M1 可选准入策略：有限验证结果','',
      '102组序列配置、5项协议/复位测试及1项故意错误期望拒绝通过；共110个逐次低优先级有界编译/仿真进程。没有长压力测试、CPU集成、PDS、硬件或主线进程操作。',
      '本轮在M0末级已测出的流式浪费上验证一个候选，没有改M0原件。单字冷读不取整行，同组再次读同一缺失行才填充。详情见PLAN.md。',
      '**定案：仅保留为可选实验参数，ADMISSION默认0；不全局替代M0。** 流式与污染访问有收益，但常见冷启动及同组交替访问有退化。','',
      '|序列（0=D，1=I）|delay|无Cache/M0/M1周期|相对M0变化|无Cache/M0/M1字节|M0/M1事务|M0/M1命中（分母）|',
      '|---|---:|---:|---:|---:|---:|---:|']
    for c in comparisons:
        report.append(f"|{c['key']}|{c['delay']}|{c['bypass_cycles']}/{c['baseline_cycles']}/{c['admission_cycles']}|{c['cycle_change_vs_m0']:+.2f}%|{c['bypass_bytes']}/{c['baseline_bytes']}/{c['admission_bytes']}|{c['baseline_transactions']}/{c['admission_transactions']}|{c['baseline_hits']}/{c['admission_hits']} ({c['eligible_reads']})|")
    report+=['','周期包含相同驱动/背压/收尾开销，沿用M0定义；非CPU或板级实测。命中率用命中数除表中合法可缓存读数；字节只计payload。',
      'stream单次逐行读：M1与无Cache流量相同；two-word每行仅读两字：首读旁路、次读才取整行，反而比M0多一个事务，应避免用于这类访问。',
      'adverse同组A/B交替：单ghost槽反复被覆盖，始终不能准入；M0两路本能容纳两行。pollution热集穿插冷行：未复用冷行不驱逐热行，因此出现收益。',
      '增加每Cache四组×(26bit tag+1valid)=108逻辑状态位，I+D共216位及比较/控制逻辑；未综合，不能换算成实际FF/LUT或频率代价。',
      '准确性：所有读值/错误来自独立字节内存；单独的list+ghost参考决定命中及后端统计，冻结在RTL实现前。旧bytes与逐次lanes均回归，覆盖写穿透、16掩码、写缺失/零掩码、MMIO、非对齐和I写错误。',
      '新MODE3：首次single、ghost复位清除、第二次4beat填充、随后命中、填充中复位不安装残行；继承MODE1/2验证已提交写保持、I/D并发及held-valid副作用。',
      '测试夹具在运行前发现MODE1固定绝对事务数不适配候选，另存execution_tb.sv改为相对事务数等待。原冻结TB/预期未改，说明和独立SHA见PRE_RUN_CORRECTION.md。',
      'candidate.sv的ADMISSION=0是缺省M0路径，本轮baseline从原M0源码编译；新参数1通过TB显式defparam开启。未新增CPU接口或指令。',
      '资源限制沿用复制的run.py：20秒、256MiB/进程、384MiB/Job，挂起创建后加入Job再恢复；64MiB目录/1MiB日志为20ms采样守卫，不是文件系统硬配额。',
      '本轮停止于一个策略的定向比较，不继续堆叠更多准入/预取/替换算法；AI仍为M0合成算子，未新增真实模型证据。']
    (R/'REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    (R/'SOURCE_DIFF.patch').write_text(''.join(difflib.unified_diff((R/'baseline.sv').read_text().splitlines(True),(R/'candidate.sv').read_text().splitlines(True),fromfile='M0/baseline.sv',tofile='M1/candidate.sv')))
    shutil.copyfile(R.parent/'prepare_m1.py',R/'prepare_m1.py')
    receipts=[json.loads(p.read_text()) for p in (R/'logs').glob('*.json')]
    (R/'PROCESS_SUMMARY.json').write_text(json.dumps(dict(processes=len(receipts),max_seconds=max(r['seconds'] for r in receipts),
        limits_triggered=sum(r['reason'] is not None for r in receipts),negative_tests=1),indent=2))
if __name__=='__main__':main()
