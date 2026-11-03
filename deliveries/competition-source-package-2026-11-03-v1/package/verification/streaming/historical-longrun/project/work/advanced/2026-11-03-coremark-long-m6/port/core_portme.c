#include "coremark.h"
#include "timer.h"
#include <stdarg.h>
#if VALIDATION_RUN
volatile ee_s32 seed1_volatile=0x3415, seed2_volatile=0x3415;
#else
volatile ee_s32 seed1_volatile=0, seed2_volatile=0;
#endif
#ifndef ITERATIONS
#define ITERATIONS 1
#endif
#if ITERATIONS < 1 || ITERATIONS > 2147483647
#error "ITERATIONS must be a positive signed 32-bit integer; automatic zero is disabled"
#endif
volatile ee_s32 seed3_volatile=0x66, seed4_volatile=ITERATIONS, seed5_volatile=0;
ee_u32 default_num_contexts=1;
volatile char ram_log[4096];
volatile ee_u32 ram_log_count,ram_log_overflow,port_error;
volatile ee_u32 timing_unavailable=0,timer_start_calls,timer_stop_calls,port_finished;
volatile ee_u32 timing_phase,timer_error;
volatile uint64_t start_ticks,end_ticks,elapsed_ticks,empty_start,empty_end;
static void putch(char ch) {
    if(ram_log_count<4095) { ram_log[ram_log_count++]=ch;ram_log[ram_log_count]=0; }
    else ram_log_overflow=1;
}
static void print_uint(ee_u32 v,unsigned base,unsigned width,char pad) {
    char digits[32];unsigned count=0;
    do { unsigned d=v%base;digits[count++]=(char)(d<10?'0'+d:'a'+d-10);v/=base; } while(v);
    while(width>count) { putch(pad);width--; }
    while(count)putch(digits[--count]);
}
int ee_printf(const char *fmt,...) {
    ee_u32 before=ram_log_count;va_list args;va_start(args,fmt);
    while(*fmt) {
        if(*fmt!='%') { putch(*fmt++);continue; }
        fmt++;char pad=' ';unsigned width=0;int is_long=0;
        if(*fmt=='0') { pad='0';fmt++; }
        while(*fmt>='0'&&*fmt<='9')width=width*10+(*fmt++-'0');
        if(*fmt=='l') { is_long=1;fmt++; }
        char spec=*fmt++;
        if(spec=='s') { const char *s=va_arg(args,const char *);while(*s)putch(*s++); }
        else if(spec=='d') {
            ee_s32 n=is_long?(ee_s32)va_arg(args,long):va_arg(args,int);ee_u32 u=(ee_u32)n;
            if(n<0) { putch('-');u=0U-u; }print_uint(u,10,width,pad);
        } else if(spec=='u'||spec=='x') {
            ee_u32 n=is_long?(ee_u32)va_arg(args,unsigned long):va_arg(args,unsigned int);
            print_uint(n,spec=='x'?16:10,width,pad);
        } else if(spec=='%')putch('%');else { port_error=1;putch('?'); }
    }
    va_end(args);return (int)(ram_log_count-before);
}
void start_time(void) { timer_start_calls++;start_ticks=counter_read();timing_phase=1; }
void stop_time(void) {
    end_ticks=counter_read();timing_phase=2;elapsed_ticks=end_ticks-start_ticks;timer_stop_calls++;
    if(end_ticks<start_ticks||elapsed_ticks>UINT32_MAX)timer_error=1;
}
CORE_TICKS get_time(void) { return timer_error?0:(CORE_TICKS)elapsed_ticks; }
secs_ret time_in_secs(CORE_TICKS ticks) { return ticks/27000000u; }
void portable_init(core_portable *p,int *argc,char *argv[]) {
    (void)argc;(void)argv;
    if(sizeof(ee_u8)!=1||sizeof(ee_u16)!=2||sizeof(ee_u32)!=4||sizeof(void*)!=4)port_error=1;
    empty_start=counter_read();empty_end=counter_read();p->portable_id=1;
}
void portable_fini(core_portable *p) {
    ee_printf("Raw start hi/lo : %08x %08x\n",(ee_u32)(start_ticks>>32),(ee_u32)start_ticks);
    ee_printf("Raw end hi/lo   : %08x %08x\n",(ee_u32)(end_ticks>>32),(ee_u32)end_ticks);
    ee_printf("Raw delta hi/lo : %08x %08x\n",(ee_u32)(elapsed_ticks>>32),(ee_u32)elapsed_ticks);
#ifdef BOARD_RUN
    ee_printf("Timer Hz set    : 27000000\n");
#else
    ee_printf("Timer Hz set    : 27000000; SIM ONLY, NO VALID SCORE\n");
#endif
    timing_phase=3;
    for(ee_u32 i=0;i<ram_log_count;i++)uart_byte((unsigned char)ram_log[i]);
    uart_drain();timing_phase=4;p->portable_id=0;port_finished=1;
}
