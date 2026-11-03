"""Deterministic, independent fault/stress generator (does not use RUN/compare)."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

EDGE_TEMPLATE = "EDGE|{cycle}|00|00000000|0|00000000|0|00000000|0|1|00|1|00|0|0|0000000000000000|0000000000000001\n"


def read_lines(path):
    return path.read_bytes().splitlines(keepends=True)


def write_bytes(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def gen_faults(input_root, out):
    seed = input_root / "inputs/seeds/S00-duplicates-kept"
    expected = read_lines(seed / "expected.log")
    actual = read_lines(seed / "actual.log")
    d = out / "generated/faults"
    d.mkdir(parents=True, exist_ok=True)
    write_bytes(d / "s00_expected.log", b"".join(expected))
    write_bytes(d / "f01_remove.log", b"".join(expected[:3] + expected[4:]))
    write_bytes(d / "f02_add.log", b"".join(expected[:3] + [b"EX|6|00000004\n"] + expected[3:]))
    write_bytes(d / "f03_duplicate.log", b"".join(expected[:4] + [expected[3]] + expected[4:]))
    write_bytes(d / "f05_swap.log", b"".join(expected[:3] + [expected[4], expected[3]] + expected[5:]))
    mutated = list(expected)
    if not mutated[4].startswith(b"WB|6|1|"):
        raise SystemExit("unexpected S00 line 5")
    mutated[4] = b"WB|6|1|00000002\n"
    write_bytes(d / "f06_mutate.log", b"".join(mutated))
    bad = list(expected)
    bad[1] = b"WB|4|1|0000000x\n"
    write_bytes(d / "f07_invalid.log", b"".join(bad))
    write_bytes(d / "f08_partial.log", b"".join(actual).rstrip(b"\r\n"))
    write_bytes(d / "f13_overlong.log", b"EX|2|" + b"0" * 600 + b"\n")
    # S02: legal decimal cycles beyond 32 bits, still trace/bus field widths.
    large = (b"EX|2147483650|00000000\n"
             b"WB|4294967301|1|00000001\n"
             b"EX|4294967302|00000004\n")
    write_bytes(d / "s02_large_cycles_expected.log", large)
    write_bytes(d / "s02_large_cycles_actual.log", large)
    print(json.dumps({"faults": str(d), "status": "GENERATED"}, ensure_ascii=False))


def gen_stress(out, sizes):
    d = out / "generated/stress"
    d.mkdir(parents=True, exist_ok=True)
    rows = []
    for size in sizes:
        target = int(size) * 1024 * 1024
        for name in ("expected.log", "actual.log"):
            path = d / ("%dMiB-%s" % (size, name))
            with path.open("wb") as f:
                total = 0
                cycle = 1
                while total < target:
                    line = EDGE_TEMPLATE.format(cycle=cycle).encode("ascii")
                    f.write(line)
                    total += len(line)
                    cycle += 1
            rows.append({"size_mib": size, "name": name, "path": str(path), "bytes": path.stat().st_size,
                         "records": cycle - 1})
    print(json.dumps({"stress": str(d), "rows": rows, "status": "GENERATED"}, ensure_ascii=False))


def gen_block_boundary(out):
    """Create two valid archives with one real field difference at >4MiB."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "frozen"))
    import block_codec
    d = out / "generated/block-boundary"
    d.mkdir(parents=True, exist_ok=True)
    raw_expected = d / "expected.log"
    raw_actual = d / "actual.log"
    lines = []
    cycle = 1
    # Use a valid EDGE stream; select the first line whose start is beyond
    # the 4MiB block boundary for the fault.
    while sum(len(x) for x in lines) < 4 * 1024 * 1024 + 4096:
        lines.append(EDGE_TEMPLATE.format(cycle=cycle).encode("ascii"))
        cycle += 1
    boundary_index = next(i for i, _ in enumerate(lines)
                          if sum(len(x) for x in lines[:i]) >= 4 * 1024 * 1024)
    mutated = list(lines)
    parts = mutated[boundary_index].decode("ascii").rstrip("\n").split("|")
    parts[5] = "00000001"
    mutated[boundary_index] = ("|".join(parts) + "\n").encode("ascii")
    raw_expected.write_bytes(b"".join(lines))
    raw_actual.write_bytes(b"".join(mutated))
    for name, source in (("expected", raw_expected), ("actual", raw_actual)):
        archive = d / (name + "_archive")
        if archive.exists():
            shutil.rmtree(archive)
        block_codec.encode(source, archive, __import__("time").monotonic() + 30)
    manifest = {
        "expected": {"path": "generated/block-boundary/expected_archive",
                     "index_SHA256": __import__("hashlib").sha256(
                         (d / "expected_archive/index.json").read_bytes()).hexdigest().upper()},
        "actual": {"path": "generated/block-boundary/actual_archive",
                   "index_SHA256": __import__("hashlib").sha256(
                       (d / "actual_archive/index.json").read_bytes()).hexdigest().upper()},
        "boundary_index_zero_based": boundary_index,
        "raw_bytes": raw_expected.stat().st_size,
    }
    (d / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8", newline="\n")
    print(json.dumps({"block_boundary": str(d), "manifest": manifest, "status": "GENERATED"},
                     ensure_ascii=False))


def gen_corrupt_archives(input_root, out):
    src = input_root / "inputs/archives/performance-trace"
    d = out / "generated/archives"
    d.mkdir(parents=True, exist_ok=True)
    f10 = d / "f10-corrupt"
    if f10.exists():
        shutil.rmtree(f10)
    shutil.copytree(src, f10)
    block = f10 / "block-000000.gz"
    data = bytearray(block.read_bytes())
    if len(data) < 20:
        raise SystemExit("archive block too small")
    data[20] ^= 0x01
    block.write_bytes(data)
    f11 = d / "f11-index"
    if f11.exists():
        shutil.rmtree(f11)
    shutil.copytree(src, f11)
    index = json.loads((f11 / "index.json").read_text(encoding="utf-8-sig"))
    index["chunks"][0]["index"] = 99
    (f11 / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8", newline="\n")
    print(json.dumps({"archives": str(d), "status": "GENERATED"}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--mode", choices=("faults", "stress", "archives", "all"), default="all")
    parser.add_argument("--sizes", default="1,16,128")
    args = parser.parse_args()
    root = Path(args.input_root)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if args.mode in ("faults", "all"):
        gen_faults(root, out)
    if args.mode in ("stress", "all"):
        gen_stress(out, [int(x) for x in args.sizes.split(",") if x])
    if args.mode in ("archives", "all"):
        gen_corrupt_archives(root, out)
        gen_block_boundary(out)


if __name__ == "__main__":
    main()
