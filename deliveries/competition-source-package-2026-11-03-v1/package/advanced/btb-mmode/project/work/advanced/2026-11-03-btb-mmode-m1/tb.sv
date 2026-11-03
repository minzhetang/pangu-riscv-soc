`timescale 1ns/1ps
module tb;
reg clk=0,rst=0;wire[31:0]pc,pa,addr,wd,epc,cause,tval;wire we,trap;wire[3:0]strb;
reg[31:0] rom[0:255];reg[31:0] ins;integer i,cycle=0,trapcycle=-1,linkwrites=0,stores=0;integer f;
always #5 clk=~clk;
always @* ins=rom[pa[9:2]];
cpu_hl4 dut(.clk(clk),.rst_n(rst),.pc(pc),.pc_phys(pa),.inst(ins),.pt_rdata(32'd0),
 .mem_addr(addr),.mem_wdata(wd),.mem_wren(we),.mem_wstrb(strb),.mem_rdata(32'd0),
 .mem_fault(1'b0),.inst_fault(1'b0),.timer_irq(1'b0),.soft_irq(1'b0),.ext_irq(1'b0),
 .s_timer_irq(1'b0),.s_soft_irq(1'b0),.s_ext_irq(1'b0),
 .dbg_mepc(epc),.dbg_mcause(cause),.dbg_mtval(tval),.dbg_trap(trap));
initial begin for(i=0;i<256;i=i+1)rom[i]=32'h00000013;$readmemh("program.hex",rom);
 f=$fopen("events.txt","w");$dumpfile("trace.vcd");$dumpvars(1,tb);repeat(5)@(negedge clk);rst=1;end
always @(posedge clk)if(rst)begin
 cycle=cycle+1;
 if(we)begin stores=stores+1;$fdisplay(f,"STORE %h %h",addr,wd);end
 if(trap&&trapcycle<0)begin trapcycle=cycle;#0.001;$fdisplay(f,"TRAP %h %h %h",epc,cause,tval);end
 if((trapcycle>=0&&cycle>trapcycle+12)||cycle==200)begin
  $fdisplay(f,"END %0d %0d %0d",cycle,linkwrites,stores);$fclose(f);$finish;
 end
end
endmodule
