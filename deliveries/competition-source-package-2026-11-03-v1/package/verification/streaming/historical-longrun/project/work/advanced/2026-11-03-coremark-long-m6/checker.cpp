#include "engine.hpp"
#ifdef REPLAY
int main(int argc,char**argv){try{
 need(argc==4,"replay bin run-dir timer-kind");Engine e;e.load(argv[1]);std::string d=argv[2];
 if(std::string(argv[3])=="clock"){
  std::ifstream t(d+"/timer-reads.txt");std::string tag,ad,va;uint32_t edge;
  while(t>>tag>>edge>>ad>>va)e.clock_read(edge,std::stoul(ad,nullptr,16),std::stoul(va,nullptr,16));
 }else for(int i=0;i<12;i++)e.timer.push_back({0,i%3==1?0x20000100u:0x20000104u,0});
 std::ifstream w(d+"/wb.txt"),s(d+"/store.txt");need(bool(w)&&bool(s),"replay streams");
 while(!e.done){auto x=e.next();std::string tag,sa,sb,sc;uint32_t aa=0,bb=0,cc=0;
  if(x.tag==1){need(bool(w>>tag>>aa>>sb)&&tag=="WB","missing WB");bb=std::stoul(sb,nullptr,16);}
  else {need(bool(s>>tag>>sa>>sb>>sc)&&tag=="STORE","missing STORE");aa=std::stoul(sa,nullptr,16);bb=std::stoul(sb,nullptr,16);cc=std::stoul(sc,nullptr,16);}
  need(x.a==aa&&x.b==bb&&x.c==cc,"replay event mismatch");
 }std::string tail;need(!(w>>tail)&&!(s>>tail),"extra replay events");
 std::ifstream state(d+"/state.txt");std::string tag,val;unsigned index,count=0;
 while(state>>tag){if(tag=="REG"||tag=="MEM"){state>>index>>val;need(std::stoul(val,nullptr,16)==(tag=="REG"?e.regs.at(index):e.word(index*4)),"replay state mismatch");count++;}else std::getline(state,tail);}
 std::ifstream uf(d+"/uart.txt",std::ios::binary);std::string u((std::istreambuf_iterator<char>(uf)),{});
 for(size_t p=0;(p=u.find("\r\n",p))!=std::string::npos;)u.erase(p,1);
 need(u==e.uart&&count==32+24576,"replay UART/state length");
 printf("MATCH instructions=%llu wb=%llu stores=%llu timer_used=%u\n",(unsigned long long)e.steps,(unsigned long long)e.wb,(unsigned long long)e.stores,e.timer_used);return 0;
 }catch(const std::exception&e){fprintf(stderr,"REJECT %s\n",e.what());return 3;}}
#else
#include "vpi_user.h"
static Engine engine;static FILE*trace=nullptr;static uint64_t records=0,totalbytes=0;
static unsigned chunk=0,chunkrecords=0,regchecks=0,memchecks=0;static bool failed=false;
static void close_chunk(){if(trace){need(fclose(trace)==0,"trace close");trace=nullptr;char a[100],b[100];snprintf(a,sizeof a,"trace/%06u.bin.part",chunk);snprintf(b,sizeof b,"trace/%06u.bin",chunk);need(rename(a,b)==0,"trace rename");chunk++;chunkrecords=0;}}
static void record(uint32_t tag,uint32_t cy,uint32_t a,uint32_t b,uint32_t c){
 need(totalbytes+20<=8ull*1024*1024*1024,"raw trace byte limit");
 if(!trace){char p[100];snprintf(p,sizeof p,"trace/%06u.bin.part",chunk);trace=fopen(p,"wb");need(trace!=nullptr,"trace open");setvbuf(trace,nullptr,_IOFBF,1024*1024);}
 uint32_t v[]={tag,cy,a,b,c};need(fwrite(v,20,1,trace)==1,"trace write");totalbytes+=20;records++;
 if(++chunkrecords==524288)close_chunk();
}
static std::vector<vpiHandle> args(){auto i=vpi_iterate(vpiArgument,vpi_handle(vpiSysTfCall,nullptr));std::vector<vpiHandle>a;vpiHandle h;while(i&&(h=vpi_scan(i)))a.push_back(h);return a;}
static uint32_t num(vpiHandle h){s_vpi_value v{};v.format=vpiVectorVal;vpi_get_value(h,&v);need(v.value.vector[0].bval==0,"X/Z task argument");return v.value.vector[0].aval;}
static std::string str(vpiHandle h){s_vpi_value v{};v.format=vpiStringVal;vpi_get_value(h,&v);return v.value.str;}
static void failure(const std::string&s){if(failed)return;failed=true;FILE*f=fopen("checker-failure.txt","wb");if(f){fprintf(f,"%s\n",s.c_str());fclose(f);}try{close_chunk();}catch(...){}vpi_printf("CHECKER_FAIL %s\n",s.c_str());vpi_control(vpiFinish,1);}
static PLI_INT32 call(PLI_BYTE8*ud){try{
 auto a=args();int which=int(intptr_t(ud));
 if(which==0){need(a.size()==1,"init args");engine.load(str(a[0]));}
 else if(which==1){need(a.size()==3,"wb args");uint32_t cy=num(a[0]),rd=num(a[1]),v=num(a[2]);need(rd>0&&rd<32,"wb rd");record(1,cy,rd,v,0);engine.accept({1,rd,v,0});}
 else if(which==2){need(a.size()==4,"store args");uint32_t cy=num(a[0]),ad=num(a[1]),v=num(a[2]),mask=num(a[3]);record(2,cy,ad,v,mask);engine.accept({2,ad,v,mask});}
 else if(which==3){need(a.size()==3,"timer args");uint32_t cy=num(a[0]),ad=num(a[1]),v=num(a[2]);record(3,cy,ad,v,0);engine.clock_read(cy,ad,v);}
 else if(which==4){need(a.size()==3,"state args");uint32_t kind=num(a[0]),idx=num(a[1]),v=num(a[2]);
  if(kind==0){need(idx==regchecks&&idx<32,"register snapshot order");need(engine.regs[idx]==v,"register snapshot mismatch");regchecks++;}
  else {need(kind==1&&idx==memchecks&&idx<24576,"memory snapshot order");need(engine.word(idx*4)==v,"memory snapshot mismatch");memchecks++;}}
 else if(which==5){need(a.size()==1,"finish args");need(engine.done&&engine.pending[1].empty()&&engine.pending[2].empty()&&regchecks==32&&memchecks==24576&&engine.timer_used==12&&engine.timer_seen==12&&engine.timer.empty(),"incomplete reference/state/timer");close_chunk();
  std::ofstream u("reference-uart.txt",std::ios::binary);u<<engine.uart;u.close();
  std::ofstream f("checker-final.json");f<<"{\"status\":\"MATCH\",\"instructions\":"<<engine.steps<<",\"wb\":"<<engine.wb<<",\"stores\":"<<engine.stores<<",\"records\":"<<records<<",\"raw_bytes\":"<<totalbytes<<",\"chunks\":"<<chunk<<",\"timer_reads\":12,\"register_checks\":32,\"word_checks\":24576,\"cycles\":"<<num(a[0])<<"}\n";f.close();
  vpi_printf("CHECKER_MATCH instructions=%llu wb=%llu stores=%llu\n",(unsigned long long)engine.steps,(unsigned long long)engine.wb,(unsigned long long)engine.stores);
 }
 }catch(const std::exception&e){failure(e.what());}return 0;}
static void regall(){const char*names[]={"$stream_init","$stream_wb","$stream_store","$stream_timer","$stream_state","$stream_finish"};for(int i=0;i<6;i++){s_vpi_systf_data d{};d.type=vpiSysTask;d.tfname=const_cast<char*>(names[i]);d.calltf=call;d.user_data=reinterpret_cast<PLI_BYTE8*>(intptr_t(i));vpi_register_systf(&d);}}
extern "C" { void(*vlog_startup_routines[])()={regall,nullptr}; }
#endif
