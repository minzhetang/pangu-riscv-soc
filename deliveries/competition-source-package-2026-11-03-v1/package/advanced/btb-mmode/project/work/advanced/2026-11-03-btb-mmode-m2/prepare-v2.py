from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
if (H/'PLAN-v2.json').exists():raise SystemExit('frozen plan exists')
p=json.loads((H/'PLAN.json').read_text());p['version']='2.0.0';p['correction']='Initial BEQ offset 0x1008 exceeds signed 13-bit encoding; preserve original plan/runs, replace with legal +8 at PC0xff8. New target PC0x1000, unchanged manually expected WB/STORE. Not a CPU fix.'
for t in p['tests']:
 if t['name']=='beq_ifmiss':
  t['name']='beq_ifmiss_v2';d=H/'inputs'/t['name'];d.mkdir();src=H/'inputs/beq_ifmiss/program.hex'
  rom=[int(s,16) for s in src.read_text().splitlines()];rom[0xff8//4]=0x00000463
  rom[0x1000//4]=rom[0x2000//4];rom[0x1004//4]=rom[0x2004//4];rom[0x1008//4]=rom[0x2008//4]
  out=d/'program.hex';out.write_text(''.join(f'{v:08x}\n' for v in rom));t['program_sha256']=hashlib.sha256(out.read_bytes()).hexdigest()
  raw=rom[0xff8//4];imm=((raw>>31)<<12)|(((raw>>7)&1)<<11)|(((raw>>25)&63)<<5)|(((raw>>8)&15)<<1)
  if imm!=8:raise RuntimeError('independent B immediate decode failed')
(H/'PLAN-v2.json').write_text(json.dumps(p,indent=2));print(hashlib.sha256((H/'PLAN-v2.json').read_bytes()).hexdigest())
