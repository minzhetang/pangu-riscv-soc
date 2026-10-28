from pathlib import Path
import re,json
H=Path(__file__).resolve().parent;P=H.parents[2]
log=(H/'gui-stdout.log').read_text(errors='replace')
block=log.split('A_R4_NETS_BEGIN',1)[1].split('A_R4_NETS_END',1)[0]
nets={n:int(i) for i,n in re.findall(r'^\s*(\d+)\s*:\s*(\S+)\s+\S+',block,re.M)}
probes=json.loads((P/'work/analysis/2026-10-28-fpga-evidence-readiness-m0/PROBE_PLAN_DRAFT.json').read_text())['probes']
source=(H/'source/cpu.v').read_text(encoding='utf-8-sig')
assert 'assign flush_if = control_flush;' in source and 'assign flush_id = control_flush;' in source
rows=[];selected=[]
for p in probes:
 name=p['logical_signal'].replace('soc.cpu_core.','soc/cpu_core/').replace('soc.','soc/').replace('[31:0]','')
 names=[name] if p['width']==1 else [name+'['+str(i)+']' for i in range(p['width'])]
 parts=[];missing=[]
 for n in names:
  candidates=[n]
  if n=='soc/cpu_core/flush_if':candidates.append('soc/cpu_core/flush_id')
  if name in ['soc/stopped','soc/stop_kind','soc/write_error']:candidates.append(n.removeprefix('soc/'))
  match=next((x for x in candidates if x in nets),None)
  if match is None:missing.append(n);continue
  part=dict(logical=n,actual=match,index=nets[match],channel=len(selected));selected.append(part);parts.append(part)
 rows.append(dict(logical=p['logical_signal'],width=p['width'],selected=parts,missing=missing))
result=dict(status='MAPPED_NOT_YET_CONNECTED',net_count=len(nets),width=len(selected),probes=rows,source='this stage new pre/synthesize/board_top_syn.adf after normal process exit and artifact hash verification',alias_proofs=['cpu flush_if/flush_id both direct control_flush','board_top direct connections for soc stopped/stop_kind/write_error'])
with (H/'NET_MAPPING.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
print('native nets',len(nets),'data bits',len(selected))
for r in rows:print(r['logical'],'missing',r['missing'])
assert len(selected)==140 and not any(r['missing'] for r in rows),'Required probe unresolved'
assert 'nt_clk' in nets and 'sys_rst_n' in nets
script='ins_set_net -core 0 -clock -connect {'+str(nets['nt_clk'])+'}\n'
script+='ins_set_net -core 0 -reset -connect {'+str(nets['sys_rst_n'])+'}\n'
script+='ins_set_net -core 0 -trig 0 -connect {'+' '.join(str(x['index']) for x in selected)+'}\n'
script+='ins_core_info -core 0 -trig 0\nins_save {'+H.as_posix()+'/debug.fic}\nputs {A_R4_CONNECTION_SAVED}\n'
with (H/'scripts/gui-connect.tcl').open('x',encoding='utf-8') as f:f.write(script)
print('140-bit connect script prepared, not yet executed')
