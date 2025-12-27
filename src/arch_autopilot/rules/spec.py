from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable

from arch_autopilot.model import Resource
from arch_autopilot.finding import Finding

RuleFunc = Callable[[list[Resource]], list[Finding]]

@dataclass(frozen=True)
class RuleSpec:
    """
    Metadata about a rule + the function that runs it.
    This lets us scale to enterprise features (grouping, tiers, CI gating) cleanly.
    """
    rule_id: str
    title: str
    pillar: str          # Security | Reliability | Cost | Ops | Performance
    default_enabled: bool
    func: RuleFunc