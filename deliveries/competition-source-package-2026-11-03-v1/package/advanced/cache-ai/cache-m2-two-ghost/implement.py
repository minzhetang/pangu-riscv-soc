import pathlib,hashlib
R=pathlib.Path(__file__).resolve().parent
s=(R/'m1.sv').read_text().replace('parameter ADMISSION=0','parameter ADMISSION=0, parameter GHOST_TWO=0',1)
s=s.replace(' reg ghost_valid[0:3];reg [25:0] ghost_tag[0:3];',''' reg ghost_valid[0:3];reg [25:0] ghost_tag[0:3];
 reg ghost_valid_b[0:3];reg [25:0] ghost_tag_b[0:3];reg ghost_fifo[0:3];''')
s=s.replace('begin ghost_valid[i]<=0;', 'begin ghost_valid_b[i]<=0;ghost_tag_b[i]<=0;ghost_fifo[i]<=0;ghost_valid[i]<=0;')
s=s.replace('(ghost_valid[si] && ghost_tag[si]==tag)', '((ghost_valid[si] && ghost_tag[si]==tag) || (GHOST_TWO && ghost_valid_b[si] && ghost_tag_b[si]==tag))')
old='if(ADMISSION && !bypass && !qaddr[31]) begin ghost_valid[si]<=1;ghost_tag[si]<=tag;end'
assert s.count(old)==1
s=s.replace(old,'''if(ADMISSION && !bypass && !qaddr[31]) begin
        if(!GHOST_TWO || !ghost_valid[si] || (ghost_valid_b[si] && !ghost_fifo[si])) begin
         ghost_valid[si]<=1;ghost_tag[si]<=tag;ghost_fifo[si]<=1;
        end else begin
         ghost_valid_b[si]<=1;ghost_tag_b[si]<=tag;ghost_fifo[si]<=0;
        end
       end''')
(R/'candidate.sv').write_text(s)
files=['candidate.sv','baseline.sv','m1.sv','backend.sv','run.py','implement.py','experiment.py']
(R/'EXECUTION_SHA256.txt').write_text(''.join(hashlib.sha256((R/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in files))
