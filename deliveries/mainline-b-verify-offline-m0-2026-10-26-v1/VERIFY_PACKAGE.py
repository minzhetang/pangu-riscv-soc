"""A bootstrap integrity check only; no executable content in inputs is run."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as inp:
        for data in iter(lambda: inp.read(1 << 20), b''):
            digest.update(data)
    return digest.hexdigest().upper()


def verify():
    entries, files = {}, set()
    for line in (ROOT / 'SHA256SUMS.txt').read_text(encoding='utf-8-sig').splitlines():
        value, name = line.split(None, 1)
        name = name.lstrip('*')
        rel = PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts or ':' in name or name in entries:
            raise ValueError('unsafe/duplicate manifest path')
        entries[name] = value.upper()
    for path in ROOT.rglob('*'):
        if path.is_symlink() or getattr(path.lstat(), 'st_file_attributes', 0) & 0x400:
            raise ValueError('links/reparse points unsupported')
        if path.is_file() and path.name != 'SHA256SUMS.txt':
            files.add(path.relative_to(ROOT).as_posix())
    if files != set(entries):
        raise ValueError('missing/extra package files; write results OUTSIDE this package')
    for name, expected in entries.items():
        if sha(ROOT / name) != expected:
            raise ValueError('SHA mismatch: ' + name)
    return dict(status='PACKAGE_INTEGRITY_PASS', files=len(files) + 1, manifest=len(entries),
                manifest_SHA256=sha(ROOT / 'SHA256SUMS.txt'), B_implementation_tested=False)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        print(json.dumps(verify(), ensure_ascii=False))
    except Exception as exc:
        print(json.dumps(dict(status='PACKAGE_INTEGRITY_FAIL', error=str(exc)), ensure_ascii=False))
        raise SystemExit(1)
