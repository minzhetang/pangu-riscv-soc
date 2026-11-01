#include <stdint.h>
#include "timer.h"
static volatile union { uint32_t w[4];uint16_t h[8];uint8_t b[16];int8_t sb[16];int16_t sh[8]; } scratch;
static void text(const char*s){while(*s)uart_byte((unsigned char)*s++);}
static void hx(uint32_t v){for(int i=28;i>=0;i-=4)uart_byte("0123456789abcdef"[(v>>i)&15]);}
static void wait_ticks(uint32_t n){uint64_t a=counter_read();while((uint32_t)(counter_read()-a)<n){}}
static const uint32_t vec[][3]={
{0x00000000u,0x00000000u,0x00000000u},
{0x00000000u,0x00000001u,0x00000000u},
{0x00000000u,0x00000002u,0x00000000u},
{0x00000000u,0xffffffffu,0x00000000u},
{0x00000000u,0x80000000u,0x00000000u},
{0x00000000u,0x7fffffffu,0x00000000u},
{0x00000000u,0x55555555u,0x00000000u},
{0x00000000u,0xaaaaaaaau,0x00000000u},
{0x00000001u,0x00000000u,0x00000000u},
{0x00000001u,0x00000001u,0x00000001u},
{0x00000001u,0x00000002u,0x00000002u},
{0x00000001u,0xffffffffu,0xffffffffu},
{0x00000001u,0x80000000u,0x80000000u},
{0x00000001u,0x7fffffffu,0x7fffffffu},
{0x00000001u,0x55555555u,0x55555555u},
{0x00000001u,0xaaaaaaaau,0xaaaaaaaau},
{0x00000002u,0x00000000u,0x00000000u},
{0x00000002u,0x00000001u,0x00000002u},
{0x00000002u,0x00000002u,0x00000004u},
{0x00000002u,0xffffffffu,0xfffffffeu},
{0x00000002u,0x80000000u,0x00000000u},
{0x00000002u,0x7fffffffu,0xfffffffeu},
{0x00000002u,0x55555555u,0xaaaaaaaau},
{0x00000002u,0xaaaaaaaau,0x55555554u},
{0xffffffffu,0x00000000u,0x00000000u},
{0xffffffffu,0x00000001u,0xffffffffu},
{0xffffffffu,0x00000002u,0xfffffffeu},
{0xffffffffu,0xffffffffu,0x00000001u},
{0xffffffffu,0x80000000u,0x80000000u},
{0xffffffffu,0x7fffffffu,0x80000001u},
{0xffffffffu,0x55555555u,0xaaaaaaabu},
{0xffffffffu,0xaaaaaaaau,0x55555556u},
{0x80000000u,0x00000000u,0x00000000u},
{0x80000000u,0x00000001u,0x80000000u},
{0x80000000u,0x00000002u,0x00000000u},
{0x80000000u,0xffffffffu,0x80000000u},
{0x80000000u,0x80000000u,0x00000000u},
{0x80000000u,0x7fffffffu,0x80000000u},
{0x80000000u,0x55555555u,0x80000000u},
{0x80000000u,0xaaaaaaaau,0x00000000u},
{0x7fffffffu,0x00000000u,0x00000000u},
{0x7fffffffu,0x00000001u,0x7fffffffu},
{0x7fffffffu,0x00000002u,0xfffffffeu},
{0x7fffffffu,0xffffffffu,0x80000001u},
{0x7fffffffu,0x80000000u,0x80000000u},
{0x7fffffffu,0x7fffffffu,0x00000001u},
{0x7fffffffu,0x55555555u,0x2aaaaaabu},
{0x7fffffffu,0xaaaaaaaau,0x55555556u},
{0x55555555u,0x00000000u,0x00000000u},
{0x55555555u,0x00000001u,0x55555555u},
{0x55555555u,0x00000002u,0xaaaaaaaau},
{0x55555555u,0xffffffffu,0xaaaaaaabu},
{0x55555555u,0x80000000u,0x80000000u},
{0x55555555u,0x7fffffffu,0x2aaaaaabu},
{0x55555555u,0x55555555u,0x38e38e39u},
{0x55555555u,0xaaaaaaaau,0x71c71c72u},
{0xaaaaaaaau,0x00000000u,0x00000000u},
{0xaaaaaaaau,0x00000001u,0xaaaaaaaau},
{0xaaaaaaaau,0x00000002u,0x55555554u},
{0xaaaaaaaau,0xffffffffu,0x55555556u},
{0xaaaaaaaau,0x80000000u,0x00000000u},
{0xaaaaaaaau,0x7fffffffu,0x55555556u},
{0xaaaaaaaau,0x55555555u,0x71c71c72u},
{0xaaaaaaaau,0xaaaaaaaau,0xe38e38e4u},
{0xbc80841bu,0x174d72e2u,0xcd67a5d6u},
{0x1da3a124u,0xf67a73f9u,0xb8b2e804u},
{0x64e29b77u,0x0f4aa467u,0xac2ac8e1u},
{0xb1f5dab2u,0x0b1c6a96u,0xa413d84cu},
{0x0ce8b406u,0xa6b88aa3u,0xf185dbd2u},
{0x381c4efbu,0x4651d4ccu,0xc761cc04u},
{0x54504aceu,0x201222d6u,0x2789e434u},
{0x245ea262u,0x72485191u,0xda8afb82u},
{0xf6e5148bu,0x8f7199d6u,0x03213f32u},
{0xd53248e0u,0xd7347079u,0xb22671e0u},
{0xd658e2e6u,0x7d115906u,0x4c3d4764u},
{0x174a4488u,0x22e4e4a1u,0xe3de3988u},
{0xe8e5b3e9u,0x9fc7c87bu,0xec0a78f3u},
{0x0058604au,0x5a8330d1u,0x24127c6au},
{0x06bf97c0u,0x7de3f695u,0x5895d2c0u},
{0x6352fef7u,0x1a715734u,0x0288bb2cu},
};
void board_qa(void){
 text("BOARD_QA_M2 BOOT\n");
 scratch.w[0]=0x88776655u;scratch.b[1]=0xa6;scratch.h[1]=0xbeef;
 if(scratch.w[0]!=0xbeefa655u||scratch.sb[1]!=-90||scratch.sh[1]!=-16657){text("RAMTEST FAIL\n");__asm__ volatile("ebreak");}
 text("RAMTEST PASS wstrb/sign/zero\n");
 for(unsigned i=0;i<sizeof(vec)/sizeof(vec[0]);i++){volatile uint32_t a=vec[i][0],b=vec[i][1];uint32_t r=a*b;if(r!=vec[i][2]){text("MULTEST FAIL index=");hx(i);text("\n");__asm__ volatile("ebreak");}}
 text("MULTEST PASS 80\n");
 MMIO32(0x2000000cu)=0;
 for(unsigned i=0;i<8;i++){uint32_t v=1u<<i;MMIO32(0x2000000cu)=v;uint32_t read=MMIO32(0x2000000cu);text("LED ");hx(i);text(" WRITE ");hx(v);text(" READ ");hx(read);text("\n");if(read!=v){text("GPIO_OUT FAIL\n");__asm__ volatile("ebreak");}wait_ticks(13500000u);}
 MMIO32(0x2000000cu)=0xa5u;text("GPIO_INPUT_READY KEY1..4 press/release;120s limit\n");
 uint32_t prev=MMIO32(0x20000010u),pressed=0,released=0;uint64_t began=counter_read(),beat=began;
 text("INPUT ");hx(prev);text("\n");
 while((uint32_t)(counter_read()-began)<3240000000u){
  uint32_t now=MMIO32(0x20000010u);
  if(now!=prev){text("INPUT ");hx(now);text("\n");pressed|=now;released|=prev&~now;prev=now;}
  if((pressed&15u)==15u&&(released&15u)==15u&&now==0){text("GPIO_INPUT PASS press=0000000f release=0000000f\n");return;}
  if((uint32_t)(counter_read()-beat)>=27000000u){text("GPIO_WAIT\n");beat=counter_read();}
 }
 text("GPIO_INPUT TIMEOUT\n");
}
void board_qa_finish(void){MMIO32(0x2000000cu)=0xa5u;text("BOARD_QA_M2 END LED=000000a5\n");uart_drain();}
