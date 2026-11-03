`timescale 1ns/1ps
`ifndef CLKS_PER_BIT
 `define CLKS_PER_BIT 16
`endif
`ifndef TB_MAX_CYCLES
 `define TB_MAX_CYCLES 300000
`endif

module tb_local_regif_txgpio_m1;

    localparam integer N = `CLKS_PER_BIT;
    localparam integer HARD_CAP = 1000000;

    reg clk;
    reg rst_n;
    reg io_sel;
    reg io_wr_en;
    reg [7:0] io_addr;
    reg [31:0] io_wdata;
    reg [3:0] io_wstrb;
    reg [7:0] gpio_in_async;

    wire [31:0] io_rdata;
    wire        io_wr_error;
    wire        uart_tx;
    wire [7:0]  gpio_out;

    local_regif_txgpio_m1 #(.CLKS_PER_BIT(N)) dut (
        .clk           (clk),
        .rst_n         (rst_n),
        .io_sel        (io_sel),
        .io_wr_en      (io_wr_en),
        .io_addr       (io_addr),
        .io_wdata      (io_wdata),
        .io_wstrb      (io_wstrb),
        .gpio_in_async (gpio_in_async),
        .io_rdata      (io_rdata),
        .io_wr_error   (io_wr_error),
        .uart_tx       (uart_tx),
        .gpio_out      (gpio_out)
    );

    integer errors;
    integer cycle_count;
    reg [1023:0] wave_file;
    integer edge_count;
    integer max_cycles;
    integer accepted_tx;
    integer accepted_gpio;
    integer rejected;
    integer frames;
    reg [7:0] last_tx_byte;
    integer last_tx_good;
    integer last_tx_duration;

    initial begin
        if ((`TB_MAX_CYCLES < 1) || (`TB_MAX_CYCLES > HARD_CAP)) begin
            $display("REGIF_TB_COMPILE_CYCLE_GUARD_REJECT value=%0d legal=1..1000000", `TB_MAX_CYCLES);
            $finish;
        end
    end

    initial clk = 1'b0;
    always #5 clk = ~clk;

    initial begin
        if ($value$plusargs("WAVE_FILE=%s", wave_file)) begin
            $dumpfile(wave_file);
            $dumpvars(0, tb_local_regif_txgpio_m1);
        end
    end

    initial begin
        cycle_count = 0;
        edge_count = 0;
        max_cycles = `TB_MAX_CYCLES;
        if ($value$plusargs("MAX_CYCLES=%d", max_cycles)) begin
            // runtime guard check
        end
        if ((max_cycles < 1) || (max_cycles > HARD_CAP)) begin
            $display("REGIF_TB_RUNTIME_CYCLE_GUARD_REJECT value=%0d legal=1..1000000", max_cycles);
            $finish;
        end
    end

    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
        edge_count = edge_count + 1;
        if (cycle_count >= max_cycles) begin
            $display("REGIF_TB_WATCHDOG_TIMEOUT edge=%0d cycles=%0d limit=%0d", edge_count, cycle_count, max_cycles);
            $finish;
        end
    end

    task automatic fail(input [1023:0] msg);
        begin
            errors = errors + 1;
            $display("CHK_FAIL %0s", msg);
        end
    endtask

    task automatic report_test(input [255:0] id, input integer e0);
        begin
            if (errors != e0) begin
                $display("TEST_FAIL %0s errors=%0d", id, errors - e0);
            end else begin
                $display("TEST_PASS %0s", id);
            end
        end
    endtask

    task automatic clear_bus;
        begin
            io_sel = 1'b0;
            io_wr_en = 1'b0;
            io_addr = 8'h00;
            io_wdata = 32'h00000000;
            io_wstrb = 4'b0000;
        end
    endtask

    task automatic reset_dut;
        begin
            rst_n = 1'b0;
            clear_bus();
            gpio_in_async = 8'h00;
            repeat (3) @(posedge clk);
            @(negedge clk);
            #1;
            rst_n = 1'b1;
            repeat (2) @(posedge clk);
            #1;
        end
    endtask

    // A request is driven at negedge and checked at the following E edge.
    task automatic request(input sel, input en, input [7:0] addr, input [31:0] data,
                           input [3:0] strobe, input exp_error, input [255:0] label);
        begin
            @(negedge clk);
            io_sel = sel;
            io_wr_en = en;
            io_addr = addr;
            io_wdata = data;
            io_wstrb = strobe;
            #1;
            if (io_wr_error !== exp_error) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s io_wr_error got=%b expected=%b addr=%02x sel=%b en=%b strb=%b",
                         label, io_wr_error, exp_error, addr, sel, en, strobe);
            end
            @(posedge clk);
            #1;
            if (sel && en) begin
                if (exp_error) rejected = rejected + 1;
                else if (addr == 8'h00) accepted_tx = accepted_tx + 1;
                else if (addr == 8'h0c) accepted_gpio = accepted_gpio + 1;
            end
            clear_bus();
        end
    endtask

    task automatic read_check(input [7:0] addr, input [31:0] expected, input [255:0] label);
        begin
            @(negedge clk);
            io_sel = 1'b1;
            io_wr_en = 1'b0;
            io_addr = addr;
            io_wdata = 32'h00000000;
            io_wstrb = 4'b0000;
            #1;
            if (io_rdata !== expected) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s addr=%02x got=%08x expected=%08x", label, addr, io_rdata, expected);
            end
            @(negedge clk);
            clear_bus();
        end
    endtask

    // Independent serial decoder on the external uart_tx pin.  Sampling at
    // mid-bit, LSB first.  Returns the decoded byte and a good-stop flag.
    task automatic decode_tx(output [7:0] data, output integer good, output integer duration);
        integer k;
        integer start_cycle;
        begin
            // request() returns one delta after E; the frame may already be low.
            if (uart_tx === 1'b1)
                @(negedge uart_tx);
            start_cycle = cycle_count;
            // One-cycle-late start sampling is still inside the start bit for N>=8.
            repeat (N/2) @(posedge clk);
            if (uart_tx !== 1'b0) begin
                errors = errors + 1;
                $display("CHK_FAIL UART start center got=%b expected=0", uart_tx);
            end
            for (k = 0; k < 8; k = k + 1) begin
                repeat (N) @(posedge clk);
                data[k] = uart_tx;
            end
            repeat (N) @(posedge clk);
            good = (uart_tx === 1'b1);
            duration = cycle_count - start_cycle;
            if (!good) begin
                errors = errors + 1;
                $display("CHK_FAIL UART stop center got=%b expected=1", uart_tx);
            end
        end
    endtask

    task automatic check_tx_frame(input [7:0] expected, input [255:0] label);
        begin
            decode_tx(last_tx_byte, last_tx_good, last_tx_duration);
            frames = frames + 1;
            if ((last_tx_byte !== expected) || (last_tx_good !== 1)) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s uart got=%02x expected=%02x good=%0d", label, last_tx_byte, expected, last_tx_good);
            end
        end
    endtask

    task automatic tx_reset_case(input integer delay_cycles, input [7:0] data,
                                 input [255:0] label);
        begin
            reset_dut();
            request(1'b1, 1'b1, 8'h00, {24'hA5A5A5, data}, 4'b1111, 1'b0, label);
            repeat (delay_cycles) @(posedge clk);
            rst_n = 1'b0;
            #1;
            if (uart_tx !== 1'b1 || gpio_out !== 8'h00 || dut.tx_ready !== 1'b0 || dut.tx_busy !== 1'b0) begin
                errors = errors + 1;
                $display("CHK_FAIL %0s reset state tx=%b out=%02x ready=%b busy=%b",
                         label, uart_tx, gpio_out, dut.tx_ready, dut.tx_busy);
            end
            repeat (3) @(posedge clk);
            @(negedge clk);
            #1;
            rst_n = 1'b1;
            repeat (2) @(posedge clk);
            #1;
            request(1'b1, 1'b1, 8'h00, {24'h5A5A5A, 8'h6A}, 4'b1111, 1'b0, label);
            check_tx_frame(8'h6A, label);
        end
    endtask

    initial begin
        errors = 0;
        accepted_tx = 0;
        accepted_gpio = 0;
        rejected = 0;
        frames = 0;
        last_tx_byte = 8'h00;
        last_tx_good = 0;
        last_tx_duration = 0;
        rst_n = 1'b0;
        clear_bus();
        gpio_in_async = 8'h00;
        repeat (3) @(posedge clk);
        @(negedge clk);
        #1;
        rst_n = 1'b1;
        repeat (2) @(posedge clk);
        #1;

        if (N == 234) begin
            // N234 minimal: normal frame, repeat/ busy rejection, reset recovery.
            $display("TEST_BEGIN W05-N234");
            request(1'b1, 1'b1, 8'h00, {24'h000000, 8'h5A}, 4'b1111, 1'b0, "W05 N234 TX");
            check_tx_frame(8'h5A, "W05 N234 TX");
            wait (dut.tx_ready === 1'b1);
            $display("TEST_PASS W05-N234");

            $display("TEST_BEGIN W06-N234");
            request(1'b1, 1'b1, 8'h00, {24'h000000, 8'hA5}, 4'b1111, 1'b0, "W06 N234 first");
            wait (dut.tx_busy === 1'b1);
            request(1'b1, 1'b1, 8'h00, {24'h000000, 8'h3C}, 4'b1111, 1'b1, "W06 N234 busy reject");
            check_tx_frame(8'hA5, "W06 N234 first");
            wait (dut.tx_ready === 1'b1);
            request(1'b1, 1'b1, 8'h00, {24'h000000, 8'hA5}, 4'b1111, 1'b0, "W06 N234 repeat");
            check_tx_frame(8'hA5, "W06 N234 repeat");
            wait (dut.tx_ready === 1'b1);
            $display("TEST_PASS W06-N234");

            $display("TEST_BEGIN W09-N234");
            tx_reset_case(2, 8'h96, "W09 N234 start reset");
            tx_reset_case(4*N, 8'h96, "W09 N234 data reset");
            tx_reset_case(9*N+2, 8'h96, "W09 N234 stop reset");
            $display("TEST_PASS W09-N234");
        end else begin
            // ---------------- W01 reset / first release ----------------
            $display("TEST_BEGIN W01");
            begin : w01
                integer e0;
                e0 = errors;
                rst_n = 1'b0;
                clear_bus();
                gpio_in_async = 8'h00;
                repeat (3) @(posedge clk);
                @(negedge clk);
                io_sel = 1'b1;
                io_addr = 8'h08;
                #1;
                if (io_rdata !== 32'h00000000 || gpio_out !== 8'h00 || uart_tx !== 1'b1 || io_wr_error !== 1'b0) begin
                    errors = errors + 1;
                    $display("CHK_FAIL W01 reset rdata=%08x out=%02x tx=%b err=%b", io_rdata, gpio_out, uart_tx, io_wr_error);
                end
                // Release and request on the same edge: pre-edge ready is 0.
                rst_n = 1'b1;
                io_sel = 1'b1;
                io_wr_en = 1'b1;
                io_addr = 8'h00;
                io_wdata = 32'h0000005A;
                io_wstrb = 4'b1111;
                #1;
                if (io_wr_error !== 1'b1) begin
                    errors = errors + 1;
                    $display("CHK_FAIL W01 release-edge accept error=%b expected=1", io_wr_error);
                end
                @(posedge clk);
                #1;
                if (dut.tx_busy !== 1'b0) begin
                    errors = errors + 1;
                    $display("CHK_FAIL W01 accepted on release edge busy=%b", dut.tx_busy);
                end
                clear_bus();
                repeat (2) @(posedge clk);
                #1;
                report_test("W01", e0);
            end

            // ---------------- W02 unselected / passive reads ----------------
            $display("TEST_BEGIN W02");
            begin : w02
                integer e0;
                e0 = errors;
                read_check(8'h08, {31'b0, dut.tx_ready}, "W02 STATUS");
                read_check(8'h00, 32'h00000000, "W02 TXDATA");
                read_check(8'h0c, {24'b0, gpio_out}, "W02 GPIO_OUT");
                read_check(8'h10, {24'b0, dut.gpio_in_sync}, "W02 GPIO_IN");
                read_check(8'h04, 32'h00000000, "W02 reserved");
                read_check(8'h02, 32'h00000000, "W02 nonaligned");
                request(1'b0, 1'b1, 8'h0c, 32'h000000AA, 4'b1111, 1'b0, "W02 unselected write");
                request(1'b1, 1'b0, 8'h0c, 32'h000000BB, 4'b1111, 1'b0, "W02 wr_en0");
                if (gpio_out !== 8'h00 || uart_tx !== 1'b1) begin
                    errors = errors + 1;
                    $display("CHK_FAIL W02 side effect out=%02x tx=%b", gpio_out, uart_tx);
                end
                report_test("W02", e0);
            end

            // ---------------- W03 GPIO A,A,B / high bits ----------------
            $display("TEST_BEGIN W03");
            begin : w03
                integer e0;
                e0 = errors;
                request(1'b1, 1'b1, 8'h0c, {24'hABCDEF, 8'hA5}, 4'b1111, 1'b0, "W03 A first");
                if (gpio_out !== 8'hA5) fail("W03 A first output");
                read_check(8'h0c, 32'h000000A5, "W03 A first read");
                request(1'b1, 1'b1, 8'h0c, {24'h123456, 8'hA5}, 4'b1111, 1'b0, "W03 A repeat");
                if (gpio_out !== 8'hA5) fail("W03 A repeat output");
                request(1'b1, 1'b1, 8'h0c, {24'hFFFFFF, 8'h5A}, 4'b1111, 1'b0, "W03 B");
                if (gpio_out !== 8'h5A) fail("W03 B output");
                read_check(8'h0c, 32'h0000005A, "W03 B read");
                if (accepted_gpio < 3) fail("W03 accepted_gpio count");
                if (uart_tx !== 1'b1) fail("W03 GPIO caused TX");
                report_test("W03", e0);
            end

            // ---------------- W04 GPIO input two-stage ----------------
            $display("TEST_BEGIN W04");
            begin : w04
                integer e0;
                e0 = errors;
                @(negedge clk);
                gpio_in_async = 8'h3C;
                @(posedge clk);
                #1;
                if (dut.gpio_in_sync !== 8'h00) begin
                    errors = errors + 1;
                    $display("CHK_FAIL W04 E0 sync=%02x expected=00", dut.gpio_in_sync);
                end
                @(posedge clk);
                #1;
                if (dut.gpio_in_sync !== 8'h3C) begin
                    errors = errors + 1;
                    $display("CHK_FAIL W04 E1 sync=%02x expected=3c", dut.gpio_in_sync);
                end
                read_check(8'h10, 32'h0000003C, "W04 GPIO_IN read");
                if (gpio_out !== 8'h5A) fail("W04 input fed output");
                report_test("W04", e0);
            end

            // ---------------- W05 TX normal frame ----------------
            $display("TEST_BEGIN W05");
            begin : w05
                integer e0;
                e0 = errors;
                request(1'b1, 1'b1, 8'h00, {24'hDEADBE, 8'h5A}, 4'b1111, 1'b0, "W05 TX 5A");
                check_tx_frame(8'h5A, "W05 TX 5A");
                wait (dut.tx_ready === 1'b1);
                read_check(8'h08, 32'h00000001, "W05 STATUS ready");
                report_test("W05", e0);
            end

            // ---------------- W06 busy reject / repeat ----------------
            $display("TEST_BEGIN W06");
            begin : w06
                integer e0;
                e0 = errors;
                request(1'b1, 1'b1, 8'h00, {24'h000000, 8'hA5}, 4'b1111, 1'b0, "W06 first");
                wait (dut.tx_busy === 1'b1);
                request(1'b1, 1'b1, 8'h00, {24'h000000, 8'h3C}, 4'b1111, 1'b1, "W06 busy reject");
                check_tx_frame(8'hA5, "W06 first frame");
                wait (dut.tx_ready === 1'b1);
                request(1'b1, 1'b1, 8'h00, {24'h000000, 8'hA5}, 4'b1111, 1'b0, "W06 repeat");
                check_tx_frame(8'hA5, "W06 repeat frame");
                wait (dut.tx_ready === 1'b1);
                report_test("W06", e0);
            end

            // ---------------- W07 invalid requests ----------------
            $display("TEST_BEGIN W07");
            begin : w07
                integer e0;
                e0 = errors;
                request(1'b1, 1'b1, 8'h04, 32'h00000001, 4'b1111, 1'b1, "W07 04");
                request(1'b1, 1'b1, 8'h14, 32'h00000002, 4'b1111, 1'b1, "W07 14");
                request(1'b1, 1'b1, 8'h08, 32'h00000003, 4'b1111, 1'b1, "W07 STATUS write");
                request(1'b1, 1'b1, 8'h10, 32'h00000004, 4'b1111, 1'b1, "W07 GPIO_IN write");
                request(1'b1, 1'b1, 8'h02, 32'h00000005, 4'b1111, 1'b1, "W07 nonaligned");
                request(1'b1, 1'b1, 8'h0c, 32'h00000006, 4'b0000, 1'b1, "W07 strobe 0");
                request(1'b1, 1'b1, 8'h0c, 32'h00000007, 4'b0001, 1'b1, "W07 strobe 1");
                request(1'b1, 1'b1, 8'h0c, 32'h00000008, 4'b0011, 1'b1, "W07 strobe 3");
                request(1'b1, 1'b1, 8'h00, 32'h00000009, 4'b1100, 1'b1, "W07 TX strobe 12");
                if (gpio_out !== 8'h5A || uart_tx !== 1'b1) begin
                    errors = errors + 1;
                    $display("CHK_FAIL W07 side effect out=%02x tx=%b", gpio_out, uart_tx);
                end
                report_test("W07", e0);
            end

            // ---------------- W08 consecutive/no dedup ----------------
            $display("TEST_BEGIN W08");
            begin : w08
                integer e0;
                e0 = errors;
                request(1'b1, 1'b1, 8'h0c, 32'h00000011, 4'b1111, 1'b0, "W08 11a");
                request(1'b1, 1'b1, 8'h0c, 32'h00000011, 4'b1111, 1'b0, "W08 11b");
                request(1'b1, 1'b1, 8'h0c, 32'h00000022, 4'b1111, 1'b0, "W08 22");
                if (gpio_out !== 8'h22) fail("W08 final output");
                read_check(8'h0c, 32'h00000022, "W08 readback");
                if (accepted_gpio < 6) fail("W08 accepted count");
                if (rejected < 8) fail("W08 rejected count");
                report_test("W08", e0);
            end

            // ---------------- W09 resets ----------------
            $display("TEST_BEGIN W09");
            begin : w09
                integer e0;
                e0 = errors;
                tx_reset_case(2, 8'h96, "W09 start reset");
                tx_reset_case(4*N, 8'h96, "W09 data reset");
                tx_reset_case(9*N+2, 8'h96, "W09 stop reset");
                report_test("W09", e0);
            end

            // ---------------- W10 checker control/negative ----------------
            $display("TEST_BEGIN W10");
            begin : w10
                integer e0;
                e0 = errors;
                // last_tx_byte is from the final W09 recovery frame.
                if (last_tx_byte === 8'h6A && last_tx_good === 1)
                    $display("W10_CONTROL_PASS");
                else
                    fail("W10 control byte/good");
                if (last_tx_byte !== 8'h00)
                    $display("W10_NEGATIVE_DETECTED wrong-byte");
                else
                    fail("W10 checker missed wrong byte");
                if ((accepted_tx === 9) && (frames === 6) &&
                    (accepted_gpio === 6) && (rejected === 10))
                    $display("W10_COUNT_PASS tx=%0d frames=%0d gpio=%0d rejected=%0d",
                             accepted_tx, frames, accepted_gpio, rejected);
                else
                    fail("W10 count control: missing/extra frame or duplicate GPIO acceptance possible");
                report_test("W10", e0);
            end
        end

        if (errors == 0)
            $display("REGIF_M1_SELFCHECK_PASS accepted_tx=%0d accepted_gpio=%0d rejected=%0d frames=%0d",
                     accepted_tx, accepted_gpio, rejected, frames);
        else
            $display("REGIF_M1_SELFCHECK_FAIL errors=%0d", errors);
        $finish;
    end

endmodule
