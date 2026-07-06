from eval_harness.models import EvalCase, ResultStatus, EvalResult
from eval_harness.reporting import summarize


def test_summarize():


    eval_case = EvalCase("2 + 3", "5")
    eval_case_2 = EvalCase("2 + 4", "5")
    eval_case_3 = EvalCase("2 + 4", "6")

    eval_result_case = [EvalResult(eval_case, "5", ResultStatus.PASSED), EvalResult(eval_case_2, "5", ResultStatus.FAILED), EvalResult(eval_case_3, "5", ResultStatus.ERROR), EvalResult(eval_case, "5", ResultStatus.PASSED)]
   
 
    summarize_case = summarize(eval_result_case)
    
    assert summarize_case["total"] == 4
    assert summarize_case["passed"] == 2
    assert summarize_case["failed"] == 1
    assert summarize_case["errored"] == 1
    assert summarize_case["pass_rate"] == 0.5
   

def test_summarize_empty_list():
    summarize_case = summarize([])
    assert summarize_case["total"] == 0
    assert summarize_case["pass_rate"] == 0.0
    




