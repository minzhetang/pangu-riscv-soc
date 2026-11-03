`timescale 1ns/1ps
module tb_cpu_timing;
  reg clk=0, rst_n=0;
  always #5 clk=~clk;
  wire [31:0] pc,addr,wdata,inst,rdata,stop_pc;
  wire wen,stopped;
  wire [3:0] strb;
  wire [1:0] kind;
  reg [31:0] rom[0:255], ram[0:63];
  reg [31:0] iq=32'h00100073,dq=0;
  integer if_sync=0,data_sync=0,i,lane,cycle=0,post=-1;
  integer model_test=0,model_checks=0;
  reg [31:0] probe_addr=0,probe_data=0;
  reg [3:0] probe_strb=0;
  reg probe_write=0;
  wire [31:0] bus_addr=model_test ? probe_addr : addr;
  wire [31:0] bus_wdata=model_test ? probe_data : wdata;
  wire [3:0] bus_strb=model_test ? probe_strb : strb;
  wire bus_write=model_test ? probe_write : (rst_n && wen);
  reg [2047:0] program_file,data_file;
  reg [31:0] sampled_pc,sampled_inst;
  assign inst=if_sync ? iq : ((pc<1024) ? rom[pc>>2] : 32'hxxxxxxxx);
  function [31:0] read_data(input [31:0] a);
    begin
      if(a>=256 && a<512) read_data=ram[(a-256)>>2];
      else if(a<256) read_data=rom[a>>2];
      else read_data=32'hxxxxxxxx;
    end
  endfunction
  // Explicit array references ensure an address-stable write updates async output.
  wire [31:0] async_data=(bus_addr>=256 && bus_addr<512)
    ? ram[(bus_addr-256)>>2] : ((bus_addr<256) ? rom[bus_addr>>2] : 32'hxxxxxxxx);
  // Diagnostic control only; not used by the CPU data input in v2.
  wire [31:0] legacy_function_data=read_data(bus_addr);
  assign rdata=data_sync ? dq : async_data;
  cpu dut(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),.mem_addr(addr),
    .mem_wdata(wdata),.mem_wren(wen),.mem_wstrb(strb),.mem_rdata(rdata),
    .eei_stop_valid(stopped),.eei_stop_kind(kind),.eei_stop_pc(stop_pc));
  initial begin
    if(!$value$plusargs("PROGRAM=%s",program_file)) $fatal(1,"PROGRAM missing");
    if(!$value$plusargs("DATA=%s",data_file)) $fatal(1,"DATA missing");
    if(!$value$plusargs("IF_SYNC=%d",if_sync)) if_sync=0;
    if(!$value$plusargs("DATA_SYNC=%d",data_sync)) data_sync=0;
    model_test=$test$plusargs("MEMORY_SELFTEST");
    $readmemh(program_file,rom); $readmemh(data_file,ram);
    $dumpfile("wave.vcd"); $dumpvars(0,tb_cpu_timing);
    repeat(3) @(negedge clk);
    if(model_test) memory_selftest();
    else rst_n=1;
  end
  // Clocked read returns after sampling edge (NBA). Read-before-write on one address.
  // This behavior model is not a PDS mapped memory or substitute vendor model.
  always @(posedge clk) begin
    // Memory is enabled while CPU is reset. Warm the first ROM response instead
    // of injecting an artificial EBREAK into the first active IF slot.
      iq <= (pc<1024) ? rom[pc>>2] : 32'hxxxxxxxx;
      dq <= read_data(bus_addr);
      if(bus_write && bus_addr>=256 && bus_addr<512)
        for(lane=0;lane<4;lane=lane+1)
          if(bus_strb[lane]) ram[(bus_addr-256)>>2][lane*8+:8] <= bus_wdata[lane*8+:8];
  end
  task memory_check(input [31:0] want_async,input [31:0] want_q);
    begin
      model_checks=model_checks+1;
      $display("MODEL_CHECK %0d time_ps=%0t addr=%08h async=%08h q=%08h legacy=%08h",model_checks,$time,bus_addr,async_data,dq,legacy_function_data);
      if(async_data!==want_async || dq!==want_q) $fatal(1,"MODEL_FAIL");
    end
  endtask
  task memory_selftest;
    begin
      // Only the model's public test inputs are driven. CPU remains in reset.
      probe_addr=256; #1;
      @(posedge clk); #1; memory_check(32'ha5a5a5a5,32'ha5a5a5a5);
      @(negedge clk); probe_write=1; probe_data=32'h11223344; probe_strb=15;
      @(posedge clk); #1; memory_check(32'h11223344,32'ha5a5a5a5);
      $display("LEGACY_DIAGNOSTIC fixed=%08h legacy=%08h",async_data,legacy_function_data);
      @(negedge clk); probe_write=0;
      @(posedge clk); #1; memory_check(32'h11223344,32'h11223344);
      @(negedge clk); probe_write=1; probe_data=32'h0000ff00; probe_strb=2;
      @(posedge clk); #1; memory_check(32'h1122ff44,32'h11223344);
      @(negedge clk); probe_write=0;
      @(posedge clk); #1; memory_check(32'h1122ff44,32'h1122ff44);
      @(negedge clk); probe_write=1; probe_data=32'h55660000; probe_strb=12;
      @(posedge clk); #1; memory_check(32'h5566ff44,32'h1122ff44);
      @(negedge clk); probe_write=0;
      @(posedge clk); #1; memory_check(32'h5566ff44,32'h5566ff44);
      $display("MODEL_SELFTEST_PASS checks=%0d CPU_active_cycles=%0d",model_checks,cycle);
      $finish;
    end
  endtask
  always @(posedge clk) if(rst_n) begin
    cycle=cycle+1;
    sampled_pc=pc; sampled_inst=inst;
    $display("EDGE %0d %0t pc=%08h inst=%08h addr=%08h rd=%08h stall=%b flush=%b stop=%b",cycle,$time,pc,inst,addr,rdata,dut.stall_if,dut.flush_if,stopped);
    if((^{wen,stopped,dut.stall_if,dut.flush_if,dut.if_valid,dut.id_valid,dut.ex_valid,dut.mem_valid})===1'bx)
      $display("UNKNOWN_CONTROL %0d",cycle);
    if(!dut.stall_if && !dut.flush_if && !dut.eei_hold) begin
      $display("FETCH %0d %08h %08h",cycle,pc,inst);
      if(pc>=1024 || inst!==rom[pc>>2]) $display("FETCH_MISMATCH %0d %08h %08h",cycle,pc,inst);
    end
    if(dut.mem_valid && dut.mem_reg_write && dut.mem_rd!=0)
      $display("WB %0d %0d %08h",cycle,dut.mem_rd,dut.wb_write_data);
    if(dut.ex_valid && dut.ex_mem_to_reg)
      $display("LOAD %0d %08h %08h",cycle,addr,rdata);
    if(dut.ex_valid && dut.ex_mem_to_reg)
      $display("LOAD_CONTEXT %0d mem_pc=%08h mem_rd=%0d response=%08h",cycle,dut.ex_pc,dut.ex_rd,rdata);
    if(wen) $display("STORE %0d %08h %08h %01h",cycle,addr,wdata,strb);
    if(stopped && post<0) begin
      $display("STOP %0d %0d %08h",cycle,kind,stop_pc); post=0;
    end
    else if(post>=0) post=post+1;
    if(cycle>=2000) begin $display("CYCLE_TIMEOUT"); $finish; end
    #1;
    if(dut.if_valid) $display("IFID %0d %08h %08h",cycle,dut.if_pc,dut.if_inst);
    if(post==8) begin
      for(i=0;i<32;i=i+1) $display("REG %0d %08h",i,dut.rf.regs[i]);
      for(i=0;i<64;i=i+1) $display("RAM %0d %08h",i,ram[i]);
      $display("SIM_END %0d time_ps=%0t",cycle,$time); $finish;
    end
  end
  initial begin #20050; $fatal(1,"ABSOLUTE_SIM_TIMEOUT"); end
endmodule
