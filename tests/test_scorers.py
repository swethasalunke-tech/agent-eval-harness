"""Tests for agent_eval.scorers."""

from agent_eval.scorers import exact_match_scorer, keyword_presence_scorer


def test_exact_match_true():
    passed, score, details = exact_match_scorer("hello world", "hello world")
    assert passed is True
    assert score == 1.0
    assert "hello world" in details


def test_exact_match_false():
    passed, score, details = exact_match_scorer("hello world", "goodbye world")
    assert passed is False
    assert score == 0.0
    assert "mismatch" in details


def test_exact_match_non_string_values():
    passed, score, _ = exact_match_scorer(42, 42)
    assert passed is True
    assert score == 1.0

    passed, score, _ = exact_match_scorer([1, 2, 3], [1, 2, 4])
    assert passed is False
    assert score == 0.0


def test_keyword_presence_required_only_all_present():
    passed, score, details = keyword_presence_scorer(
        "The quick brown fox jumps over the lazy dog",
        required_keywords=["quick", "fox", "dog"],
    )
    assert passed is True
    assert score == 1.0


def test_keyword_presence_required_only_some_missing():
    passed, score, details = keyword_presence_scorer(
        "The quick brown fox jumps",
        required_keywords=["quick", "fox", "elephant"],
    )
    assert passed is False
    assert score == 2 / 3
    assert "elephant" in details


def test_keyword_presence_forbidden_only_none_present():
    passed, score, details = keyword_presence_scorer(
        "This response is safe and helpful",
        forbidden_keywords=["error", "crash"],
    )
    assert passed is True
    assert score == 1.0


def test_keyword_presence_forbidden_only_one_present():
    passed, score, details = keyword_presence_scorer(
        "Sorry, an error occurred while processing",
        forbidden_keywords=["error", "crash"],
    )
    assert passed is False
    assert score == 0.5
    assert "error" in details


def test_keyword_presence_both_all_pass():
    passed, score, details = keyword_presence_scorer(
        "The system completed the task successfully",
        required_keywords=["completed", "task"],
        forbidden_keywords=["error", "failed"],
    )
    assert passed is True
    assert score == 1.0


def test_keyword_presence_both_mixed_result():
    passed, score, details = keyword_presence_scorer(
        "The task failed unexpectedly",
        required_keywords=["completed", "task"],
        forbidden_keywords=["error", "failed"],
    )
    assert passed is False
    assert score == 0.5
    assert "completed" in details
    assert "failed" in details


def test_keyword_presence_case_insensitive_required():
    passed, score, _ = keyword_presence_scorer(
        "THE QUICK BROWN FOX",
        required_keywords=["quick", "FOX", "Brown"],
    )
    assert passed is True
    assert score == 1.0


def test_keyword_presence_case_insensitive_forbidden():
    passed, score, _ = keyword_presence_scorer(
        "This contains an ERROR in it",
        forbidden_keywords=["error"],
    )
    assert passed is False
    assert score == 0.0


def test_keyword_presence_empty_lists_trivially_passes():
    passed, score, details = keyword_presence_scorer(
        "anything at all",
        required_keywords=[],
        forbidden_keywords=[],
    )
    assert passed is True
    assert score == 1.0
    assert "no keywords" in details


def test_keyword_presence_none_args_trivially_passes():
    passed, score, details = keyword_presence_scorer("anything at all")
    assert passed is True
    assert score == 1.0
