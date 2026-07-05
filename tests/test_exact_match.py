from eval_harness.graders import exact_match

def test_exact_match_returns_true_for_identical_strings():
    assert exact_match("10", "10")

def test_exact_match_returns_false_for_different_strings():
    assert not exact_match("2", "1") 

def test_exact_match_is_whitespace_sensitive():
    assert not exact_match("a ", "a") 

def test_exact_match_is_case_sensitive():
    assert not exact_match("Yes", "yes")

def test_exact_match_returns_true_for_two_empty_strings():
    assert exact_match("", "") 







