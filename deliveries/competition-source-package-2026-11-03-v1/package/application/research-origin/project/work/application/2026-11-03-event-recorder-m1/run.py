from pathlib import Path
import subprocess,json,time,hashlib,sys
H=Path(__file__).resolve().parent;R=H.parents[2]
T=R/'tools/xpack-riscv-none-elf-gcc-15.2.0-1/bin';I=R/'tools/iverilog-13.0-msys2-ucrt64/ucrt64'
jobs=[]
# Freeze cache before appending this session's commands; do not lose later modes.
prior_jobs=json.loads((H/'COMMANDS.json').read_text()) if '--resume' in sys.argv and (H/'COMMANDS.json').exists() else []
def write(p,o):p.write_text(json.dumps(o,indent=2),encoding='utf8')
def run(name,args,cwd=H,limit=35):
 t=time.monotonic();args=list(map(str,args))
 if '--resume' in sys.argv and (H/'logs'/f'{name}.log').exists() and name not in ['compile1']:
  matching=[j for j in prior_jobs if j['name']==name and j['rc']==0 and j['argv']==args]
  if matching:
   jobs.append(dict(matching[-1],reused_prior_execution=True))
   return (H/'logs'/f'{name}.log').read_text(errors='replace')
  if name.startswith('run-'):raise RuntimeError('Existing run evidence has no matching successful command; use a new directory')
 try:
  p=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=limit);rc=p.returncode;out=p.stdout
 except subprocess.TimeoutExpired as e:rc='TIMEOUT';out=e.stdout or b''
 except OSError as e:rc='TOOL_ERROR';out=str(e).encode()
 logfile=H/'logs'/f'{name}.log'
 if logfile.exists():
  # Future retries are unique evidence, never replace old original logs.
  suffix=1
  while logfile.with_name(f'{name}-attempt{suffix}.log').exists():suffix+=1
  logfile=logfile.with_name(f'{name}-attempt{suffix}.log')
 logfile.write_bytes(out)
 jobs.append(dict(name=name,argv=args,cwd=str(cwd),rc=rc,seconds=time.monotonic()-t));write(H/'COMMANDS.json',jobs)
 if rc!=0:raise RuntimeError((name,rc))
 return out.decode(errors='replace')

# Frozen, manually enumerated expected accepted transitions. No DUT feedback.
cases={
 'normal':([0]*4+[1]*4+[3]*4+[7]*4+[0]*16,[(5,1,0),(9,3,0),(13,7,0),(17,0,0)],0,0,0,0),
 'order_post':([0]*2+[3]*4+[7]*4+[0]*4+[1]*18,[(3,3,1),(7,7,0),(11,0,0)],1,0,1,1),
 'timeout':([0]*2+[1]*30,[(3,1,0),(9,1,2)],2,0,0,0),
 'bounce_reject':([1,0]*16,[],0,0,0,0),
 'bounce_boundary':([0,1,0,1,1]+[3]*4+[7]*4+[0]*19,[(4,1,0),(6,3,0),(10,7,0),(14,0,0)],0,0,0,0),
 'ring_wrap':([v for v in [1,3,7,0]*4 for _ in range(2)],[(2*j+1,v,0) for j,v in enumerate([1,3,7,0]*4)][-8:],0,8,0,0),
 'wrap_fault_window':([v for v in ([1,3,7,0]*3)[:10] for _ in range(2)]+[1]*4+[3]*4+[7]*4,[(11,3,0),(13,7,0),(15,0,0),(17,1,0),(19,3,0),(21,1,1),(25,3,0),(29,7,0)],1,5,0,1),
}
# This freezes before any compile/load/run, including complete input streams.
plan={k:dict(input=v[0],events=v[1],fault=v[2],evicted=v[3],rejected=v[4],frozen=v[5]) for k,v in cases.items()}
plan_path=H/'FROZEN_PLAN_v2.json'
if plan_path.exists():
 assert json.loads(plan_path.read_text())==json.loads(json.dumps(plan))
else:write(plan_path,plan)
src=[p for p in sorted((H/'source').glob('*')) if p.suffix in ['.v','.sv'] and p.name not in ['memory_model.sv','board_top.sv','board_reset_sync.sv']]
results=[]
try:
 for dense in [0,1]:
  elf=H/f'program{dense}.elf';binfile=H/f'program{dense}.bin'
  run(f'gcc{dense}',[T/'riscv-none-elf-gcc.exe','-march=rv32i','-mabi=ilp32','-O2','-ffreestanding','-fno-builtin','-msmall-data-limit=0','-mno-relax','-nostdlib','-nostartfiles','-Wl,--no-relax','-Wl,-T,firmware/link.ld',f'-DDENSE={dense}','-o',elf,'firmware/start.S','firmware/app.c'])
  run(f'objcopy{dense}',[T/'riscv-none-elf-objcopy.exe','-O','binary',elf,binfile])
  symbols={line.split()[2]:int(line.split()[0],16) for line in run(f'nm{dense}',[T/'riscv-none-elf-nm.exe',elf]).splitlines() if len(line.split())==3}
  b=binfile.read_bytes();assert len(b)<=32768;b+=bytes(32768-len(b))
  hextext=''.join(f'{int.from_bytes(b[i:i+4],"little"):08x}\n' for i in range(0,len(b),4))
  # Both modes use byte-identical RTL/TB; firmware is loaded at runtime.
  vvp=H/'app0.vvp'
  if dense==0:run('compile0',[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-s','tb','-o',vvp,*src,H/'memory_sim.sv',H/'tb.sv'])
  for name,c in plan.items():
   d=H/'runs'/f'{name}-dense{dense}';d.mkdir(exist_ok='--resume' in sys.argv)
   input_text=''.join(f'{s:02x}\n' for s in c['input'])
   if (d/'input.hex').exists():assert (d/'input.hex').read_text()==input_text and (d/'program.hex').read_text()==hextext
   else:(d/'input.hex').write_text(input_text);(d/'program.hex').write_text(hextext)
   if (d/'stop.txt').exists():
    assert any(q['name']==f'run-{name}-{dense}' and q['rc']==0 for q in prior_jobs),'Existing output without matching successful execution: use a new directory'
   run(f'run-{name}-{dense}',[I/'bin/vvp.exe','-M',I/'lib/ivl',vvp],cwd=d,limit=45)
   accepted=(d/'accepted.txt').read_bytes();wire=(d/'serial.txt').read_bytes();assert accepted==wire,'physical TX decode mismatch'
   parts=accepted.decode().split('~');assert len(parts)==3 and parts[-1]==''
   repeats=[]
   for rep in range(2):
    ram=[]
    for l in (d/f'ram{rep}.hex').read_text().splitlines():
     if l.startswith('//') or l.startswith('@'):continue
     ram+=list(map(lambda x:int(x,16),l.split()))
    def words(sym,n=1):a=(symbols[sym]-65536)//4;return ram[a:a+n]
    samples=[tuple(words('samples',64)[i:i+2]) for i in range(0,64,2)]
    assert [s for t,s in samples]==c['input'],('input mismatch',name)
    t0=words('start_tick')[0];ts=[t for t,s in samples]
    assert all(12000*(i+1)<=t-t0<=12000*(i+1)+1000 for i,t in enumerate(ts)),'deadline/jitter violation'
    assert words('late')==[0] and words('complete')==[1]
    count=words('count')[0];head=words('head')[0];ev=words('events',32)
    actual=[tuple(ev[4*((head+8-count+k)&7):4*((head+8-count+k)&7)+4]) for k in range(count)]
    expected=[(ts[i],i,s,why) for i,s,why in c['events']];assert actual==expected,(name,actual,expected)
    for sym in ['fault','evicted','rejected','frozen']:assert words(sym)==[c[sym]],(name,sym,words(sym),c[sym])
    # Exact UART including every event in order; retain all timestamp bits.
    hx=lambda vals:''.join(f'{v:08x} ' for v in vals)
    out='REC1 '+hx([dense,t0,words('end_tick')[0],words('work_ticks')[0],0,count,c['evicted'],c['rejected'],c['fault'],c['frozen']])+'\n'
    if dense:
     for i,(t,s) in enumerate(samples):out+='S '+hx([i,t,s])+'\n'
    for evv in expected:out+='E '+hx(evv)+'\n'
    out+='END\n';assert parts[rep]==out.replace('\n','\r\n'),'UART ledger bytes/order mismatch (Windows text-mode CRLF)'
    # Match exact architectural timer returns and GPIO loads, not final PASS text.
    reads=[l.split() for l in (d/'reads.txt').read_text().splitlines() if l.split()[0]==str(rep)]
    gpio_reads=[int(v[2],16)&7 for v in reads if int(v[1],16)==0x20000010]
    assert gpio_reads==c['input'],'GPIO read count/order'
    timer_values={int(v[2],16) for v in reads if int(v[1],16)==0x20000100}
    assert set(ts).issubset(timer_values),'timestamps not actual timer loads'
    repeats.append(dict(samples=samples,events=actual,work_ticks=words('work_ticks')[0],window_ticks=words('end_tick')[0]-t0,uart_bytes=len(out),fault=c['fault'],evicted=c['evicted'],rejected=c['rejected'],frozen=c['frozen']))
   assert repeats[0]==repeats[1],'reset repeat diverged'
   results.append(dict(case=name,dense=dense,status='PASS',repeats=repeats,program_bytes=binfile.stat().st_size))
   write(H/'RESULTS.json',dict(status='IN_PROGRESS',results=results))
 write(H/'RESULTS.json',dict(status='LIVE_GPIO_TIMER_CPU_SIM_PASS',results=results,jobs=jobs,physical_board=False,public_RTL_modified=False))
except Exception as e:
 write(H/'RESULTS.json',dict(status='FAILED_OR_TOOL_BLOCKED',error=repr(e),results=results,jobs=jobs));raise
print('PASS',len(results),'case/mode pairs with two resets each')
