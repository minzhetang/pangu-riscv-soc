import hashlib,json,pathlib,random
from reference_cache import oracle
R=pathlib.Path(__file__).resolve().parent
def stats(seq,ro,policy):
    lines=[[] for _ in range(4)];history=[[] for _ in range(4)];hits=tx=nb=eligible=0
    for a,w,m,d in seq:
        if a%4 or ro and w:continue
        line=a//16;s=line%4;cached=policy!='bypass' and a<0x80000000
        present=cached and line in lines[s]
        if present:lines[s].remove(line);lines[s].append(line)
        if w:
            if m:tx+=1;nb+=m.bit_count()
            continue
        eligible+=int(cached)
        if present:hits+=1;continue
        fill=cached and (policy=='m0' or line in history[s])
        tx+=1;nb+=16 if fill else 4
        if fill:
            if len(lines[s])==2:lines[s].pop(0)
            lines[s].append(line)
        elif cached:
            depth=2 if policy=='m2' else 1
            if len(history[s])==depth:history[s].pop(0)
            history[s].append(line)
    return dict(hits=hits,transactions=tx,bytes=nb,eligible_reads=eligible)
def main():
    for ro in [0,1]:
        rd=lambda a:(a,0,0,0)
        cases={'triple':[rd((i%3)*64) for i in range(48)],
               'fifo':[rd(a) for a in [0,64,128,0,64,0,64,192,256,192,256,0,64]]}
        rng=random.Random(17);cases['seeded']=[(rng.randrange(32)*4,int(not ro and i%3==0),rng.randrange(16),rng.getrandbits(32)) for i in range(64)]
        for name,seq in cases.items():
            rows,_=oracle(seq,ro,False)
            (R/'vectors'/f'{ro}_{name}.txt').write_text(''.join(' '.join(f'{v:x}' for v in row)+'\n' for row in rows))
    ex={}
    for p in sorted((R/'vectors').glob('*.txt')):
        ro=int(p.stem[0]);rows=[[int(v,16) for v in line.split()] for line in p.read_text().splitlines()]
        seq=[tuple(row[:4]) for row in rows]
        fresh,base=oracle(seq,ro,False);assert rows==fresh # inherited golden data unchanged
        ex[p.stem]={policy:stats(seq,ro,policy)|dict(requests=len(rows),mmio=base['mmio']) for policy in ['m0','m1','m2','bypass']}
    (R/'EXPECTED.json').write_text(json.dumps(ex,indent=2))
    tb=(R/'cache_tb.sv').read_text().replace('`endif\n genvar c;', '''`endif
`ifdef TWO_GHOST
 defparam dut.channel[0].u.GHOST_TWO=1;
 defparam dut.channel[1].u.GHOST_TWO=1;
`endif
 genvar c;''')
    tb=tb.replace('  end else if(mode==3) begin','''  end else if(mode==4) begin
   reset_all();
   for(i=0;i<6;i=i+1) begin
    request(1,(i%2)*64,0,0,0);response(1,(i%2)?32'h76655443:32'h36251403,0,i%4);
   end
   if(nb[1]!=40 || tx[1]!=4 || hits[63:32]!=2) $fatal(1,"two ghosts not admitted");
   reset_all();
   request(1,0,0,0,0);response(1,32'h36251403,0,2);
   request(1,64,0,0,0);response(1,32'h76655443,0,3);
   if(nb[1]!=48 || hits!=0) $fatal(1,"ghost slot reset");
   $display("TWO_GHOST_RESET_PASS");
  end else if(mode==3) begin''')
    assert 'defparam dut.channel[0].u.GHOST_TWO=1;' in tb
    (R/'cache_tb.sv').write_text(tb)
    files=[R/'PLAN.md',R/'freeze.py',R/'EXPECTED.json',R/'reference_cache.py',R/'cache_tb.sv',R/'negative.txt',*sorted((R/'vectors').glob('*'))]
    (R/'FROZEN_SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in files))
if __name__=='__main__':main()
