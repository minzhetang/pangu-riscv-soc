from pathlib import Path
import re,json,itertools
H=Path(__file__).resolve().parent
s=(H.parent/'2026-10-28-local-debug-insert-m1-r2/pds/synthesize/board_top_syn.vm').read_text()
s=s.split('module cpu\n',1)[1].split('endmodule',1)[0]
rx=re.compile(r'GTP_LUT(\d)(\w*)\s*(?:/\*.*?\*/\s*)?#\((.*?)\)\s*(\S+)\s*\((.*?)\);',re.S)
found=[];scanned=0
for m in rx.finditer(s):
 width=int(m[1]);p=dict(re.findall(r'\.(\w+)\s*\(([^()]*)\)',m[3]));ports={k:v.strip() for k,v in re.findall(r'\.(\w+)\s*\(([^()]*)\)',m[5])}
 literal=re.fullmatch(r"\s*\d+'b([01_]+)\s*",p.get('INIT',''))
 if not literal:continue
 init=int(literal[1].replace('_',''),2);scanned+=1
 for out,n in [('Z',width),('Z5',5)]:
  if out not in ports:continue
  target={'id_system_kind_reg[0]','id_valid','eei_state_reg[0]'}
  inputs=[ports.get('I'+str(i),'') for i in range(n)]
  if not target.issubset(set(inputs)):continue
  good=True;inverted=True;rows=[]
  for bits in itertools.product([0,1],repeat=n):
   if any(name in ["1'b0","1'b1"] and bit!=int(name[-1]) for name,bit in zip(inputs,bits)):continue
   env=dict(zip(inputs,bits));expect=int(not env['eei_state_reg[0]'] or (not env['id_system_kind_reg[0]'] and env['id_valid']))
   actual=(init>>sum(b<<i for i,b in enumerate(bits)))&1
   good &= actual==expect;inverted &= actual==1-expect
   rows.append(dict(inputs=bits,expected_hold=expect,output=actual))
  if good or inverted:found.append(dict(cell=m[4],output=ports[out],port=out,inverse=bool(inverted),inputs=inputs,INIT=p['INIT'].strip(),truth_rows=rows))
(H/'HOLD_MAPPING_SEARCH.json').write_text(json.dumps(dict(scanned_LUTs=scanned,matches=found,scope='HOST_STATIC_ONLY_NOT_NEW_DUT'),indent=2),encoding='utf-8')
print('Scanned',scanned,'matches',[(x['output'],x['inverse']) for x in found])
