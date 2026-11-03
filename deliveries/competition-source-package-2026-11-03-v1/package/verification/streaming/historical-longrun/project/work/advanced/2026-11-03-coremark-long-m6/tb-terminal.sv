`timescale 1fs/1fs
module tb;
parameter PRED=1,MAX_CYCLES=900000000,MUTATE=0;
reg clk=0,rst=0;always #18518518519 clk=~clk;
reg[31:0]rom[0:8191],ram[0:24575],si,sd;reg[31:0]phase_addr;
reg[63:0]ticks=0;
wire[31:0]pc,pa,addr,wd;wire we,trap;wire[3:0]strb;
function[31:0]read_data;input[31:0]a;begin
 if(a==32'h20000008)read_data=1;
 else if(a==32'h20000100)read_data=ticks[31:0];
 else if(a==32'h20000104)read_data=ticks[63:32];
 else if(a<32'h8000||(a>=32'h10000&&a<32'h18000))read_data=ram[a[16:2]];
 else read_data=0;
end endfunction
wire[31:0]ins=si,data=sd;
integer f,fu,ft,i,b,tmp,cycles=0,startcycle=-1,stopcycle=-1,donecycle=-1,finishcycle=-1;
integer train=0,wrong=0,branches=0,loadstalls=0;
integer seen_wb=0,seen_store=0,seen_timer=0;
cpu_hl4 #(.BTB_ENABLE(PRED),.BTB_INDEX_BITS(5),.SYNC_MEMORY(1)) dut(
 .clk(clk),.rst_n(rst),.pc(pc),.pc_phys(pa),.inst(ins),.pt_rdata(32'd0),
 .mem_addr(addr),.mem_wdata(wd),.mem_wren(we),.mem_wstrb(strb),.mem_rdata(data),
 .mem_fault(1'b0),.inst_fault(1'b0),.timer_irq(1'b0),.soft_irq(1'b0),.ext_irq(1'b0),
 .s_timer_irq(1'b0),.s_soft_irq(1'b0),.s_ext_irq(1'b0),.dbg_trap(trap));
always @(posedge clk)begin
 if(!rst)ticks<=0;else ticks<=ticks+1;
 si<=rom[pa[14:2]];sd<=read_data(addr);
 if(rst&&we&&addr>=32'h10000&&addr<32'h18000)
  for(b=0;b<4;b=b+1)if(strb[b])ram[addr[16:2]][8*b+:8]<=wd[8*b+:8];
end
initial begin
 for(i=0;i<24576;i=i+1)ram[i]=0;
 tmp=$value$plusargs("PHASE=%h",phase_addr);
 $readmemh("program.hex",rom);$readmemh("program.hex",ram,0,8191);
 f=$fopen("state.txt","w");fu=$fopen("uart.txt","w");ft=$fopen("timer-reads.txt","w");
 $stream_init("program.bin");$dumpfile("window.vcd");
 repeat(5)@(negedge clk);rst=1;
end
always @(posedge clk)if(rst)begin
 cycles=cycles+1;
 if(dut.pipeline_advance&&!dut.stall_all&&dut.ex_valid&&dut.ex_mem_to_reg&&(addr==32'h20000100||addr==32'h20000104))begin
  $fdisplay(ft,"READ %0d %h %h",cycles,addr,data);seen_timer=seen_timer+1;
  $stream_timer(cycles,addr,data ^ ((MUTATE==5 && seen_timer==1)?32'd1:32'd0));
 end
 
 if((^{pc,pa,we,trap,dut.stall_all,dut.pipeline_advance})===1'bx)$fatal(1,"UNKNOWN control");
 if(dut.pipeline_advance&&trap)$fatal(1,"TRAP %h %h",dut.trap_epc,dut.trap_cause);
 if(pa>=32768)$fatal(1,"BAD_FETCH %h",pa);
 if(dut.rf.we&&dut.mem_rd!=0)begin
  seen_wb=seen_wb+1;
  if(!(MUTATE==2 && seen_wb==1))
   $stream_wb(cycles,{27'd0,dut.mem_rd},dut.wb_write_data ^ ((MUTATE==1 && seen_wb==1)?32'd1:32'd0) ^ ((MUTATE==6 && seen_wb==1)?32'hxxxxxxxx:32'd0));
  if(MUTATE==3 && seen_wb==1)$stream_wb(cycles,{27'd0,dut.mem_rd},dut.wb_write_data);
 end
 if(dut.u_btb.update_valid)train=train+1;
 if(dut.pipeline_advance&&!dut.stall_all&&dut.id_valid&&(dut.id_branch||dut.id_jump))branches=branches+1;
 if(dut.pipeline_advance&&!dut.stall_all&&dut.ex_btb_mispredict)wrong=wrong+1;
 if(dut.pipeline_advance&&dut.lw_stall)loadstalls=loadstalls+1;
 if(we)begin
  if(!((addr>=32'h10000&&addr<32'h18000)||addr==32'h20000000))$fatal(1,"BAD_STORE %h",addr);
  seen_store=seen_store+1;
  $stream_store(cycles,addr,wd,{28'd0,strb} ^ ((MUTATE==4 && seen_store==1)?32'd1:32'd0));
  if(addr==32'h20000000)$fwrite(fu,"%c",wd[7:0]);
  if(addr==phase_addr&&wd==1)startcycle=cycles;
  if(addr==phase_addr&&wd==2)stopcycle=cycles;
  if(addr==32'h17ffc)begin donecycle=cycles;finishcycle=cycles+6;$dumpvars(1,tb);$dumpvars(1,dut);end
 end
 if(cycles%10000000==0)begin $display("PROGRESS cycles=%0d phase_start=%0d phase_stop=%0d",cycles,startcycle,stopcycle);$fflush();end
 if(cycles==finishcycle)begin
  #1;
  for(i=0;i<32;i=i+1)begin $fdisplay(f,"REG %0d %08h",i,dut.rf.regs[i]);$stream_state(0,i,dut.rf.regs[i]);end
  for(i=0;i<24576;i=i+1)begin $fdisplay(f,"MEM %0d %08h",i,ram[i]);$stream_state(1,i,ram[i]);end
  $fdisplay(f,"END %0d %0d %0d %0d %0d %0d %0d %0d",cycles,startcycle,stopcycle,donecycle,train,wrong,branches,loadstalls);
  $stream_finish(cycles);$fclose(f);$fclose(fu);$fclose(ft);$finish;
 end
 if(cycles>=MAX_CYCLES)$fatal(1,"CYCLE_LIMIT");
end
endmodule
