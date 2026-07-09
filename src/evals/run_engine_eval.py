from dotenv import load_dotenv
load_dotenv()

from evals.cases import CASES, ExpectedSilence, ExpectedOutcome
from eval_harness.graders import exact_match, contains_match, normalized_match
from engine.models import CorrectionTurn, Correction, Message
from engine.run_turn import run_turn

def engine_system(case) -> CorrectionTurn:
    history = [Message(role="user", content=case.input)]
    return run_turn(history, level=case.level)

def run_eval(cases: list, system) -> list[dict]:
    results = []
    for case in cases:
        try:
            actual = system(case)
            fields = run_correction_eval(actual, case.expected)
            passed = all(v["ok"] if isinstance(v, dict) else v for v in fields.values())
            results.append({"input": case.input, "passed": passed, "fields": fields})
        except Exception as e:
            results.append({"input": case.input, "error": str(e)})
    return results


def run_correction_eval(actual: CorrectionTurn, expected: ExpectedOutcome) -> dict:
    if isinstance(expected, ExpectedSilence):
        return {"silence": len(actual.corrections) == 0}

    correction = _find_correction(actual.corrections, expected)
    if correction is None:
        return {"detected": False}

    results = {}
    if expected.severity:
        results["severity"] = exact_match(correction.severity.value, expected.severity)
    if expected.correction_type:
        results["correction_type"] = {
            "ok": exact_match(correction.correction_type.value, expected.correction_type),
            "got": correction.correction_type.value,
            "expected": expected.correction_type,
    }
    if expected.fragment:
        results["fragment"] = contains_match(correction.original_fragment, expected.fragment)
    if expected.fix:
        results["fix"] = contains_match(correction.corrected_version, expected.fix)
    return results

def _find_correction(corrections: list[Correction], expected) -> Correction | None:
    if not corrections:
        return None
    if expected.fragment:
        for c in corrections:
            if contains_match(c.original_fragment, expected.fragment):
                return c
        return None
    return corrections[0]

def print_report(results: list[dict]) -> None:
    passed = 0
    for r in results:
        if "error" in r:
            print(f"ERROR  {r['input']!r}\n       {r['error']}")
            continue
        passed += r["passed"]
        print(f"{'PASS' if r['passed'] else 'FAIL'}  {r['input']!r}")
        for field, val in r["fields"].items():
            if isinstance(val, dict):
                status = "ok" if val["ok"] else "MISS"
                print(f" {field:16} {status}  (got: {val['got']}  expected: {val['expected']})")
            else:
                print(f" {field:16} {'ok' if val else 'MISS'}")

    print(f"\n{passed}/{len(results)} cases passed")

if __name__ == "__main__":
    print_report(run_eval(CASES, engine_system))