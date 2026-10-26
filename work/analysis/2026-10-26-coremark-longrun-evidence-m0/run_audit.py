"""Host-only measurements on F151 evidence; no compiler, ISA replay or DUT."""
from pathlib import Path
import collections, copy, ctypes, gzip, hashlib, json, math, struct, sys, time
from block_codec import BLOCK, LINE, encode, decode, digest, dump_new

P = Path('D:/A_FPGA_Comp')
H = Path(__file__).resolve().parent
B = P / 'work/fpga/2026-10-25-coremark-iter2-m1'
T = P / 'work/fpga/2026-10-25-board-coremark-m1'
OFFICIAL = P / 'work/system/2026-10-23-coremark-correctness-m1/upstream-direct/files'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def file_sha(path):
    h = hashlib.sha256()
    with path.open('rb') as inp:
        for data in iter(lambda: inp.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest().upper()


def selftest():
    root = H / 'host-controls'
    root.mkdir(exist_ok=False)
    data = b'WB|2|1|00000001\r\nWB|2|1|00000001\r\nSTORE|3|10|10000|01|f\n'
    raw = root / 'original.log'
    raw.write_bytes(data)
    encode(raw, root / 'control', time.monotonic() + 10)
    index_sha = file_sha(root / 'control/index.json')
    assert b''.join(decode(root / 'control', index_sha)) == data
    assert b''.join(decode(root / 'control', index_sha)).count(b'WB|2|1|00000001') == 2
    rows = [dict(id='duplicate_records_and_CRLF_preserved', status='PASS')]
    meta = read(root / 'control/index.json')
    packed = (root / 'control/block-000000.gz').read_bytes()

    def reject(name, alter, blob=packed):
        d = root / name
        d.mkdir(exist_ok=False)
        m = copy.deepcopy(meta)
        alter(m)
        dump_new(d / 'index.json', m)
        (d / 'block-000000.gz').write_bytes(blob)
        try:
            list(decode(d))
        except (AssertionError, OSError, ValueError, zlib_error) as exc:
            rows.append(dict(id=name, status='EXPECTED_REJECT', error_type=type(exc).__name__))
        else:
            raise AssertionError('missed negative: ' + name)

    # Metadata invariants are tested WITHOUT the frozen-index SHA gate.
    import zlib
    zlib_error = zlib.error
    reject('missing_index_block', lambda m: m.update(chunks=[]))
    reject('duplicated_index_block', lambda m: m['chunks'].append(copy.deepcopy(m['chunks'][0])))
    reject('out_of_order_index', lambda m: m['chunks'][0].update(index=1))
    reject('wrong_line_start', lambda m: m['chunks'][0].update(first_line=2))
    reject('wrong_whole_SHA', lambda m: m.update(SHA256='0' * 64))
    reject('path_traversal', lambda m: m['chunks'][0].update(file='../outside.gz'))
    damaged = bytes([packed[0] ^ 1]) + packed[1:]
    reject('corrupted_compressed_bytes', lambda m: None, damaged)
    truncated = packed[:-4]
    reject('truncated_gzip_with_updated_envelope', lambda m: m['chunks'][0].update(
        packed_bytes=len(truncated), packed_SHA256=digest(truncated)), truncated)
    expanded = gzip.compress(b'x' * (BLOCK + 1), compresslevel=1, mtime=0)
    reject('decompression_cap', lambda m: m['chunks'][0].update(
        packed_bytes=len(expanded), packed_SHA256=digest(expanded)), expanded)
    try:
        list(decode(root / 'control', '0' * 64))
    except AssertionError:
        rows.append(dict(id='external_frozen_index_SHA', status='EXPECTED_REJECT'))
    else:
        raise AssertionError('index SHA unchecked')
    dump_new(H / 'CODEC_SELFTEST.json', dict(status='PASS', rows=rows, new_DUT=0))


def peak_bytes():
    class Counters(ctypes.Structure):
        _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong)] + [
            (name, ctypes.c_size_t) for name in ('PeakWorkingSetSize', 'WorkingSetSize',
            'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
            'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage')]
    c = Counters()
    c.cb = ctypes.sizeof(c)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    api = ctypes.WinDLL('psapi', use_last_error=True)
    api.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(Counters), ctypes.c_ulong]
    assert api.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return c.PeakWorkingSetSize


def run():
    started = time.monotonic()
    deadline = started + 120
    inputs = []
    def protect(path):
        path = Path(path)
        inputs.append(dict(path=str(path), SHA256=file_sha(path), bytes=path.stat().st_size))
        return path
    # Protect the complete candidate input group and authoritative results.
    for q in sorted((B / 'source').iterdir()):
        protect(q)
    for rel in ['port/core_portme.c', 'port/core_portme.h', 'firmware/start.S',
                'firmware/link.ld', 'firmware/timer.h', 'tests/tb_board_coremark.sv',
                'models/peripheral_checker.py', 'models/cpu_program_reference.py',
                'precompute.py', 'check_coremark.py', 'frozen_checks.py',
                'RESULTS.json', 'quality-compare.json', 'frozen-case-plan.json']:
        protect(B / rel)
    for name in ['README.md', 'barebones_porting.md']:
        protect(OFFICIAL / name)
    selftest()
    rows, forecasts = [], []
    for name in ['performance', 'validation']:
        run = B / 'runs' / (name + '-N234')
        result = read(protect(run / 'check-result.json'))
        process = read(protect(run / 'process.json'))
        old = read(protect(T / 'runs' / (name + '-N234') / 'check-result.json'))
        assert result['status'] == old['status'] == 'PASS' and process['returncode'] == 0
        for stream in ['trace.log', 'bus.log']:
            source = protect(run / stream)
            destination = H / (name + '-' + stream.removesuffix('.log'))
            start = time.monotonic()
            meta = encode(source, destination, deadline)
            encode_s = time.monotonic() - start
            index_sha = file_sha(destination / 'index.json')
            counts, records, prev, max_line = collections.Counter(), 0, 0, 0
            start = time.monotonic()
            with source.open('rb') as raw:
                for block in decode(destination, index_sha):
                    assert time.monotonic() <= deadline
                    assert raw.read(len(block)) == block, 'byte-for-byte mismatch'
                    for line in block.splitlines(keepends=True):
                        fields = line.split(b'|', 2)
                        assert len(fields) == 3
                        kind, cycle = fields[0].decode('ascii'), int(fields[1])
                        assert prev <= cycle <= result['metrics']['physical']
                        prev = cycle
                        counts[kind] += 1
                        records += 1
                        max_line = max(max_line, len(line))
                assert raw.read(1) == b''
            verify_s = time.monotonic() - start
            assert records == meta['lines']
            if stream == 'trace.log':
                assert dict(counts) == result['trace_counts']
            else:
                assert set(counts) == {'EDGE'}
            packed_bytes = sum(x['packed_bytes'] for x in meta['chunks'])
            rows.append(dict(seed=name, stream=stream, bytes=meta['bytes'],
                records=records, counts=dict(counts), max_line_bytes=max_line,
                blocks=len(meta['chunks']), packed_bytes=packed_bytes,
                index_bytes=(destination / 'index.json').stat().st_size,
                ratio=packed_bytes / meta['bytes'], encode_host_seconds=round(encode_s, 6),
                verify_host_seconds=round(verify_s, 6), byte_for_byte=True,
                input_SHA256=meta['SHA256'], index_SHA256=index_sha,
                not_DUT=True, raw_source_retained=True))
        c1, c2 = old['detail']['raw_ticks'], result['detail']['raw_ticks']
        increment = c2 - c1
        k_min_estimate = math.ceil((270000000 - c1) / increment) + 1
        physical160 = result['metrics']['physical'] + 158 * increment
        forecasts.append(dict(seed=name, C1=c1, C2=c2, second_increment=increment,
            two_point_min_iteration_estimate=k_min_estimate, candidate_iterations=160,
            conditional_compute160=c1 + 159 * increment,
            conditional_nominal_seconds160=(c1 + 159 * increment) / 27000000,
            conditional_physical160=physical160,
            conditional_DUT_host_hours160=physical160 / result['metrics']['physical'] * process['elapsed_seconds'] / 3600,
            actual_F151_reference_host_seconds=read(B / 'oracles' / name / 'expected.json')['host_seconds'],
            not_a_run_or_sufficiency_proof=True))
    for x in inputs:
        assert file_sha(Path(x['path'])) == x['SHA256'], x['path']
    code = (B / 'check_coremark.py').read_text(encoding='utf-8')
    pointer = struct.calcsize('P')
    anchors = [dict(line=i, text=l) for i, l in enumerate(code.splitlines(), 1)
               if any(s in l for s in ['samples=', 'samples.append', 'decode_frames(samples',
                   "self.f=(d/'trace.log')", "delta/27000000", 'formal_score_valid=False'])]
    summary = dict(date_beijing='2026-10-26', stage='A-COREMARK-LONGRUN-EVIDENCE-M0',
        status='HOST_ARCHIVE_PROTOTYPE_PASS_NO_NEW_DUT', measured_archives=rows,
        forecasts=forecasts, total_raw_bytes=sum(x['bytes'] for x in rows),
        total_packed_bytes=sum(x['packed_bytes'] for x in rows),
        actual_peak_working_set_bytes=peak_bytes(), host_seconds=round(time.monotonic()-started, 6),
        list_growth=dict(pointer_bytes=pointer, nominal_minimum_cycles=270000000,
            pointer_storage_floor_bytes=pointer*270000001+sys.getsizeof([]),
            includes_neither_capacity_overallocation_nor_other_state=True),
        current_checker_anchors=anchors, original_inputs=len(inputs),
        current_DUT_collector='UNCHANGED_NOT_ROTATING',
        current_functional_checker='UNCHANGED_NOT_BLOCK_STREAM_ADAPTED',
        compiler_DUT_ISA_replay_PDS_runs=0, hardware='STOPPED', formal_score=False,
        B='v02 accepted limited; no new task or presumed reply delivery',
        limitations=['Archive ratio measured on four already accepted short-run logs only',
            'Compression does not speed up the FPGA or prove an optimization',
            'No live spool deletion/rotation or long-DUT readiness was exercised',
            'No checkpoint-resume of the CPU or hidden-state injection',
            '270M list memory is arithmetic lower bound, not allocated or run'])
    dump_new(H / 'INPUTS.json', dict(files=inputs))
    dump_new(H / 'SUMMARY.json', summary)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    run()
