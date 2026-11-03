#!/usr/bin/env python3
"""Bounded process execution shared by the peripheral runners.

Key properties:
  * child stdout/stderr go to files, not pipes, so a descendant that inherits
    a handle cannot make the parent wait forever on a pipe;
  * every process has a wall-clock timeout;
  * on timeout the process tree is terminated with a bounded taskkill/kill,
    followed by a bounded wait and a recorded cleanup result;
  * descendant processes are snapshotted with the Windows Toolhelp API and
    checked again after cleanup; a non-zero taskkill or a surviving descendant
    is recorded as FAILED, never as success;
  * output reads are truly bounded (read at most limit+1 bytes) and truncation
    is explicit; truncated logs are never treated as a clean PASS;
  * native return code, timeout, cleanup status and log completeness are
    recorded separately from the functional checker result.

The module uses only the Python standard library and explicit tool paths.
"""
from __future__ import annotations

import ctypes
import json
import os
import signal
import subprocess
import time
from ctypes import wintypes
from pathlib import Path
from typing import Optional

TREE_KILL_TIMEOUT_S = 3
TREE_WAIT_TIMEOUT_S = 3
TREE_FALLBACK_WAIT_S = 1
MAX_LOG_BYTES = 4_000_000
TH32CS_SNAPPROCESS = 0x00000002
ERROR_NO_MORE_FILES = 18


def _enumeration_error(stage, err):
    """Only Windows ERROR_NO_MORE_FILES=18 is a normal enumeration end."""
    if err == ERROR_NO_MORE_FILES:
        return None
    return "%s failed err=%s (only ERROR_NO_MORE_FILES=18 is normal)" % (stage, err)
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

_kernel32 = None


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.c_void_p),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", wintypes.WCHAR * 260),
    ]


def _get_kernel32():
    global _kernel32
    if os.name != "nt":
        return None
    if _kernel32 is None:
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        k.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        k.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        k.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
        k.Process32FirstW.restype = wintypes.BOOL
        k.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
        k.Process32NextW.restype = wintypes.BOOL
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        k.CloseHandle.restype = wintypes.BOOL
        _kernel32 = k
    return _kernel32


def _snapshot_process_table():
    """Return (parent_to_children, all_pids, error) using Toolhelp32."""
    k = _get_kernel32()
    if k is None:
        return None, None, "process-tree snapshot unsupported on this platform"
    snap = k.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap in (None, 0, -1, INVALID_HANDLE_VALUE):
        return None, None, "CreateToolhelp32Snapshot failed"
    entry = PROCESSENTRY32W()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
    parent_to_children = {}
    all_pids = set()
    try:
        ok = k.Process32FirstW(snap, ctypes.byref(entry))
        if not ok:
            err = ctypes.get_last_error()
            enum_error = _enumeration_error("Process32FirstW", err)
            if enum_error:
                return None, None, enum_error
            return parent_to_children, all_pids, None
        while True:
            pid = int(entry.th32ProcessID)
            ppid = int(entry.th32ParentProcessID)
            all_pids.add(pid)
            parent_to_children.setdefault(ppid, []).append(pid)
            ok = k.Process32NextW(snap, ctypes.byref(entry))
            if not ok:
                err = ctypes.get_last_error()
                enum_error = _enumeration_error("Process32NextW", err)
                if enum_error:
                    return None, None, enum_error
                break
    finally:
        k.CloseHandle(snap)
    return parent_to_children, all_pids, None


def snapshot_descendants(pid: int):
    """Return (descendant_pids, error) for a live process."""
    parent_to_children, _all_pids, error = _snapshot_process_table()
    if error:
        return set(), error
    descendants = set()
    stack = [pid]
    while stack:
        parent = stack.pop()
        for child in parent_to_children.get(parent, []):
            if child not in descendants:
                descendants.add(child)
                stack.append(child)
    return descendants, None


def _alive_from_snapshot(pids):
    _parent_to_children, all_pids, error = _snapshot_process_table()
    if error:
        return None, error
    return {p for p in pids if p in all_pids}, None


def taskkill_tree(pid: int):
    """Best-effort bounded taskkill; returns (method, error, taskkill_rc)."""
    method = "none"
    error = None
    taskkill_rc = None
    if os.name == "nt":
        system_root = os.environ.get("SystemRoot", r"C:\Windows")
        taskkill = Path(system_root) / "System32" / "taskkill.exe"
        if taskkill.exists():
            try:
                r = subprocess.run(
                    [str(taskkill), "/PID", str(pid), "/T", "/F"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=TREE_KILL_TIMEOUT_S,
                    shell=False,
                )
                taskkill_rc = int(r.returncode)
                method = "taskkill_tree"
                if taskkill_rc != 0:
                    error = "taskkill returned non-zero rc=%d" % taskkill_rc
            except subprocess.TimeoutExpired:
                method = "taskkill_timeout"
                error = "taskkill exceeded %ss" % TREE_KILL_TIMEOUT_S
            except Exception as exc:
                method = "taskkill_exception"
                error = str(exc)
        else:
            method = "taskkill_missing"
            error = "taskkill.exe not found"
    else:
        try:
            os.killpg(os.getpgid(pid), signal.SIGKILL)
            taskkill_rc = 0
            method = "killpg_sigkill"
        except Exception as exc:
            method = "killpg_exception"
            error = str(exc)
    try:
        os.kill(pid, signal.SIGTERM)
        method += "+os_kill"
    except Exception:
        pass
    return method, error, taskkill_rc


def terminate_tree(pid: int) -> tuple[str, Optional[str]]:
    """Compatibility wrapper returning (method, error)."""
    method, error, _rc = taskkill_tree(pid)
    return method, error


def _read_bounded(path: Path, limit: int):
    """Read at most limit+1 bytes; return (text, truncated, bytes_read, file_size)."""
    try:
        size = path.stat().st_size
        with path.open("rb") as f:
            data = f.read(limit + 1)
    except OSError:
        return "", False, 0, 0
    truncated = len(data) > limit or size > limit
    if len(data) > limit:
        data = data[:limit]
    text = data.decode("utf-8", "replace")
    if truncated:
        text += "\n[TRUNCATED read_limit=%d file_bytes=%d]\n" % (limit, size)
    return text, truncated, len(data), size


def _normalize_terminator_result(result):
    if isinstance(result, tuple) and len(result) >= 3:
        return result[0], result[1], result[2]
    if isinstance(result, tuple) and len(result) == 2:
        return result[0], result[1], None
    return "terminator_invalid_result", "terminator returned invalid result", None


def run_process(argv, cwd: Path, timeout_s: int, log_path: Path,
                terminator=taskkill_tree, max_log_bytes: int = MAX_LOG_BYTES):
    """Run argv with file-backed output and a bounded tree timeout."""
    argv = [str(x) for x in argv]
    started = time.monotonic()
    timed_out = False
    rc: Optional[int] = None
    start_error: Optional[str] = None
    cleanup_s = 0.0
    cleanup_method = "not_needed"
    cleanup_error: Optional[str] = None
    cleanup_status = "NOT_NEEDED"
    taskkill_rc = None
    descendants_before = set()
    descendants_alive = set()
    descendants_exited = set()
    descendant_check = "NOT_NEEDED"
    descendant_check_error = None
    p = None
    stdout_path = log_path.with_suffix(log_path.suffix + ".stdout.tmp")
    stderr_path = log_path.with_suffix(log_path.suffix + ".stderr.tmp")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    out_f = None
    err_f = None
    try:
        out_f = stdout_path.open("wb")
        err_f = stderr_path.open("wb")
        creationflags = 0
        if os.name == "nt":
            creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        p = subprocess.Popen(
            argv,
            cwd=str(cwd),
            stdin=subprocess.DEVNULL,
            stdout=out_f,
            stderr=err_f,
            shell=False,
            creationflags=creationflags,
        )
        try:
            p.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            timed_out = True
            cleanup_started = time.monotonic()
            descendants_before, snap_error = snapshot_descendants(p.pid)
            descendant_check = "TOOLHELP32" if snap_error is None else "FAILED"
            descendant_check_error = snap_error
            try:
                tr = terminator(p.pid)
                cleanup_method, cleanup_error, taskkill_rc = _normalize_terminator_result(tr)
            except Exception as exc:
                cleanup_method = "terminator_exception"
                cleanup_error = str(exc)
            try:
                p.wait(timeout=TREE_WAIT_TIMEOUT_S)
            except subprocess.TimeoutExpired:
                cleanup_error = (cleanup_error + "; " if cleanup_error else "") + \
                    "parent did not exit after tree kill"
                try:
                    p.kill()
                except Exception:
                    pass
                try:
                    p.wait(timeout=TREE_FALLBACK_WAIT_S)
                except Exception:
                    cleanup_error = (cleanup_error + "; " if cleanup_error else "") + \
                        "parent did not exit after fallback kill"
            parent_alive = p.poll() is None
            if descendant_check == "TOOLHELP32":
                alive, alive_error = _alive_from_snapshot(descendants_before)
                if alive_error:
                    descendant_check = "FAILED"
                    descendant_check_error = alive_error
                else:
                    descendants_alive = alive or set()
                    descendants_exited = descendants_before - descendants_alive
            else:
                alive = None
            if taskkill_rc is None:
                cleanup_status = "FAILED" if cleanup_error else "UNKNOWN"
            elif taskkill_rc != 0:
                cleanup_status = "FAILED"
            elif cleanup_error:
                cleanup_status = "FAILED"
            elif parent_alive:
                cleanup_status = "FAILED"
            elif descendants_alive:
                cleanup_status = "FAILED"
            elif descendant_check == "FAILED":
                cleanup_status = "UNKNOWN"
            else:
                cleanup_status = "SUCCESS"
            if cleanup_status == "FAILED":
                bits = []
                if taskkill_rc is not None and taskkill_rc != 0:
                    bits.append("taskkill rc=%d" % taskkill_rc)
                if parent_alive:
                    bits.append("parent alive")
                if descendants_alive:
                    bits.append("descendants alive=%s" % ",".join(str(x) for x in sorted(descendants_alive)))
                cleanup_error = (cleanup_error + "; " if cleanup_error else "") + "; ".join(bits)
            cleanup_s = round(time.monotonic() - cleanup_started, 6)
        rc = p.returncode if p is not None else None
    except OSError as exc:
        start_error = str(exc)
        rc = None
    finally:
        if p is not None and p.poll() is None:
            m, e, trc = _normalize_terminator_result(terminator(p.pid))
            cleanup_method = (cleanup_method + "+" if cleanup_method not in ("not_needed", "none") else "") + m
            if e:
                cleanup_error = (cleanup_error + "; " if cleanup_error else "") + e
            if trc is not None and trc != 0:
                cleanup_status = "FAILED"
            try:
                p.wait(timeout=TREE_WAIT_TIMEOUT_S)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
                try:
                    p.wait(timeout=TREE_FALLBACK_WAIT_S)
                except Exception:
                    pass
            if p.poll() is None:
                cleanup_status = "FAILED"
        if p is not None and rc is None:
            rc = p.returncode
        for f in (out_f, err_f):
            try:
                if f is not None:
                    f.flush()
                    f.close()
            except Exception:
                pass

    out, out_trunc, out_read, out_size = _read_bounded(stdout_path, max_log_bytes)
    err, err_trunc, err_read, err_size = _read_bounded(stderr_path, max_log_bytes)
    try:
        stdout_path.unlink()
    except OSError:
        pass
    try:
        stderr_path.unlink()
    except OSError:
        pass

    duration = round(time.monotonic() - started, 6)
    log_truncated = out_trunc or err_trunc
    combined = out + "\n" + err
    if log_truncated:
        combined += "\n[LOG_TRUNCATED]\n"
    log_text = (
        "COMMAND=" + json.dumps(argv, ensure_ascii=False) + "\n"
        + "CWD=" + str(cwd) + "\n"
        + "TIMEOUT_S=" + str(timeout_s) + "\n"
        + "RC=" + str(rc) + "\n"
        + "TIMED_OUT=" + str(timed_out) + "\n"
        + "CLEANUP_S=" + str(cleanup_s) + "\n"
        + "CLEANUP_METHOD=" + cleanup_method + "\n"
        + "CLEANUP_STATUS=" + cleanup_status + "\n"
        + "TASKKILL_RC=" + str(taskkill_rc) + "\n"
        + "CLEANUP_ERROR=" + (cleanup_error or "") + "\n"
        + "DESCENDANT_CHECK=" + descendant_check + "\n"
        + "DESCENDANTS_BEFORE=" + ",".join(str(x) for x in sorted(descendants_before)) + "\n"
        + "DESCENDANTS_ALIVE=" + ",".join(str(x) for x in sorted(descendants_alive)) + "\n"
        + "DESCENDANTS_EXITED=" + ",".join(str(x) for x in sorted(descendants_exited)) + "\n"
        + "DESCENDANT_CHECK_ERROR=" + (descendant_check_error or "") + "\n"
        + "START_ERROR=" + (start_error or "") + "\n"
        + "DURATION_S=" + str(duration) + "\n"
        + "LOG_LIMIT_BYTES=" + str(max_log_bytes) + "\n"
        + "LOG_TRUNCATED=" + str(log_truncated) + "\n"
        + "STDOUT_BYTES=" + str(out_size) + "\n"
        + "STDOUT_READ_BYTES=" + str(out_read) + "\n"
        + "STDOUT_TRUNCATED=" + str(out_trunc) + "\n"
        + "STDERR_BYTES=" + str(err_size) + "\n"
        + "STDERR_READ_BYTES=" + str(err_read) + "\n"
        + "STDERR_TRUNCATED=" + str(err_trunc) + "\n"
        + "--- STDOUT ---\n" + out
        + "\n--- STDERR ---\n" + err + "\n"
    )
    log_path.write_text(log_text, encoding="utf-8", newline="\n")
    return {
        "argv": argv,
        "cwd": str(cwd),
        "timeout_s": timeout_s,
        "returncode": rc,
        "timed_out": timed_out,
        "cleanup_s": cleanup_s,
        "cleanup_method": cleanup_method,
        "cleanup_status": cleanup_status,
        "taskkill_rc": taskkill_rc,
        "cleanup_error": cleanup_error,
        "descendants_before": sorted(descendants_before),
        "descendants_alive": sorted(descendants_alive),
        "descendants_exited": sorted(descendants_exited),
        "descendant_check": descendant_check,
        "descendant_check_error": descendant_check_error,
        "start_error": start_error,
        "duration_s": duration,
        "log_limit_bytes": max_log_bytes,
        "log_truncated": log_truncated,
        "stdout_truncated": out_trunc,
        "stderr_truncated": err_trunc,
        "stdout_bytes": out_size,
        "stderr_bytes": err_size,
        "stdout_read_bytes": out_read,
        "stderr_read_bytes": err_read,
        "stdout": out,
        "stderr": err,
        "combined": combined,
        "log_path": log_path,
        "ok": (rc == 0) and not timed_out and start_error is None and not log_truncated,
    }
