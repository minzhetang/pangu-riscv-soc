`timescale 1ns/1ps
// Observation only: retain every shared-capture event, no force/control writes.
module review_rx_dump;
    integer i;
    final begin
        $display("REVIEW_RX_CAP_COUNT count=%0d", tb_uart_rx.rx_cap.count);
        for (i=0; i<tb_uart_rx.rx_cap.count; i=i+1)
            $display("REVIEW_RX_CAP seq=%0d type=%0d data=%02x", i,
                     tb_uart_rx.rx_cap.etype[i], tb_uart_rx.rx_cap.edata[i]);
    end
endmodule
