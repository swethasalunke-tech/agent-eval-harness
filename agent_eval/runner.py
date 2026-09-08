"""EvalRunner: orchestrates running an agent function over EvalCases."""

import traceback
from typing import Any, Callable, List, Tuple

from agent_eval.core import EvalCase, EvalReport, EvalResult

ScorerFn = Callable[[Any, EvalCase], Tuple[bool, float, str]]


class EvalRunner:
    def __init__(
        self,
        cases: List[EvalCase],
        agent_fn: Callable[[Any], Any],
        scorer: ScorerFn,
    ):
        self.cases = cases
        self.agent_fn = agent_fn
        self.scorer = scorer

    def run(self) -> EvalReport:
        results: List[EvalResult] = []
        for case in self.cases:
            try:
                actual = self.agent_fn(case.input)
            except Exception as exc:  # noqa: BLE001
                tb = traceback.format_exc(limit=3)
                results.append(
                    EvalResult(
                        case_id=case.id,
                        passed=False,
                        score=0.0,
                        details=(
                            f"agent_fn raised {type(exc).__name__}: {exc}\n{tb}"
                        ),
                    )
                )
                continue

            try:
                passed, score, details = self.scorer(actual, case)
            except Exception as exc:  # noqa: BLE001
                results.append(
                    EvalResult(
                        case_id=case.id,
                        passed=False,
                        score=0.0,
                        details=f"scorer raised {type(exc).__name__}: {exc}",
                    )
                )
                continue

            results.append(
                EvalResult(
                    case_id=case.id,
                    passed=passed,
                    score=score,
                    details=details,
                )
            )

        return EvalReport(results=results)
