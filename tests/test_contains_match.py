from eval_harness.graders import contains_match


def test_contains_match_returns_true_expected_inside_output():
    assert contains_match("the answer is 42", "42")

def test_contains_match_returns_false_output_inside_expected():
    assert not contains_match("42", "the answer is 42")

def test_contains_match_returns_true_expected_inside_output_with_empty_string():
    assert not contains_match("anything", "")

def test_contains_match_returns_false_with_expected_and_output_different_string():
    assert not contains_match("hello world", "xyz")

def test_contains_match_returns_true_output_and_expected_contain_same_string():
    assert contains_match("42", "42")




