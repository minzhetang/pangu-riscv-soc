typedef unsigned int u32;
#define IO(a) (*(volatile u32 *)(a))
#define TIMER IO(0x20000100)
#ifndef DENSE
#define DENSE 0
#endif
struct event {u32 tick,index,state,reason;};
volatile struct event events[8];
volatile u32 samples[32][2], head,count,evicted,rejected,fault,post,frozen;
volatile u32 start_tick,end_tick,work_ticks,late,complete;
static u32 stable,candidate,consecutive,age;
static void put(char c){while(!(IO(0x20000008)&1)){} IO(0x20000000)=(u32)c;}
static void text(const char*s){while(*s)put(*s++);}
static void hex(u32 v){for(int i=28;i>=0;i-=4)put("0123456789abcdef"[(v>>i)&15]);}
static void word(u32 v){hex(v);put(' ');}
static void append(u32 t,u32 i,u32 s,u32 why){
 if(frozen){rejected++;return;}
 events[head]=(struct event){t,i,s,why};head=(head+1)&7;
 if(count<8)count++;else evicted++;
 if(why&&!fault){fault=why;post=2;}
 else if(fault&&post&&!--post)frozen=1;
}
int main(void){
 IO(0x2000000c)=0x40; /* scope marker, not an input handshake */
 start_tick=TIMER;u32 deadline=start_tick+12000;
 for(u32 i=0;i<32;i++,deadline+=12000){
  while((int)(TIMER-deadline)<0){}
  u32 begin=TIMER;
  u32 s=IO(0x20000010)&7;
  u32 t=TIMER;
  /* Audit snapshots are common instrumentation, excluded from product storage claims. */
  samples[i][0]=t;samples[i][1]=s;
  if(begin-deadline>1000)late++;
  age++;
  if(s!=candidate){candidate=s;consecutive=1;}else if(consecutive<2)consecutive++;
  if(consecutive==2&&s!=stable){u32 old=stable;stable=s;age=0;
   u32 legal=(old==0&&s==1)||(old==1&&s==3)||(old==3&&s==7)||(old==7&&s==0);
   append(t,i,s,legal?0:1);
  }
  if(!fault&&stable==1&&age>=6)append(t,i,stable,2);
  /* Dense mode models an additional raw-record storage write on the same samples. */
  if(DENSE){extern volatile u32 raw[32][2];raw[i][0]=t;raw[i][1]=s;}
  work_ticks+=TIMER-begin;
 }
 end_tick=TIMER;
 IO(0x2000000c)=fault?0x81:0xa5;
 text("REC1 ");word(DENSE);word(start_tick);word(end_tick);word(work_ticks);word(late);
 word(count);word(evicted);word(rejected);word(fault);word(frozen);put('\n');
 if(DENSE)for(u32 i=0;i<32;i++){text("S ");word(i);word(samples[i][0]);word(samples[i][1]);put('\n');}
 for(u32 k=0;k<count;k++){u32 slot=(head+8-count+k)&7;text("E ");word(events[slot].tick);word(events[slot].index);word(events[slot].state);word(events[slot].reason);put('\n');}
 text("END\n");while(!(IO(0x20000008)&1)){}complete=1;return 0;
}
volatile u32 raw[32][2];
