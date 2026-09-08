"""Core data structures for agent-eval-harness."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EvalCase:
    id: str
    input: Any
    expected: Any = None
    criteria: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvalResult:
    case_id: str
    passed: bool
    score: float
    details: str = ""


@dataclass
class EvalReport:
    results: List[EvalResult] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        if not self.results:
            return 0.0
        passed = sum(1 for r in self.results if r.passed)
        return passed / len(self.results)

    @property
    def average_score(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.score for r in self.results) / len(self.results)

    def summary(self) -> str:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        lines = [
            f"EvalReport: {passed}/{total} passed "
            f"({self.pass_rate * 100:.1f}%), "
            f"avg score {self.average_score:.3f}"
        ]
        for r in self.results:
            status = "PASS" if r.passed else "FAIL"
            lines.append(
                f"  [{status}] {r.case_id} score={r.score:.3f} {r.details}"
            )
        return "\n".join(lines)
