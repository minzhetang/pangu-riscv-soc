"""Read-only package identity check. Never imports project modules or starts processes."""
from pathlib import Path,PurePosixPath
import argparse,json,hashlib,os,sys
def check(root):
 root=Path(root).resolve();errors=[]
 try:m=json.loads((root/'MANIFEST.json').read_text(encoding='utf8'))
 except Exception as e:return {'status':'FAIL','errors':['manifest: '+type(e).__name__]}
 rows=m.get('files',[]);names=[];fold=set();total=0
 for row in rows:
  name=row.get('path','');q=PurePosixPath(name)
  if not name or q.is_absolute() or any(x in ['..','.'] for x in q.parts) or '\\' in name or ':' in name:
   errors.append('unsafe path: '+name);continue
  if name.casefold() in fold:errors.append('case-insensitive duplicate: '+name)
  fold.add(name.casefold());names.append(name);p=root/name
  try:
   if p.is_symlink() or (getattr(p.lstat(),'st_file_attributes',0)&0x400):raise ValueError('link/reparse point')
   b=p.read_bytes();total+=len(b)
   if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest().upper()!=row['sha256']:errors.append('identity mismatch: '+name)
  except Exception as e:errors.append('missing/unreadable: '+name+' '+type(e).__name__)
 actual=[]
 for base,dirs,files in os.walk(root,followlinks=False):
  for n in dirs:
   p=Path(base)/n
   if p.is_symlink() or getattr(p.lstat(),'st_file_attributes',0)&0x400:errors.append('linked directory: '+p.relative_to(root).as_posix())
  for n in files:actual.append((Path(base)/n).relative_to(root).as_posix())
 expected=set(names)|{'MANIFEST.json','SHA256SUMS.txt'}
 if set(actual)!=expected:errors.append('file coverage differs: extra='+str(sorted(set(actual)-expected)[:8])+' missing='+str(sorted(expected-set(actual))[:8]))
 try:
  listed={}
  for line in (root/'SHA256SUMS.txt').read_text(encoding='utf8').splitlines():
   digest,name=line.split('  ',1)
   if name in listed:errors.append('duplicate SHA entry: '+name)
   listed[name]=digest
  want={r['path']:r['sha256'] for r in rows};want['MANIFEST.json']=hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest().upper()
  if listed!=want:errors.append('SHA listing mismatch')
 except Exception as e:errors.append('SHA format: '+type(e).__name__)
 return {'status':'PASS_MATERIAL_IDENTITY_ONLY' if not errors else 'FAIL','files_checked':len(rows),'bytes_checked':total,'errors':errors,'compile_runs':0,'DUT_runs':0,'PDS_runs':0,'hardware_calls':0,'scope':'File identity/path coverage only; not functionality, buildability, ISA or hardware acceptance'}
def main():
 a=argparse.ArgumentParser();a.add_argument('--root',required=True,type=Path);a.add_argument('--output',type=Path);x=a.parse_args();r=check(x.root)
 if x.output:
  p=x.output.resolve()
  if p==x.root.resolve() or x.root.resolve() in p.parents:raise SystemExit('Output must be outside the read-only package')
  with p.open('x',encoding='utf8') as f:json.dump(r,f,ensure_ascii=False,indent=2)
 print(json.dumps(r,ensure_ascii=False));return 0 if not r['errors'] else 1
if __name__=='__main__':raise SystemExit(main())
