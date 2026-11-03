"""Automatic verdict from frozen expectations, fresh RTL logs and resource receipts.
No simulation or changes outside this directory. python check_delivery.py [--replay]
--replay makes one isolated fresh copy and reruns sequential short bounded tests.
"""
import hashlib,json,pathlib,re,shutil,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent
def frozen(filename):
    for line in (ROOT/filename).read_text().splitlines():
        sha,path=line.split('  ',1);assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
def audit():
    for f in ['CACHE_FROZEN_SHA256.txt','CACHE_SUPPLEMENT_SHA256.txt','AI_FROZEN_SHA256.txt']:frozen(f)
    expected=json.loads((ROOT/'vectors/expected.json').read_text())|json.loads((ROOT/'vectors/supplement.json').read_text())
    cache=json.loads((ROOT/'CACHE_RESULTS.json').read_text())+json.loads((ROOT/'CACHE_SUPPLEMENT_RESULTS.json').read_text())
    assert len(cache)==44
    for r in cache:
        for k in ['requests','hits','transactions','bytes','mmio']:assert r[k]==expected[r['key']][k]
        suffix='supplement' if 'lanes' in r['key'] else 'v1'
        log=(ROOT/'logs'/f"cache_{r['key']}_d{r['delay']}_{suffix}.log").read_text()
        assert 'PASS cache' in log
        nums=re.search(r'METRIC requests=(\d+) cycles=(\d+) hits=(\d+) transactions=(\d+) bytes=(\d+) mmio=(\d+)',log)
        assert list(map(int,nums.groups()))==[r[k] for k in ['requests','cycles','hits','transactions','bytes','mmio']]
    ai=json.loads((ROOT/'AI_RESULTS.json').read_text());cases=json.loads((ROOT/'ai_vectors/cases.json').read_text());assert len(ai)==16
    for idx,c in enumerate(cases):
        for s in [0,1]:
            r=ai[idx*2+s];assert r['compute_cycles']==(148 if s else 136)
            assert r['outputs']==[[k,c['raw'][k],c['y'][k]] for k in range(8)]
            log=(ROOT/'logs'/f'ai_{idx}_s{s}_v1.log').read_text()
            assert 'PASS ai' in log
            assert [list(map(int,m)) for m in re.findall(r'OUTPUT row=(\d+) raw=(-?\d+) y=(-?\d+)',log)]==r['outputs']
    special={'cache_reset_concurrent_v1':'RESET_CONCURRENT_PASS','cache_held_valid_supplement':'HELD_VALID_PASS','ai_reset_protocol_v1':'PROTOCOL_PASS',
             'cache_negative_supplement':'data ch','ai_negative_v1':'mismatch'}
    for name,marker in special.items():assert marker in (ROOT/'logs'/f'{name}.log').read_text()
    receipts=list((ROOT/'logs').glob('*.json'));assert len(receipts)==68,len(receipts)
    for p in receipts:
        r=json.loads(p.read_text());negative='negative' in p.stem
        assert r['exit']==int(negative) and r['reason'] is None
        assert r['priority']=='BELOW_NORMAL' and r['seconds']<r['wall_limit_seconds']
    if (ROOT/'SHA256SUMS.txt').exists():frozen('SHA256SUMS.txt')
    print('PASS delivery audit: 44 cache configs + 16 AI configs + directed protocols + expected negatives; 68 bounded process receipts')
def replay():
    dst=ROOT/'recheck-001';dst.mkdir(exist_ok=False)
    names=['cache.sv','cache_tb.sv','backend.sv','fc.sv','ai_tb.sv','run.py','reference_ai.py',
           'reference_cache.py','reference_cache_supplement.py','check_delivery.py','cache_plan.md',
           'cache_supplement_plan.md','ai_plan.md','CACHE_FROZEN_SHA256.txt','CACHE_SUPPLEMENT_SHA256.txt','AI_FROZEN_SHA256.txt']
    for n in names:shutil.copyfile(ROOT/n,dst/n)
    for n in ['vectors','ai_vectors']:shutil.copytree(ROOT/n,dst/n)
    for task in ['cache','cache-supplement','ai']:
        subprocess.run([sys.executable,str(dst/'run.py'),task],check=True,creationflags=0x4000)
    subprocess.run([sys.executable,str(dst/'check_delivery.py')],check=True,creationflags=0x4000)
    print('PASS independent replay:',dst)
if __name__=='__main__':
    audit()
    if '--replay' in sys.argv:replay()
