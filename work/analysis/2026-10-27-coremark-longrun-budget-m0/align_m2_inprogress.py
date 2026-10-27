from pathlib import Path
P=Path('D:/A_FPGA_Comp');M=P/'.project-memory'
p=M/'INDEX.md';s=p.read_text(encoding='utf-8-sig');old='最近更新：2026-10-27，F159/D159：只读长跑准入与采集成本分析完成，下一M2（生产有界适配+单8迭代）具体scope PENDING；无新增DUT/实施授权，B R1独立、硬件STOP。';new='最近更新：2026-10-27，D160已批准A-COREMARK-LONGRUN-READY-M2（原scope SHA不改）；主机容量/旧重放与新C/参考已完成，唯一8迭代DUT正在执行，尚未功能验收；B R1独立、硬件STOP。';assert old in s;s=s.replace(old,new,1);p.write_text(s,encoding='utf-8')
p=M/'TODO.md';s=p.read_text(encoding='utf-8-sig');s=s.replace('- [ ] 一次批准`deliveries/mainline-coremark-longrun-ready-scope-2026-10-27-v1/IMPLEMENTATION_SCOPE.md`1.0.0（PENDING）','- [x] D160用户已批准`deliveries/mainline-coremark-longrun-ready-scope-2026-10-27-v1/IMPLEMENTATION_SCOPE.md`1.0.0（原PENDING文本留作历史）',1);s=s.replace('M2通过再按实际成本/验证收益决定更长程序范围；旧1+1用完，当前不跑新任务。','M2完成后按实际成本/验证收益决定更长程序范围；旧1+1用完，本轮仅D160批准的1新C/1编译/1性能8迭代正在执行，未验收。',1);p.write_text(s,encoding='utf-8')
p=M/'COLLABORATION.md';s=p.read_text(encoding='utf-8-sig');at=s.index('版本：COLLAB v1.86');s=s[:at]+'''版本：COLLAB v1.87；2026-10-27，D160已批准A-M2，1新C/1编译及预先参考已完成，唯一8迭代DUT执行中，未功能验收。A负责采集/模型/计量；B R1仍独立且新回执未知，不改原10/27 18窗口、不重复派核心、不等待B整包。CPU/外设RTL不改，硬件STOP。

### 历史v1.86（仅M2待批状态被D160明确批准取代）

'''+s[at:];p.write_text(s,encoding='utf-8')
print('Approval/current in-progress routes aligned; no functional fact invented')
