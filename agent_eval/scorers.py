"""Scorer implementations."""

from typing import Iterable, Optional, Tuple


def exact_match_scorer(actual, expected) -> Tuple[bool, float, str]:
    passed = actual == expected
    score = 1.0 if passed else 0.0
    if passed:
        details = f"exact match: {actual!r} == {expected!r}"
    else:
        details = f"mismatch: actual={actual!r} expected={expected!r}"
    return passed, score, details


def _tokenize(text: str):
    import re

    return set(re.findall(r"\b\w+\b", text.lower()))


def _contains_keyword(actual_lower: str, actual_tokens: set, keyword: str) -> bool:
    keyword_lower = keyword.lower()
    if keyword_lower in actual_lower:
        return True
    if " " not in keyword_lower and keyword_lower in actual_tokens:
        return True
    return False


def keyword_presence_scorer(
    actual: str,
    required_keywords: Optional[Iterable[str]] = None,
    forbidden_keywords: Optional[Iterable[str]] = None,
) -> Tuple[bool, float, str]:
    required = list(required_keywords) if required_keywords else []
    forbidden = list(forbidden_keywords) if forbidden_keywords else []

    actual_str = actual if isinstance(actual, str) else str(actual)
    actual_lower = actual_str.lower()
    actual_tokens = _tokenize(actual_str)

    if not required and not forbidden:
        return True, 1.0, "no keywords specified; trivially passed"

    missing_required = [
        kw for kw in required if not _contains_keyword(actual_lower, actual_tokens, kw)
    ]
    present_forbidden = [
        kw for kw in forbidden if _contains_keyword(actual_lower, actual_tokens, kw)
    ]

    total_checks = len(required) + len(forbidden)
    satisfied_checks = (len(required) - len(missing_required)) + (
        len(forbidden) - len(present_forbidden)
    )
    score = satisfied_checks / total_checks if total_checks else 1.0

    passed = not missing_required and not present_forbidden

    detail_parts = []
    if required:
        detail_parts.append(
            f"required missing={missing_required or 'none'}"
        )
    if forbidden:
        detail_parts.append(
            f"forbidden present={present_forbidden or 'none'}"
        )
    details = "; ".join(detail_parts) if detail_parts else "ok"

    return passed, score, details
