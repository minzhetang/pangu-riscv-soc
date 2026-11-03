"""B-owned support helpers for the offline M0 CLI (ABI 1.0.0).

Only Python standard library.  Frozen comparisons remain in frozen/offline_api.py;
this module never supplies record expectations or a semantic CPU oracle.
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import sys
import time
from pathlib import Path

ABI = "B-VERIFY-OFFLINE-ABI/1.0.0"
MAX_INPUT_BYTES = 512 * 1024 * 1024
MAX_RECORDS = 6_000_000
MAX_LINE_BYTES = 512
MAX_DIFFERENCES = 16
MAX_NEIGHBORS = 2
MAX_RESULT_BYTES = 1024 * 1024
MAX_LOG_BYTES = 4 * 1024 * 1024
MAX_WORKER_WS = 256 * 1024 * 1024
CASE_MAX_BYTES = 1024 * 1024
MIN_WORKER_OVERHEAD_BYTES = 8 * 1024 * 1024
DEFAULT_CASE_SECONDS = 180.0
DEFAULT_CLEANUP_SECONDS = 8.0
MAX_TOTAL_CASE_SECONDS = 188.0
MAX_SUITE_SECONDS = 1800.0

STATUS_RC = {
    "MATCH": 0,
    "MISMATCH": 2,
    "INVALID_INPUT": 3,
    "INCOMPLETE": 4,
    "LIMIT": 5,
    "TIMEOUT": 6,
    "TOOL_ERROR": 7,
}

LIMIT_DEFAULTS = {
    "max_input_bytes_each": MAX_INPUT_BYTES,
    "max_records_each": MAX_RECORDS,
    "max_differences": MAX_DIFFERENCES,
    "max_diagnostic_neighbors_each_side": MAX_NEIGHBORS,
    "max_result_bytes": MAX_RESULT_BYTES,
    "max_log_bytes_each": MAX_LOG_BYTES,
    "worker_peak_working_set_bytes": MAX_WORKER_WS,
    "case_timeout_seconds": DEFAULT_CASE_SECONDS,
    "cleanup_seconds": DEFAULT_CLEANUP_SECONDS,
}


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as inp:
        for block in iter(lambda: inp.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest().upper()


def _is_reparse(path):
    return bool(getattr(path.lstat(), "st_file_attributes", 0) & 0x400) or path.is_symlink()


def load_json(path, max_bytes=MAX_RESULT_BYTES):
    p = Path(path)
    if not p.is_file() or p.is_symlink() or _is_reparse(p) or p.stat().st_size > max_bytes:
        raise ValueError("JSON file missing, linked, or too large")
    return json.loads(p.read_text(encoding="utf-8-sig"))


def load_case(path):
    """CASE metadata is bounded before parsing; reject links/reparse and oversize."""
    p = Path(path)
    if not p.is_file() or p.is_symlink() or _is_reparse(p):
        raise ValueError("CASE is not a regular file")
    if p.stat().st_size > CASE_MAX_BYTES:
        raise ValueError("CASE exceeds 1MiB metadata limit")
    return json.loads(p.read_text(encoding="utf-8-sig"))


def dump_json(path, value, max_bytes=MAX_RESULT_BYTES):
    """Atomically publish bounded JSON; return None rather than write oversize."""
    p = Path(path)
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if len(data) > max_bytes:
        return None
    tmp = p.with_name(p.name + ".tmp-" + str(os.getpid()))
    try:
        with tmp.open("xb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        if tmp.stat().st_size > max_bytes:
            tmp.unlink()
            return None
        os.replace(tmp, p)
        return len(data)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def normalize_limits(raw):
    """Lower-only case limits, with the hard ABI maxima as defaults."""
    raw = {} if raw is None else raw
    if not isinstance(raw, dict):
        raise ValueError("limits must be an object")
    unknown = sorted(set(raw) - set(LIMIT_DEFAULTS))
    if unknown:
        raise ValueError("unknown limits: " + ",".join(unknown))
    out = dict(LIMIT_DEFAULTS)
    for key, value in raw.items():
        if key == "case_timeout_seconds":
            number = float(value)
            if not (0.001 <= number <= DEFAULT_CASE_SECONDS):
                raise ValueError("case_timeout_seconds out of range")
            out[key] = number
        elif key == "cleanup_seconds":
            number = float(value)
            if not (0.1 <= number <= DEFAULT_CLEANUP_SECONDS):
                raise ValueError("cleanup_seconds out of range")
            out[key] = number
        else:
            number = int(value)
            if key in ("max_input_bytes_each", "max_records_each", "max_result_bytes",
                       "max_log_bytes_each", "worker_peak_working_set_bytes"):
                if number < 1 or number > LIMIT_DEFAULTS[key]:
                    raise ValueError(key + " out of range")
            elif key == "max_differences":
                if not (1 <= number <= MAX_DIFFERENCES):
                    raise ValueError("max_differences out of range")
            elif key == "max_diagnostic_neighbors_each_side":
                if not (0 <= number <= MAX_NEIGHBORS):
                    raise ValueError("neighbor limit out of range")
            out[key] = number
    if out["case_timeout_seconds"] + out["cleanup_seconds"] > MAX_TOTAL_CASE_SECONDS:
        raise ValueError("case timeout + cleanup exceeds total case limit")
    return out


def validate_case_shape(case):
    if not isinstance(case, dict):
        raise ValueError("case must be an object")
    allowed = {"id", "expected", "actual", "allow_empty", "limits"}
    extra = sorted(set(case) - allowed)
    if extra:
        raise ValueError("unexpected case fields: " + ",".join(extra))
    if not isinstance(case.get("id"), str) or not case["id"]:
        raise ValueError("case id required")
    for key in ("expected", "actual"):
        spec = case.get(key)
        if not isinstance(spec, dict):
            raise ValueError(key + " spec required")
        if spec.get("storage") not in ("raw", "archive"):
            raise ValueError(key + " storage")
        if spec.get("stream") not in ("trace", "bus"):
            raise ValueError(key + " stream")
        if not isinstance(spec.get("path"), str) or not spec["path"]:
            raise ValueError(key + " path")
        if spec.get("complete") is not True:
            # allowed here; frozen records returns INCOMPLETE so tests can observe it
            pass
        if spec["storage"] == "archive":
            if not isinstance(spec.get("index_SHA256"), str):
                raise ValueError(key + " archive index_SHA256")
    if "allow_empty" in case and not isinstance(case["allow_empty"], bool):
        raise ValueError("allow_empty must be boolean")
    normalize_limits(case.get("limits"))


def validate_worker_result(result, worker_rc=None):
    """Guard against PASS text, nonzero worker rc, or incomplete evidence."""
    errors = []
    if not isinstance(result, dict):
        return ["worker result is not an object"]
    status = result.get("status")
    if status not in STATUS_RC:
        errors.append("unknown status")
        return errors
    expected_rc = STATUS_RC[status]
    if result.get("native_rc") != expected_rc:
        errors.append("result native_rc does not match status")
    if worker_rc is not None and worker_rc != expected_rc:
        errors.append("worker process rc does not match result status")
    if result.get("ABI") != ABI:
        errors.append("wrong ABI")
    if result.get("CPU_function_proven") is not False:
        errors.append("CPU_function_proven must be false")
    if result.get("fully_consumed") is not True and status in ("MATCH", "MISMATCH"):
        errors.append("success/mismatch result not fully consumed")
    for key in ("checked", "expected_records", "actual_records", "mismatch_count"):
        value = result.get(key)
        if not isinstance(value, int) or value < 0:
            errors.append("missing/invalid " + key)
    differences = result.get("differences")
    if not isinstance(differences, list):
        errors.append("differences must be a list")
        differences = []
    if status == "MATCH":
        if result.get("fully_consumed") is not True:
            errors.append("MATCH not fully consumed")
        if result.get("mismatch_count") != 0 or differences:
            errors.append("MATCH carries differences")
        if result.get("checked") != result.get("expected_records") or result.get("checked") != result.get("actual_records"):
            errors.append("MATCH record counts disagree")
    elif status == "MISMATCH":
        if result.get("fully_consumed") is not True:
            errors.append("MISMATCH not fully consumed")
        if not result.get("mismatch_count") or not differences:
            errors.append("MISMATCH lacks differences")
    else:
        if result.get("fully_consumed") is not False:
            errors.append("failed status must report fully_consumed=false")
    return errors


# ---- Windows peak working set; returns None on non-Windows/unavailable ----
if os.name == "nt":
    from ctypes import wintypes

    class _PROCESS_MEMORY_COUNTERS_EX(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("PageFaultCount", wintypes.DWORD),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
            ("PrivateUsage", ctypes.c_size_t),
        ]

    _k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _psapi = ctypes.WinDLL("psapi", use_last_error=True)
    _k32.GetCurrentProcess.restype = wintypes.HANDLE
    _k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _k32.OpenProcess.restype = wintypes.HANDLE
    _k32.CloseHandle.argtypes = [wintypes.HANDLE]
    _psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE,
                                            ctypes.POINTER(_PROCESS_MEMORY_COUNTERS_EX),
                                            wintypes.DWORD]
    _psapi.GetProcessMemoryInfo.restype = wintypes.BOOL


def peak_working_set(pid=None):
    if os.name != "nt":
        return None
    try:
        if pid is None:
            handle = _k32.GetCurrentProcess()
            close = False
        else:
            handle = _k32.OpenProcess(0x1000 | 0x0010, False, int(pid))
            close = True
        if not handle:
            return None
        counters = _PROCESS_MEMORY_COUNTERS_EX()
        counters.cb = ctypes.sizeof(counters)
        ok = _psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb)
        if close:
            _k32.CloseHandle(handle)
        return int(counters.PeakWorkingSetSize) if ok else None
    except Exception:
        return None


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")
