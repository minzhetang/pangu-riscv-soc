from pathlib import Path
import json,hashlib,shutil,re,time,ctypes,difflib
P=Path('D:/A_FPGA_Comp');S=P/'work/fpga/2026-10-27-coremark-longrun-ready-m2';B=P/'work/fpga/2026-10-25-board-top-m1';H=P/'work/fpga/2026-10-27-board-coremark8-bitstream-m1';assert not H.exists();assert not ctypes.windll.shell32.IsUserAnAdmin();assert shutil.disk_usage(P).free>=4*1024**3
scope=P/'deliveries/mainline-board-coremark8-bitstream-scope-2026-10-27-v1/IMPLEMENTATION_SCOPE.md';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper();assert sha(scope)=='6BE782B91E2670510E9A47FC1233B51FC89CFC5B7DDE9911D4D9E4C234BE4B08'
H.mkdir();now=time.monotonic()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
save('STAGE_CLOCK.json',dict(started_monotonic=now,deadline_monotonic=now+2400,total_seconds=2400,date_client='2026-10-27'))
for d in ['source','source-before','pds/source','firmware','logs','before','evidence']:(H/d).mkdir(parents=True,exist_ok=True)
receipts=json.loads((S/'SOURCE_RECEIPTS.json').read_text(encoding='utf-8-sig'))['functional_RTL'];assert len(receipts)==13
protected={}
def pin(p):protected[str(p)]=dict(path=str(p),SHA256=sha(p))
for row in receipts:
 p=S/'source'/row['name'];assert sha(p)==row['SHA256'];pin(p)
 for root in ['source','source-before','pds/source']:shutil.copyfile(p,H/root/p.name)
for name in ['program.bin','program.elf']:
 p=S/'build/performance8'/name;pin(p);shutil.copyfile(p,H/'firmware'/name)
assert sha(H/'firmware/program.bin')=='EC365839FEA1111CB365763322E2FA99C3C3B3F6B74A5884C5B0EB30593486F0'
init=S/'cases/performance8-N234/source/init_tables.svh';pin(init);shutil.copyfile(init,H/'pds/source/init_tables.svh')
x=(H/'source/memory_model.sv').read_text(encoding='utf-8-sig');prod=x.replace('    `include "init_tables.svh"',(H/'pds/source/init_tables.svh').read_text(encoding='utf-8-sig'));prod=re.sub(r'(?ms)^`ifdef M0_VERIFY\n.*?^`endif\n','',prod);assert '`include' not in prod and 'M0_VERIFY' not in prod and '$fatal' not in prod
(H/'pds/source/memory_model.sv').write_text(prod,encoding='ascii')
# Independent comparison to prior production source after replacing only its init text.
old=(B/'pds/source/memory_model.sv').read_text(encoding='utf-8-sig');oldinit=(B/'pds/source/init_tables.svh').read_text(encoding='utf-8-sig');newinit=(H/'pds/source/init_tables.svh').read_text(encoding='utf-8-sig');assert old.count(oldinit)==1;assert re.sub(r'\s+','',old.replace(oldinit,newinit))==re.sub(r'\s+','',prod)
for p in (B/'pds/source').iterdir():
 if p.suffix in ['.v','.sv']:pin(p)
for n in ['board_pins.fdc','clock_27mhz.fdc']:
 p=B/'pds'/n;pin(p);shutil.copyfile(p,H/'pds'/n)
for p in [scope,S/'STATUS.json',S/'SUMMARY.json',S/'SOURCE_RECEIPTS.json',S/'runs/performance8-N234/check-result.json',B/'pds-audit.json',B/'pin-plan.json',B/'pds/build.tcl',B/'pds/synthesize/board_top_syn.vm']:
 pin(p)
pin(Path('D:/PDS/PDS_2022.2-SP6.4/bin/pds_shell.exe'))
# Preserve the old flow and comparison metadata, never old stage outputs.
for n in ['pds-audit.json','pin-plan.json']:shutil.copyfile(B/n,H/'before'/n)
shutil.copyfile(B/'pds/build.tcl',H/'before/build.tcl')
tcl=['set project_dir [file normalize [file dirname [info script]]]','cd $project_dir']+[f'add_design [file join $project_dir source {row["name"]}]' for row in receipts]+['add_constraint [file join $project_dir board_pins.fdc]','add_constraint [file join $project_dir clock_27mhz.fdc]','set_arch -family Logos2 -device PG2L100H -speedgrade -6 -package FBG676','compile -top_module board_top','synthesize -ads -selected_syn_tool_opt 2','dev_map','pnr','report_timing','gen_bit_stream -scbv "High Voltage"']
assert not any(re.search(r'jtag|server|cfg_program|erase|flash|download',line,re.I) for line in tcl);(H/'pds/build.tcl').write_text('\n'.join(tcl)+'\n',encoding='ascii')
# Exact ROM/RAM bytes from source constants, independent of old image file existence.
def data(name,text):
 part=text.split(name+'_BITS = {',1)[1].split('};',1)[0];v=re.findall("4096'h([0-9a-fA-F]{1024})",part);assert len(v)==64;return bytes.fromhex(''.join(v))[::-1]
rom=data('ROM',newinit);ram=data('RAM',newinit);image=(H/'firmware/program.bin').read_bytes();assert len(image)==15912 and rom==image+bytes(32768-len(image)) and ram==bytes([0xa5])*32768
save('INIT_RECEIPT.json',dict(ROM_bytes=32768,RAM_bytes=32768,image_bytes=len(image),ROM_SHA256=hashlib.sha256(rom).hexdigest().upper(),RAM_SHA256=hashlib.sha256(ram).hexdigest().upper(),image_SHA256=sha(H/'firmware/program.bin'),init_SHA256=sha(H/'pds/source/init_tables.svh'),new8_byte_equal=True,RAM_A5=True))
save('APPROVAL.json',dict(date_client='2026-10-27',decision='D164',user_reply='授权同意，继续',scope_SHA256=sha(scope),scope_LF_normalized_SHA256='BB1D768FBB82166753982CC5167569215A31606675B6D42A959DE7E976753B9D',scope_identity_erratum='No content change: previous metadata hashed normalized LF, actual reviewed Git blob uses CRLF',scope='A-BOARD-COREMARK8-BITSTREAM-M1',max_PDS=1,max_C_build=0,max_RTL_sim_compile=0,max_DUT=0,SCBV='D010 High Voltage engineering assumption carried into new copy only',hardware='STOPPED',external_tool_route='SEPARATE_SYSTEM_REVIEW'))
save('PROTECTED_ORIGINALS.json',dict(files=list(protected.values())));save('SOURCE_RECEIPTS.json',dict(functional_RTL=receipts,exact_production_files=12,memory_model='only remove M0_VERIFY and inline same new INIT; normalize whitespace compare prior production with new INIT',source_and_source_before_same=True))
(H/'FLOW_DIFF.patch').write_text(''.join(difflib.unified_diff((B/'pds/build.tcl').read_text(encoding='utf-8-sig').splitlines(True),(H/'pds/build.tcl').read_text(encoding='utf-8-sig').splitlines(True),fromfile='old/board/build.tcl',tofile='new/coremark8/build.tcl')),encoding='utf-8')
# Reuse A's verified bounded runner; only stage root/limit and owned-tree failure cleanup adapt.
shutil.copyfile(S/'stage_budget.py',H/'stage_budget.py')
ss=(S/'host_supervisor.py').read_text(encoding='utf-8-sig').replace('8*1024**2-count','32*1024**2-count')
ss=ss.replace("   try:p.kill()\n   except OSError:pass", "   try:\n    q=subprocess.run(['C:/Windows/System32/taskkill.exe','/PID',str(p.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=8)\n    state['owned_tree_cleanup_rc']=q.returncode\n   except Exception as exc:state['owned_tree_cleanup_error']=type(exc).__name__\n   if p.poll() is None:\n    try:p.kill()\n    except OSError:pass")
ss=ss.replace("'direct child and this parent; native compiler internal descendants not separately measured'","'PDS shell and this parent only; stage memory pool report retained separately, internal child peaks not separately measured'")
(H/'host_supervisor.py').write_text(ss,encoding='utf-8')
# Actual approval recorded separately; original pending proposal remains immutable.
M=P/'.project-memory';hist=M/'history/2026-10-27-coremark8-bitstream-approved';hist.mkdir();
for n in ['CURRENT.md','INDEX.md','TODO.md','COLLABORATION.md']:(hist/n).write_bytes((M/n).read_bytes())
p=M/'DECISIONS.md';text=p.read_text(encoding='utf-8-sig');assert '## D-164' not in text;entry='''## D-164：批准单次CoreMark8 CPU软件位流构建

- 2026-10-27，用户在解释目标/变化/收益后明确“授权同意，继续”，批准D163 scope1.0.0正文，实际文件SHA6BE782B91E2670510E9A47FC1233B51FC89CFC5B7DDE9911D4D9E4C234BE4B08；原BB1D…仅UTF8/LF规范化SHA，换行元数据纠错见原目录SCOPE_IDENTITY_CORRECTION.json，原件与已审Git blob完全一致、未改范围。仅新独立副本、原13功能RTL/8镜像/FDC不改、memory确定性生产绑定、最多1次PDS六阶段含gen_bit_stream；0GCC/Icarus/DUT，阶段2400秒/PDS1800秒。外部工具权限单独核准。
- 原提案PENDING为历史不回写；本范围现已批但尚未验收。High Voltage仅沿D010工程假设写新位流选项，不把软件设置当供电证明，不增ILA/160/硬件操作。工具/许可/时序/必要范围失败则停，原件保留，over_temp STOP。

''';p.write_text(text.replace('# 重要决策记录','# 重要决策记录\n\n'+entry,1),encoding='utf-8')
p=M/'CURRENT.md';text=p.read_text(encoding='utf-8-sig').replace('F162/D163（主线只读路径/窗口分析）','F162/D164（单次软件位流构建已批/未验收）',1).replace('仅已备范围，**PENDING批准**','已由D164明确批准，**实施中、未验收**',1).replace('待批`deliveries/','已批原scope`deliveries/',1);p.write_text(text,encoding='utf-8')
print(json.dumps(dict(status='INPUTS_PREPARED_NOT_BUILT',functional_sources=13,protected=len(protected),image_sha=sha(H/'firmware/program.bin'),SCBV='High Voltage',free_disk_GiB=round(shutil.disk_usage(P).free/1024**3,2)),ensure_ascii=False))
