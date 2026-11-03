"""Read-only post-run BGEU evidence audit; never invokes a DUT or native tool.

Writes one new evidence-review.json only, refusing to replace existing evidence.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(r"D:\A_FPGA_Comp")
DEFAULT = ROOT / "work/icarus/2026-10-18-cpu-bgeu"
TOP = "tb_cpu_selfcheck_v1"
DUT = TOP + ".dut."
MASK = 0xffffffff


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def signed32(x):
    x &= MASK
    return x - (1 << 32) if x & (1 << 31) else x


def bimm(word):
    raw = ((word >> 31) << 12) | (((word >> 7) & 1) << 11)
    raw |= (((word >> 25) & 63) << 5) | (((word >> 8) & 15) << 1)
    return raw - 8192 if raw & 4096 else raw


def vcd_edges(path):
    """Return stable pre-timegroup and settled post-timegroup at every posedge."""
    text = path.read_text(encoding="ascii")
    assert re.search(r"\$timescale\s+1ps\s+\$end", text), path
    header, body = text.split("$enddefinitions $end", 1)
    names, scope = {}, []
    for line in header.splitlines():
        fields = line.split()
        if not fields:
            continue
        if fields[0] == "$scope":
            scope.append(fields[2])
        elif fields[0] == "$upscope":
            scope.pop()
        elif fields[0] == "$var":
            names[".".join(scope + [fields[4]])] = fields[3]
    vals, tick, changes, ticks, edges = {}, None, [], [], []

    def num(snapshot, name):
        raw = snapshot.get(names[name], "x")
        assert not re.search("[xz]", raw, re.I), (path.name, tick, name, raw)
        return int(raw, 2)

    def commit():
        if tick is None:
            return
        before = vals.copy()
        for code, value in changes:
            vals[code] = value
        if (before.get(names[TOP + ".clk"]) == "0"
                and vals.get(names[TOP + ".clk"]) == "1"
                and before.get(names[TOP + ".rst_n"]) == "1"):
            edges.append((tick, before, vals.copy()))

    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("$"):
            continue
        if line.startswith("#"):
            commit()
            tick = int(line[1:])
            assert not ticks or tick > ticks[-1], path
            ticks.append(tick)
            changes = []
        elif line[0] in "01xXzZ":
            changes.append((line[1:], line[0].lower()))
        elif line[0] in "bB":
            value, code = line[1:].split()
            changes.append((code, value.lower()))
    commit()
    return edges, num, ticks[-1]


def expand_observations(case):
    out = []
    for row in case.get("observations", []):
        a, b, take = row["a"], row["b"], row["expected_taken"]
        count = len(take) if isinstance(take, list) else 1
        for i in range(count):
            out.append(dict(pc=row["pc"], a=int(a[i] if isinstance(a, list) else a, 16),
                b=int(b[i] if isinstance(b, list) else b, 16),
                taken=take[i] if isinstance(take, list) else take,
                offset=row["offset"], target=row["target"], kind=row["kind"]))
    return out


def audit(dest):
    result = read_json(dest / "result.json")
    assert result.get("regression_completed") and not result.get("error"), "DUT run not complete"
    frozen = read_json(dest / "input-manifest.json")
    plan = read_json(dest / "plan.json")
    expected = read_json(dest / "expected-traces.json")
    case_map = {c["id"]: c for c in plan["cases"]}
    buckets = {"protected": frozen["protected"], "inputs": frozen["inputs"],
        "tools": frozen["tool_hashes"], "scripts": frozen["scripts"], "artifacts": result["artifacts"]}
    entries = [v for values in buckets.values() for v in values]
    for row in entries:
        assert sha(Path(row["path"])) == row["sha256"].upper(), row["path"]
    report = dict(date="2026-10-18", method="Independent post-run raw log/VCD/SHA audit; no DUT rerun, no frozen edits.",
        auditor=dict(path=str(Path(__file__).resolve()), sha256=sha(Path(__file__))),
        hashes=dict(entries=len(entries), uniquePaths=len({v["path"] for v in entries}), mismatches=0,
            **{k: len(v) for k, v in buckets.items()}),
        logs=dict(cases=0, finalWords=0, continuousTRACE=0, mainWB=0, mainSTORE=0,
            newWB=0, newSTORE=0, controlWB=0, controlSTORE=0, deduplicated=False),
        waves=dict(count=0, bytes=0, precision="1ps", monotonic=True, allWB_STORE_match_rawlogs=True),
        cases=[], focused=[], control_BGEU=[])
    main_bge, main_blt, main_bltu, main_bgeu = [], [], [], []
    all_edges = {}
    for control, rows in [(False, result["cases"]), (True, result["controls"])]:
        for row in rows:
            cid = row["id"]
            case = case_map[cid]
            text = Path(row["log"]).read_text(encoding="utf-8")
            regs = re.findall(r"^REG\|(\d+)\|([0-9a-fxz]+)$", text, re.M)
            mem = re.findall(r"^MEM\|(\d+)\|([0-9a-fxz]+)$", text, re.M)
            assert len(regs) == 32 and len(mem) == 64
            assert [int(i) for i, _ in regs] == list(range(32))
            assert [int(i) for i, _ in mem] == list(range(0, 256, 4))
            assert all(not re.search("[xz]", x, re.I) for _, x in regs + mem)
            final_diffs = sum(x != f"{v:08x}" for (_, x), v in zip(regs, case["expected_regs"]))
            final_diffs += sum(x != f"{v:08x}" for (_, x), v in zip(mem, case["expected_mem"]))
            wbs = [(int(c), int(rd), int(data, 16)) for c, rd, data in
                re.findall(r"^WB\|cycle=(\d+)\|rd=(\d+)\|data=([0-9a-f]+)$", text, re.M)]
            stores = [(int(c), int(addr, 16), int(data, 16)) for c, addr, data in
                re.findall(r"^STORE\|cycle=(\d+)\|addr=([0-9a-f]+)\|data=([0-9a-f]+)$", text, re.M)]
            ew = [(r["rd"], int(r["data"], 16)) for r in expected[cid]["writebacks"]]
            es = [(int(r["address"], 16), int(r["data"], 16)) for r in expected[cid]["stores"]]
            ordered_match = [(r, d) for _, r, d in wbs] == ew and [(a, d) for _, a, d in stores] == es
            assert (not final_diffs) == (row["final_status"] == "PASS")
            assert ordered_match == (row["trace_status"] == "PASS")
            assert not re.findall(r"^PROTOCOL_ERROR\|", text, re.M)
            assert ("$finish called" in text) != ("FATAL:" in text)
            trace_lines = re.findall(r"^TRACE\|(.*)$", text, re.M)
            traces = [{k: v for k, v in (p.split("=", 1) for p in line.split("|"))} for line in trace_lines]
            wave = Path(row["wave"]["path"])
            edges, n, last_tick = vcd_edges(wave)
            assert len(edges) == len(traces) and last_tick == row["wave"]["last_tick"]
            assert [int(t["cycle"]) for t in traces] == list(range(1, len(traces) + 1))
            vw, vs, branches = [], [], []
            for (tick, pre, post), tr in zip(edges, traces):
                cycle = n(post, TOP + ".cycle")
                assert cycle == int(tr["cycle"])
                for key, sig, base in [("pc", "pc", 16), ("inst", "inst", 16),
                        ("id_pc", "id_pc", 16), ("stall", "stall_if", 2),
                        ("flush", "flush_if", 2), ("wb_en", "mem_reg_write", 2),
                        ("wb_rd", "mem_rd", 10), ("wb_data", "wb_write_data", 16)]:
                    assert n(pre, DUT + sig) == int(tr[key], base), (cid, cycle, key)
                if n(pre, DUT + "mem_reg_write") and n(pre, DUT + "mem_rd"):
                    vw.append((cycle, n(pre, DUT + "mem_rd"), n(pre, DUT + "wb_write_data")))
                if n(pre, DUT + "mem_wren"):
                    vs.append((cycle, n(pre, DUT + "mem_addr"), n(pre, DUT + "mem_wdata")))
                if not n(pre, DUT + "id_branch") or n(pre, DUT + "id_funct3") not in (4, 5, 6, 7):
                    continue
                f3 = n(pre, DUT + "id_funct3")
                pc = n(pre, DUT + "id_pc")
                word = int(case["instructions"][pc // 4]["word"], 16)
                assert word & 127 == 99 and (word >> 12) & 7 == f3
                a, b = n(pre, DUT + "forward_rs1"), n(pre, DUT + "forward_rs2")
                offset = bimm(word)
                target = (pc + offset) & MASK
                semantic = (int(signed32(a) < signed32(b)) if f3 == 4 else
                    (int(signed32(a) >= signed32(b)) if f3 == 5 else
                     (int((a & MASK) < (b & MASK)) if f3 == 6 else int((a & MASK) >= (b & MASK)))))
                observed = n(pre, DUT + "branch_taken")
                assert observed == (int(a != b) if control and f3 == 7 else semantic)
                assert n(pre, DUT + "id_imm") == offset & MASK
                assert n(pre, DUT + "branch_target") == target
                assert n(pre, DUT + "id_alu_ctrl") == 1
                assert n(pre, DUT + "alu_result") == (a - b) & MASK
                assert n(pre, DUT + "alu_zero") == int(a == b)
                assert n(pre, DUT + "id_reg_write") == n(pre, DUT + "id_mem_write") == 0
                assert n(pre, DUT + "flush_if") == n(pre, DUT + "flush_id") == observed
                if observed:
                    assert n(post, DUT + "pc_reg") == target
                    assert n(post, DUT + "if_inst") == 0
                    assert all(n(post, DUT + x) == 0 for x in
                        ("id_reg_write", "id_mem_write", "id_branch", "id_jump"))
                else:
                    assert n(post, DUT + "pc_reg") == (n(pre, DUT + "pc_reg") + 4) & MASK
                item = dict(id=cid, cycle=cycle, ps=tick, pc=pc, funct3=f3,
                    a=f"{a:08x}", b=f"{b:08x}", offset=offset, target=target,
                    taken=observed, expected_predicate=semantic, after_pc=n(post, DUT + "pc_reg"),
                    alu_ctrl=1, sub_result=f"{(a-b)&MASK:08x}", zero=int(a == b))
                branches.append(item)
                if not control:
                    (main_blt if f3 == 4 else (main_bge if f3 == 5 else
                        (main_bltu if f3 == 6 else main_bgeu))).append(item)
            assert vw == wbs and vs == stores, cid
            if cid.startswith("N"):
                obs = expand_observations(case)
                assert len(branches) == len(obs)
                for got, want in zip(branches, obs):
                    assert got["pc"] == want["pc"] and int(got["a"], 16) == want["a"] and int(got["b"], 16) == want["b"]
                    assert got["offset"] == want["offset"] and got["target"] == want["target"]
                    if not control:
                        assert got["taken"] == want["taken"]
                if control:
                    report["control_BGEU"].extend(branches)
                else:
                    all_edges[cid] = (edges, n, branches)
            metrics = dict(s.split("=", 1) for s in re.search(r"^METRICS\|(.*)$", text, re.M)[1].split("|"))
            assert int(metrics["cycles"]) == len(edges)
            assert int(metrics["sim_ns"]) == last_tick
            assert sum(int(t["stall"]) for t in traces) == int(metrics["stall_cycles"]) == row["stall_cycles"]
            assert sum(int(t["flush"]) for t in traces) == int(metrics["flush_cycles"]) == row["flush_cycles"]
            assert int(metrics["marker_cycle"]) + 4 == len(edges)
            if not control:
                assert row["strict_status"] == "PASS"
                for field in ("stall", "flush"):
                    exp = plan[field + "_expectations"].get(cid)
                    if exp is not None:
                        assert int(metrics[field + "_cycles"]) == exp
            logs = report["logs"]
            logs["cases"] += 1
            logs["finalWords"] += 96
            logs["continuousTRACE"] += len(traces)
            prefix = "control" if control else "main"
            logs[prefix + "WB"] += len(wbs)
            logs[prefix + "STORE"] += len(stores)
            if not control and cid.startswith("N"):
                logs["newWB"] += len(wbs)
                logs["newSTORE"] += len(stores)
            report["waves"]["count"] += 1
            report["waves"]["bytes"] += wave.stat().st_size
            report["cases"].append(dict(id=cid, old_source_control=control, final=row["final_status"],
                ordered_trace=row["trace_status"], strict=row["strict_status"], cycles=len(edges),
                ps=last_tick, wb=len(wbs), stores=len(stores), final_differences=final_diffs,
                stall=row["stall_cycles"], flush=row["flush_cycles"], branches=branches))

    def focused(cid):
        return next(v for k, v in all_edges.items() if k.startswith(cid + "_"))

    for cid, source, path in [("N12", 1, "EX"), ("N13", 1, "WBEX"), ("N14", 1, "WBID"),
            ("N15", 2, "EX"), ("N16", 2, "WBEX"), ("N17", 2, "WBID")]:
        edges, n, branches = focused(cid)
        item = branches[0]
        _, pre, _ = edges[item["cycle"] - 1]
        fresh = MASK if source == 1 else 1
        assert item["cycle"] == (5 if source == 1 else 4) + {"EX": 0, "WBEX": 1, "WBID": 2}[path]
        assert item["taken"] == (1 if source == 1 else 0)
        if path == "EX":
            assert n(pre, DUT + f"ex_match_rs{source}") == 1
        elif path == "WBEX":
            assert n(pre, DUT + f"ex_match_rs{source}") == 0 and n(pre, DUT + f"wb_match_rs{source}") == 1
        else:
            _, capture_pre, capture_post = edges[item["cycle"] - 2]
            assert n(capture_pre, DUT + "branch_id") == 1 and n(capture_pre, DUT + "funct3") == 7
            assert n(capture_pre, DUT + f"rs{source}_data") == 0
            assert n(capture_pre, DUT + "mem_reg_write") == 1
            assert n(capture_pre, DUT + "mem_rd") == source
            assert n(capture_pre, DUT + f"wb_id_rs{source}") == fresh
            assert n(capture_post, DUT + f"id_rs{source}_data") == fresh
            assert n(pre, DUT + f"ex_match_rs{source}") == n(pre, DUT + f"wb_match_rs{source}") == 0
        report["focused"].append(dict(id=cid, path=path, source=source, cycle=item["cycle"],
            ps=item["ps"], fresh_taken=(1 if source == 1 else 0), staleRF0_taken=(0 if source == 1 else 1), status="PASS"))
    edges, n, branches = focused("N18")
    _, pre, _ = edges[branches[0]["cycle"] - 1]
    assert n(pre, DUT + "ex_match_rs1") == n(pre, DUT + "wb_match_rs1") == 1
    assert n(pre, DUT + "ex_alu_result") == 0 and n(pre, DUT + "wb_write_data") == MASK
    assert branches[0]["taken"] == 0 and branches[0]["b"] == "00000001"
    report["focused"].append(dict(id="N18", newest_EX0_beats_older_WBffffffff=True, all_WB_kept=True))
    for cid in ("N19", "N20", "N21"):
        edges, n, branches = focused(cid)
        stalls = [(t, pre, post) for t, pre, post in edges if n(pre, DUT + "stall_if")]
        assert len(stalls) == 1
        t, pre, post = stalls[0]
        assert n(pre, DUT + "id_mem_to_reg") == 1
        assert n(post, DUT + "ex_mem_to_reg") == 1
        assert n(post, DUT + "pc_reg") == n(pre, DUT + "pc_reg")
        assert n(post, DUT + "if_inst") == n(pre, DUT + "if_inst")
        assert all(n(post, DUT + s) == 0 for s in ("id_reg_write", "id_mem_write", "id_mem_to_reg", "id_branch", "id_jump"))
        report["focused"].append(dict(id=cid, single_load_stall_ps=t, heldPC_IF=True, bubble_five_controls0=True))
    edges, n, branches = focused("N22")
    _, pre, _ = edges[branches[0]["cycle"] - 1]
    assert n(pre, DUT + "ex_mem_to_reg") == 1 and n(pre, DUT + "ex_rd") == 0
    assert n(pre, DUT + "ex_match_rs2") == n(pre, DUT + "wb_match_rs2") == 0
    assert n(pre, DUT + "forward_rs2") == n(pre, DUT + "stall_if") == 0
    assert branches[0]["taken"] == 1
    report["focused"].append(dict(id="N22", load_rd0_excluded=True, correct_1_ge_0_true=True, wrong_1_ge_2_false=True))
    _, _, branches = focused("N23")
    assert [b["a"] for b in branches] == ["00000002"] * 3
    assert [b["b"] for b in branches] == ["00000001", "00000002", "00000003"]
    assert [b["taken"] for b in branches] == [1, 1, 0]
    report["focused"].append(dict(id="N23", inclusive_unsigned_loop=branches, every_WB_0_1_2_3_retained=True))
    edges, n, branches = focused("N24")
    item = branches[0]
    _, pre, post = edges[item["cycle"] - 1]
    assert item["a"] == item["b"] == "00000001" and item["taken"] == 1
    assert n(pre, DUT + "if_pc") == 8 and n(post, DUT + "pc_reg") == 8
    report["focused"].append(dict(id="N24", equal_taken_plus4_refetch_once=True, target=8))
    edges, n, branches = focused("N26")
    _, pre, post = edges[branches[0]["cycle"] - 1]
    assert n(pre, DUT + "if_inst") & 127 == 111
    assert n(pre, DUT + "inst") & 127 == 3
    assert n(post, DUT + "pc_reg") == 16
    assert all(n(pre, DUT + "id_jump") == 0 and n(pre, DUT + "ex_mem_to_reg") == 0 for _, pre, _ in edges)
    report["focused"].append(dict(id="N26", wrong_path_JAL_LW_seen_then_squashed=True, no_link_or_load_sideeffects=True))
    report["waves"]["mainBGEU"] = dict(dynamicExecutions=len(main_bgeu), taken=sum(b["taken"] for b in main_bgeu),
        notTaken=sum(not b["taken"] for b in main_bgeu), actual_unsigned32_forward=True, B_target_and_sameedge_PC_flush=True,
        unchanged_ALU_SUB1_zero=True, keyXZ=0)
    report["waves"]["preservedBLTU"] = dict(dynamicExecutions=len(main_bltu), taken=sum(b["taken"] for b in main_bltu),
        notTaken=sum(not b["taken"] for b in main_bltu), original_unsigned_predicate_and_control_flow=True)
    report["waves"]["preservedBGE"] = dict(dynamicExecutions=len(main_bge), taken=sum(b["taken"] for b in main_bge),
        notTaken=sum(not b["taken"] for b in main_bge), original_signed_predicate_and_control_flow=True)
    report["waves"]["preservedBLT"] = dict(dynamicExecutions=len(main_blt), taken=sum(b["taken"] for b in main_blt),
        notTaken=sum(not b["taken"] for b in main_blt), original_signed_predicate_and_control_flow=True)
    # Re-read the prior post-run audit, rather than treating a comment's counts
    # as independent proof.  The frozen protected manifest covers this file.
    prior_path = ROOT / "work/icarus/2026-10-18-cpu-bltu/evidence-review.json"
    prior_review = read_json(prior_path)
    prior_cases = [c for c in prior_review["cases"] if not c["old_source_control"]]
    current_cases = {c["id"]: c for c in report["cases"] if not c["old_source_control"]}
    stable_fields = ("cycle", "ps", "pc", "funct3", "a", "b", "offset", "target", "taken", "after_pc", "alu_ctrl", "sub_result", "zero")
    prior_result = read_json(prior_path.parent / "result.json")
    prior_rows = {c["id"]: c for c in prior_result["cases"]}
    current_rows = {c["id"]: c for c in result["cases"]}
    prior_branch_count = 0
    matched_original_log_samples = 0
    for old in prior_cases:
        current = current_cases[old["id"]]
        assert all(current[k] == old[k] for k in ("cycles", "ps", "wb", "stores", "stall", "flush")), old["id"]
        assert [[b[k] for k in stable_fields] for b in current["branches"]] == [
            [b[k] for k in stable_fields] for b in old["branches"]], old["id"]
        old_log = Path(prior_rows[old["id"]]["log"]).read_text(encoding="utf-8")
        new_log = Path(current_rows[old["id"]]["log"]).read_text(encoding="utf-8")
        for prefix in ("TRACE", "WB", "STORE", "REG", "MEM", "METRICS"):
            old_rows = re.findall(r"^" + prefix + r"\|.*$", old_log, re.M)
            new_rows = re.findall(r"^" + prefix + r"\|.*$", new_log, re.M)
            assert old_rows == new_rows, (old["id"], prefix, "changed original per-cycle/event sequence")
            matched_original_log_samples += len(old_rows)
        prior_branch_count += len(old["branches"])
    report["preserved_prior188"] = dict(source=str(prior_path), sha256=sha(prior_path),
        cases=len(prior_cases), branchExecutions=prior_branch_count,
        identical_raw_TRACE_WB_STORE_REG_MEM_METRICS_rows=matched_original_log_samples,
        original_BLT_BGE_BLTU_edge_samples_and_counts_identical=True)
    new_cases = [c for c in plan["cases"] if c["id"].startswith("N")]
    assert all(c["id"] in plan["stall_expectations"] and c["id"] in plan["flush_expectations"] for c in new_cases)
    report["new_frozen_expectations"] = dict(cases=len(new_cases), stall_all_explicit=True, flush_all_explicit=True)
    assert len(result["cases"]) == 214 and len(result["controls"]) == 4
    assert report["waves"]["mainBGEU"]["dynamicExecutions"] == 28
    assert result["history_counts_all_equal"] and not result["historical_counts_are_frozen_expectations"]
    report["explicit_expectations"] = result["explicit_expectation_checks"]
    report["history_original188_counts_equal"] = True
    report["history_counts_are_frozen_expectations"] = False
    report["scope"] = "Finite aligned fixed-memory/RF0 cases only; no retiredPC or unified WB/STORE ordering; no full ISA, all offsets, wrap, trap or hardware proof."
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default=str(DEFAULT))
    args = parser.parse_args()
    dest = Path(args.directory).resolve()
    assert dest.is_relative_to(ROOT / "work/icarus")
    target = dest / "evidence-review.json"
    assert not target.exists(), "Refuse to replace historical audit"
    evidence = audit(dest)
    target.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: evidence[k] for k in ("hashes", "logs", "waves")}, ensure_ascii=False))
