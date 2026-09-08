# Build schedule

## Day 1 (this commit) — core data model, sync runner, two real scorers

- `agent_eval/core.py`: `EvalCase`, `EvalResult`, `EvalReport`.
- `agent_eval/scorers.py`: `exact_match_scorer`, `keyword_presence_scorer`.
- `agent_eval/runner.py`: synchronous `EvalRunner`, per-case exception isolation.
- `tests/test_scorers.py`, `tests/test_runner.py`: real pytest coverage,
  run locally with `python3 -m pytest tests/ -v` (see README for output).
- `DESIGN.md`, `BUILD-SCHEDULE.md`, `README.md`.

## Day 2 (planned, not started) — LLM-as-judge scorer

- Add `agent_eval/llm_judge.py` with dependency-injected LLM client,
  FakeLLMClient for tests, llm_judge_scorer function.

## Day 3 (planned, not started) — CLI + report output

- `agent_eval/cli.py` command-line entry point, JSON/HTML report output.

## Explicitly out of scope until it's actually built

- Async/parallel case execution.
- Any scorer that calls a real hosted API during the test suite.
