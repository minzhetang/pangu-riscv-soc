`timescale 1ns/1ps
module tb;
reg clk=0,rst=0;reg[7:0] pins=0;
wire tx,stopped,err;wire[7:0] leds;wire[1:0] kind;wire[31:0] stop_pc;
soc_top #(.CLKS_PER_BIT(8)) dut(.clk(clk),.rst_n(rst),.gpio_in_async(pins),.uart_tx(tx),.gpio_out(leds),.stopped(stopped),.stop_kind(kind),.stop_pc(stop_pc),.write_error(err));
always #5 clk=~clk;
reg[7:0] stimulus[0:31];integer n,cycle=0,origin=-1,run=0,idx,accepted,serial,obs,log;
reg[7:0] byte_value;integer bitno;reg decoding=0; reg[31:0] last_a0=32'hxxxxxxxx;
initial begin
 $readmemh("input.hex",stimulus);accepted=$fopen("accepted.txt","w");serial=$fopen("serial.txt","w");obs=$fopen("reads.txt","w");log=$fopen("stop.txt","w");
 $dumpfile("run.vcd");$dumpvars(1,tb);
 for(run=0;run<2;run=run+1)begin
  rst=0;pins=0;origin=-1;last_a0=32'hxxxxxxxx;repeat(8)@(negedge clk);rst=1;
  wait(stopped);@(negedge clk);
  if(kind!==2 || last_a0!==0)$fatal(1,"main return/stop mismatch");
  if(decoding)$fatal(1,"stopped during serial frame");
  if(run==0)$writememh("ram0.hex",dut.storage.ram);else $writememh("ram1.hex",dut.storage.ram);
  $fdisplay(log,"%0d %0d %h",run,cycle,leds);$fwrite(accepted,"~");$fwrite(serial,"~");
 end
 $fclose(accepted);$fclose(serial);$fclose(obs);$fclose(log);$display("TWO_RESETS_FINISHED");$finish;
end
always @(negedge clk)if(rst&&origin>=0)begin
 idx=(cycle-origin-6000)/12000;
 if(cycle-origin<6000)pins=0;else if(idx>=0&&idx<32)pins=stimulus[idx];
end
always @(posedge clk)begin
 cycle=cycle+1;if(cycle>2500000)$fatal(1,"cycle timeout");
 if(rst)begin
  if(dut.cpu_core.pipeline_advance&&dut.cpu_core.mem_reg_write&&dut.cpu_core.mem_rd==10)last_a0=dut.cpu_core.wb_write_data;
  if(err!==0)$fatal(1,"write error/X");
  if(dut.peripherals.gpio_accept&&dut.io_wdata==32'h40)origin=cycle;
  if(dut.peripherals.tx_accept)begin
   if(^dut.io_wdata===1'bx)$fatal(1,"TX X");$fwrite(accepted,"%c",dut.io_wdata[7:0]);
  end
  if(dut.cpu_core.pipeline_advance&&dut.cpu_core.ex_mem_to_reg&&dut.cpu_core.ex_valid)
   $fdisplay(obs,"%0d %h %h %h",run,dut.address,dut.route.cpu_read_data,dut.timer.ticks[31:0]);
 end
end
always @(negedge tx)if(rst&&!decoding)begin
 decoding=1;repeat(4)@(posedge clk);#0.001;if(tx!==0)$fatal(1,"UART start");
 for(bitno=0;bitno<8;bitno=bitno+1)begin repeat(8)@(posedge clk);#0.001;if(tx!==0&&tx!==1)$fatal(1,"UART X");byte_value[bitno]=tx;end
 repeat(8)@(posedge clk);#0.001;if(tx!==1)$fatal(1,"UART stop");$fwrite(serial,"%c",byte_value);decoding=0;
end
endmodule
