import pathlib,hashlib
R=pathlib.Path(__file__).resolve().parent
s=(R/'baseline.sv').read_text()
s=s.replace('parameter READ_ONLY=0','parameter READ_ONLY=0, parameter ADMISSION=0',1)
s=s.replace(' reg [25:0] saved_tag;',' reg [25:0] saved_tag;\n reg ghost_valid[0:3];reg [25:0] ghost_tag[0:3];')
s=s.replace('begin lru[i]<=0;for','begin ghost_valid[i]<=0;ghost_tag[i]<=0;lru[i]<=0;for')
s=s.replace('if(!bypass && !qaddr[31]) begin\n       maddr', 'if(!bypass && !qaddr[31] && (!ADMISSION || (ghost_valid[si] && ghost_tag[si]==tag))) begin\n       maddr')
s=s.replace('end else begin maddr<=qaddr;mlen<=0;end','''end else begin
       maddr<=qaddr;mlen<=0;
       if(ADMISSION && !bypass && !qaddr[31]) begin ghost_valid[si]<=1;ghost_tag[si]<=tag;end
      end''')
(R/'candidate.sv').write_text(s)
tb=(R/'cache_tb.sv').read_text().replace('request(1,0,1,15,32\'hdeadbeef);while(tx[1]<4)',"i=tx[1];request(1,0,1,15,32'hdeadbeef);while(tx[1]<i+1)")
(R/'execution_tb.sv').write_text(tb)
(R/'PRE_RUN_CORRECTION.md').write_text('''# Pre-run fixture correction
Frozen cache_tb.sv retained. Its inherited MODE1 reset-after-write used absolute
transaction count4, valid only for M0's earlier hit. Admission changes that earlier
hit into a fill. Before any M1 execution, execution_tb.sv changes this one wait to
the current transaction count +1. The requirement (wait for committed write) and
all expected data remain unchanged. Both designs use the SAME corrected fixture.
FROZEN_SHA256.txt stays unchanged; EXECUTION_SHA256.txt freezes this correction,
candidate, baseline, backend and bounded runner before execution.
''')
files=['candidate.sv','baseline.sv','backend.sv','execution_tb.sv','run.py','implement.py','PRE_RUN_CORRECTION.md']
(R/'EXECUTION_SHA256.txt').write_text(''.join(hashlib.sha256((R/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in files))
