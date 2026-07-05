from src.eval_harness.graders import normalized_match


def test_normalized_match_returns_true_with_identical_strings():
    assert normalized_match("4", "4")

def test_normalized_match_returns_false_with_different_strings():
    assert not normalized_match("4", "3")

def test_normalized_match_returns_true_with_space_strings():
    assert normalized_match(" 4", "4")

def test_normalized_match_returns_true_with_case_strings():
    assert normalized_match("Yes", "yes")

def test_normalized_match_returns_true_with_empty_strings():
    assert normalized_match("", "")


    
