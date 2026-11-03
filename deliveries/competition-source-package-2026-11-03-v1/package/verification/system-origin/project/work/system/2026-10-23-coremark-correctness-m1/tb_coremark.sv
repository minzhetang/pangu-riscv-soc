`timescale 1ns/1ps
module tb_coremark;
    reg clk=0,rst_n=0;
    wire [31:0] pc,inst,addr,wdata,rdata,stop_pc;
    wire wren,stopped;
    wire [3:0] wstrb;
    wire [1:0] stop_kind;
    integer cycle=0,stalls=0,flushes=0,holds=0;
    integer trace_fd,reg_fd,ram_fd,i;
    cpu dut(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),.mem_addr(addr),.mem_wdata(wdata),
        .mem_wren(wren),.mem_wstrb(wstrb),.mem_rdata(rdata),.eei_stop_valid(stopped),
        .eei_stop_kind(stop_kind),.eei_stop_pc(stop_pc));
    memory_model memory(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),.addr(addr),
        .wdata(wdata),.wren(wren),.wstrb(wstrb),.rdata(rdata));
    always #5 clk=~clk;
    initial begin
        trace_fd=$fopen("trace.log","w");
        if(!trace_fd) $fatal(1,"OUTPUT trace open");
        $dumpfile("wave.vcd"); $dumpvars(0,dut); $dumpvars(1,tb_coremark);
        repeat(4) @(negedge clk);
        rst_n=1;
    end
    // Full ordered text trace; ordinary VCD windows limit redundant waveform size.
    always @(posedge clk) if(rst_n) begin
        cycle=cycle+1;
        if(cycle>10000000) $fatal(1,"TIMEOUT 10M cycles");
        if(cycle==4096) $dumpoff;
        if((^{dut.id_valid,dut.ex_valid,dut.mem_valid,dut.mem_reg_write,wren,
              dut.ex_mem_to_reg,dut.stall_if,dut.control_flush,stopped})===1'bx)
            $fatal(1,"UNKNOWN control");
        if(dut.stall_if) stalls=stalls+1;
        if(dut.control_flush) flushes=flushes+1;
        if(dut.id_valid && !dut.eei_hold) begin
            if((^{dut.id_pc,dut.forward_rs1,dut.forward_rs2,dut.id_alu_ctrl})===1'bx)
                $fatal(1,"UNKNOWN active EX");
            if(dut.id_pc[1:0]!=0 || dut.id_pc>=32'h8000) $fatal(1,"EX invalid PC");
            $fdisplay(trace_fd,"EX|%08x",dut.id_pc);
        end
        if(dut.mem_valid && dut.mem_reg_write) begin
            if((^{dut.mem_rd,dut.wb_write_data})===1'bx) $fatal(1,"UNKNOWN WB");
            if(dut.mem_rd!=0) $fdisplay(trace_fd,"WB|%0d|%08x",dut.mem_rd,dut.wb_write_data);
        end
        if(dut.ex_valid && dut.ex_mem_to_reg) begin
            if((^{addr,rdata,dut.mem_load_data,dut.ex_pc})===1'bx) $fatal(1,"UNKNOWN READ");
            if(!(addr<32'h8000 || (addr>=32'h10000 && addr<32'h18000)))
                $fatal(1,"MEMORY_PROTOCOL invalid read");
            if((dut.ex_funct3==2 && addr[1:0]!=0) ||
               ((dut.ex_funct3==1 || dut.ex_funct3==5) && addr[0]!=0)) $fatal(1,"READ alignment");
            $fdisplay(trace_fd,"READ|%08x|%08x|%08x|%08x",dut.ex_pc,addr,rdata,dut.mem_load_data);
        end
        if(wren) begin
            if(!dut.ex_valid) $fatal(1,"STORE without validity");
            if((dut.ex_funct3==2 && addr[1:0]!=0) ||
               (dut.ex_funct3==1 && addr[0]!=0)) $fatal(1,"STORE alignment");
            $fdisplay(trace_fd,"STORE|%08x|%08x|%08x|%01x",dut.ex_pc,addr,wdata,wstrb);
        end
        if(stopped) begin
            if(holds==0) $dumpon;
            if(stop_kind!==2 || stop_pc!==32'h68 || wren || (dut.mem_valid && dut.mem_reg_write))
                $fatal(1,"STOP_PROTOCOL stop kind/PC/side effect");
        end
    end
    always @(negedge clk) if(rst_n && stopped) begin
        holds=holds+1;
        if(holds==4) begin
            reg_fd=$fopen("registers.hex","w"); ram_fd=$fopen("ram.hex","w");
            if(!reg_fd || !ram_fd) $fatal(1,"OUTPUT final state open");
            for(i=0;i<32;i=i+1) $fdisplay(reg_fd,"%08x",dut.rf.regs[i]);
            for(i=0;i<32768;i=i+1) $fdisplay(ram_fd,"%02x",memory.ram[i]);
            $fclose(reg_fd); $fclose(ram_fd); $fclose(trace_fd);
            $display("METRICS|cycles=%0d|stall=%0d|flush=%0d|holds=%0d|time_ps=%0t",cycle,stalls,flushes,holds,$time);
            $display("STOP|%0d|%08x",stop_kind,stop_pc);
            $display("SIMULATION_ENDED_NOT_FUNCTIONAL_PASS"); $finish;
        end
    end
endmodule
