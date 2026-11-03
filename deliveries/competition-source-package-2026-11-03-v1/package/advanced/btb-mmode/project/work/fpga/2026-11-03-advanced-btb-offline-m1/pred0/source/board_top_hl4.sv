`timescale 1ns/1ps
// MES2L676-100HP board wrapper for the HL4 candidate.
// KEY0 reset, KEY1..4 GPIO low nibble, eight LEDs, TX only.
// External ports match the frozen HL2 pin constraints.
module board_top_hl4 (
    input  wire       clk,
    input  wire [4:0] key_n,
    output wire       uart_tx,
    output wire [7:0] led
);
    wire sys_rst_n;
    wire [7:0] gpio_keys = {4'b0000, ~key_n[4:1]};

    wire        write_error;
    wire        timer_irq, soft_irq;
    wire [31:0] dbg_mepc, dbg_mcause, dbg_mtval, dbg_mstatus;
    wire        dbg_trap;
    wire [31:0] dbg_trap_pc;
    wire [31:0] dbg_sepc, dbg_scause, dbg_stval, dbg_sstatus;
    wire [1:0]  dbg_priv;

    board_reset_sync reset_sync (
        .clk(clk), .key0_n(key_n[0]), .sys_rst_n(sys_rst_n)
    );

    soc_top_hl4 #(
        .CLKS_PER_BIT   (234),
        .BTB_INDEX_BITS (6),
        .BTB_ENABLE     (0),
        .SYNC_MEMORY    (1)
    ) soc (
        .clk(clk), .rst_n(sys_rst_n),
        .gpio_in_async(gpio_keys),
        .uart_tx(uart_tx), .gpio_out(led),
        .write_error(write_error),
        .timer_irq(timer_irq), .soft_irq(soft_irq),
        .dbg_mepc(dbg_mepc), .dbg_mcause(dbg_mcause),
        .dbg_mtval(dbg_mtval), .dbg_mstatus(dbg_mstatus),
        .dbg_trap(dbg_trap), .dbg_trap_pc(dbg_trap_pc),
        .dbg_sepc(dbg_sepc), .dbg_scause(dbg_scause),
        .dbg_stval(dbg_stval), .dbg_sstatus(dbg_sstatus),
        .dbg_priv(dbg_priv)
    );

    // Observability is intentionally left unused at the board boundary.
    wire unused_write_error = write_error;
    wire unused_timer_irq   = timer_irq;
    wire unused_soft_irq    = soft_irq;
    wire unused_dbg_mepc    = |dbg_mepc;
    wire unused_dbg_mcause  = |dbg_mcause;
    wire unused_dbg_mtval   = |dbg_mtval;
    wire unused_dbg_mstatus = |dbg_mstatus;
    wire unused_dbg_trap    = dbg_trap;
    wire unused_dbg_trap_pc = |dbg_trap_pc;
    wire unused_dbg_sepc    = |dbg_sepc;
    wire unused_dbg_scause  = |dbg_scause;
    wire unused_dbg_stval   = |dbg_stval;
    wire unused_dbg_sstatus = |dbg_sstatus;
    wire unused_dbg_priv    = |dbg_priv;

endmodule
