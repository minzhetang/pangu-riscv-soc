from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
if (H/'PLAN-v2.json').exists():raise SystemExit('already frozen')
p=json.loads((H/'PLAN.json').read_text());p['version']='2.0.0';p['correction']='Initial adjacent-enable/disable expectation allowed the next CSR to mask an already enabled pending interrupt. Replaced before new runs using privileged ISA immediate-after-CSR evaluation rule; preserve original plan and results, do not count old case as acceptance.'
t=next(t for t in p['tests'] if t['name']=='disable_adjacent_pending')
rom=[int(x,16) for x in (H/'inputs'/t['name']/'program.hex').read_text().splitlines()]
t.update(name='adjacent_disable_precise',wb=t['wb'][:-1]+[[10,28],[11,7],[4,91]],stores=[[516,7,15],[512,91,15]],traps=[[28,0x80000007,0]],entry=284)
rom[71:75]=[0x34102573,0x00700593,0x20b02223,0x30200073]
d=H/'inputs'/t['name'];d.mkdir();out=d/'program.hex';out.write_text(''.join(f'{v:08x}\n' for v in rom));t['program_sha256']=hashlib.sha256(out.read_bytes()).hexdigest()
(H/'PLAN-v2.json').write_text(json.dumps(p,indent=2));print(hashlib.sha256((H/'PLAN-v2.json').read_bytes()).hexdigest())
