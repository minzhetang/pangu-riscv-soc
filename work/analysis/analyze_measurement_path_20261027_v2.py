from pathlib import Path
from collections import Counter
from fractions import Fraction
import sys,time,json,hashlib,re,struct,ctypes,ctypes.wintypes as w
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf-8');assert not sys.flags.optimize
P=Path('D:/A_FPGA_Comp');H=P/'work/analysis/2026-10-27-measurement-path-m0-v2';H.mkdir(exist_ok=False);S=P/'work/fpga/2026-10-27-coremark-longrun-ready-m2';B=P/'work/fpga/2026-10-25-board-top-m1';R=P/'work/fpga/2026-10-25-coremark-iter2-m1';O=P/'work/system/2026-10-23-coremark-correctness-m1/upstream-direct/files';start=time.monotonic();end=start+180
sys.path.insert(0,str(S));import block_codec
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest().upper()
def save(n,o):
 with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
class PMC(ctypes.Structure):
 _fields_=[('cb',w.DWORD),('fault',w.DWORD)]+[(n,ctypes.c_size_t) for n in ['peak','ws','a','b','c','d','page','pagepeak']]
k=ctypes.windll.kernel32;ps=ctypes.windll.psapi;k.GetCurrentProcess.restype=w.HANDLE;ps.GetProcessMemoryInfo.argtypes=[w.HANDLE,ctypes.POINTER(PMC),w.DWORD]
def peak():
 r=PMC();r.cb=ctypes.sizeof(r);assert ps.GetProcessMemoryInfo(k.GetCurrentProcess(),ctypes.byref(r),r.cb);return r.peak
def check():assert time.monotonic()<end and peak()<=256*1024**2,'readonly analysis budget'
protected=[]
def pin(p):
 assert p.is_file() and not p.is_symlink();protected.append(dict(path=str(p.relative_to(P)),bytes=p.stat().st_size,SHA256=sha(p)))
for x in read(S/'frozen-inputs.json')['files']:pin(S/x['path']);assert sha(S/x['path'])==x['SHA256']
for p in [S/'SUMMARY.json',S/'postflight.json',S/'build-result.json',S/'build/performance8/program.bin',S/'build/performance8/program.elf',S/'runs/performance8-N234/check-result.json',S/'runs/performance8-N234/streams.json',B/'pds/build.tcl',B/'pds/source/init_tables.svh',B/'pds/board_pins.fdc',B/'pds/clock_27mhz.fdc',B/'pds-audit.json',O/'README.md',O/'barebones_porting.md',R/'runs/performance-N234/check-result.json',R/'runs/validation-N234/check-result.json',P/'work/fpga/2026-10-26-coremark-stream-evidence-m1/logs/run-performance-N234/process.json',P/'reports/environment/2026-10-11-scbv-high-verification.md',P/'reports/progress/2026-10-23-mainline-focus-reset.md']:pin(p)
for p in (B/'pds/source').iterdir():
 if p.suffix in ['.v','.sv']:
  pin(p)
  if p.name!='memory_model.sv':assert sha(p)==sha(S/'source'/p.name)
# Verify the exact known production transformation, not a blanket equivalence assumption.
old_mem=(B/'pds/source/memory_model.sv').read_text(encoding='utf-8-sig');new_mem=(S/'source/memory_model.sv').read_text(encoding='utf-8-sig')
new_mem=new_mem.replace('    `include "init_tables.svh"',(B/'pds/source/init_tables.svh').read_text(encoding='utf-8-sig').rstrip())
new_mem=re.sub(r'(?ms)^`ifdef M0_VERIFY\n.*?^`endif\n','',new_mem)
assert re.sub(r'\s+','',old_mem)==re.sub(r'\s+','',new_mem),'production transformation not identical'
save('PRODUCTION_BINDING.json',dict(exact_source_files=12,memory_model='M0_VERIFY views excluded; same INIT inlined; exact nonwhitespace identity',functional_source_changed=False))
problem=[]
for x in read(P/'reports/progress/evidence/2026-10-23-focus-reset/sources-before.json'):
 if str(x['path']).startswith('题目'):
  p=P/x['path'];pin(p);assert sha(p)==x['sha256'];problem.append(x['path'])
image=(S/'build/performance8/program.bin').read_bytes();elf=(S/'build/performance8/program.elf').read_bytes();head=struct.unpack_from('<HHIIIIIHHHHHH',elf,16);assert head[1]==243
sections=[struct.unpack_from('<10I',elf,head[5]+i*head[10]) for i in range(head[11])];functions=[]
for sec in sections:
 if sec[1]!=2:continue
 st=sections[sec[6]];strings=elf[st[4]:st[4]+st[5]]
 for off in range(sec[4],sec[4]+sec[5],sec[9]):
  n,v,size,info,other,index=struct.unpack_from('<IIIBBH',elf,off);name=strings[n:].split(b'\0',1)[0].decode()
  if info&15==2 and size and v<32768:functions.append((v,v+size,name))
def fn(pc):return next((n for a,b,n in functions if a<=pc<b),'NO_FUNCTION_SYMBOL')
def rom(path):
 text=path.read_text(encoding='ascii');part=text.split('ROM_BITS = {',1)[1].split('};',1)[0];pieces=re.findall("4096'h([0-9a-fA-F]{1024})",part);assert len(pieces)==64;return bytes.fromhex(''.join(pieces))[::-1]
oldrom=rom(B/'pds/source/init_tables.svh');newrom=rom(S/'cases/performance8-N234/source/init_tables.svh');assert newrom==image+bytes(32768-len(image))
diffs=[dict(offset=i,implemented_old=a,new8=b) for i,(a,b) in enumerate(zip(oldrom,newrom)) if a!=b]
save('IMAGE_IMPLEMENTATION_GAP.json',dict(functional_sources13_unchanged=True,PDS_source12_exact_and_memory_preprocessing_verified=True,old_PDS_init_SHA256=sha(B/'pds/source/init_tables.svh'),new8_init_SHA256=sha(S/'cases/performance8-N234/source/init_tables.svh'),byte_differences=diffs,new8_matches_binary=True,new8_PDS='NOT_RUN',CPU_sbit='NOT_GENERATED',old_flow_gen_bit_stream='gen_bit_stream' in (B/'pds/build.tcl').read_text(encoding='utf-8-sig')))
r=read(S/'runs/performance8-N234/check-result.json');assert r['status']=='PASS';t0,t1=r['detail']['stamps'][2:];lo=t0+1;hi=t1+1;spec=read(S/'runs/performance8-N234/streams.json')['trace'];idx=Path(spec['path'])/'stream-index.json';assert idx.stat().st_size<=16*1024**2 and sha(idx)==spec['index_SHA256'];pin(idx);meta=read(idx)
whole=hashlib.sha256();counts={p:Counter() for p in ['before','timed','after']};pc_counts=Counter();opcounts=Counter();funcounts=Counter();gaps=Counter();last=None;total=raw=0
opname={3:'LOAD',35:'STORE',99:'BRANCH',103:'JALR',111:'JAL',19:'OP_IMM',51:'OP',55:'LUI',23:'AUIPC',115:'SYSTEM'}
for seq,seg in enumerate(meta['segments']):
 check();assert seg['seq']==seq and seg['folder']==f'{seq:06d}';d=Path(spec['path'])/seg['folder'];pin(d/'index.json')
 for p in d.glob('block-*.gz'):pin(p)
 n=b=0
 for block in block_codec.decode(d,seg['index_SHA256']):
  check();whole.update(block);b+=len(block);raw+=len(block)
  for line in block.splitlines():
   total+=1;n+=1;a=line.split(b'|');kind=a[0].decode();c=int(a[1]);part='before' if c<=lo else 'timed' if c<=hi else 'after';counts[part][kind]+=1
   if part=='timed' and kind=='EX':
    pc=int(a[2],16);assert pc%4==0 and pc+4<=len(image);pc_counts[pc]+=1;word=int.from_bytes(image[pc:pc+4],'little');opcounts[opname.get(word&127,'OTHER')]+=1;funcounts[fn(pc)]+=1
    if last is not None:assert c>last and (c-last)%2==0;gaps[c-last]+=1
    last=c
 assert n==seg['records'] and b==seg['raw_bytes']
assert (total,raw,whole.hexdigest().upper())==(meta['records'],meta['raw_bytes'],meta['raw_SHA256']);assert sum(x['EX'] for x in counts.values())==r['streams']['EX']['count']
slots=hi//2-lo//2;active=counts['timed']['EX'];hot=[dict(pc=f'0x{pc:08x}',word=f'{int.from_bytes(image[pc:pc+4],"little"):08x}',function=fn(pc),EX_events=n) for pc,n in pc_counts.most_common(16)]
save('TIMED_WINDOW_PROFILE.json',dict(status='READONLY_EXISTING_TRACE_NOT_NEW_FUNCTIONAL_TEST',timer_ticks=[t0,t1],edge_interval=dict(lower_exclusive=lo,upper_inclusive=hi,coordinate='physical posedge c; pre timer=c-1'),raw_ticks=t1-t0,nominal_seconds=str(Fraction(t1-t0,27000000)),regions={k:dict(v) for k,v in counts.items()},logical_slots=slots,EX=active,EX_per_physical_tick=float(Fraction(active,t1-t0)),EX_per_logical_slot=float(Fraction(active,slots)),logical_slots_without_EX=slots-active,gap_physical_ticks=dict(sorted(gaps.items())),opcode_counts=dict(opcounts),function_counts=dict(funcounts.most_common()),hot_PC=hot,records=total,raw_bytes=raw,trace_SHA256=whole.hexdigest().upper(),not_retirement_IPC=True,not_stall_flush_attribution=True,not_ILA=True))
x2=read(R/'runs/performance-N234/check-result.json');v2=read(R/'runs/validation-N234/check-result.json');v1=read(P/'work/fpga/2026-10-25-board-coremark-m1/runs/validation-N234/check-result.json');pin(P/'work/fpga/2026-10-25-board-coremark-m1/runs/validation-N234/check-result.json')
rate8=read(S/'SUMMARY.json')['DUT_host_seconds']/r['metrics']['physical'];rate2=read(P/'work/fpga/2026-10-26-coremark-stream-evidence-m1/logs/run-performance-N234/process.json')['elapsed_seconds']/x2['metrics']['physical'];rates=sorted([rate8,rate2]);forecast=[]
for name,a,b,ia,ib in [('performance',x2,r,2,8),('validation',v1,v2,1,2)]:
 phys=Fraction(b['metrics']['physical'])+Fraction(b['metrics']['physical']-a['metrics']['physical'],ib-ia)*(160-ib);ticks=Fraction(b['detail']['raw_ticks'])+Fraction(b['detail']['raw_ticks']-a['detail']['raw_ticks'],ib-ia)*(160-ib)
 forecast.append(dict(seed=name,iterations=160,physical_estimate=float(phys),raw_ticks_estimate=float(ticks),nominal_seconds_estimate=float(ticks/27000000),DUT_host_seconds_range=[float(phys)*q for q in rates],oracle='NOT_COMPUTED',DUT='NOT_RUN'))
save('COST_AND_VALIDITY.json',dict(status='CONDITIONAL_ARITHMETIC_ONLY',actual8_nominal_seconds=float(Fraction(t1-t0,27000000)),official_score=False,port_SIM_ONLY=True,checker_requires_short_warning=True,forecasts=forecast,both_DUT_hours=[sum(x['DUT_host_seconds_range'][i] for x in forecast)/3600 for i in [0,1]],excludes_build_reference_checker_cleanup=True,rate_conditions='different host loads, inputs, adapters; not controlled attribution',HAS_FLOAT0='Allowed; preserve raw tick precision',hardware_clock='UNVERIFIED',current8_10sec='NOT_MET',future160='NOT_AUTHORIZED'))
assert all(sha(P/x['path'])==x['SHA256'] for x in protected);check();save('INPUTS.json',dict(files=protected,problem_files_unchanged=len(problem),official_commit='1f483d5b8316753a742cbf5590caf5bd0a4e4777'));save('POSTFLIGHT.json',dict(status='READONLY_INPUTS_UNCHANGED',protected=len(protected),host_seconds=time.monotonic()-start,peak_bytes=peak(),new_build=0,new_DUT=0,new_ISA_model=0,PDS=0,hardware='STOPPED'))
print(json.dumps(dict(status='READONLY_PROFILE_COMPLETE',EX=active,logical_slots=slots,slot_density=active/slots,hot=hot[:4],image_differences=diffs,host_seconds=time.monotonic()-start,both160_DUT_hours=[sum(x['DUT_host_seconds_range'][i] for x in forecast)/3600 for i in [0,1]]),ensure_ascii=False))
