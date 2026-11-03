`timescale 1ns/1ps

// =====================================================================
// gpio_core.v
// Parameterized GPIO output register + two-stage input synchronizer
// for PERIPH-CORE-0.1-DRAFT.
//
// Scope:
//   - W = 1..32 independent output bits and W independent synchronized
//     input bits
//   - no direction control, no bidirectional inout, no tri-state, no
//     debounce, no interrupt, no read/write bus wrapper
//   - every gpio_wr_en=1 sampling edge writes the complete W-bit
//     gpio_wdata, even if the new value equals the old value
//   - gpio_wr_en=0 holds gpio_out
//   - gpio_in_async passes through two sequential flops to
//     gpio_in_sync; the input is not fed back to gpio_out
//
// Reset is asynchronous active-low.  Both the output register and both
// synchronizer stages are cleared to 0 while rst_n=0.  The TB drives
// asynchronous inputs away from sampling edges; this simulation only
// proves logical two-cycle delay, not physical metastability/MTBF.
// =====================================================================
module gpio_core #(
    parameter integer W = 8
) (
    input  wire         clk,
    input  wire         rst_n,
    input  wire         gpio_wr_en,
    input  wire [W-1:0] gpio_wdata,
    input  wire [W-1:0] gpio_in_async,
    output reg  [W-1:0] gpio_out,
    output reg  [W-1:0] gpio_in_sync
);

    // First synchronizer stage.  The second stage is the registered
    // gpio_in_sync output.  Both are reset to zero.
    reg [W-1:0] sync_meta /* synthesis syn_preserve=1 */;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            gpio_out     <= {W{1'b0}};
            sync_meta    <= {W{1'b0}};
            gpio_in_sync <= {W{1'b0}};
        end else begin
            // Full-width write; no byte enables, masking or direction.
            if (gpio_wr_en) begin
                gpio_out <= gpio_wdata;
            end

            // Two-stage input synchronization, independent of gpio_out.
            sync_meta    <= gpio_in_async;
            gpio_in_sync <= sync_meta;
        end
    end

endmodule
