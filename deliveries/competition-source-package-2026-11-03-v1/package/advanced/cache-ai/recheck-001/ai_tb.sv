`timescale 1ns/1ps
module ai_tb;
 reg clk=0;always #5 clk=~clk;
 reg rst=1,cfg_valid=0,start_valid=0,out_ready=0;
 reg [1:0] cfg_kind=0;reg [7:0] cfg_addr=0;reg [31:0] cfg_data=0;
 wire cfg_ready,start_ready,out_valid,out_last,out_error;wire [2:0] out_index;
 wire signed [39:0] out_acc;wire signed [7:0] out_y;
 fc_m0 dut(.*);
 integer cycle=0,starts=0,outputs=0;reg held=0;reg [52:0] payload;
 always @(posedge clk) begin
  cycle<=cycle+1;
  if(cycle>30000) $fatal(1,"watchdog");
  if(rst) held<=0;
  else begin
   if(start_valid && start_ready) starts<=starts+1;
   if(out_valid && out_ready) outputs<=outputs+1;
   if(held && (!out_valid || {out_index,out_last,out_error,out_acc,out_y}!==payload)) $fatal(1,"unstable output");
   held<=out_valid && !out_ready;payload<={out_index,out_last,out_error,out_acc,out_y};
   if(out_valid && cfg_ready) $fatal(1,"busy cfg");
  end
 end
 integer xs[0:15],ws[0:127],bs[0:7],ys[0:7];reg signed [63:0] sums[0:7];
 string vec,wave;integer fd,rc,i,r,stall=0,mode=0,start_cycle,config_cycle,config_elapsed,elapsed;
 task reset_all;
 begin @(negedge clk);rst=1;cfg_valid=0;start_valid=0;out_ready=0;repeat(3) @(negedge clk);rst=0;end endtask
 task config_word(input [1:0] kind,input [7:0] addr,input [31:0] value);
 begin
  @(negedge clk);cfg_valid=1;cfg_kind=kind;cfg_addr=addr;cfg_data=value;
  @(posedge clk);while(!cfg_ready) @(posedge clk);
  @(negedge clk);cfg_valid=0;
 end endtask
 task load_all;
 begin
  for(integer k=0;k<16;k=k+1) config_word(0,k,xs[k]);
  for(integer k=0;k<128;k=k+1) config_word(1,k,ws[k]);
  for(integer k=0;k<8;k=k+1) config_word(2,k,bs[k]);
 end endtask
 task start_job;
 begin
  @(negedge clk);start_valid=1;
  @(posedge clk);while(!start_ready) @(posedge clk);start_cycle=cycle;
  @(negedge clk);start_valid=0;
 end endtask
 task collect(input integer stalls,input bit verbose);
 begin
  for(integer k=0;k<8;k=k+1) begin
   while(!out_valid) @(negedge clk);
   repeat(stalls ? k%4:0) @(negedge clk);
   if(out_acc!==sums[k][39:0] || $signed(out_y)!=ys[k] || out_error || out_index!=k || out_last!=(k==7)) $fatal(1,"mismatch row%0d raw%0d expected%0d y%0d expected%0d",k,out_acc,sums[k],out_y,ys[k]);
   if(verbose) $display("OUTPUT row=%0d raw=%0d y=%0d",k,out_acc,out_y);
   out_ready=1;@(posedge clk);if(k==7) elapsed=cycle-start_cycle;
   @(negedge clk);out_ready=0;
  end
 end endtask
 initial begin
  rc=$value$plusargs("STALL=%d",stall);rc=$value$plusargs("MODE=%d",mode);
  if($value$plusargs("WAVE=%s",wave)) begin $dumpfile(wave);$dumpvars(0,ai_tb);end
  if(!$value$plusargs("VEC=%s",vec)) $fatal(1,"vectors required");
  fd=$fopen(vec,"r");if(!fd) $fatal(1,"file");
  for(i=0;i<16;i=i+1) begin rc=$fscanf(fd,"%d\n",xs[i]);if(rc!=1) $fatal(1,"parse");end
  for(i=0;i<128;i=i+1) begin rc=$fscanf(fd,"%d\n",ws[i]);if(rc!=1) $fatal(1,"parse");end
  for(i=0;i<8;i=i+1) begin rc=$fscanf(fd,"%d\n",bs[i]);if(rc!=1) $fatal(1,"parse");end
  for(i=0;i<8;i=i+1) begin rc=$fscanf(fd,"%d\n%d\n",sums[i],ys[i]);if(rc!=2) $fatal(1,"parse");end
  reset_all();
  if(mode==0) begin
   config_cycle=cycle;load_all();config_elapsed=cycle-config_cycle;
   start_job();collect(stall,1);
   $display("AI_METRIC cycles=%0d config_cycles=%0d",elapsed,config_elapsed);
   repeat(5) @(negedge clk);if(starts!=1 || outputs!=8 || out_valid) $fatal(1,"exactly once");
  end else begin
   // Invalid config must not turn missing initialization into a valid computation.
   config_word(3,0,123);config_word(0,16,123);config_word(1,128,123);config_word(2,8,123);
   start_job();while(!out_valid) @(negedge clk);
   if(!out_error || !out_last || out_acc!==0 || out_y!==0) $fatal(1,"missing-init");
   repeat(4) @(negedge clk);out_ready=1;@(negedge clk);out_ready=0;
   load_all();start_job();
   // Attempt config/start while busy: no acceptance, no data mutation.
   cfg_valid=1;cfg_kind=0;cfg_addr=0;cfg_data=127;start_valid=1;
   repeat(5) begin @(negedge clk);if(cfg_ready || start_ready) $fatal(1,"busy ready");end
   cfg_valid=0;start_valid=0;collect(1,0);
   start_job();collect(0,0); // all weights/input retained across starts
   start_job();repeat(4) @(negedge clk);reset_all();
   repeat(20) @(negedge clk);if(out_valid) $fatal(1,"ghost MAC");
   load_all();start_job();while(!out_valid) @(negedge clk);reset_all();
   repeat(20) @(negedge clk);if(out_valid) $fatal(1,"ghost response");
   start_job();while(!out_valid) @(negedge clk);if(!out_error) $fatal(1,"reset flags");
   out_ready=1;@(negedge clk);out_ready=0;
   load_all();start_job();collect(0,0);
   $display("PROTOCOL_PASS");
  end
  $display("PASS ai");$finish;
 end
endmodule
