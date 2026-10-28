from pathlib import Path
import json,re,hashlib
H=Path(__file__).resolve().parent;P=H.parents[2]
log=(H/'gui-stdout.log').read_text(errors='replace')
assert 'A_R3_NETS_BEGIN' in log and 'A_R3_NETS_END' in log
block=log.split('A_R3_NETS_BEGIN',1)[1].split('A_R3_NETS_END',1)[0]
nets={n:int(i) for i,n in re.findall(r'^\s*(\d+)\s*:\s*(\S+)\s+\S+',block,re.M)}
plan=json.loads((P/'work/analysis/2026-10-28-fpga-evidence-readiness-m0/PROBE_PLAN_DRAFT.json').read_text())['probes']
rows=[];allids=[];channel=0
for p in plan:
 name=p['logical_signal'].replace('soc.cpu_core.','soc/cpu_core/').replace('soc.','soc/').replace('[31:0]','')
 names=[name] if p['width']==1 else [name+'['+str(i)+']' for i in range(p['width'])]
 selected=[];missing=[]
 for n in names:
  candidates=[n]
  if name in ['soc/stopped','soc/stop_kind','soc/write_error']:candidates += [n.removeprefix('soc/')]
  matches=[x for x in candidates if x in nets]
  if not matches:missing.append(n);continue
  actual=matches[0];selected.append(dict(logical=n,actual=actual,index=nets[actual],channel=channel));allids.append(nets[actual]);channel+=1
 rows.append(dict(logical=p['logical_signal'],width=p['width'],selected=selected,missing=missing))
result=dict(actual_net_count=len(nets),expected_width=140,selected_width=channel,probes=rows,alias_proof='board_top connects soc.stopped/stop_kind/write_error directly to same-name board wires; exact F163 source group and comments-only candidates hashed before use',reference_ADF='ins-input/configuration-reference.adf; explicitly R2 synthesis, final new build matching still required')
with (H/'NET_MAPPING.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
print('nets',len(nets),'selected',channel)
for r in rows:print(r['logical'],'missing',r['missing'])
assert channel==140 and not any(r['missing'] for r in rows),'Incomplete probes; no connection or FIC_READY written'
assert 'nt_clk' in nets and 'sys_rst_n' in nets
prefix='D:/A_FPGA_Comp/work/fpga/2026-10-28-local-debug-insert-m1-r3/'
tcl='ins_set_net -core 0 -clock -connect {'+str(nets['nt_clk'])+'}\n'
tcl+='ins_set_net -core 0 -reset -connect {'+str(nets['sys_rst_n'])+'}\n'
tcl+='ins_set_net -core 0 -trig 0 -connect {'+' '.join(map(str,allids))+'}\n'
tcl+='ins_core_info -core 0 -trig 0\n'
tcl+='ins_save '+prefix+'debug.fic\nputs {A_R3_CONNECTION_SAVED}\n'
with (H/'scripts/gui-connect.tcl').open('x',encoding='utf-8') as f:f.write(tcl)
print('Connection script prepared; NOT executed until queued')
