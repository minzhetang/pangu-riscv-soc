"""Independent frozen expectations and complete request/apply ledger, no dedup."""
from pathlib import Path
import json,re,hashlib
import stage_redirect as s
def fetch_ledger(path,expected,image,pf,reset=False):
    pending=None;active=None;index=0;requests=hits=cancels=applies=samples=0;actions=[]
    def word(addr):return int.from_bytes(image[addr:addr+4],'little') if 0<=addr<32768 else 0
    for line in path.open(encoding='ascii'):
        a=line.strip().split('|');kind=a[0]
        assert not any(re.search('[xz]',v,re.I) for v in a[1:]),'unknown fetch state'
        if kind=='REQ':
            assert len(a)==4 and pending is None and pf==1
            c=int(a[1]);pc=int(a[2],16);target=int(a[3],16);assert c%2==1 and target%4==0
            pending=dict(cycle=c,pc=pc,target=target,sampled=False);requests+=1
        elif kind=='SAMPLE':
            assert len(a)==5 and pending and not pending['sampled']
            c=int(a[1]);pc=int(a[2],16);tag=int(a[3],16);inst=int(a[4],16)
            assert (c,pc,tag)==(pending['cycle'],pending['pc'],pending['target']) and inst==word(tag)
            pending['sampled']=True;samples+=1
        elif kind=='RESET':
            assert len(a)==3 and reset and cancels==0 and index==0 and pending and pending['sampled']
            assert int(a[1])==pending['cycle'] and int(a[2],16)==pending['target'];pending=None;cancels+=1
        elif kind=='REDIR':
            assert len(a)==7 and active is None and index<len(expected)
            e=expected[index];c=int(a[1]);pc=int(a[2],16);target=int(a[3],16);hit=int(a[4]);tag=int(a[5],16);inst=int(a[6],16)
            want=int(bool(pf and e['eligible']));assert c%2==0 and (pc,target,hit)==(e['pc'],e['target'],want)
            if pf and e['request']:
                assert pending and pending['sampled'] and (pending['cycle']+1,pending['pc'],pending['target'])==(c,pc,target)
                assert tag==target and inst==word(target)
            else:assert pending is None
            active=dict(cycle=c,pc=pc,target=target,hit=hit,expected_word=e['word']);hits+=hit
        elif kind=='APPLY':
            assert len(a)==10 and active is not None
            c=int(a[1]);pc=int(a[2],16);hit=int(a[3]);target=int(a[4],16);regpc=int(a[5],16);valid=int(a[6]);ifpc=int(a[7],16);inst=int(a[8],16);idvalid=int(a[9])
            assert (c,pc,hit,target)==(active['cycle'],active['pc'],active['hit'],active['target'])
            assert idvalid==0 and valid==hit
            assert regpc==((target+4)&0xffffffff if hit else target)
            assert ifpc==(target if hit else 0) and inst==(active['expected_word'] if hit else 0)
            actions.append(active);active=pending=None;index+=1;applies+=1
        else:raise AssertionError('unexpected fetch record '+kind)
    assert active is None and pending is None and index==len(expected)
    assert cancels==int(reset) and requests==samples==sum(bool(pf and e['request']) for e in expected)+cancels
    return dict(requests=requests,hits=hits,applies=applies,cancels=cancels,actions=actions,rows=sum(1 for _ in path.open(encoding='ascii')))
def check(c,pf,d):
    p=s.H/'cases'/c['id'];expected=s.read(p/'expected.json');text=s.log(d/'stdout.log');errors=[]
    def eq(label,a,b):
        if a!=b:errors.append(dict(kind=label,actual=str(a)[:200],expected=str(b)[:200]))
    mm=re.findall(r'^METRICS\|(.*)$',text,re.M);assert len(mm)==1
    metrics={k:int(v) for k,v in (t.split('=') for t in mm[0].split('|'))}
    streams={k:[] for k in ['EX','WB','MEM']};executions=[]
    with (d/'trace.log').open(encoding='ascii') as f:
        for line in f:
            a=line.strip().split('|');assert not any(re.search('[xz]',v,re.I) for v in a[1:]);cy=int(a[1]);assert 1<=cy<=metrics['physical']
            if a[0]=='EX':assert cy%2==0;streams['EX'].append(a[2]);executions.append((cy,int(a[2],16)))
            elif a[0]=='WB':assert cy%2==0;streams['WB'].append(a[2:])
            else:
                assert a[0] in ['READ','STORE'];assert cy%2==(1 if a[0]=='STORE' else 0);streams['MEM'].append([a[0]]+a[2:])
    for k in streams:eq('ordered '+k,streams[k],expected[k])
    regs=[int(x,16) for x in (d/'registers.hex').read_text().split()];eq('all RF',regs,expected['registers'])
    assert s.sha(p/'expected-ram.hex')==expected['ram_SHA256'];eq('all RAM',s.sha(d/'ram.hex'),expected['ram_SHA256'])
    eq('stop',re.findall(r'^STOP\|(\d+)\|([0-9a-f]{8})$',text,re.M),[(str(c['stop_kind']),f"{c['stop_pc']:08x}")])
    assert 'FATAL' not in text and 'SYSTEM_ENDED_NOT_FUNCTIONAL_PASS' in text
    ledger=fetch_ledger(d/'fetch.log',expected['redirects'],(p/'program.bin').read_bytes(),pf,c['reset_pending'])
    hit=sum(int(bool(pf and r['eligible'])) for r in expected['redirects'])
    advances=len(expected['EX'])+2*c['expected_flush']-hit+c['expected_stall']+7
    eq('logical cycle model',metrics['advances'],advances);eq('physical cycle model',metrics['physical'],2*advances+1)
    for k,v in [('stall',c['expected_stall']),('flush',c['expected_flush']),('hits',hit),('requests',ledger['requests']),('applies',ledger['applies']),('cancels',ledger['cancels']),('tail',8)]:eq(k,metrics[k],v)
    bycycle={cy:(pc,i) for i,(cy,pc) in enumerate(executions)};intervals=[]
    for action in ledger['actions']:
        pc,i=bycycle[action['cycle']];assert pc==action['pc']
        if i+1<len(executions):
            nxt,target=executions[i+1];eq('target EX PC',target,action['target']);eq('target EX interval',nxt-action['cycle'],4 if action['hit'] else 6)
            intervals.append(dict(pc=pc,cycle=action['cycle'],target=target,next_cycle=nxt,gap=nxt-action['cycle'],hit=bool(action['hit'])))
        else:eq('terminal target',action['target'],c['stop_pc'])
    return dict(status='PASS' if not errors else 'FAIL',errors=errors,metrics=metrics,
        counts={k:len(v) for k,v in streams.items()},ordered_SHA256={k:hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest().upper() for k,v in streams.items()},
        fetch={k:v for k,v in ledger.items() if k!='actions'},intervals=intervals,full_registers_checked=32,full_RAM_bytes=32768,
        limitations=['one-edge verification memory, actual primitive is later CoreMark stage','no true retirement or unified WB-MEM commit','finite cases; not entire ISA or hardware'])
