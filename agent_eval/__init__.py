"""agent_eval: a lightweight framework for scoring AI agent outputs against a rubric."""

from agent_eval.core import EvalCase, EvalResult, EvalReport
from agent_eval.runner import EvalRunner
from agent_eval.scorers import exact_match_scorer, keyword_presence_scorer

__all__ = [
    "EvalCase",
    "EvalResult",
    "EvalReport",
    "EvalRunner",
    "exact_match_scorer",
    "keyword_presence_scorer",
]
