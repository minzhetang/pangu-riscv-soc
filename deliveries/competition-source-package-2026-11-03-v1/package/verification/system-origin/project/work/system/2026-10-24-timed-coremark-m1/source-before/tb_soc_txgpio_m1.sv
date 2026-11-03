`timescale 1ns/1ps
// CANDIDATE, NOT_RUN until B intake and actual GPIO acceptance net review.
module tb_soc_txgpio_m1 #(parameter integer N=16);
    reg clk=0,rst_n=0;reg [7:0] gpio_in_async=0;
    wire uart_tx,stopped,write_error;wire [7:0] gpio_out;
    wire [1:0] stop_kind;wire [31:0] stop_pc;
    integer cycle=0,tail=0,limit=100000,events_fd,bus_fd,rf_fd,ram_fd,i;
    integer advances=0,stall=0,flush=0;
    reg [31:0] pre_addr,pre_wdata,pre_io_data;
    reg [3:0] pre_strobe;
    reg pre_write,pre_io_error,pre_tx,pre_gpio_accept;
    reg [7:0] pre_gpio_out,pre_gpio_async;
    GTP_GRS GRS_INST(.GRS_N(1'b1));
    soc_top #(.CLKS_PER_BIT(N)) dut(.*);
`ifdef B_GPIO_ACCEPT_PATH
    wire gpio_actual_accept=`B_GPIO_ACCEPT_PATH;
`else
    wire gpio_actual_accept=1'bx;
    initial $fatal(1,"B GPIO actual accept observation is NOT yet reviewed/bound");
`endif
    wire [31:0] monitor_pc=dut.pc,monitor_address=dut.address,monitor_read=dut.rdata;
    wire monitor_advance=dut.cpu_core.pipeline_advance,monitor_phase=dut.cpu_core.memory_phase;
    always #5 clk=~clk;
    initial begin
        if(!$value$plusargs("MAX_CYCLES=%d",limit))limit=100000;
        if(N!=16 && N!=234)$fatal(1,"unapproved N");
        if(limit<1 || limit>1000000)$fatal(1,"cycle budget bounds");
        events_fd=$fopen("trace.log","w");bus_fd=$fopen("bus.log","w");
        if(!events_fd||!bus_fd)$fatal(1,"trace open failed");
        $dumpfile("wave.vcd");$dumpvars(1,tb_soc_txgpio_m1);
        repeat(4)@(negedge clk);rst_n=1;
    end
    // Frozen external input timing: at E16/E4096 PRE-edge values change.
    always @(negedge clk) if(rst_n)begin
        if(cycle==15)gpio_in_async=8'h3c;
        if(cycle==4095)gpio_in_async=8'hc3;
    end
    always @(posedge clk)if(rst_n)begin
        cycle=cycle+1;if(cycle>limit)$fatal(1,"SYSTEM_TIMEOUT");
        pre_addr=dut.address;pre_wdata=dut.wdata;pre_io_data=dut.io_rdata;
        pre_write=dut.wren;pre_strobe=dut.wstrb;pre_io_error=dut.io_error;
        pre_tx=uart_tx;pre_gpio_out=gpio_out;pre_gpio_async=gpio_in_async;pre_gpio_accept=gpio_actual_accept;
        if((^{dut.cpu_core.pipeline_advance,dut.wren,dut.io_sel,dut.io_error,uart_tx,gpio_out,stopped,write_error})===1'bx)
            $fatal(1,"UNKNOWN_SYSTEM_CONTROL");
        if(write_error)$fatal(1,"SYSTEM_WRITE_REJECTED");
        if(dut.ram_we && dut.io_sel)$fatal(1,"RAM_IO_WRITE_OVERLAP");
        if(dut.cpu_core.pipeline_advance)begin
            advances=advances+1;
            if(dut.cpu_core.stall_if)stall=stall+1;
            if(dut.cpu_core.flush_if)flush=flush+1;
            if(dut.cpu_core.id_valid && !dut.cpu_core.eei_hold)
                $fdisplay(events_fd,"EX|%0d|%08x",cycle,dut.cpu_core.id_pc);
            if(dut.cpu_core.ex_valid && dut.cpu_core.ex_mem_to_reg)
                $fdisplay(events_fd,"READ|%0d|%08x|%08x|%08x|%08x",cycle,dut.cpu_core.ex_pc,dut.address,dut.rdata,dut.cpu_core.mem_load_data);
            if(!dut.cpu_core.stall_if && !dut.cpu_core.flush_if && !dut.cpu_core.eei_hold &&
               (dut.pc>=32'h8000 || dut.inst!==dut.storage.rom[dut.pc>>2]))$fatal(1,"FETCH_PC_WORD_MISMATCH");
        end
        if(dut.cpu_core.rf.we && dut.cpu_core.mem_rd!=0)
            $fdisplay(events_fd,"WB|%0d|%0d|%08x",cycle,dut.cpu_core.mem_rd,dut.cpu_core.wb_write_data);
        if(dut.wren)begin
            if(dut.cpu_core.pipeline_advance || !dut.cpu_core.ex_valid)$fatal(1,"STORE_WRONG_PHASE");
            $fdisplay(events_fd,"STORE|%0d|%08x|%08x|%08x|%01x",cycle,dut.cpu_core.ex_pc,dut.address,dut.wdata,dut.wstrb);
        end
        if(stopped && (dut.wren || (dut.cpu_core.rf.we && dut.cpu_core.mem_rd!=0)))$fatal(1,"STOP_SIDE_EFFECT");
        #1;
        $fdisplay(bus_fd,"EDGE|%0d|%02x|%08x|%0d|%08x|%01x|%08x|%0d|%0d|%02x|%0d|%02x|%0d|%0d",
            cycle,pre_gpio_async,pre_addr,pre_write,pre_wdata,pre_strobe,pre_io_data,pre_io_error,
            pre_tx,pre_gpio_out,uart_tx,gpio_out,pre_gpio_accept,stopped);
    end
    always @(negedge clk)if(rst_n && stopped)begin
        tail=tail+1;
        if(tail==32)begin
            rf_fd=$fopen("registers.hex","w");ram_fd=$fopen("ram.hex","w");
            if(!rf_fd||!ram_fd)$fatal(1,"output open failed");
            for(i=0;i<32;i=i+1)$fdisplay(rf_fd,"%08x",dut.cpu_core.rf.regs[i]);
            for(i=0;i<32768;i=i+1)$fdisplay(ram_fd,"%02x",(dut.storage.ram[i>>2]>>((i%4)*8))&255);
            $fclose(rf_fd);$fclose(ram_fd);$fclose(events_fd);$fclose(bus_fd);
            $display("METRICS|physical=%0d|advances=%0d|stall=%0d|flush=%0d|tail=%0d",cycle,advances,stall,flush,tail);
            $display("STOP|%0d|%08x",stop_kind,stop_pc);
            $display("SYSTEM_ENDED_NOT_FUNCTIONAL_PASS");$finish;
        end
    end
endmodule
