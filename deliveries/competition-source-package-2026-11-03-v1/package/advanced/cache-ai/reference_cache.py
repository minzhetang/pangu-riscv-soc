"""Independent byte-memory golden values + separate architectural cache oracle."""
import json, pathlib, hashlib
ROOT=pathlib.Path(__file__).resolve().parent
def traces(ro):
    def rd(a): return (a,0,0,0)
    cases={"locality":[rd((i%16)*4) for i in range(64)],
           "stream":[rd(i*16) for i in range(32)],
           "conflict":[rd(a) for a in [0,64,0,128,64,128,0]],
           "protocol":[rd(0),rd(0),rd(0x80000ffc),rd(0x80000ffc),rd(0x80000000),rd(0),rd(2), (0,1,15,123)]}
    if not ro:
        cases['bytes']=[rd(0)]+[(0,1,m,0x12345678 ^ (m*0x01010101)) for m in range(16)]+[rd(0),(256,1,5,0xaabbccdd),rd(256),(0x80000000,1,15,0x10203040),rd(0x80000000)]
        # Uncached alias writes do not snoop cached aliases: do NOT read stale alias.
        cases['mixed']=[((i*28)%512, int(i%3==0), (i%15)+1, (i*0x12345)&0xffffffff) for i in range(96)]
    return cases
def oracle(seq,ro,bypass):
    mem=bytearray((i*17+3)&255 for i in range(4096)); mmio=0
    ways=[[] for _ in range(4)]; hits=eligible=tx=nb=0; out=[]
    for a,w,mask,data in seq:
        err=bool(a%4 or (ro and w)); value=0; hit=0
        if not err:
            cacheable=not bypass and not a>>31
            line=a//16; s=line%4
            if not w and cacheable: eligible+=1
            if cacheable and line in ways[s]:
                hit=1; ways[s].remove(line); ways[s].append(line)
            if not w:
                if cacheable and hit: hits+=1
                else:
                    tx+=1; nb+=16 if cacheable else 4
                    if cacheable:
                        if len(ways[s])==2: ways[s].pop(0)
                        ways[s].append(line)
                if a==0x80000ffc: value=mmio; mmio+=1
                else: value=int.from_bytes(mem[a%4096:a%4096+4],'little')
            elif mask:
                tx+=1; nb+=mask.bit_count()
                for b in range(4):
                    if mask>>b&1: mem[a%4096+b]=(data>>(8*b))&255
        out.append([a,w,mask,data,value,int(err)])
    return out,dict(hits=hits,eligible_reads=eligible,transactions=tx,bytes=nb,mmio=mmio)
def generate():
    d=ROOT/'vectors'; d.mkdir(exist_ok=True); summary={}
    for ro in [0,1]:
        for name,seq in traces(ro).items():
            for bypass in [0,1]:
                rows,stats=oracle(seq,ro,bypass); key=f'{ro}_{name}_{bypass}'
                (d/(key+'.txt')).write_text(''.join(' '.join(f'{v:x}' for v in r)+'\n' for r in rows))
                summary[key]=stats|{'requests':len(rows)}
    (d/'expected.json').write_text(json.dumps(summary,indent=2))
    files=[ROOT/'cache_plan.md',ROOT/'reference_cache.py',*sorted(d.glob('*'))]
    (ROOT/'CACHE_FROZEN_SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(ROOT))+'\n' for p in files))
if __name__=='__main__': generate()
