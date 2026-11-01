#ifndef PROJECT_TIMER_H
#define PROJECT_TIMER_H
#include <stdint.h>
#define MMIO32(a) (*(volatile uint32_t *)(uintptr_t)(a))
static inline uint64_t counter_read(void) {
    uint32_t a,b,lo;
    do { a=MMIO32(0x20000104u);lo=MMIO32(0x20000100u);b=MMIO32(0x20000104u); } while(a!=b);
    return ((uint64_t)a<<32)|lo;
}
static inline void uart_byte(uint32_t v) {
    while((MMIO32(0x20000008u)&1u)==0) { }
    MMIO32(0x20000000u)=v;
}
static inline void uart_drain(void) { while((MMIO32(0x20000008u)&1u)==0) { } }
#endif
