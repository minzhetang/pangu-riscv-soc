import hashlib,json,pathlib
from reference_cache import traces,oracle
R=pathlib.Path(__file__).resolve().parent
def stats(seq,ro,policy):
    resident=[[] for _ in range(4)];ghost=[None]*4;hits=tx=nb=eligible=0
    for a,w,m,d in seq:
        if a%4 or ro and w:continue
        line=a//16;s=line%4;cached=policy!='bypass' and a<0x80000000
        present=cached and line in resident[s]
        if present:resident[s].remove(line);resident[s].append(line)
        if w:
            if m:tx+=1;nb+=m.bit_count()
            continue
        eligible+=int(cached)
        if present:hits+=1;continue
        fill=cached and (policy=='baseline' or ghost[s]==line)
        tx+=1;nb+=16 if fill else 4
        if fill:
            if len(resident[s])==2:resident[s].pop(0)
            resident[s].append(line)
        elif cached:ghost[s]=line
    return dict(hits=hits,transactions=tx,bytes=nb,eligible_reads=eligible)
def main():
    (R/'vectors').mkdir();ex={}
    for ro in [0,1]:
        cases=traces(ro)
        if not ro:
            rows=[]
            for l in (R/'old_vectors/0_lanes_0.txt').read_text().splitlines():rows.append(tuple(int(v,16) for v in l.split()[:4]))
            cases['lanes']=rows
        rd=lambda a:(a,0,0,0)
        cases['twoword']=[rd(i*16+j*4) for i in range(24) for j in range(2)]
        cases['adverse']=[rd((i%2)*64) for i in range(48)]
        cases['pollution']=[rd(a) for i in range(12) for a in [0,0,64,64,128+i*64,0,64]]
        for name,seq in cases.items():
            key=f'{ro}_{name}';rows,base=oracle(seq,ro,False)
            (R/'vectors'/f'{key}.txt').write_text(''.join(' '.join(f'{v:x}' for v in row)+'\n' for row in rows))
            ex[key]={p:stats(seq,ro,p)|dict(requests=len(rows),mmio=base['mmio']) for p in ['baseline','admission','bypass']}
    (R/'EXPECTED.json').write_text(json.dumps(ex,indent=2))
    tb=(R/'cache_tb.sv').read_text().replace(' cache_subsystem_m0 dut(.*);',''' cache_subsystem_m0 dut(.*);
`ifdef ADMISSION_M1
 defparam dut.channel[0].u.ADMISSION=1;
 defparam dut.channel[1].u.ADMISSION=1;
`endif''')
    tb=tb.replace('  end else if(mode==2) begin','''  end else if(mode==3) begin
   reset_all();request(1,0,0,0,0);response(1,32'h36251403,0,2);
   if(nb[1]!=4) $fatal(1,"first-touch bytes");
   reset_all();request(1,0,0,0,0);response(1,32'h36251403,0,1);
   if(nb[1]!=8) $fatal(1,"ghost survived reset");
   request(1,0,0,0,0);response(1,32'h36251403,0,2);
   if(nb[1]!=24 || hits[63:32]!=0) $fatal(1,"second-touch fill");
   request(1,4,0,0,0);response(1,32'h7a695847,0,3);
   if(nb[1]!=24 || hits[63:32]!=1) $fatal(1,"post-fill hit");
   reset_all();request(1,0,0,0,0);response(1,32'h36251403,0,0);
   request(1,0,0,0,0);while(tx[1]<5) @(negedge clk);reset_all();
   repeat(12) @(negedge clk);if(pvalid!=0) $fatal(1,"ghost fill response");
   request(1,0,0,0,0);response(1,32'h36251403,0,2);
   if(hits!=0) $fatal(1,"partial line installed");
   $display("ADMISSION_RESET_PASS");
  end else if(mode==2) begin''')
    (R/'cache_tb.sv').write_text(tb)
    files=[R/'PLAN.md',R/'freeze.py',R/'EXPECTED.json',R/'reference_cache.py',R/'cache_tb.sv',*sorted((R/'vectors').glob('*'))]
    (R/'FROZEN_SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in files))
if __name__=='__main__':main()
