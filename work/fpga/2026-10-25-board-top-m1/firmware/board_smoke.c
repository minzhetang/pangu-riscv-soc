#include <stdint.h>
#define REG32(off) (*(volatile uint32_t *)(uintptr_t)(0x20000000u+(off)))
#define TXDATA REG32(0x00)
#define STATUS REG32(0x08)
#define GPIO_OUT REG32(0x0c)
#define GPIO_IN REG32(0x10)
volatile uint32_t boot_cookie=0x13579bdfu;
volatile uint32_t boot_bss[4];
volatile uint32_t results[8];
volatile uint32_t signature;
static const uint8_t hexchars[]="0123456789ABCDEF";
static void put(uint32_t v) {
    while ((STATUS & 1u)==0) { }
    TXDATA=v;
}
int main(void) {
    uint32_t error=0;
    results[0]=boot_cookie;
    results[1]=boot_bss[0]|boot_bss[1]|boot_bss[2]|boot_bss[3];
    results[2]=GPIO_IN;
    GPIO_OUT=0x5a; results[3]=GPIO_OUT;
    GPIO_OUT=0x5a; results[4]=GPIO_OUT;
    GPIO_OUT=0xa5; results[5]=GPIO_OUT;
    if (results[0]!=0x13579bdfu || results[1]!=0 || (results[2]&~15u)!=0)
        error|=1;
    if (results[3]!=0x5a || results[4]!=0x5a || results[5]!=0xa5) error|=2;
    put('B'); put(hexchars[results[2]&15u]); put('\r'); put('\n'); put('A'); put('A');
    while ((STATUS & 1u)==0) { }
    results[6]=error; results[7]=6;
    signature=error?(0xbad00000u|error):0x424d3031u;
    return (int)error;
}
