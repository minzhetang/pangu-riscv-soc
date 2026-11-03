import hashlib,pathlib
R=pathlib.Path(__file__).resolve().parent
target=R/'SHA256SUMS.txt'
assert not target.exists(),'Refuse overwrite of frozen delivery'
files=sorted(p for p in R.rglob('*') if p.is_file() and p!=target)
target.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in files))
print('Sealed',len(files),'files;',sum(p.stat().st_size for p in files),'bytes')
