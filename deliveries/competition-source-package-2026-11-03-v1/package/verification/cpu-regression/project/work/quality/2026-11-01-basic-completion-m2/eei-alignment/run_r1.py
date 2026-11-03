from pathlib import Path
import subprocess,json,time,hashlib,re,sys,importlib.util
R=Path('D:/A_FPGA_Comp');H=Path(__file__).resolve().parent;W=H.parent
if not __debug__:raise SystemExit('No optimized Python')
I=R/'tools/iverilog-13.0-msys2-ucrt64/ucrt64';plan=json.loads((H/'PLAN.json').read_text());out=H/'runs-r1';out.mkdir(exist_ok=False);results=[];jobs=[]
spec=importlib.util.spec_from_file_location('owned',R/'work/pds-jtag/2026-10-30-led-official-batch-h4/owned_job.py');J=importlib.util.module_from_spec(spec);spec.loader.exec_module(J)
def run(args,cwd,label,limit):
 t=time.monotonic();job=J.OwnedJob(list(map(str,args)),cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 try:data,_=job.p.communicate(timeout=limit);rc=job.p.returncode
 except subprocess.TimeoutExpired:data=b'TIMEOUT';rc='TIMEOUT'
 time.sleep(.2);cl=job.close();(cwd/(label+'.log')).write_bytes(data);jobs.append(dict(argv=list(map(str,args)),cwd=str(cwd),label=label,rc=rc,seconds=time.monotonic()-t,cleanup=cl))
 if (rc!=0 and not (label!='compile' and rc==1 and b'TIMEOUT' in data)) or not cl['job_empty'] or cl['forced_non_console_cleanup']:raise RuntimeError('native/tool failure '+label)
 return data.decode(errors='replace')
for version in ['source','source-before']:
 for sync in [0,1]:
  d=out/(version+str(sync));d.mkdir();vvp=d/'tb.vvp';src=W/version
  run([I/'bin/iverilog.exe','-B',I/'lib/ivl','-g2012','-s','tb','-Ptb.SYNC='+str(sync),'-o',vvp,*[src/n for n in ['alu.v','control.v','regfile.v','cpu.v']],H/'tb.sv'],d,'compile',60)
  for c in plan['cases']:
   text=run([I/'bin/vvp.exe','-M',I/'lib/ivl',vvp,'+ROM='+str(H/(c['id']+'.hex')),'+VCD='+str(d/(c['id']+'.vcd'))],d,c['id'],10)
   wb=[[int(a),int(b,16)] for a,b in re.findall(r'^WB (\d+) ([0-9a-f]{8})$',text,re.M)];stores=[[int(a,16),int(b,16),int(z,16)] for a,b,z in re.findall(r'^ST ([0-9a-f]{8}) ([0-9a-f]{8}) ([0-9a-f])$',text,re.M)];m=re.findall(r'^STOP (\d+) ([0-9a-f]{8}) (\d+)$',text,re.M);rf={int(a):int(b,16) for a,b in re.findall(r'^RF (\d+) ([0-9a-f]{8})$',text,re.M)};mem=re.findall(r'^MEM ([0-9a-f]{8})$',text,re.M);expected_rf={i:0 for i in range(32)}
   for rd,val in c['wb']:expected_rf[rd]=val
   ok=len(m)==1 and int(m[0][0])==c['stop_kind'] and int(m[0][1],16)==c['stop_pc'] and wb==c['wb'] and stores==c['stores'] and rf==expected_rf and len(mem)==1 and int(mem[0],16)==c['final_mem'] and text.splitlines().count('END')==1
   results.append(dict(id=c['id'],version=version,sync=sync,status='PASS' if ok else ('TIMEOUT' if 'TIMEOUT' in text else 'FAIL'),actual_stop=m,WB=wb,STORE=stores,expected=c,full_RF_match=rf==expected_rf));print(version,sync,c['id'],results[-1]['status'],flush=True)
with (H/'RESULTS-r1.json').open('x') as f:json.dump(dict(cases=results,jobs=jobs,new_source_all_pass=all(c['status']=='PASS' for c in results if c['version']=='source'),old_counterexample_count=sum(c['status']=='FAIL' for c in results if c['version']=='source-before'),scope='Finite local EEI alignment tests, not full RV32I or physical memory signoff'),f,indent=2)
