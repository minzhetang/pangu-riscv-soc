`timescale 1ns/1ps
module soc_top #(parameter integer CLKS_PER_BIT=16)(
    input wire clk,rst_n,input wire [7:0] gpio_in_async,
    output wire uart_tx,output wire [7:0] gpio_out,
    output wire stopped,output wire [1:0] stop_kind,output wire [31:0] stop_pc,
    output wire write_error
);
    wire [31:0] pc,inst,address /* synthesis PAP_MARK_DEBUG="true" */,wdata,rdata,mem_rdata,io_rdata,io_wdata;
    wire wren /* synthesis PAP_MARK_DEBUG="true" */,ram_we,io_sel,io_we,io_error,invalid_write;
    wire [63:0] timer_ticks;
    wire [3:0] wstrb,ram_strobe,io_strobe;wire [7:0] io_addr;
    cycle_counter64 timer(.clk(clk),.rst_n(rst_n),.ticks(timer_ticks));
    cpu #(.SYNC_MEMORY(1)) cpu_core(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),
        .mem_addr(address),.mem_wdata(wdata),.mem_wren(wren),.mem_wstrb(wstrb),.mem_rdata(rdata),
        .eei_stop_valid(stopped),.eei_stop_kind(stop_kind),.eei_stop_pc(stop_pc));
    memory_model #(.LATENCY(1),.CASE(0)) storage(.clk(clk),.rst_n(rst_n),.pc(pc),.inst(inst),
        .addr(address),.wdata(wdata),.wren(ram_we),.wstrb(ram_strobe),.rdata(mem_rdata));
    soc_data_adapter route(.address(address),.write_data(wdata),.write_enable(wren),.write_strobe(wstrb),
        .memory_read_data(mem_rdata),.io_read_data(io_rdata),.timer_ticks(timer_ticks),
        .io_write_error(io_error),.cpu_read_data(rdata),
        .memory_write_enable(ram_we),.memory_write_strobe(ram_strobe),.io_select(io_sel),.io_write_enable(io_we),
        .io_address(io_addr),.io_write_data(io_wdata),.io_write_strobe(io_strobe),.invalid_write(invalid_write),.write_error(write_error));
    local_regif_txgpio_m1 #(.CLKS_PER_BIT(CLKS_PER_BIT)) peripherals(
        .clk(clk),.rst_n(rst_n),.io_sel(io_sel),.io_wr_en(io_we),.io_addr(io_addr),.io_wdata(io_wdata),
        .io_wstrb(io_strobe),.gpio_in_async(gpio_in_async),.io_rdata(io_rdata),.io_wr_error(io_error),
        .uart_tx(uart_tx),.gpio_out(gpio_out));
endmodule
