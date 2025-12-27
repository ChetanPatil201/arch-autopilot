from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from arch_autopilot.finding import Finding


def write_findings_json(findings: list[Finding], out_path: Path) -> None:
    payload: list[dict[str, Any]] = []
    for f in findings:
        payload.append(
            {
                "rule_id": f.rule_id,
                "title": f.title,
                "severity": f.severity,
                "category": f.category,
                "resource_type": f.resource_type,
                "resource_name": f.resource_name,
                "file": str(f.file),
                "evidence": f.evidence,
                "remediation": f.remediation,
                "confidence": f.confidence,
            }
        )

    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
