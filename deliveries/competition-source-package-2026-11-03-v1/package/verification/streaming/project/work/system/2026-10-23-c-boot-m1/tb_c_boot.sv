`timescale 1ns/1ps
module tb_c_boot;
    reg clk=0, rst_n=0;
    wire [31:0] pc, inst, addr, wdata, rdata, stop_pc;
    wire wren, stopped;
    wire [3:0] wstrb;
    wire [1:0] stop_kind;
    integer cycle=0, stalls=0, flushes=0, hold_edges=0;
    integer regfile_fd, memory_fd, i;
    cpu dut(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),
        .mem_addr(addr),.mem_wdata(wdata),.mem_wren(wren),.mem_wstrb(wstrb),
        .mem_rdata(rdata),.eei_stop_valid(stopped),.eei_stop_kind(stop_kind),.eei_stop_pc(stop_pc));
    memory_model memory(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),
        .addr(addr),.wdata(wdata),.wren(wren),.wstrb(wstrb),.rdata(rdata));
    always #5 clk=~clk;
    initial begin
        $dumpfile("runs/wave.vcd");
        $dumpvars(0,dut);
        $dumpvars(1,tb_c_boot);
        repeat(4) @(negedge clk);
        rst_n=1;
    end
    // Pre-NBA observations are the actual values sampled by RF/RAM on this edge.
    always @(posedge clk) if (rst_n) begin
        cycle=cycle+1;
        if (cycle > 100000) $fatal(1,"TIMEOUT cycle limit");
        if ((^{dut.mem_valid,dut.mem_reg_write,wren,dut.ex_valid,
              dut.ex_mem_to_reg,dut.id_valid,dut.stall_if,dut.control_flush,stopped}) === 1'bx)
            $fatal(1,"UNKNOWN active control");
        if (dut.stall_if) stalls=stalls+1;
        if (dut.control_flush) flushes=flushes+1;
        if (dut.mem_valid && dut.mem_reg_write) begin
            if ((^{dut.mem_rd,dut.wb_write_data}) === 1'bx) $fatal(1,"UNKNOWN WB");
            if (dut.mem_rd != 0) $display("WB|%0d|%0d|%08x",cycle,dut.mem_rd,dut.wb_write_data);
        end
        if (dut.id_valid && !dut.eei_hold) begin
            if ((^{dut.id_pc,dut.forward_rs1,dut.forward_rs2,dut.id_alu_ctrl}) === 1'bx)
                $fatal(1,"UNKNOWN EX data");
            $display("EX|%0d|%08x",cycle,dut.id_pc);
        end
        // No CPU read-enable is invented: only observe its real valid MEM load.
        if (dut.ex_valid && dut.ex_mem_to_reg) begin
            if ((^{addr,rdata,dut.mem_load_data,dut.ex_pc}) === 1'bx) $fatal(1,"UNKNOWN LOAD");
            if (!(addr < 32'h4000 || (addr >= 32'h10000 && addr < 32'h14000)))
                $fatal(1,"MEMORY_PROTOCOL unmapped real load");
            if ((dut.ex_funct3==2 && addr[1:0]!=0) ||
                ((dut.ex_funct3==1 || dut.ex_funct3==5) && addr[0]!=0))
                $fatal(1,"MEMORY_PROTOCOL load alignment");
            $display("READ|%0d|%08x|%08x|%08x|%08x",cycle,dut.ex_pc,addr,rdata,dut.mem_load_data);
        end
        if (wren) begin
            if (!dut.ex_valid || (wstrb === 0)) $fatal(1,"MEMORY_PROTOCOL store validity");
            $display("STORE|%0d|%08x|%08x|%08x|%01x",cycle,dut.ex_pc,addr,wdata,wstrb);
        end
        if (stopped && ((stop_kind !== 2) || (stop_pc !== 32'h68) ||
                        wren || (dut.mem_valid && dut.mem_reg_write)))
            $fatal(1,"STOP_PROTOCOL unexpected stop or side effect");
    end
    always @(negedge clk) if (rst_n && stopped) begin
        hold_edges=hold_edges+1;
        if (hold_edges==4) begin
            regfile_fd=$fopen("runs/registers.hex","w");
            memory_fd=$fopen("runs/ram.hex","w");
            if (!regfile_fd || !memory_fd) $fatal(1,"OUTPUT unable to open final state");
            for(i=0;i<32;i=i+1) $fdisplay(regfile_fd,"%08x",dut.rf.regs[i]);
            for(i=0;i<16384;i=i+1) $fdisplay(memory_fd,"%02x",memory.ram[i]);
            $fclose(regfile_fd); $fclose(memory_fd);
            $display("STOP|%0d|%0d|%08x",cycle,stop_kind,stop_pc);
            $display("METRICS|cycles=%0d|stall=%0d|flush=%0d|stop_hold_edges=%0d|time_ns=%0t",
                     cycle,stalls,flushes,hold_edges,$time);
            $display("SIMULATION_ENDED_NOT_YET_FUNCTIONAL_PASS");
            $finish;
        end
    end
endmodule
