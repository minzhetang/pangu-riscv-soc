`timescale 1ns/1ps
`include "rx_ledger_check.svh"
`ifndef CLKS_PER_BIT
 `define CLKS_PER_BIT 16
`endif
`ifndef TB_MAX_CYCLES
 `define TB_MAX_CYCLES 100000
`endif

// Self-checking UART RX testbench for PERIPH-CORE-RX-1.0 v1.0.0.
// The DUT is observed only through public ports.  Stimulus is generated on
// the raw serial line; expected data/error events are directed and frozen in
// the plan before execution.
module tb_uart_rx;

    localparam integer N = `CLKS_PER_BIT;
    localparam integer HALF = N / 2;
    localparam integer S_OFFSET = 3 + 9 * N + HALF;
    localparam integer FRAME_CYCLES = 10 * N;
    localparam integer MAX_CYCLES = `TB_MAX_CYCLES;
    localparam integer HARD_CAP = 1000000;
    localparam integer MAX_LEDGER_EVENTS = 512;
    localparam integer EV_ACCEPT = 1;
    localparam integer EV_CONSUME = 2;
    localparam integer EV_DROP = 3;
    localparam integer EV_CANCEL = 4;

    reg clk;
    reg rst_n;
    reg rx;
    reg rx_ready;
    reg clear_errors;

    wire       rx_valid;
    wire [7:0] rx_data;
    wire       frame_error;
    wire       overrun;

    integer errors;
    integer cycle_count;
    integer last_start_cycle;
    integer valid_assertions;
    integer consumed_count;
    integer visible_data_changes;
    integer overrun_events;
    integer frame_error_events;
    integer exp_valid;
    integer exp_consumed;
    integer exp_overrun;
    integer exp_frame_error;
    integer exp_ledger_type [0:MAX_LEDGER_EVENTS-1];
    integer exp_ledger_data [0:MAX_LEDGER_EVENTS-1];
    reg [255:0] exp_ledger_label [0:MAX_LEDGER_EVENTS-1];
    integer exp_ledger_count;
    integer act_ledger_type [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_data [0:MAX_LEDGER_EVENTS-1];
    reg [255:0] act_ledger_label [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_edge [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_pre_valid [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_pre_ready [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_pre_clear [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_pre_ov [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_pre_fe [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_post_valid [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_post_ready [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_post_clear [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_post_ov [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_post_fe [0:MAX_LEDGER_EVENTS-1];
    integer act_ledger_count;

    // Independent serial-input decoder for protocol-derived DROP data.
    reg       rx_prev;
    reg       line_active;
    reg       line_armed;
    integer   line_cnt;
    integer   line_bit;
    reg [7:0] line_data;
    reg       line_good;
    reg [2:0] line_good_pipe;

    // Last settled public state, used as the pre-reset snapshot for CANCEL.
    reg       last_valid;
    reg       last_ready;
    reg       last_clear;
    reg       last_ov;
    reg       last_fe;
    reg [7:0] last_data;
    integer ledger_i;
    integer ledger_errors;
    integer check_i;
    integer check_j;

    reg       rx_valid_q;
    reg       capture_cancel;
    reg [31:0] capture_cancel_edge;
    reg [7:0] rx_data_q;
    reg       frame_error_q;
    reg       overrun_q;

    reg [7:0] stim_bytes [0:31];
    reg [7:0] seq01 [0:6];

    uart_rx #(.CLKS_PER_BIT(N)) dut (
        .clk         (clk),
        .rst_n       (rst_n),
        .rx          (rx),
        .rx_ready    (rx_ready),
        .clear_errors(clear_errors),
        .rx_valid    (rx_valid),
        .rx_data     (rx_data),
        .frame_error (frame_error),
        .overrun     (overrun)
    );

    rx_public_capture rx_cap (
        .clk       (clk),
        .rst_n     (1'b1),
        .valid     (rx_valid),
        .ready     (rx_ready),
        .line_good_accept (line_good_pipe[0]),
        .line_good_drop (line_good_pipe[1]),
        .data      (rx_data),
        .line_data (line_data),
        .cancel    (capture_cancel),
        .cancel_edge(capture_cancel_edge)
    );

    always @(negedge rst_n) begin
        if (line_active) begin
            capture_cancel <= 1'b1;
            capture_cancel_edge <= cycle_count;
        end
    end

    always @(posedge clk)
        if (capture_cancel)
            capture_cancel <= 1'b0;

    initial clk = 1'b0;
    always #5 clk = ~clk;

    string wave_file;
    initial begin
        if ($value$plusargs("WAVE_FILE=%s", wave_file)) begin
            $dumpfile(wave_file);
            $dumpvars(0, tb_uart_rx);
        end
    end

    initial begin
        if (MAX_CYCLES > HARD_CAP) begin
            $display("TB_HARD_CAP_REJECT limit=%0d hard_cap=%0d", MAX_CYCLES, HARD_CAP);
            $finish;
        end
    end

    initial cycle_count = 0;
    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
        if (cycle_count > MAX_CYCLES) begin
            $display("TB_WATCHDOG_TIMEOUT cycles=%0d limit=%0d", cycle_count, MAX_CYCLES);
            $finish;
        end
    end

    // Visible port-event counters.  These are counts of observable events,
    // not internal write-port probes; equal data bytes are not de-duplicated.
    always @(posedge clk) begin
        if (rst_n) begin
            if (rx_valid && !rx_valid_q)
                valid_assertions <= valid_assertions + 1;
            if (rx_valid && rx_ready)
                consumed_count <= consumed_count + 1;
            if (rx_valid && (rx_data !== rx_data_q))
                visible_data_changes <= visible_data_changes + 1;
            if (frame_error && !frame_error_q)
                frame_error_events <= frame_error_events + 1;
            if (overrun && !overrun_q)
                overrun_events <= overrun_events + 1;
        end
        rx_valid_q <= rx_valid;
        rx_data_q  <= rx_data;
        frame_error_q <= frame_error;
        overrun_q     <= overrun;
    end

    // Ordered transaction ledger.  ACCEPT/CONSUME/DROP are derived from the
    // independent serial input plus public valid/ready/data; CANCEL is derived
    // from reset while a serial frame is active.  The aggregate valid/FE/OV
    // counters above remain a separate observable-state count.
    task automatic ledger_push(
        input integer typ, input [7:0] d, input [255:0] lab, input integer ev_edge,
        input integer pv, input integer pr, input integer pc, input integer po, input integer pf,
        input integer postv, input integer postr, input integer postc, input integer posto, input integer postf
    );
        begin
            act_ledger_type[act_ledger_count] = typ;
            act_ledger_data[act_ledger_count] = d;
            act_ledger_label[act_ledger_count] = lab;
            act_ledger_edge[act_ledger_count] = ev_edge;
            act_ledger_pre_valid[act_ledger_count] = pv;
            act_ledger_pre_ready[act_ledger_count] = pr;
            act_ledger_pre_clear[act_ledger_count] = pc;
            act_ledger_pre_ov[act_ledger_count] = po;
            act_ledger_pre_fe[act_ledger_count] = pf;
            act_ledger_post_valid[act_ledger_count] = postv;
            act_ledger_post_ready[act_ledger_count] = postr;
            act_ledger_post_clear[act_ledger_count] = postc;
            act_ledger_post_ov[act_ledger_count] = posto;
            act_ledger_post_fe[act_ledger_count] = postf;
            act_ledger_count = act_ledger_count + 1;
        end
    endtask

    reg       pre_valid;
    reg       pre_ready;
    reg       pre_clear;
    reg       pre_ov;
    reg       pre_fe;
    reg [7:0] pre_data;
    integer   pre_edge;
    reg       same_edge_consume;
    reg       same_edge_new_frame;
    reg [7:0] same_edge_old_data;
    integer   cancel_idx;
    integer   pending_idx [0:63];
    integer   pending_count;

    task automatic ledger_push_s(
        input integer typ, input [7:0] d, input [255:0] lab, input integer edge_value,
        input integer pv, input integer pr, input integer pc, input integer po, input integer pf
    );
        begin
            ledger_push(typ, d, lab, edge_value, pv, pr, pc, po, pf,
                        rx_valid, rx_ready, clear_errors, overrun, frame_error);
            pending_idx[pending_count] = act_ledger_count - 1;
            pending_count = pending_count + 1;
        end
    endtask

    // Independent raw-serial decoder: samples mid-start, eight mid-data bits
    // and mid-stop.  line_good is delayed by three clocks to the DUT's S edge.
    always @(posedge clk) begin
        line_good <= 1'b0;
        rx_prev   <= rx;
        if (!rst_n) begin
            line_active <= 1'b0;
            line_armed  <= 1'b0;
            line_cnt    <= 0;
            line_bit    <= 0;
            line_data   <= 8'h00;
            line_good_pipe <= 3'b000;
        end else if (line_active) begin
            line_cnt <= line_cnt + 1;
            if (line_cnt == HALF - 1) begin
                if (rx !== 1'b0) begin
                    line_active <= 1'b0;
                    line_good   <= 1'b0;
                end
            end
            if (line_cnt == N + HALF - 1 + line_bit * N) begin
                line_data[line_bit] <= rx;
                line_bit <= line_bit + 1;
            end
            if (line_cnt == 9 * N + HALF - 1) begin
                line_good   <= (rx === 1'b1);
                line_active <= 1'b0;
            end
        end else begin
            if (rx === 1'b1)
                line_armed <= 1'b1;
            if (line_armed && rx_prev && !rx) begin
                line_active <= 1'b1;
                line_armed  <= 1'b0;
                line_cnt    <= 0;
                line_bit    <= 0;
                line_data   <= 8'h00;
                line_good   <= 1'b0;
            end
        end
        line_good_pipe <= {line_good_pipe[1:0], line_good};
    end

    // True-edge public event capture.  line_good_pipe[0] is the independent
    // serial decoder marker at the DUT's real S edge.  The pre snapshot is
    // taken before this edge's NBA; the post snapshot is filled at +1 ps after
    // the same edge.  Same-edge consume + replace is CONSUME then ACCEPT.
    always @(posedge clk) begin
        if (rst_n) begin
            last_valid <= rx_valid;
            last_ready <= rx_ready;
            last_clear <= clear_errors;
            last_ov    <= overrun;
            last_fe    <= frame_error;
            last_data  <= rx_data;

            if (line_good_pipe[0]) begin
                if (!rx_valid) begin
                    ledger_push_s(EV_ACCEPT, line_data, "ACCEPT",
                                  cycle_count + 1,
                                  rx_valid, rx_ready, clear_errors, overrun, frame_error);
                end else if (rx_ready) begin
                    ledger_push_s(EV_CONSUME, rx_data, "CONSUME",
                                  cycle_count + 1,
                                  rx_valid, rx_ready, clear_errors, overrun, frame_error);
                    ledger_push_s(EV_ACCEPT, line_data, "ACCEPT-REPLACE",
                                  cycle_count + 1,
                                  rx_valid, rx_ready, clear_errors, overrun, frame_error);
                end else begin
                    ledger_push_s(EV_DROP, line_data, "DROP",
                                  cycle_count + 1,
                                  rx_valid, rx_ready, clear_errors, overrun, frame_error);
                end
            end else if (rx_valid && rx_ready) begin
                ledger_push_s(EV_CONSUME, rx_data, "CONSUME",
                              cycle_count + 1,
                              rx_valid, rx_ready, clear_errors, overrun, frame_error);
            end
        end
    end

    // Post snapshot at +1 ps after the same posedge, before the testbench's
    // 1 ns stimulus changes.  Every event keeps this edge's real public post
    // values; no DROP/pre-copy special case and no negedge late-state capture.
    always @(posedge clk) begin : post_snapshot
        integer pi;
        #0.001;
        if (pending_count > 0) begin
            for (pi = 0; pi < pending_count; pi = pi + 1) begin
                act_ledger_post_valid[pending_idx[pi]] = rx_valid;
                act_ledger_post_ready[pending_idx[pi]] = rx_ready;
                act_ledger_post_clear[pending_idx[pi]] = clear_errors;
                act_ledger_post_ov[pending_idx[pi]] = overrun;
                act_ledger_post_fe[pending_idx[pi]] = frame_error;
            end
            pending_count = 0;
        end
    end

    // Asynchronous reset cancels a frame that the independent serial decoder
    // says is in flight.  This is a protocol-derived cancel, not a post-hoc
    // testbook call.
    always @(negedge rst_n) begin : cancel_monitor
        if (line_active) begin
            cancel_idx = act_ledger_count;
            act_ledger_type[cancel_idx] = EV_CANCEL;
            act_ledger_data[cancel_idx] = 8'h00;
            act_ledger_label[cancel_idx] = "RESET-CANCEL";
            act_ledger_edge[cancel_idx] = cycle_count;
            act_ledger_pre_valid[cancel_idx] = last_valid;
            act_ledger_pre_ready[cancel_idx] = last_ready;
            act_ledger_pre_clear[cancel_idx] = last_clear;
            act_ledger_pre_ov[cancel_idx] = last_ov;
            act_ledger_pre_fe[cancel_idx] = last_fe;
            #1;
            // Sample the actual public outputs after asynchronous reset has
            // settled; do not fill a fixed zero post-state.
            act_ledger_post_valid[cancel_idx] = rx_valid;
            act_ledger_post_ready[cancel_idx] = rx_ready;
            act_ledger_post_clear[cancel_idx] = clear_errors;
            act_ledger_post_ov[cancel_idx] = overrun;
            act_ledger_post_fe[cancel_idx] = frame_error;
            act_ledger_count = cancel_idx + 1;
        end
    end

    // ------------------------------------------------------------------
    // Reporting helpers
    // ------------------------------------------------------------------
    task automatic fail(input [1023:0] msg);
        begin
            errors = errors + 1;
            $display("CHK_FAIL %0s", msg);
        end
    endtask

    task automatic report_test(input [255:0] id, input integer e0);
        begin
            if (errors != e0)
                $display("TEST_FAIL %0s errors=%0d", id, errors - e0);
            else
                $display("TEST_PASS %0s", id);
        end
    endtask

    task automatic check_known(input [255:0] label);
        begin
            if ((rx_valid !== 1'b0) && (rx_valid !== 1'b1))
                fail("rx_valid X/Z");
            if ((frame_error !== 1'b0) && (frame_error !== 1'b1))
                fail("frame_error X/Z");
            if ((overrun !== 1'b0) && (overrun !== 1'b1))
                fail("overrun X/Z");
            if (^rx_data === 1'bx)
                fail("rx_data X/Z");
        end
    endtask

    task automatic check_byte(input [7:0] exp_data, input [255:0] label);
        begin
            check_known(label);
            if (rx_valid !== 1'b1) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s rx_valid=%b expected 1", label, rx_valid);
            end
            if (rx_data !== exp_data) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s rx_data=%02x expected %02x", label, rx_data, exp_data);
            end
        end
    endtask

    task automatic check_no_errors(input [255:0] label);
        begin
            if (frame_error !== 1'b0) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s frame_error=%b expected 0", label, frame_error);
            end
            if (overrun !== 1'b0) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s overrun=%b expected 0", label, overrun);
            end
        end
    endtask

    task automatic check_errors(input exp_fe, input exp_ov, input [255:0] label);
        begin
            if (frame_error !== exp_fe) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s frame_error=%b expected %b", label, frame_error, exp_fe);
            end
            if (overrun !== exp_ov) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s overrun=%b expected %b", label, overrun, exp_ov);
            end
        end
    endtask

    // ------------------------------------------------------------------
    // Cycle / stimulus helpers
    // ------------------------------------------------------------------
    task automatic wait_until_cycle(input integer target);
        begin
            while (cycle_count < target) begin
                @(posedge clk);
                #1;
            end
        end
    endtask

    task automatic reset_dut();
        begin
            rst_n        = 1'b0;
            rx           = 1'b1;
            rx_ready     = 1'b0;
            clear_errors = 1'b0;
            repeat (3) @(posedge clk);
            @(negedge clk);
            #1;
            rst_n = 1'b1;
            repeat (4) @(posedge clk);
            #1;
        end
    endtask

    // Drive one or more raw 8N1 frames.  For count>1 the next raw start is
    // placed exactly at the previous stop-bit boundary: 10*N*T period, no
    // extra idle.  For count==1 the line returns high at that boundary.
    task automatic expect_accept(input [7:0] data, input [255:0] label);
        begin
            exp_ledger_type[exp_ledger_count] = EV_ACCEPT;
            exp_ledger_data[exp_ledger_count] = data;
            exp_ledger_label[exp_ledger_count] = label;
            exp_ledger_count = exp_ledger_count + 1;
        end
    endtask

    task automatic expect_consume(input [7:0] data, input [255:0] label);
        begin
            exp_ledger_type[exp_ledger_count] = EV_CONSUME;
            exp_ledger_data[exp_ledger_count] = data;
            exp_ledger_label[exp_ledger_count] = label;
            exp_ledger_count = exp_ledger_count + 1;
        end
    endtask

    task automatic expect_drop(input [7:0] data, input [255:0] label);
        begin
            exp_ledger_type[exp_ledger_count] = EV_DROP;
            exp_ledger_data[exp_ledger_count] = data;
            exp_ledger_label[exp_ledger_count] = label;
            exp_ledger_count = exp_ledger_count + 1;
        end
    endtask

    task automatic expect_cancel(input [255:0] label);
        begin
            exp_ledger_type[exp_ledger_count] = EV_CANCEL;
            exp_ledger_data[exp_ledger_count] = 8'h00;
            exp_ledger_label[exp_ledger_count] = label;
            exp_ledger_count = exp_ledger_count + 1;
        end
    endtask

    task automatic send_cont(input integer count, input integer phase_ps, output integer start_cycle);
        integer j;
        integer k;
        begin
            @(posedge clk);
            #(phase_ps);
            rx = 1'b0;
            start_cycle = cycle_count;
            last_start_cycle = cycle_count;
            for (j = 0; j < count; j = j + 1) begin
                for (k = 0; k < 8; k = k + 1) begin
                    repeat (N) @(posedge clk);
                    #(phase_ps);
                    rx = stim_bytes[j][k];
                end
                repeat (N) @(posedge clk);
                #(phase_ps);
                rx = 1'b1; // stop bit starts
                repeat (N) @(posedge clk);
                #(phase_ps);
                if (j != count - 1)
                    rx = 1'b0; // next raw start exactly at stop boundary
                else
                    rx = 1'b1;
            end
        end
    endtask

    // Bad-stop frame: stop is low for N+extra_low cycles, then high.
    task automatic send_bad(input [7:0] data, input integer phase_ps,
                            input integer extra_low, output integer start_cycle);
        integer k;
        begin
            @(posedge clk);
            #(phase_ps);
            rx = 1'b0;
            start_cycle = cycle_count;
            last_start_cycle = cycle_count;
            for (k = 0; k < 8; k = k + 1) begin
                repeat (N) @(posedge clk);
                #(phase_ps);
                rx = data[k];
            end
            repeat (N) @(posedge clk);
            #(phase_ps);
            rx = 1'b0; // bad stop
            repeat (N + extra_low) @(posedge clk);
            #(phase_ps);
            rx = 1'b1;
        end
    endtask

    // Good frame with a check at S post-NBA.  rx_ready must remain 0.
    task automatic send_good_check_s(input [7:0] data, input integer phase_ps,
                                     input [255:0] label);
        integer sc;
        begin
            stim_bytes[0] = data;
            sc = 0;
            exp_valid = exp_valid + 1;
            expect_accept(data, label);
            last_start_cycle = 0;
            fork
                send_cont(1, phase_ps, sc);
                begin
                    wait (last_start_cycle != 0); sc = last_start_cycle;
                    wait_until_cycle(sc + S_OFFSET);
                    check_byte(data, label);
                    check_no_errors(label);
                end
            join
        end
    endtask

    // Good frame with rx_ready asserted after the S-1 edge (same-edge test).
    task automatic send_good_same_edge(input [7:0] old_data, input [7:0] data,
                                       input integer phase_ps,
                                       output integer start_cycle);
        integer sc;
        begin
            stim_bytes[0] = data;
            sc = 0;
            exp_consumed = exp_consumed + 2;
            expect_consume(old_data, "SAME-EDGE-OLD");
            expect_accept(data, "SAME-EDGE-NEW");
            expect_consume(data, "SAME-EDGE-NEW-CONSUME");
            last_start_cycle = 0;
            fork
                send_cont(1, phase_ps, sc);
                begin
                    wait (last_start_cycle != 0); sc = last_start_cycle;
                    wait_until_cycle(sc + S_OFFSET - 1);
                    rx_ready = 1'b1;
                    wait_until_cycle(sc + S_OFFSET);
                    check_byte(data, "RX-08 same-edge S");
                    check_errors(1'b0, 1'b0, "RX-08 same-edge S");
                end
            join
            start_cycle = sc;
        end
    endtask

    // Bad frame with rx_ready asserted at the S-1 edge.
    task automatic send_bad_ready_at_s(input [7:0] data, input integer phase_ps,
                                       output integer start_cycle);
        integer sc;
        begin
            sc = 0;
            last_start_cycle = 0;
            fork
                send_bad(data, phase_ps, 0, sc);
                begin
                    wait (last_start_cycle != 0); sc = last_start_cycle;
                    wait_until_cycle(sc + S_OFFSET - 1);
                    rx_ready = 1'b1;
                end
            join
            start_cycle = sc;
        end
    endtask

    // Bad frame with clear_errors asserted at the S-1 edge.
    task automatic send_bad_clear_at_s(input [7:0] data, input integer phase_ps,
                                       output integer start_cycle);
        integer sc;
        begin
            sc = 0;
            last_start_cycle = 0;
            fork
                send_bad(data, phase_ps, 0, sc);
                begin
                    wait (last_start_cycle != 0); sc = last_start_cycle;
                    wait_until_cycle(sc + S_OFFSET - 1);
                    clear_errors = 1'b1;
                    wait_until_cycle(sc + S_OFFSET);
                    clear_errors = 1'b0;
                end
            join
            start_cycle = sc;
        end
    endtask

    task automatic consume_once(input [7:0] exp_data);
        begin
            exp_consumed = exp_consumed + 1;
            expect_consume(exp_data, "CONSUME");
            @(negedge clk);
            rx_ready = 1'b1;
            @(posedge clk);
            #1;
            rx_ready = 1'b0;
            if (rx_valid !== 1'b0) begin
                errors = errors + 1;
                $display("CHK_FAIL consume expected rx_valid=0 got=%b", rx_valid);
            end
            if (rx_data !== exp_data) begin
                errors = errors + 1;
                $display("CHK_FAIL consume data hold expected=%02x got=%02x", exp_data, rx_data);
            end
        end
    endtask

    task automatic clear_once();
        begin
            @(negedge clk);
            clear_errors = 1'b1;
            @(posedge clk);
            #1;
            clear_errors = 1'b0;
        end
    endtask

    task automatic send_false_start(input integer low_cycles, input integer phase_ps);
        begin
            @(posedge clk);
            #(phase_ps);
            rx = 1'b0;
            repeat (low_cycles) @(posedge clk);
            #(phase_ps);
            rx = 1'b1;
            repeat (2 * N) @(posedge clk);
            #(phase_ps);
        end
    endtask

    task automatic send_partial_reset(input [7:0] data, input integer phase_ps);
        begin
            @(posedge clk);
            #(phase_ps);
            rx = 1'b0;
            repeat (N) @(posedge clk);
            #(phase_ps);
            rx = data[0];
            repeat (N) @(posedge clk);
            #(phase_ps);
            rx = data[1];
            expect_cancel("RESET-DATA");
            rst_n        = 1'b0;
            rx           = 1'b1;
            rx_ready     = 1'b0;
            clear_errors = 1'b0;
            repeat (3) @(posedge clk);
            @(negedge clk);
            #1;
            rst_n = 1'b1;
            repeat (4) @(posedge clk);
            #1;
        end
    endtask

    // Good frame arriving into a full mailbox, with clear_errors at S.
    // Expected: new overrun wins, old frame_error clears, mailbox stays.
    task automatic send_good_clear_at_s(input [7:0] data, input integer phase_ps,
                                        output integer start_cycle);
        integer sc;
        begin
            stim_bytes[0] = data;
            sc = 0;
            last_start_cycle = 0;
            fork
                send_cont(1, phase_ps, sc);
                begin
                    wait (last_start_cycle != 0); sc = last_start_cycle;
                    wait_until_cycle(sc + S_OFFSET - 1);
                    clear_errors = 1'b1;
                    wait_until_cycle(sc + S_OFFSET);
                    clear_errors = 1'b0;
                end
            join
            start_cycle = sc;
        end
    endtask

    // Bad stop with a sustained low tail; clear frame_error while still low,
    // confirm it is not re-raised, then return high and recover.
    task automatic send_bad_clear_low(input [7:0] data, input integer phase_ps,
                                      input integer extra_low,
                                      output integer start_cycle);
        integer sc;
        begin
            stim_bytes[0] = data;
            sc = 0;
            last_start_cycle = 0;
            fork
                send_bad(data, phase_ps, extra_low, sc);
                begin
                    wait (last_start_cycle != 0); sc = last_start_cycle;
                    wait_until_cycle(sc + S_OFFSET + 1);
                    clear_errors = 1'b1;
                    @(posedge clk);
                    #1;
                    clear_errors = 1'b0;
                    wait_until_cycle(sc + S_OFFSET + 2);
                    if (frame_error !== 1'b0) begin
                        errors = errors + 1;
                        $display("CHK_FAIL RX-05 low-clear FE still set after clear");
                    end
                    wait_until_cycle(sc + S_OFFSET + HALF + 2 * N);
                    if (frame_error !== 1'b0) begin
                        errors = errors + 1;
                        $display("CHK_FAIL RX-05 low-clear FE re-raised during low");
                    end
                end
            join
            start_cycle = sc;
        end
    endtask

    // Reset during the START phase (after d, before the start-center check).
    task automatic send_start_reset(input [7:0] data, input integer phase_ps);
        begin
            @(posedge clk);
            #(phase_ps);
            rx = 1'b0;
            repeat (4) @(posedge clk);
            #(phase_ps);
            expect_cancel("RESET-START");
            rst_n        = 1'b0;
            rx           = 1'b1;
            rx_ready     = 1'b0;
            clear_errors = 1'b0;
            repeat (3) @(posedge clk);
            @(negedge clk);
            #1;
            rst_n = 1'b1;
            repeat (4) @(posedge clk);
            #1;
        end
    endtask

    // Reset during the STOP phase (stop started, before S).
    task automatic send_stop_reset(input [7:0] data, input integer phase_ps);
        integer k;
        begin
            @(posedge clk);
            #(phase_ps);
            rx = 1'b0;
            for (k = 0; k < 8; k = k + 1) begin
                repeat (N) @(posedge clk);
                #(phase_ps);
                rx = data[k];
            end
            repeat (N) @(posedge clk);
            #(phase_ps);
            rx = 1'b1;
            repeat (1) @(posedge clk);
            #(phase_ps);
            expect_cancel("RESET-STOP");
            rst_n        = 1'b0;
            rx           = 1'b1;
            rx_ready     = 1'b0;
            clear_errors = 1'b0;
            repeat (3) @(posedge clk);
            @(negedge clk);
            #1;
            rst_n = 1'b1;
            repeat (4) @(posedge clk);
            #1;
        end
    endtask

    // Release reset while rx is low, hold low, then return high and re-arm.
    task automatic reset_release_low();
        begin
            rst_n        = 1'b0;
            rx           = 1'b1;
            rx_ready     = 1'b0;
            clear_errors = 1'b0;
            repeat (3) @(posedge clk);
            @(negedge clk);
            #1;
            rx    = 1'b0;
            rst_n = 1'b1;
            repeat (4 * N) @(posedge clk);
            #1;
            check_errors(1'b0, 1'b0, "RX-09 reset low");
            if (rx_valid !== 1'b0) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-09 reset low rx_valid=%b expected 0", rx_valid);
            end
            @(negedge clk);
            #1;
            rx = 1'b1;
            repeat (2 * N) @(posedge clk);
            #1;
        end
    endtask

    // ------------------------------------------------------------------
    // Test cases
    // ------------------------------------------------------------------
    task automatic test_rx01();
        integer e0;
        integer i;
        begin
            $display("TEST_BEGIN RX-01");
            reset_dut();
            e0 = errors;
            seq01[0] = 8'h00;
            seq01[1] = 8'hFF;
            seq01[2] = 8'h55;
            seq01[3] = 8'hAA;
            seq01[4] = 8'h01;
            seq01[5] = 8'h80;
            seq01[6] = 8'h7E;
            for (i = 0; i < 7; i = i + 1) begin
                send_good_check_s(seq01[i], 1, "RX-01");
                consume_once(seq01[i]);
            end
            report_test("RX-01", e0);
        end
    endtask

    task automatic test_rx02();
        integer e0;
        integer p;
        begin
            $display("TEST_BEGIN RX-02");
            reset_dut();
            e0 = errors;
            if (N == 234) begin
                send_good_check_s(8'h55, 1, "RX-02 N234");
                consume_once(8'h55);
                send_good_check_s(8'hAA, 1, "RX-02 N234");
                consume_once(8'hAA);
            end else begin
                for (p = 0; p < 4; p = p + 1) begin
                    send_good_check_s(8'h55, (p == 0) ? 1 : (p == 1) ? 3 : (p == 2) ? 6 : 9, "RX-02 55");
                    consume_once(8'h55);
                    send_good_check_s(8'hAA, (p == 0) ? 1 : (p == 1) ? 3 : (p == 2) ? 6 : 9, "RX-02 AA");
                    consume_once(8'hAA);
                end
            end
            report_test("RX-02", e0);
        end
    endtask

    task automatic test_rx03();
        integer e0;
        integer i;
        integer count;
        integer sc;
        begin
            $display("TEST_BEGIN RX-03");
            reset_dut();
            e0 = errors;
            if (N == 16)
                count = 16;
            else if (N == 8)
                count = 8;
            else
                count = 2;
            exp_valid = exp_valid + count;
            exp_consumed = exp_consumed + count;
            for (i = 0; i < count; i = i + 1) begin
                stim_bytes[i] = (i % 2 == 0) ? 8'h55 : 8'hAA;
                expect_accept(stim_bytes[i], "RX-03 ACCEPT");
                expect_consume(stim_bytes[i], "RX-03 CONSUME");
            end
            rx_ready = 1'b1;
            sc = 0;
            last_start_cycle = 0;
            fork
                send_cont(count, 1, sc);
                begin
                    wait (last_start_cycle != 0); sc = last_start_cycle;
                    for (i = 0; i < count; i = i + 1) begin
                        wait_until_cycle(sc + i * FRAME_CYCLES + S_OFFSET);
                        check_byte(stim_bytes[i], "RX-03 back-to-back S");
                        check_errors(1'b0, 1'b0, "RX-03 back-to-back S");
                        @(posedge clk);
                        #1;
                        if (rx_valid !== 1'b0) begin
                            errors = errors + 1;
                            $display("CHK_FAIL RX-03 back-to-back S+1 valid=%b expected 0", rx_valid);
                        end
                    end
                end
            join
            rx_ready = 1'b0;
            check_errors(1'b0, 1'b0, "RX-03 final");
            report_test("RX-03", e0);
        end
    endtask

    task automatic test_rx04();
        integer e0;
        begin
            $display("TEST_BEGIN RX-04");
            reset_dut();
            e0 = errors;
            send_false_start(7, 1);
            check_errors(1'b0, 1'b0, "RX-04 L7");
            if (rx_valid !== 1'b0) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-04 L7 rx_valid=%b expected 0", rx_valid);
            end
            send_false_start(8, 3);
            check_errors(1'b0, 1'b0, "RX-04 L8");
            send_good_check_s(8'h5A, 1, "RX-04 good after false start");
            consume_once(8'h5A);
            report_test("RX-04", e0);
        end
    endtask

    task automatic test_rx05();
        integer e0;
        integer sc;
        begin
            $display("TEST_BEGIN RX-05");
            // 5a: bad stop retains old mailbox, rearm, full-mailbox overrun,
            // then recovery after consume.
            reset_dut();
            e0 = errors;
            send_good_check_s(8'h3C, 1, "RX-05 fill A");
            send_bad(8'hA5, 1, 0, sc);
            exp_frame_error = exp_frame_error + 1;
            if (rx_valid !== 1'b1 || rx_data !== 8'h3C) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-05 bad stop old mailbox valid=%b data=%02x", rx_valid, rx_data);
            end
            check_errors(1'b1, 1'b0, "RX-05 bad stop");
            clear_once();
            check_errors(1'b0, 1'b0, "RX-05 clear bad stop");
            stim_bytes[0] = 8'hC3;
            exp_overrun = exp_overrun + 1;
            expect_drop(8'hC3, "RX-05 5a FULL-DROP");
            send_cont(1, 1, sc);
            if (rx_valid !== 1'b1 || rx_data !== 8'h3C) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-05 full keep valid=%b data=%02x", rx_valid, rx_data);
            end
            check_errors(1'b0, 1'b1, "RX-05 full overrun");
            clear_once();
            check_errors(1'b0, 1'b0, "RX-05 clear overrun");
            consume_once(8'h3C);
            send_good_check_s(8'hC3, 1, "RX-05 recovered");
            consume_once(8'hC3);

            // 5b: bad stop with ready=1 consumes the old byte.
            reset_dut();
            send_good_check_s(8'h69, 1, "RX-05 fill B");
            expect_consume(8'h69, "RX-05 5b BAD-READY-CONSUME");
            send_bad_ready_at_s(8'h96, 1, sc);
            exp_frame_error = exp_frame_error + 1;
            exp_consumed = exp_consumed + 1;
            rx_ready = 1'b0;
            if (rx_valid !== 1'b0 || rx_data !== 8'h69) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-05 bad consume valid=%b data=%02x", rx_valid, rx_data);
            end
            check_errors(1'b1, 1'b0, "RX-05 bad consume errors");
            clear_once();
            send_good_check_s(8'h96, 1, "RX-05 after bad consume");
            consume_once(8'h96);

            // 5c: sustained low after a bad stop does not repeat a visible
            // frame; clear, then require a genuine high before the next good.
            reset_dut();
            send_bad(8'h5A, 1, 2 * N, sc);
            exp_frame_error = exp_frame_error + 1;
            check_errors(1'b1, 1'b0, "RX-05 sustained low");
            clear_once();
            check_errors(1'b0, 1'b0, "RX-05 sustained low clear");
            if (rx_valid !== 1'b0) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-05 sustained low rx_valid=%b expected 0", rx_valid);
            end
            send_good_check_s(8'h96, 1, "RX-05 after sustained low");
            consume_once(8'h96);

            // 5d: clear with a new frame_error must leave frame_error set and
            // clear the old overrun (per-bit new-event priority).
            reset_dut();
            send_good_check_s(8'h11, 1, "RX-05 clear-race fill");
            send_bad(8'h22, 1, 0, sc);
            exp_frame_error = exp_frame_error + 1;
            check_errors(1'b1, 1'b0, "RX-05 clear-race fe");
            stim_bytes[0] = 8'h33;
            exp_overrun = exp_overrun + 1;
            expect_drop(8'h33, "RX-05 5d FULL-DROP");
            send_cont(1, 1, sc);
            check_errors(1'b1, 1'b1, "RX-05 clear-race both errors");
            send_bad_clear_at_s(8'h44, 1, sc);
            check_errors(1'b1, 1'b0, "RX-05 clear-race new fe");
            clear_once();
            check_errors(1'b0, 1'b0, "RX-05 clear-race final clear");

            // 5e: clear_errors with a new overrun must set new OV, clear old
            // FE, and leave the full mailbox untouched.
            reset_dut();
            send_good_check_s(8'h11, 1, "RX-05 clear-OV fill");
            send_bad(8'h22, 1, 0, sc);
            exp_frame_error = exp_frame_error + 1;
            check_errors(1'b1, 1'b0, "RX-05 clear-OV fe");
            stim_bytes[0] = 8'h33;
            exp_overrun = exp_overrun + 1;
            expect_drop(8'h33, "RX-05 5e FULL-DROP");
            send_cont(1, 1, sc);
            check_errors(1'b1, 1'b1, "RX-05 clear-OV both");
            expect_drop(8'h44, "RX-05 5e CLEAR-RACE-DROP");
            send_good_clear_at_s(8'h44, 1, sc);
            check_errors(1'b0, 1'b1, "RX-05 clear new OV wins");
            if (rx_valid !== 1'b1 || rx_data !== 8'h11) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-05 clear-OV mailbox valid=%b data=%02x", rx_valid, rx_data);
            end
            clear_once();
            check_errors(1'b0, 1'b0, "RX-05 clear-OV final");
            consume_once(8'h11);

            // 5f: bad stop with a sustained low tail; clear FE while low,
            // confirm it is not re-raised, then recover after the line returns high.
            reset_dut();
            send_bad_clear_low(8'h5A, 1, 4 * N, sc);
            exp_frame_error = exp_frame_error + 1;
            check_errors(1'b0, 1'b0, "RX-05 low-clear final");
            send_good_check_s(8'hA5, 1, "RX-05 low-clear recovery");
            consume_once(8'hA5);
            report_test("RX-05", e0);
        end
    endtask

    task automatic test_rx06();
        integer e0;
        integer i;
        begin
            $display("TEST_BEGIN RX-06");
            reset_dut();
            e0 = errors;
            send_good_check_s(8'h5A, 1, "RX-06 S post-NBA");
            for (i = 0; i < 24; i = i + 1) begin
                @(posedge clk);
                #1;
            end
            if (rx_valid !== 1'b1 || rx_data !== 8'h5A) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-06 hold valid=%b data=%02x", rx_valid, rx_data);
            end
            consume_once(8'h5A);
            for (i = 0; i < 4; i = i + 1) begin
                @(posedge clk);
                #1;
            end
            if (rx_valid !== 1'b0 || rx_data !== 8'h5A) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-06 post-consume valid=%b data=%02x", rx_valid, rx_data);
            end
            report_test("RX-06", e0);
        end
    endtask

    task automatic test_rx07();
        integer e0;
        integer sc;
        begin
            $display("TEST_BEGIN RX-07");
            reset_dut();
            e0 = errors;
            send_good_check_s(8'hA1, 1, "RX-07 fill");
            stim_bytes[0] = 8'hB2;
            exp_overrun = exp_overrun + 1;
            expect_drop(8'hB2, "RX-07 FULL-DROP");
            send_cont(1, 1, sc);
            if (rx_valid !== 1'b1 || rx_data !== 8'hA1) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-07 full keep valid=%b data=%02x", rx_valid, rx_data);
            end
            check_errors(1'b0, 1'b1, "RX-07 full overrun");
            clear_once();
            check_errors(1'b0, 1'b0, "RX-07 clear overrun");
            consume_once(8'hA1);
            send_good_check_s(8'hA1, 1, "RX-07 same byte accepted");
            consume_once(8'hA1);
            report_test("RX-07", e0);
        end
    endtask

    task automatic test_rx08();
        integer e0;
        integer sc;
        begin
            $display("TEST_BEGIN RX-08");
            reset_dut();
            e0 = errors;
            send_good_check_s(8'hA1, 1, "RX-08 old");
            send_good_same_edge(8'hA1, 8'hB2, 1, sc);
            rx_ready = 1'b0;
            if (rx_valid !== 1'b0 || rx_data !== 8'hB2) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-08 after S+1 valid=%b data=%02x", rx_valid, rx_data);
            end
            check_errors(1'b0, 1'b0, "RX-08 after S+1");

            // Same-byte same-edge replacement: the old and new byte are both
            // A1, so valid/data alone cannot prove the accept; the ledger must.
            send_good_check_s(8'hA1, 1, "RX-08 same-byte fill");
            send_good_same_edge(8'hA1, 8'hA1, 1, sc);
            rx_ready = 1'b0;
            if (rx_valid !== 1'b0 || rx_data !== 8'hA1) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-08 same-byte after S+1 valid=%b data=%02x", rx_valid, rx_data);
            end
            check_errors(1'b0, 1'b0, "RX-08 same-byte after S+1");
            report_test("RX-08", e0);
        end
    endtask

    task automatic test_rx09();
        integer e0;
        integer sc;
        integer i;
        begin
            $display("TEST_BEGIN RX-09");
            // 9a: reset in the middle of a frame cancels it.
            reset_dut();
            e0 = errors;
            send_partial_reset(8'h5A, 1);
            if (rx_valid !== 1'b0 || rx_data !== 8'h00) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-09 mid-frame reset valid=%b data=%02x", rx_valid, rx_data);
            end
            check_errors(1'b0, 1'b0, "RX-09 mid-frame reset");
            send_good_check_s(8'hC3, 1, "RX-09 reset recovery");
            consume_once(8'hC3);

            // 9b: reset during START, then recover with a good frame.
            reset_dut();
            send_start_reset(8'h5A, 1);
            if (rx_valid !== 1'b0 || rx_data !== 8'h00) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-09 START reset valid=%b data=%02x", rx_valid, rx_data);
            end
            check_errors(1'b0, 1'b0, "RX-09 START reset");
            send_good_check_s(8'hC3, 1, "RX-09 START reset recovery");
            consume_once(8'hC3);

            // 9c: reset during STOP, then recover with a good frame.
            reset_dut();
            send_stop_reset(8'h5A, 1);
            if (rx_valid !== 1'b0 || rx_data !== 8'h00) begin
                errors = errors + 1;
                $display("CHK_FAIL RX-09 STOP reset valid=%b data=%02x", rx_valid, rx_data);
            end
            check_errors(1'b0, 1'b0, "RX-09 STOP reset");
            send_good_check_s(8'hC3, 1, "RX-09 STOP reset recovery");
            consume_once(8'hC3);

            // 9d: release reset while low, hold low, then high and good frame.
            reset_release_low();
            send_good_check_s(8'h96, 1, "RX-09 low recovery");
            consume_once(8'h96);

            // 9e: clear_errors with a new frame_error keeps the new error.
            reset_dut();
            send_good_check_s(8'h11, 1, "RX-09 clear fill");
            send_bad(8'h22, 1, 0, sc);
            exp_frame_error = exp_frame_error + 1;
            check_errors(1'b1, 1'b0, "RX-09 clear pre");
            send_bad_clear_at_s(8'h33, 1, sc);
            check_errors(1'b1, 1'b0, "RX-09 clear new error wins");
            clear_once();
            check_errors(1'b0, 1'b0, "RX-09 clear final");
            report_test("RX-09", e0);
        end
    endtask

    // ------------------------------------------------------------------
    // Main sequence
    // ------------------------------------------------------------------
    initial begin
        errors = 0;
        valid_assertions = 0;
        consumed_count = 0;
        visible_data_changes = 0;
        overrun_events = 0;
        frame_error_events = 0;
        exp_valid = 0;
        exp_consumed = 0;
        exp_overrun = 0;
        exp_frame_error = 0;
        exp_ledger_count = 0;
        act_ledger_count = 0;
        rx_prev = 1'b1;
        line_active = 1'b0;
        line_armed = 1'b0;
        line_cnt = 0;
        line_bit = 0;
        line_data = 8'h00;
        line_good = 1'b0;
        line_good_pipe = 3'b000;
        last_valid = 1'b0;
        last_ready = 1'b0;
        last_clear = 1'b0;
        last_ov = 1'b0;
        last_fe = 1'b0;
        last_data = 8'h00;
        capture_cancel = 1'b0;
        pending_count = 0;
        capture_cancel_edge = 0;
        rx_valid_q = 1'b0;
        rx_data_q = 8'h00;
        frame_error_q = 1'b0;
        overrun_q = 1'b0;
        rst_n = 1'b0;
        rx = 1'b1;
        rx_ready = 1'b0;
        clear_errors = 1'b0;

        reset_dut();
        test_rx01();
        test_rx02();
        test_rx03();
        if (N == 16)
            test_rx04();
        test_rx05();
        test_rx06();
        test_rx07();
        test_rx08();
        test_rx09();

        $display("RX_LAST_CHECK_CYCLE=%0d", cycle_count);
        $display("RX_STATS valid_assertions=%0d consumed=%0d visible_data_changes=%0d overrun_events=%0d frame_error_events=%0d",
                 valid_assertions, consumed_count, visible_data_changes, overrun_events, frame_error_events);
        $display("RX_EXPECTED valid_assertions=%0d consumed=%0d overrun_events=%0d frame_error_events=%0d",
                 exp_valid, exp_consumed, exp_overrun, exp_frame_error);
        if (valid_assertions != exp_valid) begin errors = errors + 1; $display("CHK_FAIL RX event count valid_assertions expected=%0d actual=%0d", exp_valid, valid_assertions); end
        if (consumed_count != exp_consumed) begin errors = errors + 1; $display("CHK_FAIL RX event count consumed expected=%0d actual=%0d", exp_consumed, consumed_count); end
        if (overrun_events != exp_overrun) begin errors = errors + 1; $display("CHK_FAIL RX event count overrun expected=%0d actual=%0d", exp_overrun, overrun_events); end
        if (frame_error_events != exp_frame_error) begin errors = errors + 1; $display("CHK_FAIL RX event count frame_error expected=%0d actual=%0d", exp_frame_error, frame_error_events); end
        $display("RX_LEDGER expected=%0d actual=%0d", exp_ledger_count, act_ledger_count);
        `RX_LEDGER_COMPARE(ledger_errors);
        for (ledger_i = 0; ledger_i < act_ledger_count; ledger_i = ledger_i + 1)
            $display("RX_LEDGER_ACT seq=%0d edge=%0d type=%0d data=%02x pre_valid=%b pre_ready=%b pre_clear=%b pre_ov=%b pre_fe=%b post_valid=%b post_ready=%b post_clear=%b post_ov=%b post_fe=%b label=%0s",
                     ledger_i, act_ledger_edge[ledger_i], act_ledger_type[ledger_i], act_ledger_data[ledger_i],
                     act_ledger_pre_valid[ledger_i], act_ledger_pre_ready[ledger_i], act_ledger_pre_clear[ledger_i],
                     act_ledger_pre_ov[ledger_i], act_ledger_pre_fe[ledger_i],
                     act_ledger_post_valid[ledger_i], act_ledger_post_ready[ledger_i], act_ledger_post_clear[ledger_i],
                     act_ledger_post_ov[ledger_i], act_ledger_post_fe[ledger_i], act_ledger_label[ledger_i]);
        if (ledger_errors != 0) begin
            errors = errors + ledger_errors;
            $display("CHK_FAIL RX ordered ledger mismatch errors=%0d", ledger_errors);
            for (ledger_i = 0; ledger_i < exp_ledger_count; ledger_i = ledger_i + 1)
                $display("LEDGER_EXP seq=%0d type=%0d data=%02x label=%0s", ledger_i, exp_ledger_type[ledger_i], exp_ledger_data[ledger_i], exp_ledger_label[ledger_i]);
            for (ledger_i = 0; ledger_i < act_ledger_count; ledger_i = ledger_i + 1)
                $display("LEDGER_ACT seq=%0d type=%0d data=%02x label=%0s", ledger_i, act_ledger_type[ledger_i], act_ledger_data[ledger_i], act_ledger_label[ledger_i]);
        end
        // R1 snapshot invariants: every captured pre/post field must be a
        // known 0/1 public value, and ACCEPT/DROP/CONSUME must match the true
        // event's public pre/post shape.  Exact duplicate events are rejected.
        for (check_i = 0; check_i < act_ledger_count; check_i = check_i + 1) begin
            if ((act_ledger_pre_valid[check_i] !== 0 && act_ledger_pre_valid[check_i] !== 1) ||
                (act_ledger_pre_ready[check_i] !== 0 && act_ledger_pre_ready[check_i] !== 1) ||
                (act_ledger_pre_clear[check_i] !== 0 && act_ledger_pre_clear[check_i] !== 1) ||
                (act_ledger_pre_ov[check_i] !== 0 && act_ledger_pre_ov[check_i] !== 1) ||
                (act_ledger_pre_fe[check_i] !== 0 && act_ledger_pre_fe[check_i] !== 1) ||
                (act_ledger_post_valid[check_i] !== 0 && act_ledger_post_valid[check_i] !== 1) ||
                (act_ledger_post_ready[check_i] !== 0 && act_ledger_post_ready[check_i] !== 1) ||
                (act_ledger_post_clear[check_i] !== 0 && act_ledger_post_clear[check_i] !== 1) ||
                (act_ledger_post_ov[check_i] !== 0 && act_ledger_post_ov[check_i] !== 1) ||
                (act_ledger_post_fe[check_i] !== 0 && act_ledger_post_fe[check_i] !== 1)) begin
                errors = errors + 1;
                $display("CHK_FAIL RX snapshot X/Z seq=%0d", check_i);
            end
            if (act_ledger_type[check_i] == EV_ACCEPT) begin
                if (act_ledger_label[check_i] == "ACCEPT-REPLACE") begin
                    if (act_ledger_pre_valid[check_i] !== 1 || act_ledger_pre_ready[check_i] !== 1 ||
                        act_ledger_post_valid[check_i] !== 1) begin
                        errors = errors + 1;
                        $display("CHK_FAIL RX replace snapshot seq=%0d pre=%b/%b post=%b",
                                 check_i, act_ledger_pre_valid[check_i], act_ledger_pre_ready[check_i],
                                 act_ledger_post_valid[check_i]);
                    end
                end else if (act_ledger_pre_valid[check_i] !== 0 || act_ledger_post_valid[check_i] !== 1) begin
                    errors = errors + 1;
                    $display("CHK_FAIL RX accept snapshot seq=%0d pre=%b post=%b",
                             check_i, act_ledger_pre_valid[check_i], act_ledger_post_valid[check_i]);
                end
            end else if (act_ledger_type[check_i] == EV_CONSUME) begin
                if (act_ledger_pre_valid[check_i] !== 1 || act_ledger_pre_ready[check_i] !== 1) begin
                    errors = errors + 1;
                    $display("CHK_FAIL RX consume snapshot seq=%0d pre=%b/%b",
                             check_i, act_ledger_pre_valid[check_i], act_ledger_pre_ready[check_i]);
                end
            end else if (act_ledger_type[check_i] == EV_DROP) begin
                if (act_ledger_pre_valid[check_i] !== 1 || act_ledger_pre_ready[check_i] !== 0 ||
                    act_ledger_post_valid[check_i] !== 1) begin
                    errors = errors + 1;
                    $display("CHK_FAIL RX drop snapshot seq=%0d pre=%b/%b post=%b",
                             check_i, act_ledger_pre_valid[check_i], act_ledger_pre_ready[check_i],
                             act_ledger_post_valid[check_i]);
                end
            end
            for (check_j = check_i + 1; check_j < act_ledger_count; check_j = check_j + 1) begin
                if (act_ledger_edge[check_i] == act_ledger_edge[check_j] &&
                    act_ledger_type[check_i] == act_ledger_type[check_j] &&
                    act_ledger_data[check_i] == act_ledger_data[check_j] &&
                    act_ledger_label[check_i] == act_ledger_label[check_j]) begin
                    errors = errors + 1;
                    $display("CHK_FAIL RX duplicate event seq=%0d/%0d edge=%0d", check_i, check_j,
                             act_ledger_edge[check_i]);
                end
            end
        end
        if (errors == 0)
            $display("RX_SNAPSHOT_CHECK_PASS events=%0d", act_ledger_count);
        if (errors == 0)
            $display("RX_LEDGER_PASS");
        if (rx_cap.count !== act_ledger_count) begin
            errors = errors + 1;
            $display("CHK_FAIL RX shared capture count=%0d inline=%0d", rx_cap.count, act_ledger_count);
        end else begin
            for (ledger_i = 0; ledger_i < act_ledger_count; ledger_i = ledger_i + 1) begin
                if (rx_cap.etype[ledger_i] !== act_ledger_type[ledger_i] ||
                    rx_cap.edata[ledger_i] !== act_ledger_data[ledger_i] ||
                    rx_cap.eedge[ledger_i] !== act_ledger_edge[ledger_i]) begin
                    errors = errors + 1;
                    $display("CHK_FAIL RX shared capture seq=%0d type=%0d/%0d data=%02x/%02x edge=%0d/%0d",
                             ledger_i, rx_cap.etype[ledger_i], act_ledger_type[ledger_i],
                             rx_cap.edata[ledger_i], act_ledger_data[ledger_i],
                             rx_cap.eedge[ledger_i], act_ledger_edge[ledger_i]);
                end
            end
        end
        if (errors == 0) begin
            $display("RX_CAPTURE_CROSSCHECK_PASS count=%0d ordered=1 edge_match=1", rx_cap.count);
            $display("RX_SELFCHECK_PASS");
        end else
            $display("RX_SELFCHECK_FAIL errors=%0d", errors);
        $display("RX_LAST_CYCLE=%0d", cycle_count);
        $finish;
    end

endmodule
