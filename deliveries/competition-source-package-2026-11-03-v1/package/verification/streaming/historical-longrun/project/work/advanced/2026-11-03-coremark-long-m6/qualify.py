from native import *
P=H.parent/'2026-11-03-coremark-strict-m5'
results=[]
for it in [1,192]:
 for mode in ['performance','validation']:
  text=(H/'logs'/f'host-oracle-{mode}-{it}.log').read_text()
  import re
  known=['e714','1fd7','8e3a']if mode=='performance'else ['e3c1','0747','8d84']
  crcs=[re.search(r'\[0\]'+n+r'\s*:\s*0x([0-9a-f]+)',text)[1]for n in ['crclist','crcmatrix','crcstate']]
  if crcs!=known or 'Errors detected'in text:raise RuntimeError('Host oracle failed known CRC')
  results.append(dict(mode=mode,iterations=it,crcs=crcs,final_crc=re.search(r'crcfinal\s*:\s*0x([0-9a-f]+)',text)[1],scope='Native unchanged algorithm oracle only. Fixed host timer value is NOT any performance evidence.'))
if (H/'HOST_CRC_ORACLE.json').exists():
 if json.loads((H/'HOST_CRC_ORACLE.json').read_text())!=results:raise RuntimeError('Host oracle identity changed')
else:save(H/'HOST_CRC_ORACLE.json',results)
for stage,timer in [('strict-p0','zero'),('strict-p1','zero'),('timed-p0','clock'),('timed-p1','clock'),('timed32-p1','clock')]:
 for mode in ['performance','validation']:
  native(f'replay-r3-{stage}-{mode}',[H/'replay.exe',P/'build'/mode/'program.bin',P/'runs'/stage/mode,timer],limit=90)
print('Native reference independently matched ten previous full M5 streams and states')
