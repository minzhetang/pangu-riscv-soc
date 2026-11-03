`timescale 1ns/1ps
module tb;
parameter PRED=1,SYNC=0;
reg clk=0,rst=0;always #5 clk=~clk;
reg[31:0]rom[0:2047],ram[0:8191],si,sd;reg[31:0]seed;
wire[31:0]pc,pa,addr,wd;wire we,trap;wire[3:0]strb;
wire[31:0]ins=SYNC?si:rom[pa[12:2]],data=SYNC?sd:ram[addr[14:2]];
integer f,fw,fs,i,b,cycles=0,startcycle=-1,donecycle=-1,finishcycle=-1,train=0,wrong=0,branches=0,loadstalls=0;integer tmp;
cpu_hl4 #(.BTB_ENABLE(PRED),.SYNC_MEMORY(SYNC)) dut(.clk(clk),.rst_n(rst),.pc(pc),.pc_phys(pa),.inst(ins),.pt_rdata(32'd0),.mem_addr(addr),.mem_wdata(wd),.mem_wren(we),.mem_wstrb(strb),.mem_rdata(data),.mem_fault(1'b0),.inst_fault(1'b0),.timer_irq(1'b0),.soft_irq(1'b0),.ext_irq(1'b0),.s_timer_irq(1'b0),.s_soft_irq(1'b0),.s_ext_irq(1'b0),.dbg_trap(trap));
always @(posedge clk)begin
 si<=rom[pa[12:2]];sd<=ram[addr[14:2]];
 if(rst&&we)for(b=0;b<4;b=b+1)if(strb[b])ram[addr[14:2]][8*b+:8]<=wd[8*b+:8];
end
initial begin
 for(i=0;i<8192;i=i+1)ram[i]=0;
 tmp=$value$plusargs("SEED=%h",seed);ram[2048]=seed;$readmemh("program.hex",rom);$readmemh("program.hex",ram,0,2047);
 f=$fopen("state.txt","w");fw=$fopen("wb.txt","w");fs=$fopen("store.txt","w");
 $dumpfile("window.vcd");$dumpvars(1,tb);$dumpvars(1,dut);repeat(5)@(negedge clk);rst=1;
end
always @(posedge clk)if(rst)begin
 cycles=cycles+1;
 if(cycles==2048)$dumpoff;
 if((^{pc,pa,we,trap,dut.stall_all,dut.pipeline_advance})===1'bx)$fdisplay(f,"UNKNOWN control");
 if(dut.pipeline_advance&&trap)$fdisplay(f,"TRAP %h %h",dut.trap_epc,dut.trap_cause);
 if(pa>=8192)$fdisplay(f,"BAD_FETCH %h",pa);
 if(dut.rf.we&&dut.mem_rd!=0)begin
  if((^{dut.mem_rd,dut.wb_write_data})===1'bx)$fdisplay(f,"UNKNOWN wb");
  $fdisplay(fw,"WB %0d %08h",dut.mem_rd,dut.wb_write_data);
 end
 if(dut.u_btb.update_valid)train=train+1;
 if(dut.pipeline_advance&&!dut.stall_all&&dut.id_valid&&(dut.id_branch||dut.id_jump))branches=branches+1;
 if(dut.pipeline_advance&&!dut.stall_all&&dut.ex_btb_mispredict)wrong=wrong+1;
 if(dut.pipeline_advance&&dut.lw_stall)loadstalls=loadstalls+1;
 if(we)begin
  if((^{addr,wd,strb})===1'bx)$fdisplay(f,"UNKNOWN store");
  if(addr>=32768)$fdisplay(f,"BAD_STORE %h",addr);
  if(addr<8192)$fdisplay(f,"BAD_ROM_WRITE %h",addr);
  $fdisplay(fs,"STORE %08h %08h %h",addr,wd,strb);
  if(addr==32'h3000)startcycle=cycles;
  if(addr==32'h3020)begin donecycle=cycles;finishcycle=cycles+6;$dumpon;end
 end
 if(cycles==finishcycle || cycles>=300000)begin
  #0.002;for(i=0;i<32;i=i+1)$fdisplay(f,"REG %0d %08h",i,dut.rf.regs[i]);
  for(i=0;i<8192;i=i+1)$fdisplay(f,"MEM %0d %08h",i,ram[i]);
  $fdisplay(f,"END %0d %0d %0d %0d %0d %0d %0d",cycles,startcycle,donecycle,train,wrong,branches,loadstalls);$fclose(f);$fclose(fw);$fclose(fs);$finish;
 end
end
endmodule
