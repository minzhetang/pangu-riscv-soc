#!/usr/bin/env python3
"""B-owned offline M0-R1 CLI (ABI 1.0.0, package 1.0.1).

Only bounded resource/error guards and an internal fixed-fixture test hook are
new.  Frozen comparison semantics and the original 1.0.0 ABI are unchanged.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN_ROOT = HERE
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE / "src"))
import support  # noqa: E402

WORKER = HERE / "src" / "worker.py"
STATUS_RC = support.STATUS_RC


def emit(status, case_id=None, out=None, extra=None):
    payload = {"status": status, "native_rc": STATUS_RC.get(status, 7),
               "case": case_id, "out": str(out) if out is not None else None,
               "error": None}
    if extra:
        payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False))
    return STATUS_RC.get(status, 7)


def base_result(case_id, limits, status="TOOL_ERROR", reason=None):
    return {
        "kind": "B_VERIFY_OFFLINE_RESULT",
        "case_id": case_id,
        "ABI": support.ABI,
        "CPU_function_proven": False,
        "new_DUT": 0,
        "limits": limits,
        "status": status,
        "native_rc": STATUS_RC[status],
        "fully_consumed": False,
        "checked": 0,
        "expected_records": 0,
        "actual_records": 0,
        "mismatch_count": 0,
        "differences": [],
        "neighbors": [],
        "first_difference": None,
        "termination": "error",
        "worker_started": False,
        "worker_exited": False,
        "worker_peak_bytes": None,
        "worker_self_peak_bytes": None,
        "memory_threshold_bytes": limits.get("worker_peak_working_set_bytes"),
        "memory_observed_bytes": None,
        "trigger": reason,
        "parent_peak_bytes": support.peak_working_set(),
        "measurement_method": "Windows GetProcessMemoryInfo PeakWorkingSetSize",
        "log_truncated": False,
        "stdout_bytes": 0,
        "stderr_bytes": 0,
        "worker_stdout": None,
        "worker_stderr": None,
        "command": None,
        "elapsed_s": 0.0,
        "case_sha256": None,
        "run_py_sha256": support.sha256_file(Path(__file__)),
        "worker_sha256": None,
        "error": reason,
    }


def truncate_file(path, limit):
    try:
        if path.exists() and path.stat().st_size > limit:
            with path.open("r+b") as fh:
                fh.truncate(limit)
    except OSError:
        pass


def publish(out, result, max_bytes):
    """Publish only within this case's result budget; no over-limit fallback."""
    written = support.dump_json(Path(out) / "result.json", result, max_bytes=max_bytes)
    return written is not None


def execute_case(case, input_root, out, limits, started, worker_path=WORKER):
    """Single bounded parent path used by production and fixed test fixtures."""
    case_id = case["id"]
    out = Path(out)
    if not out.exists():
        out.mkdir(parents=True, exist_ok=False)
    result = base_result(case_id, limits, "TOOL_ERROR", None)
    result["worker_sha256"] = support.sha256_file(Path(worker_path))
    result["case_sha256"] = None
    # A threshold below minimal interpreter overhead is rejected before spawn.
    if limits["worker_peak_working_set_bytes"] < support.MIN_WORKER_OVERHEAD_BYTES:
        result.update({
            "status": "LIMIT", "native_rc": 5, "fully_consumed": False,
            "termination": "preflight_memory_limit",
            "trigger": "worker_peak_working_set_bytes below minimum runner overhead",
            "memory_threshold_bytes": limits["worker_peak_working_set_bytes"],
            "memory_observed_bytes": None, "worker_started": False,
            "worker_exited": False,
            "elapsed_s": round(time.monotonic() - started, 6),
        })
        publish(out, result, limits["max_result_bytes"])
        return result, 5, out
    deadline = started + limits["case_timeout_seconds"]
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        result.update({"status": "TIMEOUT", "native_rc": 6,
                       "termination": "deadline_before_worker",
                       "trigger": "case deadline exhausted before worker start"})
        publish(out, result, limits["max_result_bytes"])
        return result, 6, out
    command = {
        "argv": [sys.executable, "-B", str(worker_path), "--case-file", str(case.get("file")),
                 "--input-root", str(input_root), "--out", str(out),
                 "--deadline-seconds", "%.6f" % max(0.0, remaining)],
        "cwd": str(RETURN_ROOT),
        "python": sys.executable,
        "optimize": sys.flags.optimize,
        "case_id": case_id,
        "input_root": str(input_root),
        "out": str(out),
        "deadline_seconds": max(0.0, remaining),
    }
    (out / "command.json").write_text(json.dumps(command, ensure_ascii=False, indent=2) + "\n",
                                      encoding="utf-8", newline="\n")
    stdout_path = out / "worker.stdout.log"
    stderr_path = out / "worker.stderr.log"
    hard_deadline = started + limits["case_timeout_seconds"] + limits["cleanup_seconds"]
    log_limited = False
    timed_out = False
    worker_peak = None
    worker_rc = None
    with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
        proc = subprocess.Popen(command["argv"], cwd=str(RETURN_ROOT),
                                stdout=stdout, stderr=stderr, shell=False,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        result["worker_started"] = True
        while proc.poll() is None:
            now = time.monotonic()
            current = support.peak_working_set(proc.pid)
            if current is not None:
                worker_peak = current if worker_peak is None else max(worker_peak, current)
            if stdout_path.stat().st_size > limits["max_log_bytes_each"] or \
                    stderr_path.stat().st_size > limits["max_log_bytes_each"]:
                log_limited = True
                proc.kill()
                break
            if now > hard_deadline:
                timed_out = True
                proc.kill()
                break
            time.sleep(0.02)
        try:
            worker_rc = proc.wait(timeout=limits["cleanup_seconds"])
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.kill()
            worker_rc = proc.wait(timeout=limits["cleanup_seconds"])
    raw_stdout_size, raw_stderr_size = stdout_path.stat().st_size, stderr_path.stat().st_size
    if raw_stdout_size > limits["max_log_bytes_each"] or raw_stderr_size > limits["max_log_bytes_each"]:
        log_limited = True
    truncate_file(stdout_path, limits["max_log_bytes_each"])
    truncate_file(stderr_path, limits["max_log_bytes_each"])
    result.update({
        "command": command,
        "elapsed_s": round(time.monotonic() - started, 6),
        "worker_rc": worker_rc,
        "worker_exited": True,
        "worker_peak_bytes": worker_peak,
        "stdout_bytes": stdout_path.stat().st_size,
        "stderr_bytes": stderr_path.stat().st_size,
        "raw_stdout_bytes": raw_stdout_size,
        "raw_stderr_bytes": raw_stderr_size,
        "log_truncated": log_limited,
        "worker_stdout": "worker.stdout.log",
        "worker_stderr": "worker.stderr.log",
    })
    if timed_out:
        result.update({"status": "TIMEOUT", "native_rc": 6,
                       "termination": "parent_timeout",
                       "trigger": "case_timeout exceeded; worker killed and waited"})
        publish(out, result, limits["max_result_bytes"])
        return result, 6, out
    if log_limited:
        result.update({"status": "LIMIT", "native_rc": 5,
                       "termination": "log_limit",
                       "trigger": "stdout/stderr reached max_log_bytes_each"})
        publish(out, result, limits["max_result_bytes"])
        return result, 5, out
    worker_result = None
    try:
        worker_result = support.load_json(out / "worker-result.json",
                                          max_bytes=limits["max_result_bytes"])
    except Exception as exc:
        worker_result = None
        result["error"] = "%s: %s" % (type(exc).__name__, exc)
    if worker_result is None:
        if worker_rc == 5:
            result.update({"status": "LIMIT", "native_rc": 5,
                           "termination": "worker_result_limit",
                           "trigger": "worker produced no result within max_result_bytes"})
        elif worker_rc == 6:
            result.update({"status": "TIMEOUT", "native_rc": 6,
                           "termination": "worker_timeout"})
        else:
            result.update({"status": "TOOL_ERROR", "native_rc": 7,
                           "termination": "missing_worker_result",
                           "trigger": "worker result missing or invalid"})
        publish(out, result, limits["max_result_bytes"])
        return result, result["native_rc"], out
    errors = support.validate_worker_result(worker_result, worker_rc=worker_rc)
    if errors:
        result.update({"status": "TOOL_ERROR", "native_rc": 7,
                       "termination": "worker_evidence_rejected",
                       "trigger": "; ".join(errors)})
        publish(out, result, limits["max_result_bytes"])
        return result, 7, out
    result = dict(worker_result)
    result.update({
        "kind": "B_VERIFY_OFFLINE_RESULT",
        "case_id": case_id,
        "worker_rc": worker_rc,
        "worker_started": True,
        "worker_exited": True,
        "worker_peak_bytes": worker_peak,
        "worker_self_peak_bytes": worker_result.get("worker_reported_peak_bytes"),
        "memory_threshold_bytes": limits["worker_peak_working_set_bytes"],
        "measurement_method": "parent polling Windows GetProcessMemoryInfo PeakWorkingSetSize on worker; self-report also retained",
        "worker_stdout": "worker.stdout.log",
        "worker_stderr": "worker.stderr.log",
        "stdout_bytes": stdout_path.stat().st_size,
        "stderr_bytes": stderr_path.stat().st_size,
        "log_truncated": result.get("log_truncated", False),
        "elapsed_s": round(time.monotonic() - started, 6),
        "command": command,
        "case_sha256": support.sha256_file(Path(case["file"])) if case.get("file") else None,
        "run_py_sha256": support.sha256_file(Path(__file__)),
        "worker_sha256": support.sha256_file(Path(worker_path)),
        "termination": "normal",
    })
    observed = [x for x in (worker_peak, worker_result.get("worker_reported_peak_bytes")) if x is not None]
    if not observed:
        result.update({"status": "TOOL_ERROR", "native_rc": 7,
                       "termination": "memory_measurement_failed",
                       "trigger": "no worker working-set observation"})
        publish(out, result, limits["max_result_bytes"])
        return result, 7, out
    observed_peak = max(observed)
    result["memory_observed_bytes"] = observed_peak
    if observed_peak > limits["worker_peak_working_set_bytes"]:
        result.update({"status": "LIMIT", "native_rc": 5,
                       "fully_consumed": False,
                       "termination": "memory_limit",
                       "trigger": "worker peak exceeds configured threshold",
                       "memory_threshold_bytes": limits["worker_peak_working_set_bytes"],
                       "memory_observed_bytes": observed_peak})
        publish(out, result, limits["max_result_bytes"])
        return result, 5, out
    published = publish(out, result, limits["max_result_bytes"])
    if not published:
        # No over-limit result file may be published; the real CLI rejects.
        return result, 5, out
    return result, result["native_rc"], out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-file", required=True)
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--out", required=True)
    # Fixed, reviewed fixtures only; normal users do not need this option.
    parser.add_argument("--fixture-worker", choices=("none", "log_flood", "sleep_forever",
                                                     "nonzero_rc", "missing_result", "pass_text"),
                        default="none")
    args = parser.parse_args()
    started = time.monotonic()
    out = Path(args.out).resolve()
    input_root = Path(args.input_root).resolve()
    # Unified protection before any output mutation, including -O and bad CASE.
    if out.exists():
        return emit("TOOL_ERROR", "existing-out", None,
                    {"error": "output directory already exists; no overwrite"})
    if sys.flags.optimize != 0:
        # The optimized runtime is rejected before any output creation, including
        # when the requested output would be inside a protected tool tree.
        return emit("INVALID_INPUT", "optimized-python", None,
                    {"error": "Python -O/-OO is unsupported; no output created"})
    if out == input_root or input_root in out.parents:
        return emit("TOOL_ERROR", "protected-out", None,
                    {"error": "output must be outside input root"})
    if out == RETURN_ROOT or RETURN_ROOT in out.parents:
        return emit("TOOL_ERROR", "protected-return", None,
                    {"error": "output must be outside the return tool"})
    if not input_root.is_dir():
        return emit("INVALID_INPUT", "invalid-input-root", None,
                    {"error": "input root is not a directory"})
    try:
        case = support.load_case(args.case_file)
        support.validate_case_shape(case)
        limits = support.normalize_limits(case.get("limits"))
    except Exception as exc:
        return emit("INVALID_INPUT", "invalid-case", None,
                    {"error": "%s: %s" % (type(exc).__name__, exc)})
    case["file"] = str(Path(args.case_file).resolve())
    out.mkdir(parents=True, exist_ok=False)
    worker = WORKER
    if args.fixture_worker != "none":
        mapping = {
            "log_flood": HERE / "tests/fixtures/log_flood_worker.py",
            "sleep_forever": HERE / "tests/fixtures/sleep_forever_worker.py",
            "nonzero_rc": HERE / "tests/fixtures/nonzero_worker.py",
            "missing_result": HERE / "tests/fixtures/missing_result_worker.py",
            "pass_text": HERE / "tests/fixtures/pass_text_worker.py",
        }
        worker = mapping[args.fixture_worker]
    result, rc, out = execute_case(case, input_root, out, limits, started, worker_path=worker)
    return emit(result.get("status", "TOOL_ERROR"), result.get("case_id"), out,
                {"error": result.get("error"), "worker_rc": result.get("worker_rc")})


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
