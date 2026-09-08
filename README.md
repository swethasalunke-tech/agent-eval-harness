# agent-eval-harness

A lightweight framework for scoring an AI agent's outputs against a rubric
across many test cases, so regressions can be caught automatically instead
of eyeballed.

## Status: Day 1

Implemented and tested (see `DESIGN.md`):

- `EvalCase`, `EvalResult`, `EvalReport` (`agent_eval/core.py`)
- `exact_match_scorer`, `keyword_presence_scorer` (`agent_eval/scorers.py`)
- `EvalRunner`, synchronous, per-case exception isolation (`agent_eval/runner.py`)

Not built yet: LLM-as-judge scorer, async/parallel runner, CLI, JSON/HTML
report output. See `BUILD-SCHEDULE.md`.

## Install

```bash
pip install -r requirements.txt
```

## Run the tests

```bash
python3 -m pytest tests/ -v
```

## Usage

```python
from agent_eval.core import EvalCase
from agent_eval.runner import EvalRunner
from agent_eval.scorers import exact_match_scorer, keyword_presence_scorer

def agent_fn(question: str) -> str:
    if question == "capital of france":
        return "The capital of France is Paris."
    return "I don't know."

cases = [
    EvalCase(
        id="capital-1",
        input="capital of france",
        criteria={"required_keywords": ["Paris"], "forbidden_keywords": ["I don't know"]},
    ),
]

def keyword_scorer(actual, case):
    return keyword_presence_scorer(
        actual,
        case.criteria.get("required_keywords"),
        case.criteria.get("forbidden_keywords"),
    )

runner = EvalRunner(cases=cases, agent_fn=agent_fn, scorer=keyword_scorer)
report = runner.run()
print(report.summary())
```

## Project layout

```
agent_eval/
  core.py       EvalCase, EvalResult, EvalReport
  scorers.py    exact_match_scorer, keyword_presence_scorer
  runner.py     EvalRunner
tests/
  test_scorers.py
  test_runner.py
DESIGN.md
BUILD-SCHEDULE.md
```
