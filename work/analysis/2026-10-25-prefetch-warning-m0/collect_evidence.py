"""Preserve bounded read-only evidence; never execute PDS/models or dump headers."""
from pathlib import Path
import json,re,hashlib,collections,sqlite3,zlib,sys
import netlist_graph as n,cell_arcs
P=n.P;H=n.H;OLD=P/'work/fpga/2026-10-25-board-top-m1';NEW=P/'work/fpga/2026-10-25-resolved-target-fetch-m1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def save(name,o):
    if (H/name).exists():
        assert json.loads(read(H/name))==o,name
        return
    with (H/name).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def read(p):return p.read_text(encoding='utf-8-sig')
def witness(root,intermediate):
    p=root/'pds/synthesize/board_top_syn.vm';mods,_=n.parse(p);m=mods['cpu']
    candidates=[i for i in m['instances'] if i['ports'].get('Z')==['mem_load_half','[','15',']']]
    assert len(candidates)==1;target=candidates[0];assert target['type']=='GTP_LUT6D'
    assert target['ports']['I5']==["1'b1"] and target['ports']['Z']==['mem_load_half','[','15',']']
    params=target['params'];six=['I'+str(i) for i in range(6)]
    raw=cell_arcs.dependencies('GTP_LUT6D',params,six,'Z');fixed=cell_arcs.dependencies('GTP_LUT6D',params,six,'Z',{'I5':1})
    assert 'I4' in raw and 'I4' not in fixed and fixed==['I0','I1','I2']
    checks=0
    for x in range(32):
        v={'I'+str(i):(x>>i)&1 for i in range(5)}|{'I5':1}
        assert cell_arcs.value('GTP_LUT6D',params,'Z',v)==(v['I2'] if v['I0'] else v['I1']);checks+=1
    text=read(p).splitlines();positions=[i for i,s in enumerate(text,1) if '.Z (mem_load_half[15])' in s]
    return dict(path=str(p),SHA256=sha(p),module='cpu',instance=target['name'],primitive=target['type'],Z_connection='mem_load_half[15]',Z5_connection=target['ports']['Z5'],I4_connection=target['ports']['I4'],I5_actual="1'b1",Z_line=positions,INIT=target['params']['INIT'],unconstrained_input_sensitivity=raw,actual_tied_input_sensitivity=fixed,independent_mux_equation_checks=checks,conclusion='The graph feedback through I4 to Z disappears with actual I5=1; a shared coarse-analysis false positive, not proof of origin of any PDS warning',new_DUT_runs=0)
def run():
    sys.stdout.reconfigure(encoding='utf-8')
    save('ANALYSIS_SCOPE.json',dict(date_beijing='2026-10-25',decision='D141',authorization='User continued after F146 recommendation: read-only warning analysis',base_git='c92bb98b12deaad52aa0dcc7e16bb747204b6f4f',changes_allowed='new analysis/report/memory only',compiler_runs=0,DUT_runs=0,PDS_runs=0,hardware='STOPPED',candidate_promoted=False))
    source=[]
    for root in [OLD,NEW]:
        for p in sorted((root/'source').iterdir()):
            if p.is_file():source.append(dict(path=str(p),SHA256=sha(p)))
    inventories=[];logs=[]
    for label,root in [('old',OLD),('new',NEW)]:
        for p in sorted((root/'pds').rglob('*')):
            if p.is_file():
                start=p.read_bytes()[:16]
                binary=(b'\0' in start or start.startswith(b'\x1f\x8b') or p.suffix in ['.db','.adf'])
                inventories.append(dict(path=str(p),bytes=p.stat().st_size,SHA256=sha(p),classification='opaque tool database; not decoded' if binary else 'text/source or tool report',contents_not_executed=True))
        f=root/'pds/flow.log';lines=read(f).splitlines();begin=next(i for i,s in enumerate(lines) if s=='Start sdm2adm.');end=next(i for i in range(begin,len(lines)) if lines[i].startswith('Executing : sdm2adm successfully.'))
        block=lines[begin:end+1];assert not any(re.search('hostname|license|hostid',s,re.I) for s in block)
        logs.append(dict(label=label,path=str(f),SHA256=sha(f),first_line=begin+1,last_line=end+1,warning_count=sum('Loop was found during constant probe.' in s for s in block),stage_lines=block))
    assert [x['warning_count'] for x in logs]==[7,8]
    help_rows=[]
    for relative in ['bin/helpDoc_pango.qch','syn/lib/html/synerrmsg.qch','syn/lib/html/fpgahelp.qch']:
        p=Path('D:/PDS/PDS_2022.2-SP6.4')/relative;c=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)
        checks=0;exact=[];general=[];unreadable=[]
        for name,data in c.execute('select n.Name,d.Data from FileNameTable n join FileDataTable d on n.FileId=d.Id'):
            if not re.search(r'\.(html?|txt|xml)$',name,re.I):continue
            try:s=zlib.decompress(data[4:]).decode('utf-8',errors='replace')
            except Exception as e:unreadable.append(dict(path=name,error=type(e).__name__));continue
            checks+=1;plain=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s))
            if re.search('constant.?probe|Loop was found during constant probe',plain,re.I):exact.append(name)
            if re.search(r'combinational\s+(?:loop|cycle)|组合环',plain,re.I):general.append(name)
        c.close();help_rows.append(dict(path=str(p),SHA256=sha(p),text_entries_read=checks,unreadable=unreadable,exact_warning_pages=exact,general_loop_pages=sorted(set(general)),interpretation='Generic Loops/CL179/CL181 material is not an official interpretation of the different sdm2adm warning'))
    graph_names=['2026-10-25-board-top-m1-graph.json','2026-10-25-resolved-target-fetch-m1-graph.json','2026-10-25-resolved-target-fetch-m1-graph-precise.json','2026-10-25-board-top-m1-graph-constrained.json','2026-10-25-resolved-target-fetch-m1-graph-constrained.json']
    graphs={k:json.loads(read(H/k)) for k in graph_names}
    for k,g in graphs.items():
        assert sha(Path(g['path']))==g['SHA256'] and g['all_statements_parsed'] and g['unsupported_syntax_skipped']==0
        if 'constrained' in k:assert g['graph']['acyclic'] and g['with_async_FF_control_arcs']['acyclic']
    witnesses=[witness(OLD,'_N1903'),witness(NEW,'_N1633')]
    save('SHARED_LUT_WITNESS.json',dict(status='CONFIRMED_SHARED_COARSE_FALSE_POSITIVE',cases=witnesses,new_DUT_runs=0))
    save('INPUTS.json',dict(source=source,pds_inventory=inventories,warning_blocks=logs,help=help_rows,web_search=dict(official_domain='pangomicro.com',queries=['"Loop was found during constant probe"','PDS "组合环"'],result='No search results; not evidence of absent errata',downloaded=False),uncovered=['Opaque .db/.adf intermediate graphs cannot be attributed by current read-only text exports','PNR export lists instances/pins/nets but no pin-to-net mapping','No tool execution or complete PDF/help-image content search this phase','No official interpretation of the exact warning obtained']))
    save('ANALYZER_SELFTEST.json',dict(parser=n.selftest(),Boolean=cell_arcs.selftest(),first_strict_parser_halt='GTP_INBUF whitelist missing; official header inspected and INBUF/OUTBUF explicitly supported before accepted graph results',false_positive_preserved=graph_names[:3],DUT_runs=0))
    summary=dict(status='READ_ONLY_NARROWING_COMPLETE_ROOT_CAUSE_OPEN',fact='F147',decisions=['D141','D142'],old_warning_count=7,new_warning_count=8,old_final_netlist=dict(primitives=3821,comb_nodes=4770,comb_edges=12286,acyclic=True),new_final_netlist=dict(primitives=3965,comb_nodes=4939,comb_edges=12966,acyclic=True),both_async_control_graphs_acyclic=True,shared_LUT_false_positive_proven=True,new_feature_FFs=sum(x['type'].startswith('GTP_DFF') for x in graphs[graph_names[-1]]['feature_primitives']),exact_warning_help_hits=sum(len(x['exact_warning_pages']) for x in help_rows),help_text_entries=sum(x['text_entries_read'] for x in help_rows),candidate_promoted=False,stable_baseline='F143 O2',remaining='sdm2adm internal warning attribution and official validity/severity remain unknown',compiler_runs=0,DUT_runs=0,PDS_runs=0,hardware='STOPPED')
    assert summary['new_feature_FFs']==33
    save('SUMMARY.json',summary);print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':run()
