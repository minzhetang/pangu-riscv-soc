"""Bounded, lossless archive prototype for EXISTING evidence, never a DUT checker.

No filtering/deduplication. Input bytes and line order are preserved. Publication
is atomic at manifest creation; sources and raw spool are never deleted here.
"""
from pathlib import Path, PurePosixPath
import gzip, hashlib, json, time, zlib

BLOCK = 4 * 1024 * 1024
LINE = 512
INPUT_CAP = 512 * 1024 * 1024


def digest(data):
    return hashlib.sha256(data).hexdigest().upper()


def dump_new(path, value):
    with Path(path).open('x', encoding='utf-8') as out:
        json.dump(value, out, ensure_ascii=False, indent=2)
        out.write('\n')


def encode(source, destination, deadline):
    source, destination = Path(source), Path(destination)
    assert source.is_file() and source.stat().st_size <= INPUT_CAP
    destination.mkdir(exist_ok=False)
    chunks, total, lines, buf, nbuf = [], 0, 0, bytearray(), 0
    whole = hashlib.sha256()

    def flush():
        nonlocal buf, nbuf
        if not buf:
            return
        raw = bytes(buf)
        packed = gzip.compress(raw, compresslevel=1, mtime=0)
        name = f'block-{len(chunks):06d}.gz'
        assert len(packed) <= BLOCK + 65536
        with (destination / name).open('xb') as out:
            out.write(packed)
        chunks.append(dict(index=len(chunks), file=name, bytes=len(raw),
                           packed_bytes=len(packed), lines=nbuf,
                           first_line=lines - nbuf + 1, last_line=lines,
                           raw_SHA256=digest(raw), packed_SHA256=digest(packed)))
        buf, nbuf = bytearray(), 0

    with source.open('rb') as inp:
        while True:
            assert time.monotonic() <= deadline, 'host stage deadline'
            line = inp.readline(LINE + 1)
            if not line:
                break
            assert len(line) <= LINE, 'oversized record'
            if len(buf) + len(line) > BLOCK:
                flush()
            total += len(line)
            assert total <= INPUT_CAP
            whole.update(line)
            lines += 1
            buf.extend(line)
            nbuf += 1
    flush()
    manifest = dict(format='LOSSLESS-EVIDENCE-BLOCKS-1', block_cap=BLOCK,
                    line_cap=LINE, bytes=total, lines=lines,
                    SHA256=whole.hexdigest().upper(), chunks=chunks)
    dump_new(destination / 'index.json', manifest)
    return manifest


def decode(destination, expected_index_SHA256=None):
    """Yield verified blocks; consumer must exhaust iterator for final checks.

    The frozen external index SHA is mandatory in the production caller; the
    optional argument permits deliberately hostile schema tests without hiding
    behind a single manifest-hash rejection.
    """
    destination = Path(destination)
    index_path = destination / 'index.json'
    assert index_path.stat().st_size <= 2 * 1024 * 1024
    index = index_path.read_bytes()
    if expected_index_SHA256 is not None:
        assert digest(index) == expected_index_SHA256, 'index SHA'
    meta = json.loads(index)
    assert meta['format'] == 'LOSSLESS-EVIDENCE-BLOCKS-1'
    assert meta['block_cap'] == BLOCK and meta['line_cap'] == LINE
    assert 0 <= meta['bytes'] <= INPUT_CAP
    assert len(meta['chunks']) <= INPUT_CAP // (BLOCK - LINE) + 2
    whole, total, lines = hashlib.sha256(), 0, 0
    for number, row in enumerate(meta['chunks']):
        assert row['index'] == number
        assert row['file'] == f'block-{number:06d}.gz'
        name = PurePosixPath(row['file'])
        assert not name.is_absolute() and len(name.parts) == 1 and ':' not in str(name)
        path = destination / str(name)
        assert not path.is_symlink() and not getattr(path.lstat(), 'st_file_attributes', 0) & 0x400
        assert 0 < row['bytes'] <= BLOCK
        assert 0 < path.stat().st_size == row['packed_bytes'] <= BLOCK + 65536
        packed = path.read_bytes()
        assert digest(packed) == row['packed_SHA256'], 'packed SHA'
        dec = zlib.decompressobj(31)
        raw = dec.decompress(packed, BLOCK + 1)
        assert len(raw) <= BLOCK and dec.eof and not dec.unused_data and not dec.unconsumed_tail
        assert len(raw) == row['bytes'] and digest(raw) == row['raw_SHA256'], 'raw SHA'
        records = raw.splitlines(keepends=True)
        assert all(len(line) <= LINE for line in records)
        assert len(records) == row['lines']
        assert row['first_line'] == lines + 1
        assert row['last_line'] == lines + len(records)
        lines += len(records)
        total += len(raw)
        assert total <= INPUT_CAP
        whole.update(raw)
        yield raw
    assert total == meta['bytes'] and lines == meta['lines']
    assert whole.hexdigest().upper() == meta['SHA256'], 'whole SHA'
