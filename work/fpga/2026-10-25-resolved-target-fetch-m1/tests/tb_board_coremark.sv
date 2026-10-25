`timescale 1ns/1ps
module tb_board_coremark #(parameter integer PHASE_ADDR=0);
    localparam integer N=234;
    integer key_pattern=0;reg [4:0] key_n=0;
    integer serial_fd=0;
    reg clk=0;wire rst_n=board_dut.sys_rst_n;
    wire [7:0] gpio_in_async={4'b0,~key_n[4:1]};
    wire uart_tx,stopped,write_error;wire [7:0] gpio_out;wire [1:0] stop_kind;wire [31:0] stop_pc;
    integer cycle=0,tail=0,limit=6000000,events_fd,bus_fd,rf_fd,ram_fd,i;
    integer advances=0,stall=0,flush=0,wave_until=1024;reg dumping=1;
    reg [31:0] pre_addr,pre_wdata,pre_io_data,pre_phase=0;
    reg [3:0] pre_strobe;reg pre_write,pre_io_error,pre_tx,pre_gpio_accept;
    reg [7:0] pre_gpio_out,pre_gpio_async;reg [63:0] pre_ticks;
    GTP_GRS GRS_INST(.GRS_N(1'b1));board_top board_dut(.clk(clk),.key_n(key_n),.uart_tx(uart_tx),.led(gpio_out));
    assign stopped=board_dut.soc.stopped;
    assign write_error=board_dut.soc.write_error;
    assign stop_kind=board_dut.soc.stop_kind;
    assign stop_pc=board_dut.soc.stop_pc;
    wire gpio_actual_accept=board_dut.soc.peripherals.u_gpio.gpio_wr_en;
    wire [31:0] monitor_pc=board_dut.soc.pc,monitor_address=board_dut.soc.address,monitor_read=board_dut.soc.rdata;
    wire [63:0] monitor_ticks=board_dut.soc.timer_ticks;
    wire monitor_advance=board_dut.soc.cpu_core.pipeline_advance,monitor_phase=board_dut.soc.cpu_core.memory_phase;
    integer fetch_fd=0,pref_seen=0,pref_class=0,pref_cycle=0;
    reg pref_req,pref_hit,pref_redir;reg [31:0] pref_target,pref_pc,pref_id_pc;
    reg [31:0] pref_settled_cycle=0;
    wire monitor_pref_req=board_dut.soc.cpu_core.redirect_request,monitor_pref_hit=board_dut.soc.cpu_core.redirect_fetch_hit;
    wire monitor_pref_valid=board_dut.soc.cpu_core.fetch_redirect_valid;
    wire [31:0] monitor_pref_tag=board_dut.soc.cpu_core.fetch_redirect_pc,monitor_target=board_dut.soc.cpu_core.redirect_target;
    wire [31:0] monitor_id_pc=board_dut.soc.cpu_core.id_pc,monitor_pc_reg=board_dut.soc.cpu_core.pc_reg;
    wire [31:0] monitor_if_pc=board_dut.soc.cpu_core.if_pc,monitor_if_inst=board_dut.soc.cpu_core.if_inst,monitor_inst=board_dut.soc.inst;
    wire monitor_if_valid=board_dut.soc.cpu_core.if_valid,monitor_id_valid=board_dut.soc.cpu_core.id_valid;
    // PRE signals are sampled before the edge, monitor_* after NBA at settled marker.
    always @(posedge clk)if(rst_n)begin
        pref_cycle=monitor_ticks+1;pref_req=monitor_pref_req;pref_hit=monitor_pref_hit;
        pref_target=monitor_target;pref_pc=monitor_pc;pref_id_pc=monitor_id_pc;
        pref_redir=board_dut.soc.cpu_core.pipeline_advance&&board_dut.soc.cpu_core.id_valid&&!board_dut.soc.cpu_core.eei_hold&&board_dut.soc.cpu_core.control_flush;
        if(pref_cycle%2==1&&pref_req)$fdisplay(fetch_fd,"REQ|%0d|%08x|%08x",pref_cycle,pref_id_pc,pref_pc);
        if(pref_redir)$fdisplay(fetch_fd,"REDIR|%0d|%08x|%08x|%0d|%08x|%08x",pref_cycle,pref_id_pc,pref_target,pref_hit,monitor_pref_tag,monitor_inst);
        #1;
        if(pref_cycle%2==1&&pref_req)$fdisplay(fetch_fd,"SAMPLE|%0d|%08x|%08x|%08x",pref_cycle,pref_id_pc,monitor_pref_tag,monitor_inst);
        if(pref_redir)$fdisplay(fetch_fd,"APPLY|%0d|%08x|%0d|%08x|%08x|%0d|%08x|%08x|%0d",pref_cycle,pref_id_pc,pref_hit,pref_target,monitor_pc_reg,monitor_if_valid,monitor_if_pc,monitor_if_inst,monitor_id_valid);
        pref_settled_cycle=pref_cycle;
    end
    // 37.037 ns period at 1 ps precision, nominal 27 MHz.
    always begin #18.518;clk=1;#18.519;clk=0;end
    initial begin
        if(!$value$plusargs("MAX_CYCLES=%d",limit))limit=6000000;
        if(N!=16&&N!=234)$fatal(1,"UNAPPROVED_N");
        if(limit<1||limit>6000000)$fatal(1,"BUDGET_BOUNDS");
        events_fd=$fopen("trace.log","w");bus_fd=$fopen("bus.log","w");
        serial_fd=$fopen("uart-pins.log","w");if(!serial_fd)$fatal(1,"PIN_LOG_OPEN");
        fetch_fd=$fopen("fetch.log","w");if(!fetch_fd)$fatal(1,"FETCH_LOG_OPEN");
        if(!events_fd||!bus_fd)$fatal(1,"TRACE_OPEN");
        $dumpfile("wave.vcd");$dumpvars(1,tb_board_coremark);$dumpvars(1,board_dut);
        key_pattern=0;
        key_n[4:1]=~key_pattern[3:0];key_n[0]=0;
        repeat(4)@(negedge clk);key_n[0]=1;
    end
    // Continuous actual pin transitions, independent of native VCD windows.
    always @(uart_tx or rst_n) begin
        #0.001;
        if(serial_fd) $fdisplay(serial_fd,"PIN|%0t|%0d|%b|%b|%b",$realtime,cycle,clk,rst_n,uart_tx);
    end
    always @(posedge clk)if(rst_n)begin
        cycle=cycle+1;if(cycle>limit)$fatal(1,"SYSTEM_TIMEOUT");
        pre_addr=board_dut.soc.address;pre_wdata=board_dut.soc.wdata;pre_io_data=board_dut.soc.rdata;
        pre_write=board_dut.soc.wren;pre_strobe=board_dut.soc.wstrb;pre_io_error=board_dut.soc.io_error;
        pre_ticks=board_dut.soc.timer_ticks;
        pre_tx=uart_tx;pre_gpio_out=gpio_out;pre_gpio_async=gpio_in_async;pre_gpio_accept=gpio_actual_accept;
        if(pre_ticks!==(64'(cycle)-1))$fatal(1,"COUNTER_PRE_EDGE");
        if((^{board_dut.soc.cpu_core.pipeline_advance,board_dut.soc.wren,board_dut.soc.io_sel,board_dut.soc.io_error,uart_tx,gpio_out,stopped,write_error})===1'bx)
            $fatal(1,"UNKNOWN_SYSTEM_CONTROL");
        if(write_error)$fatal(1,"SYSTEM_WRITE_REJECTED");
        if(board_dut.soc.ram_we&&board_dut.soc.io_sel)$fatal(1,"RAM_IO_OVERLAP");
        if(monitor_pref_req)begin
            pref_class=board_dut.soc.cpu_core.id_jump?(board_dut.soc.cpu_core.id_alu_src?9:8):board_dut.soc.cpu_core.id_funct3;
            if((pref_seen&(1<<pref_class))==0)begin
                pref_seen=pref_seen|(1<<pref_class);if(wave_until<cycle+16)wave_until=cycle+16;
            end
        end
        if(PHASE_ADDR!=0&&pre_write&&pre_addr==PHASE_ADDR)begin
            pre_phase=pre_wdata;wave_until=cycle+256;
        end
        if((cycle<=wave_until||pre_addr==32'h20000100||pre_addr==32'h20000104||stopped)&&!dumping)begin $dumpon;dumping=1;end
        if(cycle>wave_until&&pre_addr!=32'h20000100&&pre_addr!=32'h20000104&&!stopped&&dumping)begin $dumpoff;dumping=0;end
        if(board_dut.soc.cpu_core.pipeline_advance)begin
            advances=advances+1;if(board_dut.soc.cpu_core.stall_if)stall=stall+1;if(board_dut.soc.cpu_core.flush_if)flush=flush+1;
            if(board_dut.soc.cpu_core.id_valid&&!board_dut.soc.cpu_core.eei_hold)$fdisplay(events_fd,"EX|%0d|%08x",cycle,board_dut.soc.cpu_core.id_pc);
            if(board_dut.soc.cpu_core.ex_valid&&board_dut.soc.cpu_core.ex_mem_to_reg)
                $fdisplay(events_fd,"READ|%0d|%08x|%08x|%08x|%08x",cycle,board_dut.soc.cpu_core.ex_pc,board_dut.soc.address,board_dut.soc.rdata,board_dut.soc.cpu_core.mem_load_data);
            if(!board_dut.soc.cpu_core.stall_if&&!board_dut.soc.cpu_core.flush_if&&!board_dut.soc.cpu_core.eei_hold&&
                (board_dut.soc.pc>=32'h8000||board_dut.soc.inst!==board_dut.soc.storage.rom[board_dut.soc.pc>>2]))$fatal(1,"FETCH_MISMATCH");
        end
        if(board_dut.soc.cpu_core.rf.we&&board_dut.soc.cpu_core.mem_rd!=0)$fdisplay(events_fd,"WB|%0d|%0d|%08x",cycle,board_dut.soc.cpu_core.mem_rd,board_dut.soc.cpu_core.wb_write_data);
        if(board_dut.soc.wren)begin
            if(board_dut.soc.cpu_core.pipeline_advance||!board_dut.soc.cpu_core.ex_valid)$fatal(1,"STORE_PHASE");
            $fdisplay(events_fd,"STORE|%0d|%08x|%08x|%08x|%01x",cycle,board_dut.soc.cpu_core.ex_pc,board_dut.soc.address,board_dut.soc.wdata,board_dut.soc.wstrb);
        end
        if(stopped&&(board_dut.soc.wren||(board_dut.soc.cpu_core.rf.we&&board_dut.soc.cpu_core.mem_rd!=0)))$fatal(1,"STOP_SIDE_EFFECT");
        #1;if(board_dut.soc.timer_ticks!==64'(cycle))$fatal(1,"COUNTER_POST_EDGE");
        // Sparse bus: every IO address or actual low serial level is retained.
        // Omitted serial samples are high; omitted bus requests cannot select IO.
        if(pre_addr[31:8]==24'h200000||pre_addr[31:3]==29'h04000020||!pre_tx||!uart_tx||cycle<=16||stopped)
            $fdisplay(bus_fd,"EDGE|%0d|%02x|%08x|%0d|%08x|%01x|%08x|%0d|%0d|%02x|%0d|%02x|%0d|%0d|%016x|%016x",
                cycle,pre_gpio_async,pre_addr,pre_write,pre_wdata,pre_strobe,pre_io_data,pre_io_error,
                pre_tx,pre_gpio_out,uart_tx,gpio_out,pre_gpio_accept,stopped,pre_ticks,board_dut.soc.timer_ticks);
    end
    always @(negedge clk)if(rst_n&&stopped)begin
        tail=tail+1;if(tail==32)begin
            rf_fd=$fopen("registers.hex","w");ram_fd=$fopen("ram.hex","w");
            if(!rf_fd||!ram_fd)$fatal(1,"OUTPUT_OPEN");
            for(i=0;i<32;i=i+1)$fdisplay(rf_fd,"%08x",board_dut.soc.cpu_core.rf.regs[i]);
            for(i=0;i<32768;i=i+1)$fdisplay(ram_fd,"%02x",(board_dut.soc.storage.ram[i>>2]>>((i%4)*8))&255);
            $fclose(rf_fd);$fclose(ram_fd);$fclose(events_fd);$fclose(bus_fd);$fclose(serial_fd);$fclose(fetch_fd);
            $display("METRICS|physical=%0d|advances=%0d|stall=%0d|flush=%0d|tail=%0d",cycle,advances,stall,flush,tail);
            $display("STOP|%0d|%08x",stop_kind,stop_pc);$display("SYSTEM_ENDED_NOT_FUNCTIONAL_PASS");$finish;
        end
    end
endmodule
