"""Read-only installed Inserter/interface preflight; never launch vendor tools."""
from pathlib import Path
import hashlib,json,re,sqlite3,zlib,sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
P=Path('D:/A_FPGA_Comp');H=Path(__file__).resolve().parent
V=Path('D:/PDS/PDS_2022.2-SP6.4');B=P/'work/fpga/2026-10-27-board-coremark8-bitstream-m1'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest().upper()
def save(n,o):
    with (H/n).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
paths=[V/'bin/cdt_ins.exe',V/'bin/pds_shell.exe',V/'bin/helpDoc_pango.qch',B/'pds/synthesize/board_top_syn.adf',B/'pds/synthesize/board_top_syn.vm',B/'SUMMARY.json',B/'FROZEN_INPUTS.json']
examples=[V/'example/PG2L100H_adc_test/pnr/adc_ctrl_demo_syn.fic',V/'example/PG2L100H_lvds4to1/pnr/pgd_ddr_lvds4to1_top_syn.fic',V/'example/PGL25G_lvds8to1/pnr/lvds8to1_debug.fic']
paths+=examples
pins=[dict(path=str(p),bytes=p.stat().st_size,SHA256=sha(p)) for p in paths]
save('INPUTS.json',dict(files=pins,scope='read-only installed binary/help and historical examples; not native process or license query'))
b=(V/'bin/cdt_ins.exe').read_bytes();strings=set(re.findall(rb'[\x20-\x7e]{3,}',b))
flags={x:x.encode() in strings for x in ['-batch','-version','ins_set_file','ins_list_nets','ins_set_net','ins_save']}
# Presence in the binary is only a static interface clue, not validated invocation syntax.
example_rows=[]
for p in examples:
    text=p.read_text(encoding='utf-8-sig');fields={}
    for line in text.splitlines():
        if not line.strip() or line.startswith('#'):continue
        k,sep,v=line.partition('=')
        if sep:
            if k in fields:raise ValueError('DUPLICATE_FIC_KEY')
            fields[k]=v
    selected={k:v for k,v in fields.items() if k in ['Project.device.deviceFamily','Project.device.deviceModel','Project.device.devicePackage','Project.device.deviceSpeedGrade','Project.unit.dimension','Project.unit<0>.dataDepth','Project.unit<0>.dataEqualsTrigger','Project.unit<0>.clockChannel','Project.unit<0>.triggerPortCount']}
    channel_keys=[k for k in fields if re.fullmatch(r'Project\.unit<\d+>\.(?:triggerChannel<\d+><\d+>|dataChannel<\d+>)',k)]
    example_rows.append(dict(path=str(p),fields=selected,serialized_channel_entries=len(channel_keys),input_path_exists=(Path(fields.get('Project.device.designInputFile',''))).is_file(),historical_example_not_active_project=True))
db=sqlite3.connect((V/'bin/helpDoc_pango.qch').as_uri()+'?mode=ro',uri=True)
html_count=0;official=[]
for name,title,blob in db.execute('SELECT n.Name,n.Title,d.Data FROM FileNameTable n JOIN FileDataTable d ON n.FileId=d.Id'):
    if not name.lower().endswith(('.html','.htm')):continue
    html_count+=1
    if name!='Fabric_Inserter_User_Guide.htm':continue
    text=re.sub('<[^>]+>',' ',zlib.decompress(blob[4:]).decode('utf-8','replace'))
    official.append(dict(name=name,has_set_file='ins_set_file' in text,has_list_nets='ins_list_nets' in text,net_selection_uses_indices='序号为参数' in text,GUI_free_startup_syntax_documented='-batch' in text,full_text_not_redistributed=True))
db.close()
save('PREFLIGHT.json',dict(status='STATIC_READY_RUNTIME_INTERFACE_UNVERIFIED',executable_flags_static=flags,help_html_entries_considered=html_count,official_help=official,examples=example_rows,existing_ADF_present=True,batch_command_line_syntax='NOT_EXECUTED_OR_VERIFIED',old_examples_speed_not_target_scope=True,new_fic=0,native_invocations=0,new_PDS=0,new_DUT=0,GUI=0,hardware='STOPPED',next='bounded native interface and isolated debug insertion scope approval; no external consultation prerequisite'))
assert all(sha(Path(r['path']))==r['SHA256'] for r in pins)
save('POSTFLIGHT.json',dict(protected_inputs=len(pins),unchanged=True,new_native=0,new_PDS=0,new_DUT=0,hardware='STOPPED'))
print(json.dumps(dict(status='STATIC_READY_RUNTIME_INTERFACE_UNVERIFIED',inputs=len(pins),examples=len(examples),static_flags=flags,new_native=0,hardware='STOPPED')))
