from __future__ import annotations

from arch_autopilot.finding import Finding
from arch_autopilot.model import Resource

def az004_keyvault_soft_delete_retention(resources: list[Resource]) -> list[Finding]:
    """
    AZ004: Key Vault should have soft delete enabled and an adequate retention period.
    Terraform: azurerm_key_vault.soft_delete_retention_days should be set (commonly >= 7).
    """
    findings: list[Finding] = []

    for r in resources:
        if r.rtype != "azurerm_key_vault":
            continue

        days = r.values.get("soft_delete_retention_days")

        # v1: treat missing or too-low retention as risky
        try:
            days_int = int(days) if days is not None else None
        except Exception:
            days_int = None

        if days_int is not None and days_int >= 7:
            continue

        findings.append(
            Finding(
                rule_id="AZ004",
                title="Key Vault soft delete retention is missing or too low",
                severity="high",
                category="Security",
                resource_type=r.rtype,
                resource_name=r.name,
                file=r.file,
                evidence="soft_delete_retention_days is missing or < 7 days.",
                remediation="Set soft_delete_retention_days to at least 7 (or your policy) on azurerm_key_vault.",
                confidence=0.85,
            )
        )

    return findings


