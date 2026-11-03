#pragma once
#include <array>
#include <vector>
#include <deque>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <cstdlib>
struct Event { uint32_t tag,a,b,c; };
struct Timer { uint32_t edge,addr,value; };
inline void need(bool ok,const std::string&s){if(!ok)throw std::runtime_error(s);}
inline int32_t sext(uint32_t v,unsigned n){return int32_t(v<<(32-n))>>(32-n);}
struct Engine {
 std::array<uint32_t,32> regs{};std::array<uint8_t,0x18000> mem{};
 std::deque<Timer> timer;std::string uart;uint32_t pc=0,code=0;
 std::deque<Event> pending[3];
 uint64_t steps=0,wb=0,stores=0,limit=700000000;bool done=false;
 unsigned timer_seen=0,timer_used=0;
 void load(const std::string&bin){
  std::ifstream f(bin,std::ios::binary);need(bool(f),"open binary");
  std::vector<char>b((std::istreambuf_iterator<char>(f)),{});code=uint32_t(b.size());
  need(code>0&&code<=32768&&code%4==0,"binary size");
  for(unsigned i=0;i<32768;i+=4)mem[i]=0x13;
  memcpy(mem.data(),b.data(),b.size());
 }
 uint32_t word(uint32_t a)const{need(a+4<=mem.size(),"word address");uint32_t v=0;memcpy(&v,mem.data()+a,4);return v;}
 void clock_read(uint32_t edge,uint32_t addr,uint32_t value){
  need(edge>=2&&(addr==0x20000100||addr==0x20000104),"timer address/edge");
  uint32_t expect=addr==0x20000100?edge-2:0;
  need(value==expect,"timer clock equation");need(++timer_seen<=12,"too many timer reads");
  timer.push_back({edge,addr,expect});
 }
 Event next(){
  need(!done,"extra event after done");
  while(++steps<=limit){
   need(pc%4==0&&pc+4<=code,"reference fetch range/alignment");
   uint32_t ins=word(pc),op=ins&127,rd=ins>>7&31,rs1=ins>>15&31,rs2=ins>>20&31,
    fun=ins>>12&7,hi=ins>>25,a=regs[rs1],b=regs[rs2],nxt=pc+4,val=0;
   bool wr=false,store=false;Event event{};
   switch(op){
    case 0x37:val=ins&0xfffff000;wr=true;break;
    case 0x17:val=pc+(ins&0xfffff000);wr=true;break;
    case 0x6f:{int32_t im=sext((ins>>31<<20)|((ins>>12&255)<<12)|((ins>>20&1)<<11)|((ins>>21&1023)<<1),21);val=pc+4;wr=true;nxt=pc+im;break;}
    case 0x67:need(fun==0,"jalr funct3");val=pc+4;wr=true;nxt=(a+sext(ins>>20,12))&~1u;break;
    case 0x63:{int32_t im=sext((ins>>31<<12)|((ins>>7&1)<<11)|((ins>>25&63)<<5)|((ins>>8&15)<<1),13);bool take=false;
     switch(fun){case 0:take=a==b;break;case 1:take=a!=b;break;case 4:take=int32_t(a)<int32_t(b);break;case 5:take=int32_t(a)>=int32_t(b);break;case 6:take=a<b;break;case 7:take=a>=b;break;default:need(false,"branch encoding");}if(take)nxt=pc+im;break;}
    case 3:case 0x23:{
     int32_t im=op==3?sext(ins>>20,12):sext((ins>>25<<5)|(ins>>7&31),12);
     uint32_t addr=a+im,n=fun==0||fun==4?1:fun==1||fun==5?2:fun==2?4:0;
     need(n!=0&&(op==3||fun<=2),"load/store encoding");
     bool io=addr==0x20000000||addr==0x20000008||addr==0x20000100||addr==0x20000104;
     need(addr%n==0&&(io||(uint64_t(addr)+n<=mem.size()&&(addr<0x8000||addr>=0x10000))),"data address/alignment");
     if(op==3){
      if(addr==0x20000100||addr==0x20000104){need(!timer.empty(),"timer input unavailable before reference load");auto t=timer.front();timer.pop_front();need(t.addr==addr,"reference timer read order");val=t.value;timer_used++;}
      else if(io)val=addr==0x20000008?1:0;
      else {val=0;memcpy(&val,mem.data()+addr,n);}
      if(fun<4&&n<4)val=sext(val,n*8);wr=true;
     }else{
      if(io){need(addr==0x20000000,"forbidden MMIO store");uart+=char(b&255);}
      else {need(addr>=0x10000,"store to ROM");memcpy(mem.data()+addr,&b,n);}
      unsigned lane=addr%4;uint32_t mask=n==4?0xffffffffu:(1u<<(8*n))-1;
      event={2,addr,(b&mask)<<(lane*8),((1u<<n)-1)<<lane};store=true;stores++;
      if(addr==0x17ffc&&b==0x600d600d)done=true;
     }break;}
    case 0x13:case 0x33:{uint32_t rhs=op==0x13?uint32_t(sext(ins>>20,12)):b;unsigned sh=rhs&31;
     need(op!=0x33||hi==0||(hi==32&&(fun==0||fun==5)),"R encoding");
     switch(fun){case 0:val=op==0x33&&hi==32?a-rhs:a+rhs;break;case 1:val=a<<sh;break;case 2:val=int32_t(a)<int32_t(rhs);break;case 3:val=a<rhs;break;case 4:val=a^rhs;break;case 5:val=hi==32?uint32_t(int32_t(a)>>sh):a>>sh;break;case 6:val=a|rhs;break;case 7:val=a&rhs;break;}wr=true;break;}
    default:need(false,"unsupported instruction in reference");
   }
   pc=nxt;regs[0]=0;
   if(wr&&rd){regs[rd]=val;wb++;return {1,rd,val,0};}
   if(store)return event;
  }throw std::runtime_error("reference instruction limit");
 }
 void accept(const Event&actual){need(actual.tag==1||actual.tag==2,"event type");
  while(pending[actual.tag].empty()){
   auto e=next();pending[e.tag].push_back(e);
   need(pending[1].size()<=32&&pending[2].size()<=32,"reference unmatched stream limit");
  }
  Event e=pending[actual.tag].front();pending[actual.tag].pop_front();
  if(e.tag!=actual.tag||e.a!=actual.a||e.b!=actual.b||e.c!=actual.c){
  char b[256];snprintf(b,sizeof b,"event mismatch step=%llu nextPC=%08x expect=%u/%08x/%08x/%x actual=%u/%08x/%08x/%x",(unsigned long long)steps,pc,e.tag,e.a,e.b,e.c,actual.tag,actual.a,actual.b,actual.c);throw std::runtime_error(b);}}
};
