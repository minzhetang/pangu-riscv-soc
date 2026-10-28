from pathlib import Path
import json,re,hashlib
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
gui=json.loads((H/'GUI_RESULT.json').read_text());assert gui['rc']==0 and gui['root_exited']
path=H/'debug.fic';s=path.read_text(encoding='utf-8-sig')
d=dict(line.split('=',1) for line in s.splitlines() if line and not line.startswith('#') and '=' in line)
assert d['Project.unit.dimension']=='1'
assert d['Project.unit<0>.clockChannel']=='nt_clk' and d['Project.unit<0>.clockEdge']=='Rising'
assert d['Project.unit<0>.dataDepth']=='1024' and d['Project.unit<0>.dataEqualsTrigger']=='true'
assert d['Project.unit<0>.enableStorageQualification']=='false' and d['Project.unit<0>.enableMultiWindow']=='false'
assert d['Project.unit<0>.triggerPortCount']=='1' and d['Project.unit<0>.triggerPortWidth<0>']=='140'
mapping=json.loads((H/'NET_MAPPING.json').read_text());assert mapping['width']==140
ordered=[x for p in mapping['probes'] for x in p['selected']]
for row in ordered:assert d['Project.unit<0>.triggerChannel<0><'+str(row['channel'])+'>']==row['actual']
assert len([k for k in d if k.startswith('Project.unit<0>.triggerChannel')])==140
assert d['Project.device.designInputFile'].replace('\\','/')==(H/'pre/synthesize/board_top_syn.adf').as_posix()
vm=(H/'pre/synthesize/board_top_syn.vm').read_text();assert re.search(r'GTP_INBUF.*?\.O\s*\(nt_clk\).*?\.I\s*\(clk\)',vm,re.S)
log=(H/'gui-stdout.log').read_text(errors='replace')
assert 'A_R4_CONNECTION_SAVED' in log and 'ins_set_net -core 0 -reset -connect' in log
result=dict(status='PASS_FULL_140_CONNECTIONS',FIC_SHA256=sha(path),FIC_bytes=path.stat().st_size,ordered_data_bits=140,unit_count=1,clock='nt_clk buffered physical clk',clock_edge='Rising',depth=1024,filter=False,multi_window=False,all_data=True,device_source='PRE PDS set_arch Logos2 PG2L100H/-6/FBG676; GUI target visually matched',requested_reset='sys_rst_n',reset_serialized=False,reset_status='COMMAND_ACCEPTED_BUT_NO_RESET_CHANNEL_IN_SAVED_FIC; GENERATED_CORE_RESET_AUDIT_PENDING',sys_rst_n_observed_data_channel=next(x['channel'] for x in ordered if x['logical']=='sys_rst_n'),native_GUI_exit=0,not_hardware_capture=True)
with (H/'FIC_AUDIT.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result))
