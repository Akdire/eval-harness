from eval_harness.models import EvalCase, EvalResult, ResultStatus

def test_eval_result():
    case0 = EvalCase("6 + 4", "10")
    case2 = ResultStatus("passed")
    case1 = EvalResult(case0, "det riktig svar er 10", case2)
    assert case0.input == "6 + 4"
    assert case0.expected == "10"
    assert case1.actual_output == "det riktig svar er 10"
    assert case1.status == case2


def test_eval_result_to_dict_status_passed():
    case0 = EvalCase("6 + 4", "10")
    case1 = EvalResult(case0, "det riktig svar er 10", ResultStatus.PASSED)
    assert case1.to_dict() == {"case": {"input": "6 + 4", "expected": "10"}, "actual_output": "det riktig svar er 10", "status":  "passed"}

def test_eval_result_to_dict_status_failed():
    case0 = EvalCase("6 + 4", "10")
    case1 = EvalResult(case0, "det riktig svar er 11", ResultStatus.FAILED)
    assert case1.to_dict() == {"case": {"input": "6 + 4", "expected": "10"}, "actual_output": "det riktig svar er 11", "status":  "failed"}
    assert case1.to_dict() == {"case": {"input": "6 + 4", "expected": "10"}, "actual_output": "det riktig svar er 11", "status":  "failed"}

def test_eval_result_to_dict_status_error():
    case0 = EvalCase("6 + 4", "10")
    case1 = EvalResult(case0, "det riktig svar er 10", ResultStatus.ERROR)
    assert case1.to_dict() == {"case": {"input": "6 + 4", "expected": "10"}, "actual_output": "det riktig svar er 10", "status":  "error"}
    assert case1.to_dict() == {"case": {"input": "6 + 4", "expected": "10"}, "actual_output": "det riktig svar er 10", "status":  "error"}


