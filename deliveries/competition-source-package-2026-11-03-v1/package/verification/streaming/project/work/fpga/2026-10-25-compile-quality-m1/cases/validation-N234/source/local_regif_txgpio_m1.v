`timescale 1ns/1ps

// LOCAL-REGIF-TXGPIO-M1 / 1.0.0
// Zero-wait TX/GPIO wrapper for the frozen TX and GPIO cores.
//
// Contract boundary:
//   - 8-bit byte offset from the system IO window; no global address decode.
//   - Reads are combinational and side-effect free.
//   - A write request is the set of pre-edge inputs
//       rst_n && io_sel && io_wr_en.
//   - Only aligned (addr[1:0]==00), full-strobe (4'b1111) writes to 0x00
//     (TXDATA) or 0x0c (GPIO_OUT) can succeed.
//   - TX additionally requires pre-edge tx_ready==1; busy writes are rejected.
//   - Every other request asserts io_wr_error and causes no core side effect.
//   - High 24 write-data bits are ignored; GPIO is fixed at 8 bits.
module local_regif_txgpio_m1 #(
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
    output wire [7:0]  gpio_out
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

    // TX and GPIO accept only on the E edge with all pre-edge conditions true.
    wire tx_accept   = request && addr_tx   && addr_aligned && strobe_full && tx_ready;
    wire gpio_accept = request && addr_gpio && addr_aligned && strobe_full;
    wire write_ok    = tx_accept || gpio_accept;

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

    reg [31:0] rdata;
    always @* begin
        rdata = 32'h00000000;
        if (rst_n && io_sel && addr_aligned) begin
            case (io_addr)
                8'h00: rdata = 32'h00000000;                       // TXDATA reads 0
                8'h08: rdata = {31'b0, tx_ready};                  // STATUS
                8'h0c: rdata = {24'b0, gpio_out};                  // GPIO_OUT
                8'h10: rdata = {24'b0, gpio_in_sync};              // GPIO_IN
                default: rdata = 32'h00000000;                     // reserved
            endcase
        end
    end

    assign io_rdata = rdata;

    // Simulation-only illegal parameter rejection.  This is not a hardware
    // reset controller and does not add a new clock domain.
    initial begin
        if (CLKS_PER_BIT < 8) begin
            $display("REGIF_ILLEGAL_CLKS_PER_BIT=%0d minimum=8", CLKS_PER_BIT);
            $finish;
        end
    end

    // The wrapper intentionally has no hidden registered write pulse; the
    // core write enables above are the only side-effect sources.
    wire unused_tx_busy = tx_busy;
    wire unused_gpio_sync = gpio_in_sync;

endmodule
