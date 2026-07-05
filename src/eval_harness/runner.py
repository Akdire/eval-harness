from src.eval_harness.models import EvalCase, EvalResult, ResultStatus
    
def run_eval(cases: list[EvalCase], system: callable, grader:callable) -> list[EvalResult]:
    case_results = []
   
    for case in cases:
        try:   
            actual_output = system(case.input)
        
        except Exception as e:
            case_results.append(EvalResult(case, str(e), ResultStatus.ERROR))
            continue

        passed = grader(actual_output, case.expected)
        status = ResultStatus.PASSED if passed else ResultStatus.FAILED
        case_results.append(EvalResult(case, actual_output, status))
    return case_results

