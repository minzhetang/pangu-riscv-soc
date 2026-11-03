typedef unsigned int u32;
volatile u32 data[32];
__attribute__((noinline)) u32 mix0(u32 x) { return (x<<3)^(x>>7)^0x13579bdfu; }
__attribute__((noinline)) u32 mix1(u32 x) { return (x>>2)+(x<<5)+0x2468ace0u; }
u32 (*volatile operation)(u32);
int main(void) {
 volatile u32 *const out=(volatile u32 *)0x3000;
 u32 x=*(volatile u32 *)0x2000;
 out[0]=0x12345678;
 for(u32 i=0;i<32;i++) {
  x^=x<<13; x^=x>>17; x^=x<<5; data[i]=x&65535;
 }
 for(u32 i=1;i<32;i++) {
  u32 v=data[i],j=i;
  while(j && data[j-1]>v) {data[j]=data[j-1];j--;}
  data[j]=v;
 }
 u32 sum=0,crc=0xffffffff;
 for(u32 i=0;i<32;i++) {
  sum+=data[i];
  u32 v=data[i];
  for(u32 k=0;k<4;k++) {
   crc^=v&255;v>>=8;
   for(u32 b=0;b<8;b++)crc=(crc>>1)^((crc&1)?0xedb88320u:0);
  }
 }
 x=sum;
 for(u32 i=0;i<64;i++) {operation=(i&1)?mix1:mix0;x=operation(x^data[i&31]);}
 out[1]=sum;out[2]=~crc;out[3]=x;
 for(u32 i=1;i<32;i++)if(data[i-1]>data[i])return 1;
 return 0;
}
