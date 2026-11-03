from execute import *
from reference import emulate
import itertools
if (H/'TIMED_PLAN.json').exists():raise SystemExit('timed attempt exists')
(H/'TIMED_PLAN.json').write_text(json.dumps(dict(scope='Additional clock-driven simulated mtime. No formal score (<10s target time).',clock_rule='At rising edge N after reset: counter sample = N-1; one-edge registered memory read supplied to MEM at edge N is N-2; high word zero during bounded run.',reference_rule='Check each accepted timer read address/value against fixed clock rule; sequential ISA model consumes computed rule values in independent instruction order, not DUT data. Fixed CRC/main return and full streams/state required.',modes=['performance','validation'],pred=[0,1],max_cycles=4000000,process_seconds=600),indent=2))
results=[]
for pred in [0,1]:
 name=f'timed-p{pred}';vvp=H/(name+'.vvp')
 if run('compile-'+name,[I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-Wall','-s','tb',f'-Ptb.PRED={pred}','-o',vvp,*sorted((H/'source').glob('*.v')),H/'tb-timed.sv'],H,35):raise SystemExit('TOOL_ERROR')
 for mode in ['performance','validation']:
  d=H/'runs'/name/mode;d.mkdir(parents=True,exist_ok=False);(d/'program.hex').write_bytes((H/'build'/mode/'program.hex').read_bytes());symbols=json.loads((H/'build'/mode/'symbols.json').read_text())
  rc=run(name+'-'+mode,[I/'bin/vvp.exe','-M',I/'lib/ivl',vvp,f'+PHASE={symbols["timing_phase"]:x}'],d,600)
  timer=[];timer_ok=True
  for line in (d/'timer-reads.txt').read_text().splitlines():
   _,cycle,addr,value=line.split();cycle=int(cycle);addr=int(addr,16);expected=cycle-2 if addr==0x20000100 else 0
   timer_ok &= int(value,16)==expected;timer.append((addr,expected))
  if not timer_ok:raise RuntimeError('Clock rule mismatch; preserve evidence, do not adjust rule to fit DUT')
  e=H/'timed-expected'/name/mode;model=emulate(mode,e,timer)
  state=(d/'state.txt').read_text().splitlines();checks=dict(native=rc==0,timer_rule=timer_ok,timer_read_count=len(timer)==12,unknown=not any(s.startswith(('UNKNOWN','TRAP','BAD_')) for s in state))
  for fn,tag in [('wb.txt',None),('store.txt',None),('regs.txt','REG '),('memory.txt','MEM '),('uart.txt',None)]:
   with (d/('state.txt' if tag else fn)).open() as aa,(e/fn).open() as bb:
    stream=(s for s in aa if s.startswith(tag)) if tag else aa;checks[fn]=all(a==b for a,b in itertools.zip_longest(stream,bb))
  end=[list(map(int,s.split()[1:])) for s in state if s.startswith('END ')];checks['completed']=len(end)==1 and 0<end[0][1]<end[0][2]<end[0][3]<4000000
  result=dict(mode=mode,pred=pred,status='PASS' if all(checks.values()) else 'FAIL',checks=checks,timer_reads=timer,model=model,end=end,seconds=jobs[-1]['seconds']);results.append(result);(H/'TIMED_RESULTS.json').write_text(json.dumps(results,indent=2));print(result,flush=True)
  if result['status']!='PASS':raise SystemExit(1)
