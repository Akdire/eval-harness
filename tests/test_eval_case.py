from eval_harness.models import EvalCase 

def test_eval_case_stores_input_and_expected():
    case = EvalCase("2 + 2", "4")
    assert case.input == "2 + 2"
    assert case.expected == "4"


def test_eval_case_to_dict():
    case = EvalCase("3 + 5", "8")
    assert case.to_dict() == {"input": "3 + 5", "expected": "8"}






