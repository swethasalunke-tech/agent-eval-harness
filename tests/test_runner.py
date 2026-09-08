"""Tests for agent_eval.runner.EvalRunner."""

import pytest

from agent_eval.core import EvalCase
from agent_eval.runner import EvalRunner
from agent_eval.scorers import exact_match_scorer, keyword_presence_scorer


def exact_match_case_scorer(actual, case):
    return exact_match_scorer(actual, case.expected)


def keyword_case_scorer(actual, case):
    return keyword_presence_scorer(
        actual,
        case.criteria.get("required_keywords"),
        case.criteria.get("forbidden_keywords"),
    )


def make_cases():
    return [
        EvalCase(id="case-1", input="hello", expected="HELLO-hello"),
        EvalCase(id="case-2", input="world", expected="WORLD-world"),
        EvalCase(id="case-3", input="foo", expected="FOO-foo"),
    ]


def test_runner_agent_always_passes():
    def agent_fn(x):
        return f"{x.upper()}-{x}"

    cases = make_cases()
    runner = EvalRunner(cases, agent_fn, exact_match_case_scorer)
    report = runner.run()

    assert len(report.results) == 3
    assert all(r.passed for r in report.results)
    assert report.pass_rate == 1.0
    assert report.average_score == 1.0


def test_runner_agent_always_fails():
    def agent_fn(x):
        return "definitely wrong output"

    cases = make_cases()
    runner = EvalRunner(cases, agent_fn, exact_match_case_scorer)
    report = runner.run()

    assert len(report.results) == 3
    assert all(not r.passed for r in report.results)
    assert report.pass_rate == 0.0
    assert report.average_score == 0.0


def test_runner_catches_exception_on_specific_case():
    def agent_fn(x):
        if x == "world":
            raise ValueError("simulated failure for 'world'")
        return f"{x.upper()}-{x}"

    cases = make_cases()
    runner = EvalRunner(cases, agent_fn, exact_match_case_scorer)

    report = runner.run()

    assert len(report.results) == 3

    results_by_id = {r.case_id: r for r in report.results}

    assert results_by_id["case-1"].passed is True
    assert results_by_id["case-3"].passed is True

    failed = results_by_id["case-2"]
    assert failed.passed is False
    assert failed.score == 0.0
    assert "ValueError" in failed.details
    assert "simulated failure for 'world'" in failed.details


def test_runner_scorer_exception_is_also_isolated():
    def agent_fn(x):
        return x

    def broken_scorer(actual, case):
        raise RuntimeError("scorer is broken")

    cases = [EvalCase(id="only-case", input="x", expected="x")]
    runner = EvalRunner(cases, agent_fn, broken_scorer)

    report = runner.run()

    assert len(report.results) == 1
    assert report.results[0].passed is False
    assert "RuntimeError" in report.results[0].details


def test_pass_rate_calculation_mixed_results():
    def agent_fn(x):
        mapping = {"hello": "HELLO-hello", "world": "WRONG", "foo": "FOO-foo"}
        return mapping[x]

    cases = make_cases()
    runner = EvalRunner(cases, agent_fn, exact_match_case_scorer)
    report = runner.run()

    assert len(report.results) == 3
    passed_count = sum(1 for r in report.results if r.passed)
    assert passed_count == 2
    assert report.pass_rate == pytest.approx(2 / 3)


def test_pass_rate_empty_report_is_zero_not_error():
    runner = EvalRunner([], lambda x: x, exact_match_case_scorer)
    report = runner.run()
    assert report.results == []
    assert report.pass_rate == 0.0


def test_runner_with_keyword_presence_scorer():
    def agent_fn(x):
        return f"The result for {x} completed successfully with no errors."

    cases = [
        EvalCase(
            id="kw-1",
            input="task-a",
            criteria={
                "required_keywords": ["completed", "successfully"],
                "forbidden_keywords": ["error"],
            },
        ),
    ]
    runner = EvalRunner(cases, agent_fn, keyword_case_scorer)
    report = runner.run()

    assert len(report.results) == 1
    assert report.results[0].passed is False
