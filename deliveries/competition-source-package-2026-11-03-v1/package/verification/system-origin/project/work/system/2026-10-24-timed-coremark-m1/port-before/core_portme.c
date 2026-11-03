/* RAM-only correctness port. No UART, host I/O, CSR, MMIO or invented timing. */
#include "coremark.h"
#include <stdarg.h>
#if VALIDATION_RUN
volatile ee_s32 seed1_volatile=0x3415, seed2_volatile=0x3415;
#else
volatile ee_s32 seed1_volatile=0, seed2_volatile=0;
#endif
volatile ee_s32 seed3_volatile=0x66, seed4_volatile=1, seed5_volatile=0;
ee_u32 default_num_contexts=1;
volatile char ram_log[4096];
volatile ee_u32 ram_log_count, ram_log_overflow, port_error;
volatile ee_u32 timing_unavailable=1, timer_start_calls, timer_stop_calls, port_finished;

static void putch(char ch) {
    if (ram_log_count<4095) {
        ram_log[ram_log_count++]=ch;
        ram_log[ram_log_count]=0;
    } else ram_log_overflow=1;
}
static void print_uint(ee_u32 v, unsigned base, unsigned width, char pad) {
    char digits[32]; unsigned count=0;
    do { unsigned d=v%base; digits[count++]=(char)(d<10?'0'+d:'a'+d-10); v/=base; } while(v);
    while (width>count) { putch(pad); width--; }
    while (count) putch(digits[--count]);
}
int ee_printf(const char *fmt, ...) {
    ee_u32 before=ram_log_count;
    va_list args; va_start(args,fmt);
    while (*fmt) {
        if (*fmt!='%') { putch(*fmt++); continue; }
        fmt++;
        char pad=' '; unsigned width=0; int is_long=0;
        if (*fmt=='0') { pad='0'; fmt++; }
        while(*fmt>='0' && *fmt<='9') { width=width*10+(*fmt++-'0'); }
        if (*fmt=='l') { is_long=1; fmt++; }
        char spec=*fmt++;
        if (spec=='s') { const char *s=va_arg(args,const char *); while(*s) putch(*s++); }
        else if(spec=='d') {
            ee_s32 n=is_long?(ee_s32)va_arg(args,long):va_arg(args,int);
            ee_u32 u=(ee_u32)n;
            if(n<0) { putch('-'); u=0U-u; }
            print_uint(u,10,width,pad);
        } else if(spec=='u' || spec=='x') {
            ee_u32 n=is_long?(ee_u32)va_arg(args,unsigned long):va_arg(args,unsigned int);
            print_uint(n,spec=='x'?16:10,width,pad);
        } else if(spec=='%') putch('%');
        else { port_error=1; putch('?'); }
    }
    va_end(args);
    return (int)(ram_log_count-before);
}
/* No timer exists in this CRC-only port. Zero is an explicitly unavailable
   duration, NOT a measurement. Upstream's <10s validity error must remain. */
void start_time(void) { timer_start_calls++; }
void stop_time(void) { timer_stop_calls++; }
CORE_TICKS get_time(void) { return 0; }
secs_ret time_in_secs(CORE_TICKS ticks) { (void)ticks; return 0; }
void portable_init(core_portable *p,int *argc,char *argv[]) {
    (void)argc; (void)argv;
    if(sizeof(ee_u8)!=1 || sizeof(ee_u16)!=2 || sizeof(ee_u32)!=4 || sizeof(void *)!=4)
        port_error=1;
    p->portable_id=1;
}
void portable_fini(core_portable *p) { p->portable_id=0; port_finished=1; }
