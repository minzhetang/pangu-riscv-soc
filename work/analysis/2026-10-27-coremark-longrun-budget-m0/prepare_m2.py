from pathlib import Path
import json,hashlib,shutil,time,ast
P=Path('D:/A_FPGA_Comp');B=P/'work/fpga/2026-10-26-coremark-stream-evidence-m1';R=P/'work/fpga/2026-10-25-coremark-iter2-m1';H=P/'work/fpga/2026-10-27-coremark-longrun-ready-m2';assert not H.exists();H.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(p,v):
 with p.open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
scope=P/'deliveries/mainline-coremark-longrun-ready-scope-2026-10-27-v1/IMPLEMENTATION_SCOPE.md';assert sha(scope)=='B878F14BF530B9EAD8820AB7770E16954B2F21DEFC81B02E9AD02DCBD48B2F6B'
assert shutil.disk_usage(P).free>=12*1024**3
now=time.monotonic();save(H/'STAGE_CLOCK.json',dict(started_monotonic=now,deadline_monotonic=now+7200,total_seconds=7200,date_client='2026-10-27'))
for n in ['source','source-before','models','models-before','tests','before','port','upstream','firmware','build','cases','compile','runs','replays','oracles','logs','controls']:(H/n).mkdir()
protected=[]
for root in [B,R/'source',R/'models',R/'port',R/'upstream',R/'firmware',R/'build',R/'oracles']:
 for p in root.rglob('*'):
  if p.is_file():protected.append(dict(path=str(p),SHA256=sha(p)))
protected.append(dict(path=str(scope),SHA256=sha(scope)))
for p in (B/'source').iterdir():
 if p.is_file():
  for target in ['source','source-before']:shutil.copyfile(p,H/target/p.name)
for p in (B/'models').iterdir():
 if p.is_file():
  for target in ['models','models-before']:shutil.copyfile(p,H/target/p.name)
p=H/'models/cpu_program_reference.py';s=p.read_text(encoding='utf-8-sig');assert s.count('self.steps<5000000')==1;p.write_text(s.replace('self.steps<5000000','self.steps<25000000'),encoding='utf-8')
for p in (B/'tests').iterdir():
 if p.is_file():shutil.copyfile(p,H/'tests'/p.name);shutil.copyfile(p,H/'before'/p.name)
for name in ['stage_coremark.py','check_coremark.py','frozen_checks.py','stream_io.py','stream_peripherals.py','audit_uart.py','audit_wave.py','host_supervisor.py','run_capture_once.py','guarded_entry.py']:
 shutil.copyfile(B/name,H/name);shutil.copyfile(B/name,H/'before'/name)
shutil.copyfile(B/'block_codec.py',H/'block_codec.py')
for target in ['port','upstream','firmware']:
 for p in (R/target).iterdir():
  if p.is_file():shutil.copyfile(p,H/target/p.name)
for name in ['performance','validation']:
 shutil.copytree(R/'build'/name,H/'build'/name);shutil.copytree(R/'oracles'/name,H/'oracles'/name)
 d=H/'replays'/(name+'-N234');d.mkdir()
 for q in ['process.json','stdout.log','registers.hex','ram.hex','ram-output.txt','uart-pins.log']:shutil.copyfile(R/'runs'/(name+'-N234')/q,d/q)
 shutil.copyfile(B/'replays'/(name+'-N234')/'streams.json',d/'streams.json')
shutil.copytree(R/'cases/performance-N234/source',H/'cases/performance8-N234/source')
for name in ['manual-plan.json','frozen-case-plan.json']:shutil.copyfile(B/name,H/name)
save(H/'BASE_BUILD_RESULT.json',json.loads((R/'build-result.json').read_text(encoding='utf-8-sig')))
save(H/'protected-originals.json',dict(files=list({r['path']:r for r in protected}.values())))
save(H/'APPROVAL.json',dict(stage='A-COREMARK-LONGRUN-READY-M2',decision='D160',date_client='2026-10-27',user_reply='同意',scope_SHA256=sha(scope),max_C_build=1,max_RTL_compile=1,max_new_DUT=1,iterations=8,stage_seconds=7200,hardware='STOPPED',external_compiler_route='SEPARATE_TOOL_PERMISSION'))
save(H/'TEST_PLAN.json',dict(frozen_before_execution=True,original_RTL=13,container_real_bytes_min=536870913,container_small_segments=1025,host_negative=['bad index','bad payload','missing/reordered/duplicate segment','missing END','oversized line','spool limit','absolute deadline','unavailable memory','invalid resource/read metadata','-O'],old_replays=['performance-N234','validation-N234'],new_program='performance8',iterations=8,raw_limit_each=17179869184,record_limit_each=500000000,segments_limit_each=16384,index_limit=16777216,archive_limit_run=4294967296,spool_limit=33554432,compile_seconds=120,DUT_seconds=2400,DUT_cycles=32000000,oracle_steps=25000000,oracle_seconds=900,check_seconds=1800,stage_seconds=7200,new_oracle='Computed independently and frozen BEFORE DUT; no extrapolation used as expected result'))
# Reuse only well-defined helper functions, never old stage main/build/run entry points.
src=(R/'stage_coremark.py').read_text(encoding='utf-8-sig');tree=ast.parse(src);wanted=['elf_symbols','initial_word','table']
helpers='\n\n'.join(ast.get_source_segment(src,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted)
text=(H/'stage_coremark.py').read_text(encoding='utf-8-sig');text=text.replace('import json,hashlib','import json,hashlib,struct')+'\n'+helpers+'\n';(H/'stage_coremark.py').write_text(text,encoding='utf-8')
# Record specific stage approval, leaving original proposal/status untouched.
M=P/'.project-memory';snap=M/'history/2026-10-27-m2-approved';snap.mkdir()
for n in ['CURRENT.md','INDEX.md','DECISIONS.md','TODO.md','COLLABORATION.md']:(snap/n).write_bytes((M/n).read_bytes())
q=M/'DECISIONS.md';t=q.read_text(encoding='utf-8');assert '## D-160：' not in t;t=t.replace('## D-159：','''## D-160：用户批准M2具体范围，单次新C构建/编译/8迭代DUT

- 2026-10-27，用户对明确M2范围回复“同意”。采用D159 scope1.0.0 SHA B878F14BF530B9EAD8820AB7770E16954B2F21DEFC81B02E9AD02DCBD48B2F6B，新独立`work/fpga/2026-10-27-coremark-longrun-ready-m2/`；旧PENDING在本具体范围被取代，原提案不改。
- 只改A验证容器/限额/监督与参考预算，13RTL/ISA语义/官方算法/port/启动链接不改；host规模控制/旧双2重放/先验，再仅1C构建及必要辅助命令/1 Icarus编译/1性能8迭代DUT。阶段总7200秒，各预算按原scope，外部工具权限仍另核；禁止追加160/新CPU/PDS/硬件。
- 当前已准备副本但未执行，不把授权/文件存在当验收。B R1解耦，over_temp STOP/原件保护/失败停留规则保持。

## D-159：''',1);q.write_text(t,encoding='utf-8',newline='\n')
q=M/'CURRENT.md';t=q.read_text(encoding='utf-8');t=t.replace('F159/D159；','F159/D160（M2已批实施，未验收）；',1).replace('**下一范围待批**','**当前已批阶段**').replace('仅技术推荐PENDING，D156的1+1已用完','D160已明确批准该M2范围，原D156的1+1已用完').replace('待批`deliveries/','已批原scope `deliveries/');q.write_text(t,encoding='utf-8',newline='\n')
print(json.dumps(dict(status='M2_APPROVED_PREPARED',path=str(H),protected=len({r['path']:r for r in protected}),new_tools_or_DUT=0,free_disk_GiB=round(shutil.disk_usage(P).free/1024**3,2))))
