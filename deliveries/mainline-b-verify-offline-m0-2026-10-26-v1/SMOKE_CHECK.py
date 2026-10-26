"""A-provided minimal fixture/entry check; NOT B's deliverable or full suite."""
from pathlib import Path
import argparse
import json
import sys
import time

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'frozen'))
import offline_api as api
from VERIFY_PACKAGE import verify


def smoke(output, include_real):
    api.runtime_guard()
    receipt = verify()
    output = Path(output).resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError('output must be outside immutable package')
    output.mkdir(exist_ok=False, parents=True)
    plan = json.loads((ROOT / 'inputs/SEED_PLAN.json').read_text(encoding='utf-8-sig'))
    rows = []
    for case in plan['cases']:
        deadline = time.monotonic() + 15
        try:
            got = api.compare(api.records(ROOT, case['expected'], deadline=deadline),
                              api.records(ROOT, case['actual'], deadline=deadline),
                              allow_empty=case['allow_empty'], deadline=deadline)
            status = got['status']
            first = got['differences'][0]['ordinal'] if got['differences'] else None
        except api.InputError as exc:
            got, status, first = dict(message=str(exc)), exc.status, None
        passed = status == case['expected_status'] and first == case['first_mismatch_ordinal']
        rows.append(dict(id=case['id'], expected=case['expected_status'], actual=status,
                         expected_first=case['first_mismatch_ordinal'], actual_first=first,
                         passed=passed, detail=got))
    if include_real:
        real = json.loads((ROOT / 'inputs/REAL_CASES.json').read_text(encoding='utf-8-sig'))['cases'][0]
        deadline = time.monotonic() + 180
        start = time.monotonic()
        got = api.compare(api.records(ROOT, real['input'], deadline=deadline),
                          api.records(ROOT, real['input'], deadline=deadline), deadline=deadline)
        rows.append(dict(id='A_REAL_RECORD_REPLAY', actual=got['status'],
                         passed=got['status'] == 'MATCH' and got['checked'] == real['records'],
                         detail=got, host_seconds=round(time.monotonic() - start, 6),
                         same_accepted_observation_read_twice=True, new_DUT=False))
    result = dict(status='A_BOOTSTRAP_PASS' if all(x['passed'] for x in rows) else 'A_BOOTSTRAP_FAIL',
                  package=receipt, rows=rows, B_suite_executed=False, new_DUT=0)
    with (output / 'bootstrap-result.json').open('x', encoding='utf-8') as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        out.write('\n')
    return result


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    parser.add_argument('--include-real', action='store_true')
    options = parser.parse_args()
    try:
        result = smoke(options.out, options.include_real)
        print(json.dumps(dict(status=result['status'], cases=len(result['rows']),
                              B_suite_executed=False, new_DUT=0), ensure_ascii=False))
        raise SystemExit(0 if result['status'] == 'A_BOOTSTRAP_PASS' else 1)
    except Exception as exc:
        print(json.dumps(dict(status='A_BOOTSTRAP_ERROR', error=str(exc)), ensure_ascii=False))
        raise SystemExit(1)
