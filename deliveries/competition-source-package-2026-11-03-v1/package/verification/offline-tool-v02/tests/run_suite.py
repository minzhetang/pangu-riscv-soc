"""B-owned frozen acceptance suite driver for B-VERIFY-OFFLINE-M0."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN_ROOT = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(RETURN_ROOT / "src"))
import support  # noqa: E402
sys.path.insert(0, str(RETURN_ROOT))
import RUN as runner  # noqa: E402

RUN = RETURN_ROOT / "RUN.py"
GEN = HERE / "generate.py"
CASES = HERE / "cases"
LOGS = RETURN_ROOT / "logs"
DIAG = RETURN_ROOT / "diagnostics"
PRESSURE = RETURN_ROOT / "pressure"


def sha(path):
    return support.sha256_file(path)


def run_cmd(argv, cwd, timeout=240):
    start = time.monotonic()
    try:
        proc = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout,
                              shell=False, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        return {"argv": [str(x) for x in argv], "cwd": str(cwd), "rc": proc.returncode,
                "stdout": proc.stdout, "stderr": proc.stderr,
                "elapsed_s": round(time.monotonic() - start, 6), "timed_out": False}
    except subprocess.TimeoutExpired as exc:
        return {"argv": [str(x) for x in argv], "cwd": str(cwd), "rc": 124,
                "stdout": (exc.stdout or "") if isinstance(exc.stdout, str) else "",
                "stderr": (exc.stderr or "") if isinstance(exc.stderr, str) else "",
                "elapsed_s": round(time.monotonic() - start, 6), "timed_out": True}


def write_case(path, case):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(case, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def copy_artifacts(case_id, out):
    dest = LOGS / case_id
    dest.mkdir(parents=True, exist_ok=True)
    if out and Path(out).is_dir():
        for name in ("result.json", "worker-result.json", "command.json",
                     "worker.stdout.log", "worker.stderr.log"):
            src = Path(out) / name
            if src.is_file():
                shutil.copy2(src, dest / name)


def hash_tree(root):
    root = Path(root)
    return {p.relative_to(root).as_posix(): support.sha256_file(p)
            for p in root.rglob("*") if p.is_file()}


def artifact_text(path, limit=4 * 1024 * 1024):
    p = Path(path)
    if not p.exists():
        return ""
    data = p.read_bytes()
    if len(data) > limit:
        data = data[:limit]
    return data.decode("utf-8", errors="replace")


def expected_match(entry, result, rc, inputs, out=None):
    exp = entry["expected"]
    result_file = bool(out and (Path(out) / "result.json").is_file())
    worker_file = bool(out and (Path(out) / "worker-result.json").is_file())
    status_by_rc = {0: "MATCH", 2: "MISMATCH", 3: "INVALID_INPUT", 4: "INCOMPLETE",
                    5: "LIMIT", 6: "TIMEOUT", 7: "TOOL_ERROR"}
    actual = {
        "run_status": result.get("status") if result else status_by_rc.get(rc, "NO_RESULT"),
        "native_rc": result.get("native_rc") if result else rc,
        "parent_rc": rc,
        "result_file": result_file,
        "worker_result_file": worker_file,
        "output_created": bool(out and Path(out).exists()),
        "checked": result.get("checked") if result else None,
        "expected_records": result.get("expected_records") if result else None,
        "actual_records": result.get("actual_records") if result else None,
        "worker_started": result.get("worker_started") if result else None,
        "worker_rc": result.get("worker_rc") if result else None,
        "memory_threshold": result.get("memory_threshold_bytes") if result else None,
        "memory_observed": result.get("memory_observed_bytes") if result else None,
        "protected_tree_unchanged": result.get("protected_tree_unchanged") if result else None,
        "marker_ok": bool(out and (Path(out) / "marker.txt").is_file()
                         and (Path(out) / "marker.txt").read_text(encoding="ascii") == "preexisting\n"),
        "first": result.get("first_difference") if result else None,
        "inputs": inputs,
    }
    checks = []
    checks.append(("status", actual["run_status"] == exp["run_status"]))
    checks.append(("native_rc", int(actual["native_rc"]) == int(exp["native_rc"])))
    checks.append(("parent_rc", int(actual["parent_rc"]) == int(exp["native_rc"])))
    if "checked" in exp:
        checks.append(("checked", actual["checked"] == exp["checked"]))
    if "expected_records" in exp:
        checks.append(("expected_records", actual["expected_records"] == exp["expected_records"]))
    if "actual_records" in exp:
        checks.append(("actual_records", actual["actual_records"] == exp["actual_records"]))
    if "expect_result_file" in exp:
        checks.append(("result_file", actual["result_file"] == bool(exp["expect_result_file"])))
    if "output_created" in exp:
        checks.append(("output_created", actual["output_created"] == bool(exp["output_created"])))
    if "expect_worker_started" in exp:
        checks.append(("worker_started", actual["worker_started"] == bool(exp["expect_worker_started"])))
    if "worker_rc" in exp:
        checks.append(("worker_rc", actual["worker_rc"] == exp["worker_rc"]))
    if "memory_threshold" in exp:
        checks.append(("memory_threshold", actual["memory_threshold"] == exp["memory_threshold"]))
    if "memory_observed_gt" in exp:
        checks.append(("memory_observed_gt", actual["memory_observed"] is not None
                       and actual["memory_observed"] > exp["memory_observed_gt"]))
    if "protected_tree_unchanged" in exp:
        checks.append(("protected_tree_unchanged", actual["protected_tree_unchanged"] == bool(exp["protected_tree_unchanged"])))
    if "marker_unchanged" in exp:
        checks.append(("marker_unchanged", actual["marker_ok"] == bool(exp["marker_unchanged"])))
    if "max_result_bytes" in exp:
        p = (Path(out) / "result.json") if out else None
        checks.append(("max_result_bytes", bool(p and p.is_file() and p.stat().st_size <= exp["max_result_bytes"])))
    if "max_worker_result_bytes" in exp:
        p = (Path(out) / "worker-result.json") if out else None
        checks.append(("max_worker_result_bytes", bool(p and p.is_file() and p.stat().st_size <= exp["max_worker_result_bytes"])))
    if "max_log_bytes" in exp:
        vals = []
        if out:
            for n in ("worker.stdout.log", "worker.stderr.log"):
                q = Path(out) / n
                if q.exists():
                    vals.append(q.stat().st_size)
        checks.append(("max_log_bytes", bool(vals) and all(v <= exp["max_log_bytes"] for v in vals)))
    if "max_elapsed" in exp:
        checks.append(("max_elapsed", result is not None and result.get("elapsed_s") is not None
                       and result.get("elapsed_s") <= exp["max_elapsed"]))
    if "first" in exp and exp["first"] is not None:
        first = actual["first"] or {}
        checks.append(("first_ordinal", first.get("ordinal") == exp["first"]["ordinal"]))
        if "kind" in exp["first"]:
            checks.append(("first_kind", first.get("kind") == exp["first"]["kind"]))
        if "field" in exp["first"]:
            checks.append(("first_field", first.get("field") == exp["first"]["field"]))
        if "expected" in exp["first"]:
            checks.append(("first_expected", first.get("expected") == exp["first"]["expected"]))
        if "actual" in exp["first"]:
            checks.append(("first_actual", first.get("actual") == exp["first"]["actual"]))
    if "neighbor_ordinals" in exp:
        neighbors = result.get("neighbors", []) if result else []
        checks.append(("neighbors", [n.get("ordinal") for n in neighbors] == exp["neighbor_ordinals"]))
    if "min_bytes_each" in exp:
        bytes_values = [v.get("bytes") for v in inputs.values() if isinstance(v, dict) and v.get("bytes") is not None]
        checks.append(("min_bytes_each", len(bytes_values) == 2 and all(v >= exp["min_bytes_each"] for v in bytes_values)))
    if "min_cycle" in exp:
        try:
            text = Path(inputs["actual_path"]).read_text(encoding="ascii")
            checks.append(("min_cycle", str(exp["min_cycle"]) in text or "4294967301" in text))
        except Exception:
            checks.append(("min_cycle", False))
    return checks, actual


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", required=True)
    ap.add_argument("--plan", default=str(HERE / "PLAN.json"))
    ap.add_argument("--plan-sha", default=str(HERE / "PLAN.sha256"))
    ap.add_argument("--work", required=True)
    args = ap.parse_args()
    package = Path(args.package).resolve()
    work = Path(args.work).resolve()
    plan_path = Path(args.plan).resolve()
    if work.exists():
        raise SystemExit("work directory must be fresh: " + str(work))
    work.mkdir(parents=True, exist_ok=False)
    plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    plan_sha = sha(plan_path)
    declared = Path(args.plan_sha).read_text(encoding="ascii").split()[0].upper()
    if plan_sha != declared:
        raise SystemExit("PLAN SHA mismatch: %s != %s" % (plan_sha, declared))
    CASES.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    DIAG.mkdir(parents=True, exist_ok=True)
    PRESSURE.mkdir(parents=True, exist_ok=True)
    # Remove previous derived pressure/diagnostic files; logs are overwritten
    # per case below.  Never touch the frozen input package or plan.
    for old in PRESSURE.glob("*.json"):
        old.unlink()
    for old in DIAG.glob("*.json"):
        old.unlink()
    for old in LOGS.iterdir():
        if old.is_dir():
            shutil.rmtree(old)
        else:
            old.unlink()
    generate_log = LOGS / "generate.log"
    generated_root = work / "input"
    output_root = work / "out"
    generated_root.mkdir(parents=True, exist_ok=False)
    output_root.mkdir(parents=True, exist_ok=False)
    gen = run_cmd([sys.executable, "-B", str(GEN), "--input-root", str(package),
                   "--out", str(generated_root), "--mode", "all", "--sizes", "1,16,128"], RETURN_ROOT, timeout=600)
    generate_log.write_text(json.dumps(gen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if gen["rc"] != 0:
        raise SystemExit("generator failed; see " + str(generate_log))

    rows = []
    suite_start = time.monotonic()
    for entry in plan["cases"]:
        cid = entry["id"]
        kind = entry["kind"]
        row = {"id": cid, "acceptance_id": entry["acceptance_id"], "kind": kind,
               "input_root": entry.get("input_root"), "expected": entry["expected"],
               "case_file": None, "command": None, "actual": None,
               "test_status": "FAIL", "logs": "logs/" + cid, "notes": entry.get("note", "")}
        case_path = CASES / (cid + ".json")
        out = None
        result = None
        rc = None
        cmd = None
        inputs = {}
        if kind in ("run", "existing_out", "optimized_python", "fixture"):
            if entry.get("case"):
                case_obj = json.loads(json.dumps(entry["case"]))
                if entry.get("archive_manifest"):
                    manifest = json.loads((generated_root / entry["archive_manifest"]).read_text(encoding="utf-8-sig"))
                    for side in ("expected", "actual"):
                        if case_obj[side].get("index_SHA256") == "FROM_MANIFEST":
                            case_obj[side]["index_SHA256"] = manifest[side]["index_SHA256"]
                write_case(case_path, case_obj)
            else:
                write_case(case_path, {"id": cid,
                    "expected": {"storage": "raw", "stream": "trace", "path": "inputs/seeds/S00-duplicates-kept/expected.log", "complete": True},
                    "actual": {"storage": "raw", "stream": "trace", "path": "inputs/seeds/S00-duplicates-kept/actual.log", "complete": True},
                    "allow_empty": False, "limits": {}})
            root = package if entry.get("input_root") == "package" else generated_root
            out = output_root / cid
            if kind == "existing_out":
                out.mkdir(parents=True, exist_ok=False)
                (out / "marker.txt").write_text("preexisting\n", encoding="ascii")
            if kind == "optimized_python":
                argv = [sys.executable, "-O", "-B", str(RUN), "--case-file", str(case_path),
                        "--input-root", str(root), "--out", str(out)]
            elif kind == "fixture":
                argv = [sys.executable, "-B", str(RUN), "--case-file", str(case_path),
                        "--input-root", str(root), "--out", str(out),
                        "--fixture-worker", entry["fixture_worker"]]
            else:
                argv = [sys.executable, "-B", str(RUN), "--case-file", str(case_path),
                        "--input-root", str(root), "--out", str(out)]
            cmd = run_cmd(argv, RETURN_ROOT, timeout=240)
            rc = cmd["rc"]
            if out.is_dir() and (out / "result.json").is_file():
                try:
                    result = support.load_json(out / "result.json")
                except Exception:
                    result = None
            if result:
                inputs = {k: result.get(k + "_input") for k in ("expected", "actual")}
                inputs["actual_path"] = str(root / entry["case"]["actual"]["path"]) if entry.get("case") else None
            row.update({"case_file": str(case_path.relative_to(RETURN_ROOT)),
                        "command": {**cmd, "out": str(out)}})
        elif kind == "optimized_protected":
            write_case(CASES / "C3-optimized-protected.json", {
                "id": "C3-optimized-protected",
                "expected": {"storage": "raw", "stream": "trace", "path": "inputs/seeds/S00-duplicates-kept/expected.log", "complete": True},
                "actual": {"storage": "raw", "stream": "trace", "path": "inputs/seeds/S00-duplicates-kept/actual.log", "complete": True},
                "allow_empty": False, "limits": {}})
            tool_copy = work / "protected-tool"
            shutil.copytree(RETURN_ROOT, tool_copy)
            before = hash_tree(tool_copy)
            out = tool_copy / "forbidden-output-probe"
            cmd = run_cmd([sys.executable, "-O", "-B", str(tool_copy / "RUN.py"),
                           "--case-file", str(CASES / "C3-optimized-protected.json"),
                           "--input-root", str(package), "--out", str(out)], tool_copy, timeout=120)
            after = hash_tree(tool_copy)
            rc = cmd["rc"]
            result = {"status": "INVALID_INPUT" if rc == 3 else "NO_RESULT",
                      "native_rc": rc, "fully_consumed": False,
                      "checked": 0, "expected_records": 0, "actual_records": 0,
                      "mismatch_count": 0, "differences": [],
                      "worker_started": False,
                      "protected_tree_unchanged": before == after}
            row.update({"command": cmd, "output_created": out.exists(),
                        "protected_tree_unchanged": before == after,
                        "case_file": "tests/cases/C3-optimized-protected.json"})
        elif kind == "invalid_case":
            case_path.write_text("{not valid json\n", encoding="utf-8")
            out = output_root / cid
            cmd = run_cmd([sys.executable, "-B", str(RUN), "--case-file", str(case_path),
                           "--input-root", str(package), "--out", str(out)], RETURN_ROOT, timeout=60)
            rc = cmd["rc"]
            result = None
            row.update({"command": cmd, "output_created": out.exists(), "case_file": str(case_path.relative_to(RETURN_ROOT))})
        elif kind == "invalid_root":
            out = output_root / cid
            cmd = run_cmd([sys.executable, "-B", str(RUN), "--case-file", str(CASES / "C0-default.json"),
                           "--input-root", str(work / "missing-input-root"), "--out", str(out)],
                          RETURN_ROOT, timeout=60)
            rc = cmd["rc"]
            result = None
            row.update({"command": cmd, "output_created": out.exists()})
        elif kind == "oversize_case":
            case_path.write_text('{"id":"oversize","padding":"' + "X" * (1024 * 1024 + 1) + '"}', encoding="utf-8")
            out = output_root / cid
            cmd = run_cmd([sys.executable, "-B", str(RUN), "--case-file", str(case_path),
                           "--input-root", str(package), "--out", str(out)], RETURN_ROOT, timeout=60)
            rc = cmd["rc"]
            result = None
            row.update({"command": cmd, "output_created": out.exists(), "case_file": str(case_path.relative_to(RETURN_ROOT))})
        elif kind == "oversize_index":
            src = generated_root / "generated/block-boundary/expected_archive"
            dst = generated_root / "generated/oversize-index"
            shutil.copytree(src, dst)
            with (dst / "index.json").open("ab") as fh:
                fh.write(b" " * (2 * 1024 * 1024 + 2))
            case_obj = {"id": cid,
                        "expected": {"storage": "archive", "stream": "bus",
                                     "path": "generated/oversize-index",
                                     "index_SHA256": "A" * 64, "complete": True},
                        "actual": {"storage": "archive", "stream": "bus",
                                   "path": "generated/oversize-index",
                                   "index_SHA256": "A" * 64, "complete": True},
                        "allow_empty": False, "limits": {}}
            write_case(case_path, case_obj)
            out = output_root / cid
            cmd = run_cmd([sys.executable, "-B", str(RUN), "--case-file", str(case_path),
                           "--input-root", str(generated_root), "--out", str(out)], RETURN_ROOT, timeout=60)
            rc = cmd["rc"]
            if (out / "result.json").is_file():
                result = support.load_json(out / "result.json")
            row.update({"command": cmd, "case_file": str(case_path.relative_to(RETURN_ROOT))})
        elif kind == "unit_memory":
            case_obj = json.loads(json.dumps(entry["case"]))
            write_case(case_path, case_obj)
            case_obj["file"] = str(case_path)
            out = output_root / cid
            limits = support.normalize_limits(case_obj.get("limits"))
            old_peak = support.peak_working_set
            support.peak_working_set = lambda pid=None: None
            try:
                result, rc, out = runner.execute_case(
                    case_obj, package, out, limits, time.monotonic(),
                    worker_path=RETURN_ROOT / "tests/fixtures/no_peak_worker.py")
            finally:
                support.peak_working_set = old_peak
            cmd = {"argv": ["internal:execute_case", "no_peak_worker.py"],
                   "cwd": str(RETURN_ROOT), "rc": rc, "elapsed_s": result.get("elapsed_s"),
                   "timed_out": False, "stdout": "", "stderr": ""}
            row.update({"command": cmd, "case_file": str(case_path.relative_to(RETURN_ROOT))})
        elif kind == "guard_nonzero_rc":
            fake = {"status": "MATCH", "native_rc": 0, "ABI": support.ABI, "CPU_function_proven": False,
                    "fully_consumed": True, "checked": 8, "expected_records": 8,
                    "actual_records": 8, "mismatch_count": 0, "differences": []}
            errs = support.validate_worker_result(fake, worker_rc=1)
            result = {"status": "REJECT_NOT_MATCH" if errs else "ACCEPTED",
                      "native_rc": 7, "fully_consumed": False,
                      "checked": 0, "expected_records": 0, "actual_records": 0,
                      "mismatch_count": 0, "differences": [],
                      "guard_errors": errs}
            row["guard"] = result
            (LOGS / cid).mkdir(parents=True, exist_ok=True)
            (LOGS / cid / "guard.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                                   encoding="utf-8")
        elif kind == "guard_printed_pass":
            fake = {"status": "MATCH", "native_rc": 0, "ABI": support.ABI, "CPU_function_proven": False,
                    "mismatch_count": 0, "differences": []}
            errs = support.validate_worker_result(fake, worker_rc=0)
            result = {"status": "REJECT_NOT_MATCH" if errs else "ACCEPTED",
                      "native_rc": 7, "fully_consumed": False,
                      "checked": 0, "expected_records": 0, "actual_records": 0,
                      "mismatch_count": 0, "differences": [],
                      "guard_errors": errs}
            row["guard"] = result
            (LOGS / cid).mkdir(parents=True, exist_ok=True)
            (LOGS / cid / "guard.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                                   encoding="utf-8")
        elif kind == "moved":
            # Copy the immutable input package and the return tool to a fresh
            # Chinese/space path; no original absolute path is passed to RUN.
            moved = work / "moved 中文 空格"
            moved.mkdir(parents=True, exist_ok=False)
            in_copy = moved / "input package"
            tool_copy = moved / "return tool"
            shutil.copytree(package, in_copy)
            shutil.copytree(RETURN_ROOT, tool_copy)
            case_copy = tool_copy / "tests/cases/R01.json"
            write_case(case_copy, {
                "id": "R01",
                "expected": {"storage": "raw", "stream": "trace",
                             "path": "inputs/seeds/S00-duplicates-kept/expected.log", "complete": True},
                "actual": {"storage": "raw", "stream": "trace",
                           "path": "inputs/seeds/S00-duplicates-kept/actual.log", "complete": True},
                "allow_empty": False, "limits": {}})
            out = moved / "out R01"
            argv = [sys.executable, "-B", str(tool_copy / "RUN.py"),
                    "--case-file", str(case_copy), "--input-root", str(in_copy), "--out", str(out)]
            cmd = run_cmd(argv, moved, timeout=240)
            rc = cmd["rc"]
            if (out / "result.json").is_file():
                result = support.load_json(out / "result.json")
            if result:
                inputs = {k: result.get(k + "_input") for k in ("expected", "actual")}
                inputs["actual_path"] = str(in_copy / "inputs/seeds/S00-duplicates-kept/actual.log")
            row.update({"case_file": str(case_copy.relative_to(tool_copy)),
                        "moved_paths": {"input": str(in_copy), "tool": str(tool_copy),
                                        "out": str(out)},
                        "command": {**cmd, "out": str(out)}})
        else:
            raise SystemExit("unknown kind " + kind)
        if result is None:
            status_by_rc = {0: "MATCH", 2: "MISMATCH", 3: "INVALID_INPUT", 4: "INCOMPLETE",
                            5: "LIMIT", 6: "TIMEOUT", 7: "TOOL_ERROR"}
            cli = {}
            try:
                lines = [x for x in (cmd or {}).get("stdout", "").splitlines() if x.strip()]
                cli = json.loads(lines[-1]) if lines else {}
            except Exception:
                cli = {}
            result = {"status": cli.get("status", status_by_rc.get(rc, "NO_RESULT")),
                      "native_rc": cli.get("native_rc", rc if rc is not None else 7),
                      "worker_rc": cli.get("worker_rc"),
                      "worker_started": bool(out and (Path(out) / "worker.stdout.log").is_file()),
                      "fully_consumed": False, "checked": 0,
                      "expected_records": 0, "actual_records": 0,
                      "mismatch_count": 0, "differences": []}
        if kind not in ("guard_nonzero_rc", "guard_printed_pass"):
            checks, actual = expected_match(entry, result, rc, inputs, out)
            row["actual"] = actual
            row["checks"] = [{"name": n, "pass": bool(v)} for n, v in checks]
            row["test_status"] = "PASS" if all(v for _, v in checks) else "FAIL"
        else:
            exp = entry["expected"]["run_status"]
            row["actual"] = {"run_status": result["status"], "native_rc": result.get("native_rc")}
            row["test_status"] = "PASS" if exp == result["status"] == "REJECT_NOT_MATCH" else "FAIL"
        row["result"] = result
        row["elapsed_s"] = (row.get("command") or {}).get("elapsed_s")
        # Persist bounded logs and diagnostics.
        if out:
            copy_artifacts(cid, out)
        ind = LOGS / cid
        ind.mkdir(parents=True, exist_ok=True)
        (ind / "suite.stdout.log").write_text((cmd or {}).get("stdout", ""), encoding="utf-8")
        (ind / "suite.stderr.log").write_text((cmd or {}).get("stderr", ""), encoding="utf-8")
        if case_path.is_file():
            shutil.copy2(case_path, ind / "case.json")
        if kind in ("run", "existing_out", "optimized_python", "moved", "fixture",
                    "optimized_protected", "invalid_case", "invalid_root",
                    "oversize_case", "oversize_index", "unit_memory"):
            diag = {"id": cid, "status": result.get("status"),
                    "no_difference": not bool(result.get("differences")),
                    "first_difference": result.get("first_difference"),
                    "neighbors": result.get("neighbors", []),
                    "differences": result.get("differences", []),
                    "error": result.get("error"),
                    "checked": result.get("checked"),
                    "expected_records": result.get("expected_records"),
                    "actual_records": result.get("actual_records")}
            (DIAG / (cid + ".json")).write_text(json.dumps(diag, ensure_ascii=False, indent=2) + "\n",
                                                 encoding="utf-8")
        if cid.startswith("S01") or cid == "S02":
            PRESSURE.mkdir(exist_ok=True)
            pressure_row = {"id": cid, "status": result.get("status"),
                            "expected_input": result.get("expected_input"),
                            "actual_input": result.get("actual_input"),
                            "checked": result.get("checked"),
                            "elapsed_s": row.get("elapsed_s"),
                            "worker_peak_bytes": result.get("worker_peak_bytes"),
                            "parent_peak_bytes": result.get("parent_peak_bytes"),
                            "worker_peak_limit_bytes": support.MAX_WORKER_WS,
                            "within_worker_limit": (result.get("worker_peak_bytes") is not None and
                                                    result.get("worker_peak_bytes") <= support.MAX_WORKER_WS)}
            (PRESSURE / (cid + ".json")).write_text(json.dumps(pressure_row, ensure_ascii=False, indent=2) + "\n",
                                                    encoding="utf-8")
        rows.append(row)
        print("%-34s %-18s %s" % (cid, result.get("status"), row["test_status"]))
    suite_seconds = time.monotonic() - suite_start
    all_pass = all(r["test_status"] == "PASS" for r in rows)
    summary = {
        "kind": "B_VERIFY_OFFLINE_RESULTS",
        "task": "B-VERIFY-OFFLINE-M0-R1",
        "ABI": support.ABI,
        "amendment": "1.0.1 resource/error guards",
        "plan": str(Path(args.plan).relative_to(RETURN_ROOT)) if Path(args.plan).is_relative_to(RETURN_ROOT) else args.plan,
        "plan_sha256": plan_sha,
        "source_package_manifest_sha256": plan["source_package"]["manifest_SHA256"],
        "python": sys.version,
        "suite_elapsed_s": round(suite_seconds, 6),
        "total_suite_seconds_limit": plan["total_suite_seconds_limit"],
        "all_test_pass": all_pass,
        "local_only": True,
        "CPU_function_proven": False,
        "new_DUT": 0,
        "cases": rows,
        "notes": ["Test PASS means the frozen expected outcome was met; negative cases PASS when the expected rejection occurred.",
                  "P02 is replay of already accepted old observations, not independent ISA validation.",
                  "No hardware, PDS, simulator, install, or external network was used."]
    }
    (HERE / "results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                       encoding="utf-8", newline="\n")
    pressure = {"kind": "B_VERIFY_OFFLINE_PRESSURE", "plan_sha256": plan_sha,
                "suite_elapsed_s": round(suite_seconds, 6),
                "measurement_method": "parent polls Windows GetProcessMemoryInfo PeakWorkingSetSize on the worker; parent self-peak reported separately",
                "limits": {"worker_peak_working_set_bytes": support.MAX_WORKER_WS,
                           "case_timeout_seconds": support.DEFAULT_CASE_SECONDS,
                           "total_suite_seconds": support.MAX_SUITE_SECONDS},
                "generated_inputs_in_return": False,
                "rows": []}
    for p in sorted(PRESSURE.glob("*.json")):
        if p.name == "results.json":
            continue
        pressure["rows"].append(json.loads(p.read_text(encoding="utf-8-sig")))
    (PRESSURE / "results.json").write_text(json.dumps(pressure, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8", newline="\n")
    commands = ["# Commands executed", "", "Plan SHA256: `%s`" % plan_sha, ""]
    for row in rows:
        if row.get("command"):
            c = row["command"]
            commands.append("## " + row["id"])
            commands.append("cwd: `%s`" % c.get("cwd"))
            commands.append("native_rc: `%s` elapsed_s: `%s` timed_out: `%s`" %
                            (c.get("rc"), c.get("elapsed_s"), c.get("timed_out")))
            commands.append("argv: `%s`" % json.dumps(c.get("argv"), ensure_ascii=False))
            commands.append("")
    (RETURN_ROOT / "COMMANDS.md").write_text("\n".join(commands) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"all_test_pass": all_pass, "cases": len(rows), "suite_elapsed_s": round(suite_seconds, 3)},
                     ensure_ascii=False))
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
