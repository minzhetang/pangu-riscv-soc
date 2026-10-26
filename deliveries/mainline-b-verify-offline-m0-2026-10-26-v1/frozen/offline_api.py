"""A-owned offline record adapter, ABI 1.0.0; NOT an ISA/DUT oracle.

Extracts the existing matching principle: consume each record, compare every
field, reject missing/extra records at EOF, preserve duplicates. Full timestamped
observation records are compared here; no claim of architectural retirement.
Only this task's offline wrapper is new. Mainline CPU/reference/TB are unchanged.
"""
from itertools import zip_longest
from pathlib import Path, PurePosixPath
import re
import sys
import time
import zlib

ABI = 'B-VERIFY-OFFLINE-ABI/1.0.0'
MAX_RECORDS = 6_000_000
MAX_BYTES = 512 * 1024 * 1024
MAX_LINE = 512
SENTINEL = object()
TRACE = {
    'EX': ('dec', 'h8'),
    'WB': ('dec', 'rd', 'h8'),
    'READ': ('dec', 'h8', 'h8', 'h8', 'h8'),
    'STORE': ('dec', 'h8', 'h8', 'h8', 'h1'),
}
BUS = {'EDGE': ('dec', 'h2', 'h8', 'bit', 'h8', 'h1', 'h8', 'bit',
                'bit', 'h2', 'bit', 'h2', 'bit', 'bit', 'h16', 'h16')}


class InputError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


def require(ok, message, status='INVALID_INPUT'):
    if not ok:
        raise InputError(status, message)


def runtime_guard():
    require(sys.version_info >= (3, 10), 'Python >=3.10 required', 'TOOL_ERROR')
    # The immutable F153 codec uses assertions. Never run it under -O/-OO.
    require(sys.flags.optimize == 0, 'optimized Python is unsupported')


def child(root, relative):
    root = Path(root).resolve(strict=True)
    rel = PurePosixPath(str(relative).replace('\\', '/'))
    require(not rel.is_absolute() and '..' not in rel.parts and ':' not in str(rel), 'unsafe relative path')
    q = root
    for part in rel.parts:
        q = q / part
        require(not q.is_symlink() and not getattr(q.lstat(), 'st_file_attributes', 0) & 0x400,
                'links/reparse points unsupported')
    q.resolve(strict=True).relative_to(root)
    return q


def parse_record(line, stream):
    require(isinstance(line, bytes) and 0 < len(line) <= MAX_LINE, 'record length/type')
    require(line.endswith(b'\n'), 'unterminated record')
    text = line[:-2] if line.endswith(b'\r\n') else line[:-1]
    try:
        parts = text.decode('ascii').split('|')
    except UnicodeDecodeError as exc:
        raise InputError('INVALID_INPUT', 'non-ASCII record') from exc
    table = TRACE if stream == 'trace' else BUS if stream == 'bus' else {}
    require(parts[0] in table, 'unknown stream or record kind')
    fields = table[parts[0]]
    require(len(parts) == len(fields) + 1, 'field count')
    out = [parts[0]]
    for spec, token in zip(fields, parts[1:]):
        if spec.startswith('h'):
            require(re.fullmatch('[0-9a-fA-F]{' + spec[1:] + '}', token) is not None,
                    'hex width/XZ/character')
            out.append(int(token, 16))
        else:
            require(re.fullmatch('[0-9]+', token) is not None, 'nonnegative decimal required')
            value = int(token)
            ceiling = 1 if spec == 'bit' else 31 if spec == 'rd' else (1 << 64) - 1
            require(0 <= value <= ceiling, 'decimal range')
            require(spec != 'rd' or value != 0, 'WB rd=x0 not emitted by this frozen format')
            out.append(value)
    require(out[1] >= 1, 'cycle is one-based')
    return tuple(out)


def records(root, spec, *, max_records=MAX_RECORDS, max_bytes=MAX_BYTES, deadline=None):
    """Verified local raw/archive records. Exhaustion is required for success."""
    runtime_guard()
    require(spec.get('complete') is True, 'missing complete snapshot receipt', 'INCOMPLETE')
    require(1 <= max_records <= MAX_RECORDS and 1 <= max_bytes <= MAX_BYTES, 'limit policy')
    mode = spec.get('storage')
    try:
        path = child(root, spec['path'])
    except (OSError, ValueError, KeyError) as exc:
        raise InputError('INVALID_INPUT', 'missing/unsafe input path') from exc

    def raw_lines():
        require(path.is_file() and path.stat().st_size <= max_bytes, 'raw byte budget', 'LIMIT')
        with path.open('rb') as inp:
            while True:
                line = inp.readline(MAX_LINE + 1)
                if not line:
                    break
                yield line

    def archive_lines():
        import block_codec
        require(path.is_dir(), 'archive directory required')
        child(root, spec['path'].rstrip('/\\') + '/index.json')
        require(re.fullmatch('[0-9A-F]{64}', spec.get('index_SHA256', '')) is not None,
                'fixed external index SHA required')
        for block in block_codec.decode(path, spec['index_SHA256']):
            # Frozen v1 blocks contain complete LF/CRLF lines, not arbitrary fragments.
            for line in block.splitlines(keepends=True):
                yield line

    require(mode in ('raw', 'archive'), 'storage mode')
    iterator = raw_lines() if mode == 'raw' else archive_lines()
    previous, total, count = 0, 0, 0
    try:
        for line in iterator:
            if deadline is not None:
                require(time.monotonic() <= deadline, 'deadline', 'TIMEOUT')
            total += len(line)
            count += 1
            require(total <= max_bytes and count <= max_records, 'stream budget', 'LIMIT')
            row = parse_record(line, spec['stream'])
            require(row[1] > previous if spec['stream'] == 'bus' else row[1] >= previous,
                    'cycle ordering')
            previous = row[1]
            yield row
    except (AssertionError, OSError, ValueError, KeyError, TypeError, zlib.error) as exc:
        raise InputError('INVALID_INPUT', 'container/record failure: ' + type(exc).__name__) from exc


def compare(expected, actual, *, allow_empty=False, max_records=MAX_RECORDS,
            max_differences=16, deadline=None):
    """Pointwise comparison only: no hash shortcut, masking or deduplication."""
    runtime_guard()
    require(1 <= max_records <= MAX_RECORDS and 1 <= max_differences <= 32, 'comparison limits')
    seen, ne, na, differences, mismatches = 0, 0, 0, [], 0
    for seen, (left, right) in enumerate(zip_longest(expected, actual, fillvalue=SENTINEL), 1):
        if deadline is not None:
            require(time.monotonic() <= deadline, 'deadline', 'TIMEOUT')
        require(seen <= max_records, 'comparison record budget', 'LIMIT')
        ne += int(left is not SENTINEL)
        na += int(right is not SENTINEL)
        if left != right:
            mismatches += 1
            if len(differences) < max_differences:
                differences.append(dict(ordinal=seen,
                    kind='EXTRA' if left is SENTINEL else 'MISSING' if right is SENTINEL else 'FIELD',
                    expected=None if left is SENTINEL else left,
                    actual=None if right is SENTINEL else right))
    require(allow_empty or seen != 0, 'empty stream not allowed', 'INCOMPLETE')
    return dict(status='MATCH' if mismatches == 0 else 'MISMATCH', checked=seen,
                expected_records=ne, actual_records=na, mismatch_count=mismatches,
                differences=differences, fully_consumed=True,
                CPU_function_proven=False, ABI=ABI)
