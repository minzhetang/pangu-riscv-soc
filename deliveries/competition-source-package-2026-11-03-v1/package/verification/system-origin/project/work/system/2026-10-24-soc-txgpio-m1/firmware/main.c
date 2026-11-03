#include <stdint.h>
_Static_assert(sizeof(uint32_t)==4 && sizeof(void *)==4,"RV32 ILP32 required");
#define REG32(offset) (*(volatile uint32_t *)(uintptr_t)(0x20000000u+(offset)))
#define TXDATA REG32(0x00)
#define STATUS REG32(0x08)
#define GPIO_OUT REG32(0x0c)
#define GPIO_IN REG32(0x10)

volatile uint32_t boot_cookie=0x13579bdfu;
volatile uint32_t boot_bss[4];
volatile uint32_t results[12];
volatile uint32_t signature;
static const uint8_t message[12]={'P','G','1','0','0',' ','M','1','\r','\n','A','A'};

__attribute__((noinline,noclone))
static uint32_t stack_checksum(uint32_t x) {
    volatile uint32_t slot[4];
    slot[0]=x;slot[1]=x+3;slot[2]=x*2;
    slot[3]=slot[0]+slot[1]+slot[2];
    return slot[0]+slot[1]+slot[2]+slot[3];
}
static void send_byte(uint32_t value) {
    while((STATUS&1u)==0) { }
    TXDATA=value;
}
int main(void) {
    uint32_t errors=0;
    results[0]=boot_cookie;
    results[1]=boot_bss[0]|boot_bss[1]|boot_bss[2]|boot_bss[3];
    results[2]=stack_checksum(boot_cookie&15u); /* 8*15+6=126 */
    if(results[0]!=0x13579bdfu || results[1]!=0 || results[2]!=126) errors|=1;

    GPIO_OUT=0x5a;results[3]=GPIO_OUT;
    GPIO_OUT=0x5a;results[4]=GPIO_OUT;
    GPIO_OUT=0xa5;results[5]=GPIO_OUT;
    if(results[3]!=0x5a || results[4]!=0x5a || results[5]!=0xa5) errors|=2;
    while((GPIO_IN&255u)!=0x3cu) { }
    results[6]=GPIO_IN;
    for(uint32_t i=0;i<12;i++) send_byte(message[i]);
    while((STATUS&1u)==0) { } /* final stop bit must finish before EBREAK */
    while((GPIO_IN&255u)!=0xc3u) { }
    results[7]=GPIO_IN;
    results[8]=12;results[9]=GPIO_OUT;results[10]=errors;
    signature=errors?0xbad00000u|errors:0x534f4331u;
    return (int)errors;
}
