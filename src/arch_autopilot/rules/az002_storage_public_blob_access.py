from __future__ import annotations

from arch_autopilot.finding import Finding
from arch_autopilot.model import Resource


def az002_storage_public_blob_access(resources: list[Resource]) -> list[Finding]:
    """
    AZ002: Storage account should disable public blob access.
    Terraform: azurerm_storage_account.allow_blob_public_access must be false.
    """
    findings: list[Finding] = []

    for r in resources:
        if r.rtype != "azurerm_storage_account":
            continue

        val = r.values.get("allow_blob_public_access")

        # Secure value is explicitly False. Missing is treated as risky for v1.
        if val is False:
            continue

        findings.append(
            Finding(
                rule_id="AZ002",
                title="Storage account allows public blob access",
                severity="high",
                category="Security",
                resource_type=r.rtype,
                resource_name=r.name,
                file=r.file,
                evidence="allow_blob_public_access is missing or not set to false.",
                remediation="Set allow_blob_public_access = false on the azurerm_storage_account.",
                confidence=0.9,
            )
        )

    return findings
