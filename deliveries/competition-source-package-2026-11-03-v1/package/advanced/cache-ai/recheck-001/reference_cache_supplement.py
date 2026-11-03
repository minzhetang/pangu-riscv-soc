import hashlib,json
from reference_cache import ROOT,oracle
def generate():
    seq=[(0,0,0,0)]
    for m in range(16):
        seq += [(0,1,m,0xfedcba98 ^ (m*0x1020304)),(0,0,0,0)]
        a=256+m*16
        seq += [(a,1,m,0x89abcdef ^ (m*0x03020100)),(a,0,0,0)]
    ex={}
    for bp in [0,1]:
        rows,stats=oracle(seq,0,bp);key=f'0_lanes_{bp}'
        (ROOT/'vectors'/f'{key}.txt').write_text(''.join(' '.join(f'{v:x}' for v in r)+'\n' for r in rows))
        ex[key]=stats|{'requests':len(rows)}
    (ROOT/'vectors/supplement.json').write_text(json.dumps(ex,indent=2))
    lines=(ROOT/'vectors/0_lanes_0.txt').read_text().splitlines();r=lines[0].split();r[4]='0';lines[0]=' '.join(r)
    (ROOT/'vectors/negative.txt').write_text('\n'.join(lines)+'\n')
    files=[ROOT/'cache_supplement_plan.md',ROOT/'reference_cache_supplement.py',ROOT/'vectors/supplement.json',ROOT/'vectors/negative.txt',*ROOT.glob('vectors/*lanes*.txt')]
    (ROOT/'CACHE_SUPPLEMENT_SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT))+'\n' for p in files))
if __name__=='__main__':generate()
