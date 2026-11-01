`timescale 1ns/1ps
module tb;
 parameter SYNC=0;
 reg clk=0,rst_n=0;always #5 clk=~clk;
 wire[31:0] pc,addr,wd;wire[3:0]strb;wire we,stopped;wire[1:0]kind;wire[31:0]stop_pc;
 reg[31:0]rom[0:63];reg[31:0]data=32'h88776655,iq=0,dq=0;wire[31:0]inst=SYNC?iq:rom[pc[7:2]];wire[31:0]rd=SYNC?dq:data;
 cpu #(.SYNC_MEMORY(SYNC)) dut(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),.mem_addr(addr),.mem_wdata(wd),.mem_wren(we),.mem_wstrb(strb),.mem_rdata(rd),.eei_stop_valid(stopped),.eei_stop_kind(kind),.eei_stop_pc(stop_pc));
 string image,wave;integer cy=0,i,post_cycles=0;reg was_stop=0;
 initial begin if(!$value$plusargs("ROM=%s",image)||!$value$plusargs("VCD=%s",wave))$fatal(1,"args");$readmemh(image,rom);$dumpfile(wave);$dumpvars(0,tb);#12 rst_n=1;end
 always @(posedge clk)begin
  iq<=rom[pc[7:2]];dq<=data;
  if(rst_n)begin
   cy=cy+1;
   if(dut.pipeline_advance&&dut.mem_valid&&dut.mem_reg_write&&dut.mem_rd!=0)begin
    if(was_stop)$fatal(1,"WB after stop");$display("WB %0d %08x",dut.mem_rd,dut.wb_write_data);
   end
   if(we)begin
    if(was_stop)$fatal(1,"STORE after stop");$display("ST %08x %08x %x",addr,wd,strb);
    for(i=0;i<4;i=i+1)if(strb[i])data[i*8+:8]<=wd[i*8+:8];
   end
   if(cy>250)$fatal(1,"TIMEOUT");
  end
  #1;
  if(rst_n&&stopped&&!was_stop)begin
   $display("STOP %0d %08x %0d",kind,stop_pc,cy);for(i=0;i<32;i=i+1)$display("RF %0d %08x",i,dut.rf.regs[i]);$display("MEM %08x",data);was_stop=1;
   end else if(was_stop)begin
   post_cycles=post_cycles+1;if(post_cycles==5)begin $display("END");$finish;end
  end
 end
endmodule
