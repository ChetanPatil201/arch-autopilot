from __future__ import annotations

from arch_autopilot.finding import Finding
from arch_autopilot.model import Resource


def az001_storage_https_only(resources: list[Resource]) -> list[Finding]:
    findings: list[Finding] = []

    for r in resources:
        if r.rtype != "azurerm_storage_account":
            continue

        val = r.values.get("enable_https_traffic_only")
        if val is True:
            continue

        findings.append(
            Finding(
                rule_id="AZ001",
                title="Storage account does not enforce HTTPS-only traffic",
                severity="high",
                category="Security",
                resource_type=r.rtype,
                resource_name=r.name,
                file=r.file,
                evidence="enable_https_traffic_only is missing or not set to true.",
                remediation="Set enable_https_traffic_only = true on the azurerm_storage_account.",
                confidence=0.95,
            )
        )

    return findings
