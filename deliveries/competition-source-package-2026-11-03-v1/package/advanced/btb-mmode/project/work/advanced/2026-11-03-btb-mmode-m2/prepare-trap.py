from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
if (H/'PLAN-trap.json').exists():raise SystemExit('frozen plan exists')
base=json.loads((H/'PLAN-v2.json').read_text())['tests'][0];tests=[]
for name,inst,cause,tval,resolve in [('misaligned_jump_ifmiss',0x002002ef,0,0xffa,1),('ebreak_ifmiss',0x00100073,3,0xff8,0)]:
 t=dict(base);t.update(name=name,wb=base['wb'][:-1],stores=[],traps=[[0xff8,cause,tval]],focus_train=0,focus_resolve=resolve,expected_status=[['00000800','3']])
 rom=[int(x,16) for x in (H/'inputs/jal_ifmiss/program.hex').read_text().splitlines()];rom[0xff8//4]=inst
 d=H/'inputs'/name;d.mkdir();p=d/'program.hex';p.write_text(''.join(f'{v:08x}\n' for v in rom));t['program_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();tests.append(t)
p=H/'PLAN-trap.json';p.write_text(json.dumps(dict(version='1.0.0',scope='Exception commit held across a real IF translation miss, older WB must be retained; existing S fixture only',tests=tests),indent=2));print(hashlib.sha256(p.read_bytes()).hexdigest())
