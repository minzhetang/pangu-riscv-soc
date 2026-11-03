`timescale 1ns/1ps
module tb;
reg clk=0,rst=0;reg[7:0]pins=0;
wire tx,stopped,err;wire[7:0]leds;wire[1:0]kind;wire[31:0]stop_pc;
soc_top #(.CLKS_PER_BIT(8)) dut(.clk(clk),.rst_n(rst),.gpio_in_async(pins),.uart_tx(tx),.gpio_out(leds),.stopped(stopped),.stop_kind(kind),.stop_pc(stop_pc),.write_error(err));
always #5 clk=~clk;
reg[7:0]stimulus[0:127];integer period=12000,nsamp=32,repeats=2,maxcycles=2500000;
integer cycle=0,origin=-1,run=0,idx,i,a,s,o,f,pending=0,gi=0;
reg decoding=0;reg[7:0]bv;reg[31:0]last_a0=32'hxxxxxxxx;
initial begin
 if($value$plusargs("PERIOD=%d",period))begin end
 if($value$plusargs("COUNT=%d",nsamp))begin end
 if($value$plusargs("REPEATS=%d",repeats))begin end
 if($value$plusargs("MAX_CYCLES=%d",maxcycles))begin end
 if(period<1||nsamp<1||nsamp>128||repeats<1||repeats>2||maxcycles>7000000)$fatal(1,"bad limits");
 for(i=0;i<128;i=i+1)stimulus[i]=0;$readmemh("input.hex",stimulus);
 a=$fopen("accepted.txt","w");s=$fopen("serial.txt","w");o=$fopen("observe.txt","w");f=$fopen("stop.txt","w");
 $dumpfile("io.vcd");$dumpvars(1,tb); // sparse public IO, not clock/cycle flooding
 for(run=0;run<repeats;run=run+1)begin
  rst=0;pins=0;origin=-1;pending=0;gi=0;last_a0=32'hxxxxxxxx;repeat(8)@(negedge clk);rst=1;
  wait(stopped);@(negedge clk);
  if(kind!==2||last_a0!==0||decoding)$fatal(1,"main return/stop/frame mismatch");
  if(run==0)$writememh("ram0.hex",dut.storage.ram);else $writememh("ram1.hex",dut.storage.ram);
  $fdisplay(f,"%0d %0d %h",run,cycle,leds);$fwrite(a,"~");$fwrite(s,"~");
 end
 $fclose(a);$fclose(s);$fclose(o);$fclose(f);$display("BOUNDED_RESETS_FINISHED");$finish;
end
always @(negedge clk)if(rst&&origin>=0)begin
 if(cycle-origin<period/2)pins=0;
 else begin idx=(cycle-origin-period/2)/period;if(idx>=0&&idx<nsamp)pins=stimulus[idx];end
end
always @(posedge clk)begin
 cycle=cycle+1;if(cycle>maxcycles)$fatal(1,"cycle timeout");
 if(rst)begin
  if(err!==0)$fatal(1,"write error/X");
  if(dut.cpu_core.pipeline_advance&&dut.cpu_core.mem_reg_write&&dut.cpu_core.mem_rd==10)last_a0=dut.cpu_core.wb_write_data;
  if(dut.peripherals.gpio_accept&&dut.io_wdata==32'h40)begin origin=cycle;$fdisplay(o,"%0d ORIGIN %h",run,dut.timer.ticks[31:0]);end
  if(dut.peripherals.tx_accept)begin if(^dut.io_wdata===1'bx)$fatal(1,"TX X");$fwrite(a,"%c",dut.io_wdata[7:0]);end
  if(dut.cpu_core.pipeline_advance&&dut.cpu_core.ex_mem_to_reg&&dut.cpu_core.ex_valid)begin
   if(dut.address==32'h20000010)begin
    if(pending)$fatal(1,"GPIO without timestamp");pending=1;
    $fdisplay(o,"%0d G %0d %h %h",run,gi,dut.route.cpu_read_data,dut.timer.ticks[31:0]);
   end else if(dut.address==32'h20000100&&pending)begin
    if(dut.route.cpu_read_data!==dut.timer.ticks[31:0])$fatal(1,"timer identity");
    $fdisplay(o,"%0d T %0d %h",run,gi,dut.route.cpu_read_data);gi=gi+1;pending=0;
   end
  end
 end
end
integer bitno;
always @(negedge tx)if(rst&&!decoding)begin
 decoding=1;repeat(4)@(posedge clk);#0.001;if(tx!==0)$fatal(1,"UART start");
 for(bitno=0;bitno<8;bitno=bitno+1)begin repeat(8)@(posedge clk);#0.001;if(tx!==0&&tx!==1)$fatal(1,"UART X");bv[bitno]=tx;end
 repeat(8)@(posedge clk);#0.001;if(tx!==1)$fatal(1,"UART stop");$fwrite(s,"%c",bv);decoding=0;
end
endmodule
