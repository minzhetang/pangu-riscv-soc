"""Read-only final delta review; no received entrypoints/binaries executed."""
from pathlib import Path,PurePosixPath
import hashlib,json,re,sys,ast,collections,importlib.util
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
P=Path('D:/A_FPGA_Comp');H=Path(__file__).resolve().parent
OUTER=P/'队员成果接收/handoff-mainline-v02-20261025'
E=OUTER/'artifacts/stage-return-final-20261027-v02'
OLD=P/'队员成果接收/increment-20261024-2335'
SPEC=importlib.util.spec_from_file_location('previous_owned_intake',P/'reports/progress/evidence/2026-10-25-increment-2335-alignment/intake.py')
PREV=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(PREV)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,o):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def canonical(rel):
    return rel.removeprefix('work/B-RETURN/stage-return-final-20261027-v02/')
def resolve(rel):
    q=PurePosixPath(rel.replace('\\','/'));assert not q.is_absolute() and '..' not in q.parts and ':' not in str(q)
    rel=canonical(str(q))
    if rel.startswith('work/B-RETURN/stage-return-final-20261027-v01/'):
        return P/'队员成果接收/stage-return-final-20261027-v01'/rel.removeprefix('work/B-RETURN/stage-return-final-20261027-v01/')
    m=re.match(r'work/B-RETURN/([^/]+)/(.+)',rel)
    if m and m[1]=='mainline-increment-2335-response-2026-10-25-v1':return P/'deliveries'/m[1]/m[2]
    if (E/rel).is_file():return E/rel
    return PREV.resolve(rel)
def mark(rel,kind,detail):
    p=H/'coverage.json';o=read(p) if p.exists() else {}
    r=o.setdefault(rel,dict(SHA256=sha(E/rel),actions=[]));assert r['SHA256']==sha(E/rel)
    r['actions'].append(dict(kind=kind,detail=detail));p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def init():
    files=[]
    for p in sorted(E.rglob('*')):
        assert not p.is_symlink() and not getattr(p.lstat(),'st_file_attributes',0)&0x400
        if not p.is_file():continue
        rel=p.relative_to(E).as_posix();files.append(dict(path=rel,bytes=p.stat().st_size,SHA256=sha(p)))
        mark(rel,'HASH_ONLY','inventory')
    assert len(files)==70
    sums=(E/'SHA256SUMS.txt').read_text(encoding='utf-8-sig').splitlines();assert len(sums)==69
    for line in sums:
        digest,rel=line.split(None,1);rel=rel.lstrip('*');assert sha(resolve(rel))==digest.upper()
    assert {l.split(None,1)[1].lstrip('*') for l in sums}=={r['path'] for r in files if r['path']!='SHA256SUMS.txt'}
    changes=read(E/'CHANGED_FILES.json')['files'];checks=[]
    for row in changes:
        path=canonical(row['path']);actual_sha=sha(E/path)
        before=PREV.resolve(path) if row['old_sha256'] else None
        if before:assert sha(before)==row['old_sha256']
        checks.append(dict(path=path,old=str(before) if before else None,new=str(E/path),SHA256=actual_sha,declared_SHA256=row['new_sha256'],new_SHA_match=actual_sha==row['new_sha256']))
    source=read(E/'SOURCE_INDEX.json')['entries']
    for row in source:assert sha(E/canonical(row['path']))==row['new_sha256']
    deps=read(E/'DEPENDENCIES.json')['entries'];actual=[]
    for d in deps:
        p=resolve(d['path']);assert sha(p)==d['sha256'];actual.append(dict(**d,actual=str(p)))
    save(H/'protected.json',dict(files=files,dependencies=actual,changes=checks))
    save(H/'intake.json',dict(files=70,bytes=sum(x['bytes'] for x in files),manifest=69,manifest_SHA256=sha(E/'SHA256SUMS.txt'),changed=len(changes),changed_SHA_mismatches=[c for c in checks if not c['new_SHA_match']],old_values=sum(bool(x['old_sha256']) for x in changes),source_index=len(source),dependencies=len(actual),ZIP_present=False,new_DUT=0))
    for rel in ['SHA256SUMS.txt','CHANGED_FILES.json','SOURCE_INDEX.json','DEPENDENCIES.json']:mark(rel,'FULL_PARSE','all paths/version/SHA/old values resolved')
    print(json.dumps(read(H/'intake.json')))
def structured():
    def leaves(o):
        if isinstance(o,dict):return sum(leaves(v) for v in o.values())
        if isinstance(o,list):return sum(leaves(v) for v in o)
        return 1
    js=[];logs=[]
    for p in sorted(E.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(E).as_posix()
        if p.suffix=='.json':
            o=read(p);js.append(dict(path=rel,leaves=leaves(o),keys=list(o) if isinstance(o,dict) else None));mark(rel,'FULL_PARSE',dict(all_fields=True,leaves=leaves(o)))
        elif p.suffix=='.log':
            lines=p.read_text(encoding='utf-8-sig').splitlines();tokens=[]
            for line in lines:
                if not re.match(r'^(RX_LEDGER_ACT|RX_NEG_|REGIF_REQ|REGIF_TX_EVENT|REGIF_GPIO_EVENT|TX_EVT|GPIO_EVT|RX_SHARED)',line):tokens.append(line)
            logs.append(dict(path=rel,lines=len(lines),markers=tokens));mark(rel,'FULL_PARSE','all lines/records read, semantic correlation pending')
        elif p.suffix=='.sha256':
            content=p.read_text(encoding='utf-8-sig');target=p.with_suffix('.json');assert sha(target) in content.upper();mark(rel,'FULL_PARSE','frozen plan SHA matches')
    save(H/'structured.json',js);save(H/'logs.json',logs)
    print(json.dumps(dict(json=len(js),logs=len(logs),lines=sum(x['lines'] for x in logs))))
def chunk(rel,start=1,count=140):
    p=E/rel;lines=p.read_text(encoding='utf-8-sig').splitlines();end=min(len(lines),start+count-1)
    print('FILE',rel,'LINES',len(lines),'READ',start,end)
    print('\n'.join(f'{i+1}: {l}' for i,l in enumerate(lines[start-1:end],start-1)))
    mark(rel,'READ_RANGE',dict(start=start,end=end,total=len(lines)))
def diff():
    lines=(E/'DIFF.patch').read_text(encoding='utf-8-sig').splitlines(keepends=True);i=0;rows=[];chunks=[]
    while i<len(lines):
        if not lines[i].startswith('--- '):i+=1;continue
        old=lines[i][4:].strip();new=lines[i+1][4:].strip();i+=2
        rel=re.sub(r'^(?:a|b)/','',new);rel=rel.removeprefix('final/')
        # Actual labels are checked below against the CHANGED_FILES paths.
        candidates=[r for r in read(H/'protected.json')['changes'] if new.endswith(r['path'])]
        assert len(candidates)==1,(old,new);c=candidates[0];rel=c['path']
        before=Path(c['old']).read_text(encoding='utf-8-sig').splitlines(keepends=True) if c['old'] else []
        out=[];pos=0;hunks=[];context_errors=[]
        while i<len(lines) and not lines[i].startswith(('--- ','diff --git ')):
            if not lines[i].startswith('@@ '):i+=1;continue
            m=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',lines[i]);assert m
            start=max(0,int(m[1])-1);out.extend(before[pos:start]);pos=start;block=[lines[i]];i+=1
            while i<len(lines) and not lines[i].startswith(('@@ ','--- ','diff --git ')):
                l=lines[i];i+=1
                if l.startswith('\\ No newline'):continue
                if not l.strip() and l[0] not in ' +-':continue
                assert l[0] in ' +-',(rel,i,repr(l))
                if l[0] in ' -':
                    if pos>=len(before) or before[pos].rstrip('\r\n')!=l[1:].rstrip('\r\n'):context_errors.append(dict(line=pos+1,declared=l[1:].rstrip(),actual=before[pos].rstrip() if pos<len(before) else None))
                    pos+=1
                if l[0] in ' +':out.append(l[1:])
                block.append(l)
            hunks.append(''.join(block))
        out.extend(before[pos:]);exact=''.join(out).splitlines()==(E/rel).read_text(encoding='utf-8-sig').splitlines()
        rows.append(dict(path=rel,hunks=len(hunks),exact_reconstruction=exact,old_context_errors=context_errors))
        if Path(rel).suffix in ['.py','.sv']:chunks.append(dict(path=rel,hunks=hunks))
    save(H/'diff.json',rows);save(H/'code-diff.json',chunks);mark('DIFF.patch','FULL_PARSE',dict(files=len(rows),hunks=sum(x['hunks'] for x in rows),exact_reconstruction=all(x['exact_reconstruction'] for x in rows)))
    print(json.dumps(dict(files=len(rows),hunks=sum(x['hunks'] for x in rows),code_files=len(chunks))))
if __name__=='__main__':
    if sys.argv[1]=='chunk':chunk(sys.argv[2],*[int(x) for x in sys.argv[3:]])
    else:dict(init=init,structured=structured,diff=diff)[sys.argv[1]]()
