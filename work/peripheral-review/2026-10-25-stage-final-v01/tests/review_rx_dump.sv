`timescale 1ns/1ps
module review_rx_dump;
integer k;
final begin
 for(k=0;k<tb_uart_rx.rx_cap.count;k=k+1)
  $display("A_SHARED_RX seq=%0d type=%0d data=%02x edge=%0d",k,tb_uart_rx.rx_cap.etype[k],tb_uart_rx.rx_cap.edata[k],tb_uart_rx.rx_cap.eedge[k]);
end
endmodule
