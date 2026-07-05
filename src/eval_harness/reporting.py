from src.eval_harness.models import EvalResult, ResultStatus

def summarize(results: list[EvalResult]) -> dict:

    total = len(results)
    passed = 0
    failed = 0
    errored = 0

    for result in results:
        if result.status == ResultStatus.PASSED:
            passed += 1
        elif result.status == ResultStatus.FAILED:
            failed += 1
        elif result.status == ResultStatus.ERROR:
            errored += 1

    return {"total": total, "passed": passed, "failed": failed, "errored": errored, "pass_rate": passed / total if total > 0 else 0.0}
