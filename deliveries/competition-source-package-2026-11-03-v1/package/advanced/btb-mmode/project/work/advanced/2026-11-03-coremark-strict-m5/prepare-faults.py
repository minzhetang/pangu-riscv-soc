from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
if (H/'FAULT_PLAN.json').exists():raise SystemExit('frozen')
def c(a,rs,rd=0):return (a<<20)|(rs<<15)|0x1000|(rd<<7)|0x73
cases=[('instruction_access',0x00700293,1,8,1),('load_access',0x22002283,5,0x220,2),('store_access',0x22102023,7,0x220,2),('readonly_csr',c(0xc00,1,5),2,c(0xc00,1,5),0),('unknown_csr',c(0x7ff,1,5),2,c(0x7ff,1,5),0),('illegal_multiply',0x021082b3,2,0x021082b3,0)]
tests=[]
for name,ins,cause,tval,fault in cases:
 rom=[0x13]*1024;rom[:4]=[0x10000093,c(0x305,1),ins,0x20102023];rom[64:67]=[0x04d00593,0x20b02223,0x6f]
 d=H/'inputs'/name;d.mkdir(parents=True);p=d/'program.hex';p.write_text(''.join(f'{v:08x}\n' for v in rom))
 tests.append(dict(name=name,mask=0,fault=fault,wb=[[1,256],[11,77]],stores=[[516,77,15]],traps=[[8,cause,tval]],entry=256,status=['00001800','3'],trap_status=['00001800','3'],enable_pc=4,program_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(H/'FAULT_PLAN.json').write_text(json.dumps(dict(scope='Finite M-mode external access faults and CSR/unsupported-ISA precision; frozen before DUT',tests=tests),indent=2))
