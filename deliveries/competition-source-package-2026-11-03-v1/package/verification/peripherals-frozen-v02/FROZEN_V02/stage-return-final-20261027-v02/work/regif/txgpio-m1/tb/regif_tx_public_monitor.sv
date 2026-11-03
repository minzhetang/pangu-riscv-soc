`timescale 1ns/1ps

// Shared public uart_tx serial capture.  It observes only clk/rst_n/uart_tx and
// does not use tx_ready or any stimulus-task byte.  Used by the formal wrapper
// TB and by the synthetic capture-path negative TB.
module regif_tx_public_monitor #(
    parameter integer N = 16
) (
    input wire clk,
    input wire rst_n,
    input wire uart_tx
);
    localparam integer HALF = N / 2;

    integer cycle_count;
    integer tx_start_count;
    integer tx_complete_count;
    integer tx_cancel_count;
    integer tx_bad_stop_count;
    integer tx_bad_start_count;
    integer active;
    integer cnt;
    integer bit_idx;
    integer prev;
    reg [7:0] shift;
    reg stop_sample_good;
    reg [7:0] complete_data [0:31];

    initial begin
        cycle_count = 0;
        tx_start_count = 0;
        tx_complete_count = 0;
        tx_cancel_count = 0;
        tx_bad_stop_count = 0;
        tx_bad_start_count = 0;
        active = 0;
        cnt = 0;
        bit_idx = 0;
        prev = 1;
        shift = 8'h00;
        stop_sample_good = 1'b0;
    end

    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
        prev <= uart_tx;
        if (!rst_n) begin
            if (active == 1) begin
                tx_cancel_count = tx_cancel_count + 1;
                $display("REGIF_TX_FRAME event=CANCEL idx=%0d edge=%0d observed_edge=%0d", tx_cancel_count, cycle_count, cycle_count + 1);
            end
            active <= 0;
            cnt <= 0;
            bit_idx <= 0;
            shift <= 8'h00;
            stop_sample_good <= 1'b0;
        end else if (active == 1) begin
            cnt <= cnt + 1;
            if (cnt == HALF - 1) begin
                if (uart_tx !== 1'b0) begin
                    tx_bad_start_count = tx_bad_start_count + 1;
                    $display("REGIF_TX_FRAME event=BAD_START edge=%0d observed_edge=%0d", cycle_count, cycle_count + 1);
                end
            end
            if (cnt == N + HALF - 1 + bit_idx * N) begin
                shift[bit_idx] <= uart_tx;
                bit_idx <= bit_idx + 1;
            end
            if (cnt == 9*N + HALF - 1)
                stop_sample_good <= (uart_tx === 1'b1);
            if (cnt == 10*N - 1) begin
                active <= 0;
                if (stop_sample_good === 1'b1) begin
                    complete_data[tx_complete_count] = shift;
                    tx_complete_count = tx_complete_count + 1;
                    $display("REGIF_TX_FRAME event=COMPLETE idx=%0d edge=%0d data=%02x observed_edge=%0d",
                             tx_complete_count, cycle_count, shift, cycle_count + 1);
                end else begin
                    tx_bad_stop_count = tx_bad_stop_count + 1;
                    $display("REGIF_TX_FRAME event=BAD_STOP idx=%0d edge=%0d data=%02x observed_edge=%0d",
                             tx_bad_stop_count, cycle_count, shift, cycle_count + 1);
                end
            end
        end else if (prev === 1'b1 && uart_tx === 1'b0) begin
            active <= 1;
            cnt <= 0;
            bit_idx <= 0;
            shift <= 8'h00;
            stop_sample_good <= 1'b0;
            tx_start_count = tx_start_count + 1;
            $display("REGIF_TX_FRAME event=START edge=%0d observed_edge=%0d", cycle_count, cycle_count + 1);
        end
    end
endmodule
