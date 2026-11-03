#include "engine.hpp"
#include <fcntl.h>
#include <io.h>
int main(int argc,char**argv){try{
 need(argc==3,"bin and run-directory required");_setmode(_fileno(stdin),_O_BINARY);
 Engine e;e.load(argv[1]);uint32_t row[5];uint64_t count=0;
 while(true){size_t n=fread(row,1,20,stdin);if(n==0)break;need(n==20,"truncated binary record");count++;
  if(row[0]==3)e.clock_read(row[1],row[2],row[3]);
  else {need(row[0]==1||row[0]==2,"unknown event tag");e.accept({row[0],row[2],row[3],row[4]});}
 }
 need(!ferror(stdin)&&e.done&&e.pending[1].empty()&&e.pending[2].empty()&&e.timer_seen==12&&e.timer_used==12&&e.timer.empty(),"truncated/missing/extra event stream");
 std::string d=argv[2],tag,val,line;std::ifstream state(d+"/state.txt");unsigned index,checks=0;
 while(state>>tag){if(tag=="REG"||tag=="MEM"){state>>index>>val;need(std::stoul(val,nullptr,16)==(tag=="REG"?e.regs.at(index):e.word(index*4)),"replayed state differs");checks++;}else std::getline(state,line);}
 need(checks==32+24576,"state snapshot incomplete");
 std::ifstream uart(d+"/uart.txt",std::ios::binary);std::string u((std::istreambuf_iterator<char>(uart)),{});
 for(size_t p=0;(p=u.find("\r\n",p))!=std::string::npos;)u.erase(p,1);
 need(u==e.uart,"UART mismatch");
 printf("{\"status\":\"MATCH\",\"records\":%llu,\"instructions\":%llu,\"wb\":%llu,\"stores\":%llu,\"state_checks\":%u}\n",(unsigned long long)count,(unsigned long long)e.steps,(unsigned long long)e.wb,(unsigned long long)e.stores,checks);return 0;
 }catch(const std::exception&e){fprintf(stderr,"REJECT %s\n",e.what());return 3;}}
