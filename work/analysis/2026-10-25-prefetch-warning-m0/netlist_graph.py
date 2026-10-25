"""Read-only, restricted structural Verilog reader, not a simulator/synthesizer.
Reject unsupported syntax/widths/unknown primitives. Each combinational cell is
conservatively all-inputs-to-all-outputs; FF/RAM clocked state is a boundary.
No tool/model code is executed. Proprietary models are read for headers only.
"""
from pathlib import Path
import re,json,hashlib,collections,sys
P=Path('D:/A_FPGA_Comp');H=Path(__file__).resolve().parent
LIB=Path('D:/PDS/PDS_2022.2-SP6.4/arch/vendor/pango/verilog/simulation')
TOKEN=re.compile(r'\s+|"(?:\\.|[^"\\])*"|\\[^\s]+|\d+\s*\x27[sS]?[bBoOdDhH][0-9a-fA-F_xXzZ?]+|[A-Za-z_$][\w$]*|\d+|[^\s]')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def clean(s):return re.sub(r'\(\*.*?\*\)|/\*.*?\*/|//[^\n]*','',s,flags=re.S)
def toks(s):return [x for x in TOKEN.findall(clean(s)) if not x.isspace()]
def norm(x):return x[1:] if x.startswith('\\') else x
def block(t,start):
    opening=t[start]; closing={'(':')','[':']','{':'}'}[opening];depth=1;i=start+1
    while depth:
        assert i<len(t),'Unbalanced structural syntax'
        if t[i]==opening:depth+=1
        elif t[i]==closing:depth-=1
        i+=1
    return t[start+1:i-1],i
def split(t,delimiter=','):
    out=[];last=0;stack=[]
    for i,x in enumerate(t):
        if x in ['(','[','{']:stack.append(x)
        elif x in [')',']','}']:assert stack.pop()=={')':'(',']':'[','}':'{'}[x]
        elif x==delimiter and not stack:out.append(t[last:i]);last=i+1
    out.append(t[last:]);return out
def declarations(t):
    out={};direct=None;width=None
    for part in split(t):
        if part[0] in ['input','output','inout','wire','tri','tri1']:
            direct=part.pop(0);width=None
        while part and part[0] in ['wire','reg','signed','unsigned']:part.pop(0)
        if part and part[0]=='[':
            q,i=block(part,0); assert len(q)==3 and q[1]==':',q
            width=(int(q[0]),int(q[2]));part=part[i:]
        assert len(part)==1,(direct,part)
        out[norm(part[0])]=(direct,width)
    return out
def named(t):
    out={}
    for part in split(t):
        assert part[:1]==['.'] and part[2]=='(',part[:5]
        inner,i=block(part,2);assert i==len(part)
        name=norm(part[1]);assert name not in out;out[name]=inner
    return out
def module_header(t,i):
    assert t[i]=='module';name=norm(t[i+1]);i+=2
    if t[i]=='#':_,i=block(t,i+1)
    ports,i=block(t,i);assert t[i]==';'
    return name,declarations(ports),i+1
def parse(path):
    t=toks(path.read_text(encoding='utf-8-sig'));i=0;mods={};inst_total=0
    while i<len(t):
        name,ports,i=module_header(t,i);decl=dict(ports);inst=[]
        while t[i]!='endmodule':
            j=t.index(';',i);s=t[i:j];i=j+1
            if s[0] in ['wire','input','output','inout','tri','tri1']:
                for key,v in declarations(s).items():
                    if key in decl:assert decl[key][1]==v[1]
                    else:decl[key]=v
                continue
            typ=norm(s[0]);k=1;params={}
            if s[k]=='#': q,k=block(s,k+1);params=named(q)
            instance=norm(s[k]);k+=1
            assert s[k]=='(',(name,s[:5]);q,k=block(s,k);assert k==len(s)
            inst.append(dict(type=typ,name=instance,params=params,ports=named(q)));inst_total+=1
        i+=1;assert name not in mods
        mods[name]=dict(ports=ports,decl=decl,instances=inst)
    return mods,inst_total
def bitnames(name,width):
    if width is None:return [name]
    a,b=width;return [name+'['+str(i)+']' for i in range(a,b+(1 if a<=b else -1),1 if a<=b else -1)]
def expression(t,decl,wires):
    if not t:return []
    if t[0]=='{':
        inner,i=block(t,0);assert i==len(t)
        if len(inner)>1 and inner[0].isdigit() and inner[1]=='{':
            q,j=block(inner,1);assert j==len(inner)
            return expression(q,decl,wires)*int(inner[0])
        return [v for part in split(inner) for v in expression(part,decl,wires)]
    if len(t)==1 and "'" in t[0]:
        width=int(t[0].split("'",1)[0]);return [None]*width
    if len(t)==1 and t[0].isdigit():return [None]*32
    n=norm(t[0]);assert n in decl,('unknown net',n)
    bits=bitnames(n,decl[n][1]);resolved=[wires.get(b,b) for b in bits]
    if len(t)>1:
        assert t[1]=='[';q,j=block(t,1);assert j==len(t)
        idx=[int(q[0])] if len(q)==1 else list(range(int(q[0]),int(q[2])+(1 if int(q[0])<=int(q[2]) else -1),1 if int(q[0])<=int(q[2]) else -1))
        resolved=[wires.get(n+'['+str(i)+']',n+'['+str(i)+']') for i in idx]
        assert all(n+'['+str(i)+']' in bits for i in idx)
    return resolved
def primitive_header(typ):
    path=LIB/(typ+'.v');assert path.is_file(),typ
    t=toks(path.read_text(encoding='utf-8-sig'));i=t.index('module');name,ports,j=module_header(t,i);assert name==typ
    assert all(v[0] in ['input','output'] for v in ports.values())
    return ports,dict(path=str(path),SHA256=sha(path),ports={k:dict(direction=d,width=len(bitnames(k,w))) for k,(d,w) in ports.items()})
def topo(graph):
    deg={n:0 for n in graph}
    for nexts in graph.values():
        for x in nexts:deg[x]=deg.get(x,0)+1
    todo=collections.deque(sorted(n for n,d in deg.items() if d==0));visited=0
    while todo:
        n=todo.popleft();visited+=1
        for x in graph.get(n,[]):
            deg[x]-=1
            if deg[x]==0:todo.append(x)
    return dict(nodes=len(deg),edges=sum(len(s) for s in graph.values()),visited=visited,acyclic=visited==len(deg),residual_nodes=[n for n,d in deg.items() if d>0])
def analyze(path,precision=False,constrained=False):
    mods,count=parse(path);headers={};evidence={};leaf=[];hier=[];pin_count=0
    def flatten(name,prefix,aliases):
        nonlocal pin_count
        m=mods[name];wires={b:prefix+b for n,(_,width) in m['decl'].items() for b in bitnames(n,width)};wires.update(aliases)
        for inst in m['instances']:
            typ=inst['type'];full=prefix+inst['name']; actual={p:expression(e,m['decl'],wires) for p,e in inst['ports'].items()}
            if typ in mods:
                formal=mods[typ]['ports'];assert set(actual)==set(formal),(name,typ,set(formal)-set(actual))
                mapping={}
                for p,(_,width) in formal.items():
                    b=bitnames(p,width);assert len(b)==len(actual[p]),(name,typ,p,len(b),len(actual[p]))
                    mapping.update(zip(b,actual[p]))
                hier.append(dict(type=typ,path=full));flatten(typ,full+'/',mapping)
            else:
                if typ not in headers:headers[typ],evidence[typ]=primitive_header(typ)
                assert set(actual)<=set(headers[typ]),(typ,set(actual)-set(headers[typ]))
                for p,bits in actual.items():
                    assert not bits or len(bits)==len(bitnames(p,headers[typ][p][1])),(typ,p,len(bits))
                inputs=[b for p,bs in actual.items() if headers[typ][p][0]=='input' for b in bs if b is not None]
                outputs=[b for p,bs in actual.items() if headers[typ][p][0]=='output' for b in bs if b is not None]
                fixed={p:int(e[0][-1]) for p,e in inst['ports'].items() if len(e)==1 and e[0] in ["1'b0","1'b1"]}
                pin_count+=sum(len(x) for x in actual.values());leaf.append(dict(type=typ,path=full,inputs=inputs,outputs=outputs,ports=actual,params=inst['params'],fixed_inputs=fixed))
    flatten('board_top','',{})
    graph=collections.defaultdict(set);async_graph=collections.defaultdict(set)
    seq=[];comb=[]
    for c in leaf:
        typ=c['type'];is_seq=typ.startswith('GTP_DFF') or typ=='GTP_DRM18K_E1'
        if is_seq:
            seq.append(c)
            # Additional asynchronous FF C/P/R/S -> Q arcs, not data/CE/clock arcs.
            if typ.startswith('GTP_DFF'):
                for p,bs in c['ports'].items():
                    if p in ['C','P','R','S']:
                        for i in bs:
                            if i is not None:async_graph[i].update(c['outputs'])
        else:
            assert typ.startswith('GTP_LUT') or typ.startswith('GTP_MUX2LUT') or typ in ['GTP_INV','GTP_GRS','GTP_INBUF','GTP_OUTBUF','GTP_CLKBUFG'],typ
            comb.append(c)
            if precision:
                import cell_arcs
                ins=[p for p in c['ports'] if headers[typ][p][0]=='input']
                for output,bits in c['ports'].items():
                    if headers[typ][output][0]!='output' or not bits:continue
                    deps=cell_arcs.dependencies(typ,c['params'],ins,output,c['fixed_inputs'] if constrained else {})
                    for inp in deps:
                        for i in c['ports'][inp]:
                            if i is not None:graph[i].update(b for b in bits if b is not None);async_graph[i].update(b for b in bits if b is not None)
            else:
                for i in c['inputs']:graph[i].update(c['outputs']);async_graph[i].update(c['outputs'])
    t=topo(graph);a=topo(async_graph)
    # Summaries only; graph detail is local and carries no vendor model source.
    return dict(path=str(path),SHA256=sha(path),modules=len(mods),parsed_instances=count,hierarchy_instances=len(hier),flattened_primitives=len(leaf),port_bits_parsed=pin_count,types=dict(collections.Counter(c['type'] for c in leaf)),sequential_cells=len(seq),combinational_cells=len(comb),graph=t,with_async_FF_control_arcs=a,library=evidence,feature_primitives=[dict(path=c['path'],type=c['type'],outputs=c['outputs']) for c in leaf if 'fetch_redirect' in c['path']],precision='INIT sensitivity and direct tied constants' if constrained else ('INIT Boolean input sensitivity' if precision else 'all-inputs to all-outputs overapproximation'),limitations=['Post-synthesis only, not inaccessible sdm2adm constant-probe internal graph','All FF/data/enable/clock and synchronous DRM paths are state boundaries; implicit global GRS not a full reset/CDC proof','Only direct literal ties constrained; unresolved constant aliases conservatively left free; no cell-internal/physical defect proof','No post-route connectivity proof; exported PNR lists omit pin-to-net bindings'],all_statements_parsed=True,unsupported_syntax_skipped=0)
def selftest():
    assert topo({'a':{'b'},'b':{'c'}})['acyclic']
    assert not topo({'a':{'b'},'b':{'a'}})['acyclic']
    assert not topo({'a':{'a'}})['acyclic']
    assert topo({'q':{'d'}})['acyclic'] # no d->q arc across FF
    assert expression(['{',"1'b0",',','b','[','1',':','0',']','}'],{'b':('wire',(3,0))},{'b[1]':'parent/bit1','b[0]':'parent/bit0'})==[None,'parent/bit1','parent/bit0']
    assert norm('\\n[3]')=='n[3]'
    return dict(status='PASS',synthetic_graph_positive_negative=4,expression_alias_concat=1,escaped_identifier=1,new_DUT_runs=0)
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(selftest()))
    name=sys.argv[1];target=P/'work/fpga'/name/'pds/synthesize/board_top_syn.vm'
    constrained=len(sys.argv)>2 and sys.argv[2]=='constrained'
    precision=constrained or (len(sys.argv)>2 and sys.argv[2]=='precise')
    if precision:
        import cell_arcs;print(json.dumps(cell_arcs.selftest()))
    result=analyze(target,precision,constrained)
    with (H/(name+('-graph-constrained.json' if constrained else ('-graph-precise.json' if precision else '-graph.json')))).open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({k:result[k] for k in ['modules','flattened_primitives','types','graph','with_async_FF_control_arcs']},ensure_ascii=False))
