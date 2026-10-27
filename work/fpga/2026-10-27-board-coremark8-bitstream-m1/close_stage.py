from pathlib import Path
import hashlib, json, sys, time
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
H = Path(__file__).resolve().parent
P = H.parents[2]
from stage_budget import check, CLOCK
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest().upper()
def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n, obj):
    with (H / n).open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')
if __name__ == '__main__':
    check()
    summary = read(H / 'SUMMARY.json')
    assert summary['status'] == 'SOFTWARE_BITSTREAM_GENERATED_WITH_KNOWN_LIMITS'
    originals = read(H / 'PROTECTED_ORIGINALS.json')['files']
    frozen = read(H / 'FROZEN_INPUTS.json')['files']
    assert all(sha(Path(r['path'])) == r['SHA256'] for r in originals)
    assert all(sha(H / r['path']) == r['SHA256'] for r in frozen)
    assert sha(Path(summary['bitstream']['path'])) == summary['bitstream']['SHA256']
    assert read(H / 'PDS-attempt.json')['used'] == 1
    # No license file is scanned. Only files made inside this independent stage.
    rows = []
    for p in sorted(H.rglob('*')):
        if p.is_file() and p.name not in {'SHA256SUMS.json', 'POSTFLIGHT.json'}:
            assert not p.is_symlink() and not getattr(p.lstat(), 'st_file_attributes', 0) & 0x400
            rows.append(dict(path=p.relative_to(H).as_posix(), bytes=p.stat().st_size, SHA256=sha(p)))
    save('SHA256SUMS.json', dict(files=rows, scope='local evidence; binary/vendor/native logs not Git-distributable'))
    check()
    elapsed = round(time.monotonic() - CLOCK['started_monotonic'], 3)
    save('POSTFLIGHT.json', dict(status='PASS_WITH_DOCUMENTED_LIMITS', originals=len(originals), frozen_inputs=len(frozen), originals_unchanged=True, frozen_unchanged=True, manifest_files=len(rows), manifest_SHA256=sha(H/'SHA256SUMS.json'), local_evidence_bytes=sum(r['bytes'] for r in rows), elapsed_seconds=elapsed, budget_seconds=2400, within_stage_budget=elapsed <= 2400, PDS_invocations=1, new_C=0, new_simulation=0, new_DUT=0, hardware='STOPPED', git_and_documentation_closeout='separate non-build administrative work unit'))
    print(json.dumps(dict(status='CLOSED', elapsed_seconds=elapsed, files=len(rows), originals=len(originals), frozen=len(frozen), SHA256=summary['bitstream']['SHA256'])))
