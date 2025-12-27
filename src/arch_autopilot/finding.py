from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    severity: str
    category: str
    resource_type: str
    resource_name: str
    file: Path
    evidence: str
    remediation: str
    confidence: float = 1.0