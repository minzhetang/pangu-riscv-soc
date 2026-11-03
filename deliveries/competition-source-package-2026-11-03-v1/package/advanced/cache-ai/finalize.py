"""One-time evidence manifest generation after all verification and documentation."""
import datetime,hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    target=R/'SHA256SUMS.txt'
    if target.exists():raise RuntimeError('Final manifest already exists; refuse overwrite')
    tools=next(p/'tools/iverilog-13.0-msys2-ucrt64/ucrt64/bin' for p in R.parents if (p/'tools/iverilog-13.0-msys2-ucrt64/ucrt64/bin/vvp.exe').exists())
    suites={}
    for name,path in [('initial',R),('independent_replay',R/'recheck-001')]:
        receipts=[json.loads(p.read_text()) for p in (path/'logs').glob('*.json')]
        assert len(receipts)==68
        suites[name]=dict(processes=len(receipts),max_seconds=max(x['seconds'] for x in receipts),
            sum_process_seconds=sum(x['seconds'] for x in receipts),limits_triggered=sum(x['reason'] is not None for x in receipts),
            positive_exits=sum(x['exit']==0 for x in receipts),expected_negative_exits=sum(x['exit']==1 for x in receipts))
    provenance=dict(created_at=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),
        scope='independent prototype and finite simulation only; synthetic AI tensors',
        mainline_control_actions=0,shared_memory_writes=0,git_commands=0,pds_runs=0,hardware_actions=0,
        tests=suites,tools={p.name:dict(path=str(p),sha256=sha(p)) for p in [tools/'iverilog.exe',tools/'vvp.exe']},
        freeze_order='cache plan/reference/vectors hashed before cache RTL; targeted supplement frozen before supplemental TB/run; AI plan/reference/vectors hashed before FC RTL',
        failure='initial runner WinError2 before compiler launch; empty cache_compile_v1.log retained; corrected path passed; no failed VVP executed',
        model_search='rg --files common onnx/tflite/pt/pth/npz/npy excluding tools and independent deliverable: no filenames; archives not exhausted')
    (R/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2))
    paths=sorted(p for p in R.rglob('*') if p.is_file() and p!=target)
    target.write_text(''.join(sha(p)+'  '+p.relative_to(R).as_posix()+'\n' for p in paths))
    print(json.dumps(dict(files=len(paths),bytes=sum(p.stat().st_size for p in paths),tests=suites),indent=2))
if __name__=='__main__':main()
