from pathlib import Path
import json
from check_report import check
H=Path(__file__).resolve().parent
def fixture(indices,states,reasons,fault=0,frozen=0):
 h=[2700000,128,20,128,0,1000,1000+2700000*128+244,12800,0,len(indices),0,0,fault,frozen]
 text='REC2 '+''.join(f'{x:08x} ' for x in h)+'\n'
 for i,s,r in zip(indices,states,reasons):text+='E '+''.join(f'{x:08x} ' for x in [1000+(i+1)*2700000+244,i,s,r])+'\n'
 return (text+'END\n').encode()
good=dict(transport_clean=True,end_marker_seen=True)
normal=fixture([2,6,10,14],[1,3,7,0],[0]*4)
timeout=fixture([2,22,30,35],[1,1,0,1],[0,2,1,0],2,1)
for c,b in [('normal',normal),('timeout',timeout),('idle',fixture([],[],[]))]:check(b,c,good)
bad=[('missing',normal.replace(normal.splitlines(keepends=True)[2],b''),'normal',good),('duplicate',normal.replace(b'END\n',normal.splitlines(keepends=True)[-2]+b'END\n'),'normal',good),('truncated',normal[:-2],'normal',good),('trailing',normal+b'X','normal',good),('wrong_state',fixture([2,6,10,14],[1,2,7,0],[0]*4),'normal',good),('timeout_age',fixture([2,21,30,35],[1,1,0,1],[0,2,1,0],2,1),'timeout',good),('uart_error',normal,'normal',dict(transport_clean=False,end_marker_seen=True))]
out=[]
for name,b,c,t in bad:
 try:check(b,c,t)
 except Exception as e:out.append(dict(name=name,rejected=True,reason=str(e)))
 else:raise AssertionError(name)
with (H/'CHECKER_SELFTEST.json').open('x') as f:json.dump(dict(status='PASS_HOST_FIXTURES_ONLY_NOT_DUT',positive=3,negative=out),f,indent=2)
print('3 positive and 7 negative host checker fixtures PASS; no DUT')
