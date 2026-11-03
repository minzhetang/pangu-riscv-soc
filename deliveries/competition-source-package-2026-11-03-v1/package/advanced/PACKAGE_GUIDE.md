# 三个独立高阶方向

## Cache与准入策略

cache-ai根为M0两路I/D各128B、4组×2路、16B行，写穿透/写缺失不分配/LRU；cache-m1-admission新增二次访问准入；cache-m2-two-ghost新增双ghost及FIFO位。完整cache/backend/TB、冻结向量、独立字节/替换参考、正负日志及量化表随包；原VVP不提供，旧原SHA清单仍是历史身份。

典型D/delay3：局部性直通709→M0 390拍；流式直通357而M0 918拍，M1/M2恢复357；两行交替M1 534→M2 282，但M0仍270。M2增加220历史逻辑bit/Cache，不当实际FF；三行/每行两字/FIFO冲突等退化也列在COMPARISON。默认ADMISSION=0、GHOST_TWO=0不改。bit31旁路规则不匹配基础MMIO，不能直接接线替换存储；未CPU集成、综合或板测。

## 动态预测及所选M-mode

btb-mmode/project是主线修复后代码树，含M1/M2/M3前后反例、M4真C、M5双种子CoreMark短测，以及pred0/1/32三套PDS离线工程。REPRODUCE_C.py是已有隔离真C复验入口；M5脚本保留一次性/固定计划守卫，不在包内直接重跑。

重点修复停顿旧STORE重复、副作用资格、重复训练、IF miss与redirect链接、未对齐目标异常归属、暖机循环中断及CSR后IRQ优先。检查cause/EPC/tval/状态/返回和禁止副作用，不以进handler判成功。当前推荐BTB_ENABLE=1、BTB_INDEX_BITS=5、SYNC_MEMORY=1。八RTL仍保留原耦合特权模块；S/U/PMP/Sv32未完整验收，不称M-only整核或完整高阶2。M5性能对照/资源只属于一次迭代镜像，不套基础SM2实机成绩。

## 定点AI算子

cache-ai内FC RTL、AI TB、reference_ai.py和vectors保存16×8全连接算子：128MAC/任务、40bit累加、int8输入/权重尺度1/64，bias/raw尺度1/4096；对称最近舍入、半值离零，饱和到[-128,127]。8组合成张量×两种背压，逐行raw40及int8检查；完成136/148拍，配置304拍另计。

这是一套完整算子控制/存储/数值/握手原型，未取得或移植真实网络，也无识别率、端到端模型延迟或CPU加速比。合成极值饱和不伪装成模型准确率。

上述成果按问题、机制、原始实验与适用条件展示。没有因“独立原型”而抹去研究价值，也没有把三方向拼成已验板级系统。复现条件见根文档；本轮没有执行任何候选构建或仿真。
