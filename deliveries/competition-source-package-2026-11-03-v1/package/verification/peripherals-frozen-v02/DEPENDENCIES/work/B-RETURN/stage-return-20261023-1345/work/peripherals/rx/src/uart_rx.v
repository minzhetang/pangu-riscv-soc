`timescale 1ns/1ps
// UART 8N1 receiver core, PERIPH-CORE-RX-1.0 v1.0.0.
// Single clock, two-stage synchronizer, one-byte mailbox.
// The main logic reads only the pre-edge second synchronizer stage.
module uart_rx #(
    parameter integer CLKS_PER_BIT = 16
) (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       rx,
    input  wire       rx_ready,
    input  wire       clear_errors,
    output reg        rx_valid,
    output reg  [7:0] rx_data,
    output reg        frame_error,
    output reg        overrun
);

    localparam integer N    = CLKS_PER_BIT;
    localparam integer HALF = N / 2;
    localparam integer CNT_W = $clog2(9 * N + HALF + 4);

    localparam [2:0] S_IDLE      = 3'd0;
    localparam [2:0] S_START     = 3'd1;
    localparam [2:0] S_DATA      = 3'd2;
    localparam [2:0] S_STOP      = 3'd3;
    localparam [2:0] S_WAIT_HIGH = 3'd4;

    reg [2:0]         state;
    reg [CNT_W-1:0]   phase_cnt;
    reg [2:0]         data_idx;
    reg [7:0]         data_capture;

    reg               rx_meta;
    reg               rx_sync;
    reg               rx_sync_prev;
    reg [1:0]         warmup_cnt;
    reg               armed;

    reg               fe_event;
    reg               ov_event;

    // N<8 is an illegal configuration.  Reject it explicitly at simulation
    // start instead of silently clamping or truncating a counter.
    initial begin
        if (N < 8) begin
            $display("RX_ILLEGAL_CLKS_PER_BIT=%0d minimum=8", N);
            $finish;
        end
    end

    // Exactly two synchronizer stages.  Both async-reset to the idle-high
    // value; the receiver only reads rx_sync's pre-edge value.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_meta      <= 1'b1;
            rx_sync      <= 1'b1;
            rx_sync_prev <= 1'b1;
        end else begin
            rx_meta      <= rx;
            rx_sync      <= rx_meta;
            rx_sync_prev <= rx_sync;
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state        <= S_IDLE;
            phase_cnt    <= {CNT_W{1'b0}};
            data_idx     <= 3'd0;
            data_capture <= 8'h00;
            rx_valid     <= 1'b0;
            rx_data      <= 8'h00;
            frame_error  <= 1'b0;
            overrun      <= 1'b0;
            warmup_cnt   <= 2'd0;
            armed        <= 1'b0;
            fe_event     <= 1'b0;
            ov_event     <= 1'b0;
        end else begin
            fe_event = 1'b0;
            ov_event = 1'b0;

            // Reset release: two sync warmup edges, then arm only after the
            // pre-edge second stage is actually high.  The same edge does not
            // count as a falling start.
            if (!armed) begin
                if (warmup_cnt < 2'd2)
                    warmup_cnt <= warmup_cnt + 2'd1;
                else if (rx_sync)
                    armed <= 1'b1;
            end

            // A synchronous consumer may consume an existing byte on any
            // edge without a completion.  Completion cases below override
            // this default where the contract requires hold/replace.
            if (rx_valid && rx_ready)
                rx_valid <= 1'b0;

            case (state)
                S_IDLE: begin
                    phase_cnt <= {CNT_W{1'b0}};
                    data_idx  <= 3'd0;
                    if (armed && rx_sync_prev && !rx_sync) begin
                        state     <= S_START;
                        phase_cnt <= {CNT_W{1'b0}};
                    end
                end

                S_START: begin
                    phase_cnt <= phase_cnt + {{(CNT_W-1){1'b0}}, 1'b1};
                    if (phase_cnt == (HALF - 1)) begin
                        if (rx_sync) begin
                            // False/short start: no valid, no new error.
                            state <= S_IDLE;
                        end else begin
                            state     <= S_DATA;
                            phase_cnt <= {CNT_W{1'b0}};
                            data_idx  <= 3'd0;
                        end
                    end
                end

                S_DATA: begin
                    phase_cnt <= phase_cnt + {{(CNT_W-1){1'b0}}, 1'b1};
                    if (phase_cnt == (N - 1 + data_idx * N)) begin
                        data_capture[data_idx] <= rx_sync;
                        if (data_idx == 3'd7) begin
                            state     <= S_STOP;
                            phase_cnt <= {CNT_W{1'b0}};
                        end else begin
                            data_idx <= data_idx + 3'd1;
                        end
                    end
                end

                S_STOP: begin
                    phase_cnt <= phase_cnt + {{(CNT_W-1){1'b0}}, 1'b1};
                    if (phase_cnt == (N - 1)) begin
                        if (rx_sync) begin
                            // Good stop.  Publish in this edge's NBA; never
                            // push the update to an extra S+1 pipeline cycle.
                            if (!rx_valid) begin
                                rx_valid <= 1'b1;
                                rx_data  <= data_capture;
                            end else if (rx_ready) begin
                                // Same-edge consume old + replace new.
                                rx_valid <= 1'b1;
                                rx_data  <= data_capture;
                            end else begin
                                // Full and not consumed: keep old, drop new.
                                ov_event = 1'b1;
                            end
                            state <= S_IDLE;
                        end else begin
                            // Bad stop: sticky frame_error, no mailbox write.
                            fe_event = 1'b1;
                            state    <= S_WAIT_HIGH;
                        end
                    end
                end

                S_WAIT_HIGH: begin
                    phase_cnt <= {CNT_W{1'b0}};
                    if (rx_sync)
                        state <= S_IDLE;
                end

                default: begin
                    state     <= S_IDLE;
                    phase_cnt <= {CNT_W{1'b0}};
                end
            endcase

            // Per-bit new-error priority; clear_errors clears only bits with
            // no new event on this edge.  Reset has already taken priority.
            frame_error <= fe_event | (frame_error & ~clear_errors);
            overrun     <= ov_event | (overrun     & ~clear_errors);
        end
    end

endmodule
