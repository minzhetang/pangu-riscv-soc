"""B-owned offline worker: typed pointwise comparison using frozen ABI 1.0.0.

No CPU/ISA semantic model.  This worker consumes every typed record through the
frozen A-owned reader and compares every field without deduplication or hashes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from itertools import zip_longest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN_ROOT = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(RETURN_ROOT / "frozen"))
sys.path.insert(0, str(HERE))
import offline_api as api  # noqa: E402
import support  # noqa: E402

SENTINEL = object()
FIELDS = {
    "trace": {
        "EX": ["kind", "cycle", "pc"],
        "WB": ["kind", "cycle", "rd", "data"],
        "READ": ["kind", "cycle", "pc", "addr", "raw", "loaded"],
        "STORE": ["kind", "cycle", "pc", "addr", "data", "mask"],
    },
    "bus": {
        "EDGE": ["kind", "cycle", "gpio_async", "addr", "write", "data", "mask",
                 "read", "error", "pre_tx", "pre_gpio", "post_tx", "post_gpio",
                 "accept", "stop", "pre_ticks", "post_ticks"],
    },
}


class CountingIter:
    def __init__(self, iterator):
        self.iterator = iterator
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        value = next(self.iterator)
        self.count += 1
        return value


def _deadline_check(deadline):
    if deadline is not None and time.monotonic() > deadline:
        raise api.InputError("TIMEOUT", "deadline during identity pre-read")


def identity(root, spec, deadline, max_bytes):
    """Bounded identity pre-read; it shares the case deadline."""
    path = api.child(root, spec["path"])
    if spec["storage"] == "raw":
        size = path.stat().st_size
        if size > max_bytes:
            raise api.InputError("LIMIT", "raw input exceeds case byte budget before identity")
        h = hashlib.sha256()
        read = 0
        with path.open("rb") as inp:
            while True:
                _deadline_check(deadline)
                block = inp.read(1024 * 1024)
                if not block:
                    break
                read += len(block)
                if read > max_bytes:
                    raise api.InputError("LIMIT", "raw input exceeds case byte budget during identity")
                h.update(block)
        return {"storage": "raw", "path": spec["path"], "bytes": size,
                "sha256": h.hexdigest().upper()}
    index = path / "index.json"
    if not index.is_file() or index.is_symlink() or support._is_reparse(index):
        raise api.InputError("INVALID_INPUT", "archive index is not a regular file")
    if index.stat().st_size > 2 * 1024 * 1024:
        raise api.InputError("INVALID_INPUT", "archive index exceeds 2MiB limit")
    _deadline_check(deadline)
    meta = json.loads(index.read_text(encoding="utf-8-sig"))
    _deadline_check(deadline)
    return {"storage": "archive", "path": spec["path"],
            "bytes": int(meta["bytes"]), "lines": int(meta["lines"]),
            "index_SHA256": support.sha256_file(index)}


def field_diff(stream, expected, actual):
    names = FIELDS[stream].get(expected[0] if expected is not SENTINEL and expected else
                               actual[0] if actual is not SENTINEL and actual else None, [])
    if expected is SENTINEL or actual is SENTINEL:
        return None, None, None
    for index, (left, right) in enumerate(zip(expected, actual)):
        if left != right:
            return names[index] if index < len(names) else "field%d" % index, left, right
    return None, expected, actual


def collect_neighbors(root, expected_spec, actual_spec, first, stream, limits, deadline):
    """Bounded diagnostic re-read; it never gets a fresh budget."""
    if not isinstance(first, int) or first < 1:
        return [], None
    try:
        _deadline_check(deadline)
        left = api.records(root, expected_spec,
                           max_records=limits["max_records_each"],
                           max_bytes=limits["max_input_bytes_each"], deadline=deadline)
        right = api.records(root, actual_spec,
                            max_records=limits["max_records_each"],
                            max_bytes=limits["max_input_bytes_each"], deadline=deadline)
        lo = max(1, first - limits["max_diagnostic_neighbors_each_side"])
        hi = first + limits["max_diagnostic_neighbors_each_side"]
        neighbors = []
        for ordinal, (exp, act) in enumerate(zip_longest(left, right, fillvalue=SENTINEL), 1):
            if ordinal < lo:
                continue
            if ordinal > hi:
                break
            neighbors.append({
                "ordinal": ordinal,
                "expected": None if exp is SENTINEL else list(exp),
                "actual": None if act is SENTINEL else list(act),
                "relation": "EQUAL" if exp == act else
                            "MISSING_ACTUAL" if act is SENTINEL else
                            "EXTRA_ACTUAL" if exp is SENTINEL else "DIFFER",
            })
        return neighbors, None
    except api.InputError as exc:
        return [], "%s: %s" % (exc.status, exc)
    except Exception as exc:
        return [], "%s: %s" % (type(exc).__name__, exc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-file", required=True)
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--deadline-seconds", type=float, default=None)
    args = parser.parse_args()
    out = Path(args.out)
    started = time.monotonic()
    case = support.load_case(args.case_file)
    support.validate_case_shape(case)
    limits = support.normalize_limits(case.get("limits"))
    remaining = args.deadline_seconds
    deadline = started + (float(remaining) if remaining is not None
                          else limits["case_timeout_seconds"])
    input_root = Path(args.input_root)
    result = {
        "kind": "B_VERIFY_OFFLINE_WORKER",
        "case_id": case["id"],
        "ABI": support.ABI,
        "CPU_function_proven": False,
        "new_DUT": 0,
        "limits": limits,
        "expected_input": None,
        "actual_input": None,
        "status": "TOOL_ERROR",
        "native_rc": 7,
        "fully_consumed": False,
        "checked": 0,
        "expected_records": 0,
        "actual_records": 0,
        "mismatch_count": 0,
        "differences": [],
        "neighbors": [],
        "first_difference": None,
        "termination": "error",
        "diagnostic_error": None,
    }
    exp_iter = act_iter = None
    try:
        api.runtime_guard()
        result["expected_input"] = identity(input_root, case["expected"],
                                            deadline, limits["max_input_bytes_each"])
        result["actual_input"] = identity(input_root, case["actual"],
                                          deadline, limits["max_input_bytes_each"])
        stream = case["expected"]["stream"]
        exp_iter = CountingIter(api.records(
            input_root, case["expected"], max_records=limits["max_records_each"],
            max_bytes=limits["max_input_bytes_each"], deadline=deadline))
        act_iter = CountingIter(api.records(
            input_root, case["actual"], max_records=limits["max_records_each"],
            max_bytes=limits["max_input_bytes_each"], deadline=deadline))
        got = api.compare(exp_iter, act_iter, allow_empty=bool(case.get("allow_empty", False)),
                          max_records=limits["max_records_each"],
                          max_differences=limits["max_differences"], deadline=deadline)
        result.update({
            "status": got["status"],
            "native_rc": support.STATUS_RC[got["status"]],
            "fully_consumed": bool(got["fully_consumed"]),
            "checked": got["checked"],
            "expected_records": got["expected_records"],
            "actual_records": got["actual_records"],
            "mismatch_count": got["mismatch_count"],
            "differences": got["differences"],
            "termination": "normal",
        })
        if got["status"] == "MISMATCH":
            first = got["differences"][0]
            field, field_expected, field_actual = field_diff(
                stream, first["expected"] if first["expected"] is not None else SENTINEL,
                first["actual"] if first["actual"] is not None else SENTINEL)
            result["first_difference"] = {
                "ordinal": first["ordinal"], "kind": first["kind"], "field": field,
                "expected": first["expected"], "actual": first["actual"],
                "field_expected": field_expected, "field_actual": field_actual,
            }
            result["neighbors"], result["diagnostic_error"] = collect_neighbors(
                input_root, case["expected"], case["actual"], first["ordinal"], stream,
                limits, deadline)
    except api.InputError as exc:
        result.update({
            "status": exc.status,
            "native_rc": support.STATUS_RC.get(exc.status, 7),
            "fully_consumed": False,
            "error": str(exc),
            "termination": "early_error",
            "checked": exp_iter.count if exp_iter else 0,
            "expected_records": exp_iter.count if exp_iter else 0,
            "actual_records": act_iter.count if act_iter else 0,
        })
    except MemoryError:
        result.update({"status": "TOOL_ERROR", "native_rc": 7, "error": "MemoryError",
                       "termination": "resource_error"})
    except Exception as exc:
        result.update({"status": "TOOL_ERROR", "native_rc": 7,
                       "error": "%s: %s" % (type(exc).__name__, exc),
                       "termination": "tool_error"})
    result["elapsed_s"] = round(time.monotonic() - started, 6)
    result["worker_reported_peak_bytes"] = support.peak_working_set()
    result["measurement_method"] = "Windows GetProcessMemoryInfo PeakWorkingSetSize (worker self-report); parent also measures child"
    published = support.dump_json(out / "worker-result.json", result,
                                  max_bytes=limits["max_result_bytes"])
    if published is None:
        # No over-limit worker result may be published.  The CLI still has a
        # bounded status line with the real rejection code.
        print(json.dumps({"status": "LIMIT", "native_rc": 5, "case": result["case_id"],
                          "reason": "worker-result exceeds max_result_bytes; no file published"},
                         ensure_ascii=False))
        return 5
    print(json.dumps({"status": result["status"], "native_rc": result["native_rc"],
                      "case": result["case_id"]}, ensure_ascii=False))
    return result["native_rc"]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
