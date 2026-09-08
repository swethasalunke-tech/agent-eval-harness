# Design

## Goal

`agent-eval-harness` is a lightweight framework for scoring an AI agent's
outputs against a rubric across many test cases, so regressions can be
caught automatically instead of eyeballed.

## Day 1 scope (this commit)

Implemented and tested:

- `agent_eval/core.py` — EvalCase, EvalResult, EvalReport.
- `agent_eval/scorers.py` — exact_match_scorer, keyword_presence_scorer.
- `agent_eval/runner.py` — EvalRunner, synchronous, per-case exception isolation.

## Explicitly deferred

- LLM-as-judge scorer (needs injected client, day 2).
- Async/parallel runner.
- CLI.
- JSON/HTML report output.

## Design notes

Scorers are plain functions, not classes. EvalRunner expects a scorer with
signature (actual, case) -> (passed, score, details). Exceptions from
agent_fn or the scorer are isolated per-case.
