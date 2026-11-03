`timescale 1ns/1ps

// =====================================================================
// uart_tx.v
// 8N1 UART transmitter core for PERIPH-CORE-0.1-DRAFT.
//
// Scope:
//   - one byte at a time, LSB first, no FIFO, no parity, no flow control
//   - CLKS_PER_BIT integer N >= 8; no fractional divider
//   - registered tx_ready / tx_busy; ready and busy are complementary
//     outside reset (both are 0 during asynchronous reset)
//
// Timing (E = accepted request sampling edge):
//   - start low from E through E+N-1
//   - data bit k begins at E+N+k*N, k=0..7
//   - stop high begins at E+9N and is held for N clocks
//   - tx_ready returns to 1 at E+10N; the next acceptance can occur
//     no earlier than E+10N+1 (registered, non-lookahead ready)
//
// A single-cycle tx_valid pulse while tx_ready=0 is ignored.  A valid
// held across busy is accepted once per actual ready handshake; equal
// data values are not de-duplicated.
// =====================================================================
module uart_tx #(
    parameter integer CLKS_PER_BIT = 16
) (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       tx_valid,
    input  wire [7:0] tx_data,
    output reg        tx_ready,
    output reg        tx_busy,
    output reg        tx
);

    // N=8..234 are the covered configurations.  $clog2(8)=3,
    // $clog2(234)=8; the counter never wraps before the terminal value.
    localparam integer CNT_W = $clog2(CLKS_PER_BIT);

    localparam [1:0] ST_IDLE  = 2'd0,
                     ST_START = 2'd1,
                     ST_DATA  = 2'd2,
                     ST_STOP  = 2'd3;

    reg [1:0]        state;
    reg [CNT_W-1:0]  clk_cnt;
    reg [2:0]        bit_idx;
    reg [7:0]        data_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state    <= ST_IDLE;
            clk_cnt  <= {CNT_W{1'b0}};
            bit_idx  <= 3'd0;
            data_reg <= 8'd0;
            tx       <= 1'b1;
            tx_ready <= 1'b0;
            tx_busy  <= 1'b0;
        end else begin
            case (state)
                ST_IDLE: begin
                    tx      <= 1'b1;
                    tx_busy <= 1'b0;

                    // tx_ready is registered.  Gating on the old ready
                    // value prevents acceptance in the first clock after
                    // reset release, when ready is still 0.
                    if (tx_valid && tx_ready) begin
                        data_reg <= tx_data;
                        tx_ready <= 1'b0;
                        tx_busy  <= 1'b1;
                        tx       <= 1'b0;       // start bit
                        clk_cnt  <= {CNT_W{1'b0}};
                        bit_idx  <= 3'd0;
                        state    <= ST_START;
                    end else begin
                        tx_ready <= 1'b1;
                    end
                end

                ST_START: begin
                    tx_ready <= 1'b0;
                    tx_busy  <= 1'b1;
                    tx       <= 1'b0;

                    if (clk_cnt == CLKS_PER_BIT - 1) begin
                        clk_cnt <= {CNT_W{1'b0}};
                        bit_idx <= 3'd0;
                        tx      <= data_reg[0];
                        state   <= ST_DATA;
                    end else begin
                        clk_cnt <= clk_cnt + 1'b1;
                    end
                end

                ST_DATA: begin
                    tx_ready <= 1'b0;
                    tx_busy  <= 1'b1;

                    if (clk_cnt == CLKS_PER_BIT - 1) begin
                        clk_cnt <= {CNT_W{1'b0}};
                        if (bit_idx == 3'd7) begin
                            tx      <= 1'b1;   // stop bit
                            state   <= ST_STOP;
                        end else begin
                            bit_idx <= bit_idx + 1'b1;
                            tx      <= data_reg[bit_idx + 1'b1];
                        end
                    end else begin
                        clk_cnt <= clk_cnt + 1'b1;
                        tx      <= data_reg[bit_idx];
                    end
                end

                ST_STOP: begin
                    tx_ready <= 1'b0;
                    tx_busy  <= 1'b1;
                    tx       <= 1'b1;

                    if (clk_cnt == CLKS_PER_BIT - 1) begin
                        clk_cnt  <= {CNT_W{1'b0}};
                        state    <= ST_IDLE;
                        tx_ready <= 1'b1;   // E+10N: idle, next accept E+10N+1
                        tx_busy  <= 1'b0;
                        tx       <= 1'b1;
                    end else begin
                        clk_cnt <= clk_cnt + 1'b1;
                    end
                end

                default: begin
                    // Defensive recovery for an unexpected state encoding.
                    state    <= ST_IDLE;
                    clk_cnt  <= {CNT_W{1'b0}};
                    bit_idx  <= 3'd0;
                    tx       <= 1'b1;
                    tx_ready <= 1'b0;
                    tx_busy  <= 1'b0;
                end
            endcase
        end
    end

endmodule
