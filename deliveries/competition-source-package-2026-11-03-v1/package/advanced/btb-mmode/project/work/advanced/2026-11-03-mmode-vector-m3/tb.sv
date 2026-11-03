`timescale 1ns/1ps
module tb;
parameter PRED=1;
parameter SYNC=0;
reg clk=0,rst=0;wire[31:0]pc,pa,addr,wd,epc,cause,tval,ptaddr;wire we,trap;wire[3:0]strb;
reg[31:0]rom[0:1023];reg[31:0]sync_ins;wire[31:0]ins=SYNC ? sync_ins : rom[pa[11:2]];reg[31:0]irq=0;
integer i,cycle=0,f,mask=0,refresh=0,stallcycles=0,irq_at=1;reg irq_done=0;
reg[31:0]ram[0:2047];reg[31:0]sync_data;integer b;
wire[31:0]read_data=SYNC ? sync_data : ram[addr[12:2]];
always #5 clk=~clk;
always @(posedge clk) sync_ins<=rom[pa[11:2]];
always @(posedge clk)begin
 sync_data<=ram[addr[12:2]];
 if(rst && we) for(b=0;b<4;b=b+1) if(strb[b]) ram[addr[12:2]][8*b+:8]<=wd[8*b+:8];
end
cpu_hl4 #(.BTB_ENABLE(PRED),.SYNC_MEMORY(SYNC)) dut(.clk(clk),.rst_n(rst),.pc(pc),.pc_phys(pa),.inst(ins),.pt_addr(ptaddr),.pt_rdata(32'hcf),
 .mem_addr(addr),.mem_wdata(wd),.mem_wren(we),.mem_wstrb(strb),.mem_rdata(read_data),
 .mem_fault(1'b0),.inst_fault(1'b0),.timer_irq(irq[7]),.soft_irq(irq[3]),.ext_irq(irq[11]),
 .s_timer_irq(1'b0),.s_soft_irq(1'b0),.s_ext_irq(1'b0),
 .dbg_mepc(epc),.dbg_mcause(cause),.dbg_mtval(tval),.dbg_trap(trap));
initial begin
 for(i=0;i<2048;i=i+1)ram[i]=0;
 $readmemh("program.hex",rom);i=$value$plusargs("IRQ=%d",mask);i=$value$plusargs("REFRESH=%d",refresh);
 i=$value$plusargs("IRQ_AT=%d",irq_at);if(SYNC && irq_at!=80)irq_at=2*irq_at;
 f=$fopen("events.txt","w");$dumpfile("trace.vcd");$dumpvars(0,tb);
 repeat(5)@(negedge clk);rst=1;
end
always @(negedge clk) if(rst)begin
 if(cycle>=irq_at&&!irq_done)irq=mask;else irq=0;
 if(refresh&&cycle==80)rom[2]=32'h00700513;
end
always @(posedge clk)if(rst)begin
 cycle=cycle+1;
 if((^{pc,pa,we,trap,dut.stall_all,dut.pipeline_advance})===1'bx) $fdisplay(f,"UNKNOWN_CONTROL %0d",cycle);
 if(dut.stall_all)begin stallcycles=stallcycles+1;$fdisplay(f,"STALL %0d %h",cycle,dut.id_pc);end
 if(dut.rf.we && dut.mem_rd!=0)begin
  if((^{dut.mem_rd,dut.wb_write_data})===1'bx)$fdisplay(f,"UNKNOWN_WB");
  $fdisplay(f,"WB %0d %h",dut.mem_rd,dut.wb_write_data);
 end
 if(we)begin
  if(addr[31:13]!=0)$fdisplay(f,"UNKNOWN_RANGE");
  if((^{addr,wd,strb})===1'bx)$fdisplay(f,"UNKNOWN_STORE");
  $fdisplay(f,"STORE %h %h %h",addr,wd,strb);
 end
 if(dut.u_btb.update_valid)$fdisplay(f,"TRAIN %0d %h %b",cycle,dut.id_pc,dut.stall_all);
 if(dut.pipeline_advance && dut.csr_commit_eff)$fdisplay(f,"CSR %0d %h %h %h",cycle,dut.id_pc,dut.ex_csr_addr,dut.ex_csr_wdata);
 if(trap && dut.pipeline_advance)begin
  $fdisplay(f,"VECTOR %0d %h %h",cycle,dut.redirect_pc,dut.mstatus);
  $fdisplay(f,"TRAP_PRE %0d %h %h %h",cycle,dut.trap_epc,dut.trap_cause,dut.trap_tval);
  irq_done<=1;
  #0.001;$fdisplay(f,"TRAP %h %h %h",epc,cause,tval);
  $fdisplay(f,"TRAP_STATUS %h %h",dut.mstatus,dut.priv);
  $fdisplay(f,"REDIRECT_POST %h",pc);
 end
 if(cycle==400)begin
  #0.002;for(i=0;i<32;i=i+1)$fdisplay(f,"REG %0d %h",i,dut.rf.regs[i]);
  for(i=0;i<2048;i=i+1)$fdisplay(f,"MEM %0d %h",i,ram[i]);
  $fdisplay(f,"STATUS %h %h",dut.mstatus,dut.priv);
  $fdisplay(f,"END %0d %0d",cycle,stallcycles);$fclose(f);$finish;
 end
end
endmodule
