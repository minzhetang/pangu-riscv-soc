"""Read-only automatic verdict; no subprocess or simulator launch."""
import hashlib,json,pathlib,re
R=pathlib.Path(__file__).resolve().parent
def hashes(file):
    for line in (R/file).read_text().splitlines():
        sha,name=line.split('  ',1);assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha,name
def main():
    hashes('FROZEN_SHA256.txt');hashes('EXECUTION_SHA256.txt')
    ex=json.loads((R/'EXPECTED.json').read_text());rows=json.loads((R/'RESULTS.json').read_text())
    expected={(key,p,d) for key in ex for p in ['baseline','admission','bypass'] for d in [0,3]}
    assert len(rows)==102 and {(x['key'],x['policy'],x['delay']) for x in rows}==expected
    for r in rows:
        label=f"{r['key']}_{r['policy']}_d{r['delay']}"
        raw=(R/'logs'/f'{label}.log').read_text();assert 'PASS cache' in raw
        m=re.search(r'METRIC requests=(\d+) cycles=(\d+) hits=(\d+) transactions=(\d+) bytes=(\d+) mmio=(\d+)',raw)
        fields=['requests','cycles','hits','transactions','bytes','mmio']
        assert list(map(int,m.groups()))==[r[k] for k in fields]
        for k in fields:
            if k!='cycles':assert r[k]==ex[r['key']][r['policy']][k]
    for p in ['baseline','admission']:
        for mode in [1,2]+([3] if p=='admission' else []):
            marker={1:'RESET_CONCURRENT_PASS',2:'HELD_VALID_PASS',3:'ADMISSION_RESET_PASS'}[mode]
            assert marker in (R/'logs'/f'protocol_{p}_{mode}.log').read_text()
    assert 'data ch' in (R/'logs/negative_admission.log').read_text()
    receipts=list((R/'logs').glob('*.json'));assert len(receipts)==110
    for p in receipts:
        r=json.loads(p.read_text());assert r['exit']==int(p.stem=='negative_admission') and r['reason'] is None
        assert r['priority']=='BELOW_NORMAL' and r['seconds']<20
    if (R/'SHA256SUMS.txt').exists():hashes('SHA256SUMS.txt')
    # Protect every pre-existing M0 manifest entry, including original AI evidence.
    parent=R.parent
    for line in (parent/'SHA256SUMS.txt').read_text().splitlines():
        sha,name=line.split('  ',1);assert hashlib.sha256((parent/name).read_bytes()).hexdigest()==sha,name
    print('PASS M1 audit: 102 configs +5 protocols +1 expected negative; 110 bounded process receipts; M0 preserved')
if __name__=='__main__':main()
