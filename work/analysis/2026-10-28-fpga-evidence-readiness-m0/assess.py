from pathlib import Path
import hashlib,json,math,re,sys,time
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
P=Path('D:/A_FPGA_Comp');H=Path(__file__).resolve().parent
S=P/'work/fpga/2026-10-27-coremark-longrun-ready-m2'
B=P/'work/fpga/2026-10-27-board-coremark8-bitstream-m1'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest().upper()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,v):
    with (H/n).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
start=time.monotonic()
summary=read(B/'SUMMARY.json');sources=read(B/'SOURCE_RECEIPTS.json')['functional_RTL']
assert len(sources)==13
rows=[]
for row in sources:
    for root in [S/'source',B/'source',B/'source-before']:
        p=root/row['name'];digest=sha(p);assert digest==row['SHA256'];rows.append(dict(path=str(p),SHA256=digest))
bit=Path(summary['bitstream']['path']);assert sha(bit)==summary['bitstream']['SHA256']
rows.append(dict(path=str(bit),SHA256=sha(bit)))
for row in read(H/'PDF_INDEX.json'):
    p=Path(row['path']);assert sha(p)==row['SHA256'];rows.append(dict(path=str(p),SHA256=row['SHA256']))
remote=H/'remote_lab_developer_manual.pdf'
assert sha(remote)=='05FE830148F5638E0A6986938BE06DA916E700F283B28BA9ECA253A82620FDD0'
rows.append(dict(path=str(remote),SHA256=sha(remote)))
for name in ['pds/clock_27mhz.fdc','pds/board_pins.fdc']:
    p=B/name;rows.append(dict(path=str(p),SHA256=sha(p)))
save('INPUTS.json',dict(date_client='2026-10-28',base_commit='18a1e22388a0e4b64255f7e14f11c71fb9de69a0',files=rows,scope='read-only existing source/bitstream/documents; no new compilation/DUT/PDS/hardware'))
save('BASELINE_CHECK.json',dict(functional_source13_matches_F163_and_F160=True,bitstream=dict(path=str(bit),bytes=bit.stat().st_size,SHA256=sha(bit)),new_PDS=0,new_DUT=0,new_sim_compile=0,new_C=0,hardware='STOPPED',license='LAST_CHECKOUT_2026-10-27_PROMPT_7_DAYS_NOT_RECHECKED_TODAY'))
spec=[('soc.cpu_core.id_pc',32,'cpu.v'),('soc.cpu_core.id_valid',1,'cpu.v'),('soc.cpu_core.pipeline_advance',1,'cpu.v'),('soc.cpu_core.eei_hold',1,'cpu.v'),('soc.cpu_core.stall_if',1,'cpu.v'),('soc.cpu_core.flush_if',1,'cpu.v'),('soc.cpu_core.branch_taken',1,'cpu.v'),('sys_rst_n',1,'board_top.sv'),('soc.timer_ticks[31:0]',32,'soc_top.sv'),('soc.address',32,'soc_top.sv'),('soc.wren',1,'soc_top.sv'),('soc.wdata',32,'soc_top.sv'),('soc.stopped',1,'soc_top.sv'),('soc.stop_kind',2,'soc_top.sv'),('soc.write_error',1,'soc_top.sv')]
vm=(B/'pds/synthesize/board_top_syn.vm').read_text(encoding='utf-8-sig')
probes=[]
for expr,width,src in spec:
    token=expr.split('.')[-1].split('[')[0];lines=(S/'source'/src).read_text(encoding='utf-8-sig').splitlines()
    line_ids=[i+1 for i,line in enumerate(lines) if re.search(r'\b'+re.escape(token)+r'\b',line)]
    assert line_ids,(expr,src)
    probes.append(dict(logical_signal=expr,width=width,source=src,source_line_refs=line_ids,netlist_lexical_occurrences=len(re.findall(re.escape(token),vm)),lexical_occurrence_is_not_connectable_net_proof=True))
width=sum(x['width'] for x in probes);assert width==140
save('PROBE_PLAN_DRAFT.json',dict(status='TECHNICAL_DRAFT_NOT_IMPLEMENTED_OR_NEW_SCOPE_APPROVAL',probes=probes,logical_width=width,depth=1024,logical_payload_bits=width*1024,DRM36_payload_lower_bound=math.ceil(width*1024/36864),actual_placement_resources='NOT_IMPLEMENTED',logical_sample_clock_Hz=27000000,selectable_clock_net='MUST_RESOLVE_VALID_INTERNAL_CLOCK_IN_INSERTER_NOT_BLIND_TOP_PORT',sample_edge='rising; physical sample phase/delay requires calibration',window_us=1024/27,mode='single window, All Data, no qualification filter or multi-window initially',clock_port='not counted as data',EX_definition='id_valid && pipeline_advance && !eei_hold; not retirement',trigger_ranges=read(P/'work/analysis/2026-10-27-measurement-path-m0-v2/ILA_EVIDENCE_DRAFT.json')['trigger_ranges'],limitations=['Actual insertable net mapping requires new approved PDS scope','Optimized signals may need separately approved nonfunctional preservation metadata','No FIC/debug bitstream/capture exists','No sampled raw result or physical timing calibration','Remote PCIe DMA integration requirements and actual device unknown']))
save('READING_COVERAGE.json',dict(remote_manual=dict(version='1.0',date='2026/1/7',pages=24,text_read=list(range(1,25)),visually_checked=[2,8,11,13,17,23,24],not_claimed='all screenshot details on every page'),inserter=dict(version='1.0',date='2022.07.12',text_extracted_pages=49,visually_checked=[2,7,17,24,26,40,47],relevant_sections=['2.3.6-8','3.4.3','4.1','5.2.13-15']),debugger=dict(version='1.1',date='2023.04.24',text_extracted_pages=107,visually_checked=[2,9,18,38],printed_page_offset=-1,relevant_sections=['1','4.3 File menu','5.4']),initial_stdout_truncation='Relevant adopted pages re-read in complete targeted output; unused selected page text not claimed fully displayed',new_guide_or_thermal_full_review=False,existing_thermal_rules_reused=True))
save('PLATFORM_GATES.json',dict(status='DOCUMENTED_FALLBACK_NOT_OPERATIONALLY_READY',public_manual_internal_Debugger='DOCUMENTED_NOT_REPRODUCED',public_portal='HTTP200_HTML_TITLE_ONLY',remote_model_package_pins_clock='UNKNOWN_CURRENT_INVENTORY',FIC_debug_transport_wrapper='UNKNOWN',UART_raw_and_timer_clock='UNKNOWN',HTTPS_login_fees_quota_slot='UNKNOWN',local_over_temp='OPEN_STOPPED_NO_NEW_REPLY_CHECKED',human_action='Forward four grouped questions; no accounts/uploads/reservation/payment/hardware granted',B='D158 scoped guards independent; no repeat core work; new ETA unknown',deadline='Existing reviewed 2026-11-04 18:00 Asia/Shanghai, not reverified this round',next_implementation='New debug copy and minimal insertion build only after exact platform and specific scope approval'))
assert all(sha(Path(r['path']))==r['SHA256'] for r in rows)
save('POSTFLIGHT.json',dict(status='READONLY_ANALYSIS_COMPLETE',protected_files=len(rows),unchanged=True,analysis_seconds=round(time.monotonic()-start,3),new_PDS=0,new_DUT=0,new_C=0,new_sim_compile=0,hardware='STOPPED',new_accounts=0,uploads=0,external_messages=0,limitations='No hardware readiness or timing/performance approval inferred'))
print(json.dumps(dict(status='READONLY_ANALYSIS_COMPLETE',protected_files=len(rows),probe_width=width,payload_bits=width*1024,hardware='STOPPED')))
