from pathlib import Path,PurePosixPath
import json,hashlib,stat,ast
P=Path('D:/A_FPGA_Comp');B=P/'队员成果接收/B-VERIFY-OFFLINE-M0-return-v02';V=P/'队员成果接收/B-VERIFY-OFFLINE-M0-return-v01';H=P/'work/analysis/2026-10-27-b-offline-r1-review';H.mkdir(exist_ok=True);assert not any(H.iterdir())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
rows=[]
for p in B.rglob('*'):
 st=p.lstat();assert not p.is_symlink() and not getattr(st,'st_file_attributes',0)&0x400,p
 if p.is_file():assert stat.S_ISREG(st.st_mode) and st.st_size<4*1024**2,p;rows.append(dict(path=p.relative_to(B).as_posix(),bytes=st.st_size,SHA256=sha(p),read_status='HASH_ONLY_NOT_YET_REVIEWED'))
manifest=[]
for line in (B/'SHA256SUMS.txt').read_text(encoding='utf-8-sig').splitlines():
 value,name=line.split('  ',1);x=PurePosixPath(name);assert not x.is_absolute() and '..' not in x.parts and ':' not in name and '\\' not in name;assert sha(B/name)==value;manifest.append(name)
assert len(set(manifest))==len(manifest);actual={r['path'] for r in rows};assert actual==set(manifest)|{'SHA256SUMS.txt'}
for name in ['offline_api.py','block_codec.py']:assert sha(B/'frozen'/name)==sha(V/'frozen'/name)
# Fully parse every JSON, Python AST, and text without executing package content.
errors=[]
for row in rows:
 p=B/row['path']
 try:
  if p.suffix=='.json':obj=json.loads(p.read_text(encoding='utf-8-sig'));row['read_status']='FULL_JSON_PARSED';row['top_type']=type(obj).__name__
  elif p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8-sig'));row['read_status']='FULL_AST_PARSED_NOT_EXECUTED'
  else:p.read_text(encoding='utf-8-sig');row['read_status']='FULL_TEXT_READ_NOT_YET_SEMANTIC_REVIEW'
 except Exception as exc:
  if row['path'] in ['logs/R1-INVALID-JSON/case.json','tests/cases/R1-INVALID-JSON.json'] and isinstance(exc,json.JSONDecodeError):row['read_status']='EXPECTED_INVALID_JSON_FULL_BYTES_READ'
  else:row['read_status']='UNREADABLE';errors.append(dict(path=row['path'],error=repr(exc)))
assert not errors,errors
v01=[dict(path=p.relative_to(V).as_posix(),SHA256=sha(p)) for p in V.rglob('*') if p.is_file()]
result=dict(status='INTAKE_IDENTITY_ONLY_NOT_FUNCTIONAL_PASS',root=str(B),files=len(rows),manifest_entries=len(manifest),manifest_SHA256=sha(B/'SHA256SUMS.txt'),bytes=sum(r['bytes'] for r in rows),plan_SHA256=sha(B/'tests/PLAN.json'),frozen_same_v01=True,errors=errors,rows=rows)
(H/'INTAKE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(H/'v01-before.json').write_text(json.dumps(v01,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['files','manifest_entries','manifest_SHA256','bytes','plan_SHA256','frozen_same_v01']},ensure_ascii=False))
