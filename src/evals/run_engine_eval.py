"""
run_engine_eval.py — run the correction engine against the eval cases, N times each,
and report pass RATES (not single pass/fail), because the engine is nondeterministic.

Place at: eval-harness/evals/run_engine_eval.py
Run:      python -m evals.run_engine_eval
"""

from dotenv import load_dotenv
load_dotenv()

from evals.cases import CASES, ExpectedSilence, ExpectedOutcome
from eval_harness.graders import exact_match, contains_match, normalized_match
from engine.models import CorrectionTurn, Correction, Message
from engine.run_turn import run_turn


def spans_overlap(actual: str, expected: str) -> bool:
    """Direction-safe fragment match: the engine may return a tighter or wider span than
    our expected one ('må husker' vs 'må husker at'); same error, so match if either
    contains the other."""
    a, e = actual.strip().casefold(), expected.strip().casefold()
    return a in e or e in a


def engine_system(case) -> CorrectionTurn:
    history = [Message(role=r, content=c) for (r, c) in case.context]
    history.append(Message(role="user", content=case.input))
    return run_turn(history, level=case.level)


def _ok(field_val) -> bool:
    return field_val["ok"] if isinstance(field_val, dict) else field_val


def run_correction_eval(actual: CorrectionTurn, expected: ExpectedOutcome) -> dict:
    if isinstance(expected, ExpectedSilence):
        return {"silence": len(actual.corrections) == 0}

    correction = _find_correction(actual.corrections, expected)
    if correction is None:
        return {"detected": False}

    results = {}
    if expected.severity:
        results["severity"] = {"ok": exact_match(correction.severity.value, expected.severity),
                               "got": correction.severity.value, "expected": expected.severity}
    if expected.correction_type:
        results["correction_type"] = {"ok": exact_match(correction.correction_type.value, expected.correction_type),
                                      "got": correction.correction_type.value, "expected": expected.correction_type}
    if expected.fragment:
        results["fragment"] = {"ok": spans_overlap(correction.original_fragment, expected.fragment)}
    if expected.fix:
        results["fix"] = {"ok": contains_match(correction.corrected_version, expected.fix)}
    return results


def _find_correction(corrections: list[Correction], expected) -> Correction | None:
    if not corrections:
        return None
    if expected.fragment:
        for c in corrections:
            if spans_overlap(c.original_fragment, expected.fragment):
                return c
        return None
    return corrections[0]


def run_eval(cases: list, system, runs: int = 5) -> list[dict]:
    """Run each case `runs` times. One run is a sample, not a verdict — we report rates."""
    results = []
    for case in cases:
        field_pass, n_ok, errors = {}, 0, 0
        for _ in range(runs):
            try:
                fields = run_correction_eval(system(case), case.expected)
            except Exception:
                errors += 1
                continue
            if all(_ok(v) for v in fields.values()):
                n_ok += 1
            for f, v in fields.items():
                field_pass[f] = field_pass.get(f, 0) + (1 if _ok(v) else 0)
        graded = runs - errors
        results.append({
            "input": case.input,
            "graded": graded,
            "case_rate": (n_ok / graded) if graded else 0.0,
            "field_rate": {f: c / graded for f, c in field_pass.items()} if graded else {},
            "errors": errors,
        })
    return results


def print_report(results: list[dict], runs: int) -> None:
    stable = 0
    for r in results:
        rate = r["case_rate"]
        tag = "PASS" if rate == 1.0 else ("FLAKY" if rate > 0 else "FAIL")
        stable += (rate == 1.0)
        note = f"  ({r['errors']} errors)" if r["errors"] else ""
        pct = round(rate * 100)
        print(f"{tag:5} [{pct:3d}%]  {r['input']!r}{note}")
        for field, fr in r["field_rate"].items():
            mark = "ok" if fr == 1.0 else f"{round(fr*100)}%"
            print(f"        {field:16} {mark}")
    total = len(results)
    print(f"\n{stable}/{total} cases pass on EVERY run (of {runs}).")
    print("FLAKY = the engine is nondeterministic on that case (passes some runs, fails others).")


if __name__ == "__main__":
    RUNS = 5
    print_report(run_eval(CASES, engine_system, runs=RUNS), RUNS)



