#include "timer.h"
volatile uint32_t initialized=0x13579bdfu;
volatile uint32_t checksum,signature;
volatile uint64_t stamps[4],deltas[2];
int main(void) {
    stamps[0]=counter_read();stamps[1]=counter_read();
    uint32_t sum=0;
    stamps[2]=counter_read();
    for(uint32_t i=1;i<=32;i++) { checksum=sum;sum+=i; }
    checksum=sum;stamps[3]=counter_read();
    deltas[0]=stamps[1]-stamps[0];deltas[1]=stamps[3]-stamps[2];
    uint32_t err=(initialized!=0x13579bdfu)||(checksum!=528u)||
        !(stamps[0]<stamps[1]&&stamps[1]<stamps[2]&&stamps[2]<stamps[3])||
        !(deltas[1]>deltas[0]);
    signature=err?0xbad00001u:0x54494d31u;
    uart_byte('T');uart_byte('I');uart_byte('M');uart_byte('1');uart_byte('\r');uart_byte('\n');uart_drain();
    return (int)err;
}
