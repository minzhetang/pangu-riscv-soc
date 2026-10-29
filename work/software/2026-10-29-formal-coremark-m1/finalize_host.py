from pathlib import Path
import sys,json,re,copy,time
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
from stage_coremark import read,save,sha
from measurement_report import parse
from stage_budget import check
check();start=time.monotonic();rows=[];reports=[]
tests=['good','bad_crc','bad_final','bad_iterations','duplicate_ticks','missing_flags','truncated','wrong_delta','overflow_delta','wrong_hz','extra_output','duplicate_status']
save(H/'HOST_CONTROL_PLAN.json',dict(before_controls=True,cases=tests,good='candidate or short-only; never formal',negative='ValueError',DUT=0))
for c in read(H/'FROZEN_PLAN.json')['cases']:
 tid=c['id'];o=read(H/'oracles-recovery'/tid/'expected.json');text=(H/'oracles-recovery'/tid/'expected-report.txt').read_text();flags=json.loads(re.search(r'^#define FLAGS_STR (.+)$',(H/'build'/tid/'build_identity.h').read_text(),re.M)[1]);e={**c,'crcfinal':o['crcfinal']}
 out=parse(text,e,flags);assert out['formal_score_valid'] is False and out['hardware_valid'] is False;reports.append(dict(id=tid,parsed=out))
 variants=dict(good=text,bad_crc=text.replace(f"0x{e['standard_CRC'][0]:04x}",'0x0000'),bad_final=text.replace('0x'+e['crcfinal'],'0x0000'),bad_iterations=re.sub(r'^(Iterations\s*:)\s*\d+',r'\g<1> 999',text,flags=re.M),duplicate_ticks=text+'Total ticks : 1\n',missing_flags=re.sub(r'^Compiler flags.+\n','',text,flags=re.M),truncated=text[:len(text)//2],wrong_delta=re.sub(r'^(Raw delta hi/lo\s*:) .+$',r'\g<1> 00000000 00000001',text,flags=re.M),overflow_delta=re.sub(r'^(Raw delta hi/lo\s*:) .+$',r'\g<1> 00000001 00000000',text,flags=re.M),wrong_hz=text.replace('27000000;','13500000;'))
 variants['extra_output']=text+'unexpected result\n'
 variants['duplicate_status']=text+('Errors detected\n' if c['iterations']==2 else 'Correct operation validated. See README.md for run and reporting rules.\n')
 for name,t in variants.items():
  check();assert time.monotonic()-start<60
  try:r=parse(t,e,flags)
  except ValueError as ex:assert name!='good';rows.append(dict(id=tid+'/'+name,status='EXPECTED_REJECT',error=str(ex)))
  else:assert name=='good';rows.append(dict(id=tid+'/'+name,status='PASS_CONTROL'))
save(H/'HOST_CONTROL_RESULTS.json',dict(status='PASS_HOST_ONLY',rows=rows,reports=reports,seconds=time.monotonic()-start,new_DUT=0,not_target_evidence=True))
print('48 host report controls pass; no formal/hardware promotion')
