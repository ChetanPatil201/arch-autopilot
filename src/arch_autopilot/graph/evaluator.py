from __future__ import annotations

from typing import Any


class AIEvaluationResult:
    """
    Represents whether an AI step behaved correctly.

    This is NOT about quality of writing.
    This is about correctness, safety, and trust.
    """

    def __init__(self, passed: bool, reason: str | None = None) -> None:
        self.passed = passed
        self.reason = reason

    def __bool__(self) -> bool:
        return self.passed


class FindingsEvaluator:
    """
    Evaluates whether an AI-modified findings list
    still respects the original findings set.

    This prevents hallucinations and silent data corruption.
    """

    def evaluate(
        self,
        original: list[dict[str, Any]],
        modified: list[dict[str, Any]],
    ) -> AIEvaluationResult:
        """
        Rules:
        1. No findings added
        2. No findings removed
        3. Identity of each finding must remain the same
        """

        def key(f: dict[str, Any]) -> tuple:
            return (
                f.get("rule_id"),
                f.get("resource_type"),
                f.get("resource_name"),
                f.get("file"),
            )

        original_keys = sorted(key(f) for f in original)
        modified_keys = sorted(key(f) for f in modified)

        if original_keys != modified_keys:
            return AIEvaluationResult(
                passed=False,
                reason="AI modified the findings set (added/removed/changed findings).",
            )

        return AIEvaluationResult(passed=True)
