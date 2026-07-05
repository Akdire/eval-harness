from src.eval_harness.runner import run_eval
from src.eval_harness.models import EvalCase, ResultStatus
from src.eval_harness.graders import exact_match

def fake_system(text):
    return "4"

def exploding_system(text):    
    raise ValueError("boom")

def test_run_eval_passed_path_and_size():
    list_eval_case = [EvalCase("2 + 2", "4")]
    results = run_eval(list_eval_case, fake_system, exact_match)
    assert len(results) == 1
    assert results[0].status == ResultStatus.PASSED


def test_run_eval_failed_path_and_size():
    list_eval_case = [EvalCase("2 + 2", "3")]
    results = run_eval(list_eval_case, fake_system, exact_match)
    assert len(results) == 1
    assert results[0].status == ResultStatus.FAILED


def test_run_eval_error_path_and_size():
    list_eval_case = [EvalCase("2 + 2", "no")]
    results = run_eval(list_eval_case, exploding_system, exact_match)
    assert len(results) == 1
    assert results[0].status == ResultStatus.ERROR



