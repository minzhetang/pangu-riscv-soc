`timescale 1ns/1ps

// LOCAL-REGIF-HL2 / 1.0.0
// HL2 extension of the frozen TX/GPIO wrapper.
//
// New, aligned, full-strobe registers in the same 256-byte IO window:
//   0x14  MTIMECMP_LO  (rw, reset all ones)
//   0x18  MTIMECMP_HI  (rw, reset all ones)
//   0x1c  MSIP         (rw, reset 0; bit 0 drives machine software IRQ)
//
// Existing TX/GPIO addresses and the original error contract are unchanged.
// Reads are combinational and side-effect free.  Only aligned 32-bit writes
// with strobe 4'b1111 are accepted; every other request raises io_wr_error
// and has no register side effect.
module local_regif_hl2 #(
    parameter integer CLKS_PER_BIT = 16
) (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        io_sel,
    input  wire        io_wr_en,
    input  wire [7:0]  io_addr,
    input  wire [31:0] io_wdata,
    input  wire [3:0]  io_wstrb,
    input  wire [7:0]  gpio_in_async,
    output wire [31:0] io_rdata,
    output wire        io_wr_error,
    output wire        uart_tx,
    output wire [7:0]  gpio_out,
    output wire [63:0] mtimecmp,
    output wire [31:0] msip
);

    wire        tx_ready;
    wire        tx_busy;
    wire        tx;
    wire [7:0]  gpio_in_sync;

    wire addr_aligned = (io_addr[1:0] == 2'b00);
    wire strobe_full  = (io_wstrb == 4'b1111);
    wire request      = rst_n && io_sel && io_wr_en;

    wire addr_tx      = (io_addr == 8'h00);
    wire addr_gpio    = (io_addr == 8'h0c);
    wire addr_cmp_lo  = (io_addr == 8'h14);
    wire addr_cmp_hi  = (io_addr == 8'h18);
    wire addr_msip    = (io_addr == 8'h1c);

    wire tx_accept   = request && addr_tx     && addr_aligned && strobe_full && tx_ready;
    wire gpio_accept = request && addr_gpio   && addr_aligned && strobe_full;
    wire cmp_lo_accept = request && addr_cmp_lo && addr_aligned && strobe_full;
    wire cmp_hi_accept = request && addr_cmp_hi && addr_aligned && strobe_full;
    wire msip_accept   = request && addr_msip   && addr_aligned && strobe_full;
    wire write_ok    = tx_accept || gpio_accept ||
                       cmp_lo_accept || cmp_hi_accept || msip_accept;

    assign io_wr_error = request && !write_ok;

    // Frozen TX core: direct request, no extra pipeline or queue.
    assign uart_tx = tx;
    uart_tx #(.CLKS_PER_BIT(CLKS_PER_BIT)) u_tx (
        .clk      (clk),
        .rst_n    (rst_n),
        .tx_valid (tx_accept),
        .tx_data  (io_wdata[7:0]),
        .tx_ready (tx_ready),
        .tx_busy  (tx_busy),
        .tx       (tx)
    );

    // Frozen GPIO core: fixed 8-bit width, full-width write.
    gpio_core #(.W(8)) u_gpio (
        .clk           (clk),
        .rst_n         (rst_n),
        .gpio_wr_en    (gpio_accept),
        .gpio_wdata    (io_wdata[7:0]),
        .gpio_in_async (gpio_in_async),
        .gpio_out      (gpio_out),
        .gpio_in_sync  (gpio_in_sync)
    );

    // Timer compare and software-interrupt pending registers.
    // Reset mtimecmp high so the timer comparator cannot fire at reset.
    reg [31:0] mtimecmp_lo_q;
    reg [31:0] mtimecmp_hi_q;
    reg [31:0] msip_q;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mtimecmp_lo_q <= 32'hffff_ffff;
            mtimecmp_hi_q <= 32'hffff_ffff;
            msip_q        <= 32'h0000_0000;
        end else begin
            if (cmp_lo_accept) mtimecmp_lo_q <= io_wdata;
            if (cmp_hi_accept) mtimecmp_hi_q <= io_wdata;
            if (msip_accept)   msip_q        <= io_wdata;
        end
    end

    assign mtimecmp = {mtimecmp_hi_q, mtimecmp_lo_q};
    assign msip     = msip_q;

    reg [31:0] rdata;
    always @* begin
        rdata = 32'h00000000;
        if (rst_n && io_sel && addr_aligned) begin
            case (io_addr)
                8'h00: rdata = 32'h00000000;                       // TXDATA reads 0
                8'h08: rdata = {31'b0, tx_ready};                  // STATUS
                8'h0c: rdata = {24'b0, gpio_out};                  // GPIO_OUT
                8'h10: rdata = {24'b0, gpio_in_sync};              // GPIO_IN
                8'h14: rdata = mtimecmp_lo_q;                      // MTIMECMP_LO
                8'h18: rdata = mtimecmp_hi_q;                      // MTIMECMP_HI
                8'h1c: rdata = msip_q;                             // MSIP
                default: rdata = 32'h00000000;                     // reserved
            endcase
        end
    end

    assign io_rdata = rdata;

    // Simulation-only illegal parameter rejection.
    initial begin
        if (CLKS_PER_BIT < 8) begin
            $display("REGIF_ILLEGAL_CLKS_PER_BIT=%0d minimum=8", CLKS_PER_BIT);
            $finish;
        end
    end

    wire unused_tx_busy = tx_busy;
    wire unused_gpio_sync = gpio_in_sync;

endmodule
