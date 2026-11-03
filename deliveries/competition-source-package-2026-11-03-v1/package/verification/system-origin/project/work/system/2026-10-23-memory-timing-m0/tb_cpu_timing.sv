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
  assign rdata=data_sync ? dq : read_data(addr);
  cpu dut(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),.mem_addr(addr),
    .mem_wdata(wdata),.mem_wren(wen),.mem_wstrb(strb),.mem_rdata(rdata),
    .eei_stop_valid(stopped),.eei_stop_kind(kind),.eei_stop_pc(stop_pc));
  initial begin
    if(!$value$plusargs("PROGRAM=%s",program_file)) $fatal(1,"PROGRAM missing");
    if(!$value$plusargs("DATA=%s",data_file)) $fatal(1,"DATA missing");
    if(!$value$plusargs("IF_SYNC=%d",if_sync)) if_sync=0;
    if(!$value$plusargs("DATA_SYNC=%d",data_sync)) data_sync=0;
    $readmemh(program_file,rom); $readmemh(data_file,ram);
    $dumpfile("wave.vcd"); $dumpvars(0,tb_cpu_timing);
    repeat(3) @(negedge clk);
    rst_n=1;
  end
  // Clocked read returns after sampling edge (NBA). Read-before-write on one address.
  // This behavior model is not a PDS mapped memory or substitute vendor model.
  always @(posedge clk) begin
    if(!rst_n) begin iq<=32'h00100073; dq<=0; end
    else begin
      iq <= (pc<1024) ? rom[pc>>2] : 32'hxxxxxxxx;
      dq <= read_data(addr);
      if(wen && addr>=256 && addr<512)
        for(lane=0;lane<4;lane=lane+1)
          if(strb[lane]) ram[(addr-256)>>2][lane*8+:8] <= wdata[lane*8+:8];
    end
  end
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
endmodule
