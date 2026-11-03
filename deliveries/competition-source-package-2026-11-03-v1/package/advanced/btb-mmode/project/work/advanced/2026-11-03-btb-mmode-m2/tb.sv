`timescale 1ns/1ps
module tb;
parameter PRED=1,SYNC=0;
reg clk=0,rst=0;always #5 clk=~clk;
reg[31:0]rom[0:4095],ram[0:2047],si,sd;
wire[31:0]pc,pa,addr,wd,epc,cause,tval;wire we,trap;wire[3:0]strb;
wire[31:0]ins=SYNC?si:rom[pa[13:2]];
wire[31:0]data=SYNC?sd:ram[addr[12:2]];
integer i,b,cycle=0,f;
cpu_hl4 #(.BTB_ENABLE(PRED),.SYNC_MEMORY(SYNC)) dut(.clk(clk),.rst_n(rst),.pc(pc),.pc_phys(pa),.inst(ins),.pt_rdata(32'hcf),
 .mem_addr(addr),.mem_wdata(wd),.mem_wren(we),.mem_wstrb(strb),.mem_rdata(data),.mem_fault(1'b0),.inst_fault(1'b0),
 .timer_irq(1'b0),.soft_irq(1'b0),.ext_irq(1'b0),.s_timer_irq(1'b0),.s_soft_irq(1'b0),.s_ext_irq(1'b0),
 .dbg_mepc(epc),.dbg_mcause(cause),.dbg_mtval(tval),.dbg_trap(trap));
always @(posedge clk)begin
 si<=rom[pa[13:2]];sd<=ram[addr[12:2]];
 if(rst&&we)for(b=0;b<4;b=b+1)if(strb[b])ram[addr[12:2]][8*b+:8]<=wd[8*b+:8];
end
initial begin
 for(i=0;i<2048;i=i+1)ram[i]=0;
 $readmemh("program.hex",rom);f=$fopen("events.txt","w");$dumpfile("trace.vcd");$dumpvars(0,tb);
 repeat(5)@(negedge clk);rst=1;
end
always @(posedge clk)if(rst)begin
 cycle=cycle+1;
 if((^{pc,we,trap,dut.stall_all,dut.pipeline_advance,dut.redirect})===1'bx)$fdisplay(f,"UNKNOWN control");
 // Physical translation output is unspecified on a TLB miss. Check only
 // addresses accepted by the IF pipeline, not an inactive miss port.
 if(dut.i_hit && !dut.stall_all && (^{pa,ins})===1'bx)$fdisplay(f,"UNKNOWN accepted_fetch");
 if(dut.rf.we && (^{dut.mem_rd,dut.wb_write_data})===1'bx)$fdisplay(f,"UNKNOWN wb");
 if(we && (^{addr,wd,strb})===1'bx)$fdisplay(f,"UNKNOWN store");
 if(dut.rf.we&&dut.mem_rd!=0)$fdisplay(f,"WB %0d %h",dut.mem_rd,dut.wb_write_data);
 if(we)begin
  if(addr[31:13]!=0)$fdisplay(f,"UNKNOWN address");
  $fdisplay(f,"STORE %h %h %h",addr,wd,strb);
 end
 if(dut.id_valid && dut.id_pc==32'hff8 && dut.stall_all)
  $fdisplay(f,"FOCUS_HOLD %0d %h %h %b %b %b",cycle,dut.id_pc,pc,dut.i_hit,dut.redirect,dut.u_btb.update_valid);
 if(dut.u_btb.update_valid)$fdisplay(f,"TRAIN %0d %h %b",cycle,dut.id_pc,dut.stall_all);
 if(dut.pipeline_advance&&dut.id_valid&&!dut.stall_all&&(dut.id_branch||dut.id_jump))$fdisplay(f,"RESOLVE %0d %h",cycle,dut.id_pc);
 if(dut.redirect && dut.stall_all)$fdisplay(f,"REDIRECT_HELD %0d %h",cycle,dut.id_pc);
 if(trap&&dut.pipeline_advance)begin
  $fdisplay(f,"TRAP_PRE %0d %h %h %h",cycle,dut.trap_epc,dut.trap_cause,dut.trap_tval);
  #0.001;$fdisplay(f,"TRAP %h %h %h",epc,cause,tval);
 end
 if(cycle==400)begin
  #0.002;
  for(i=0;i<32;i=i+1)$fdisplay(f,"REG %0d %h",i,dut.rf.regs[i]);
  for(i=0;i<2048;i=i+1)$fdisplay(f,"MEM %0d %h",i,ram[i]);
  $fdisplay(f,"STATUS %h %h",dut.mstatus,dut.priv);$fdisplay(f,"END %0d",cycle);$fclose(f);$finish;
 end
end
endmodule
