from __future__ import annotations

from arch_autopilot.finding import Finding
from arch_autopilot.model import Resource

def az003_keyvault_purge_protection(resources: list[Resource]) -> list[Finding]:
    """
    AZ003: Key Vault should enable purge protection.
    Terraform: azurerm_key_vault.purge_protection_enabled must be true.
    """
    findings: list[Finding] = []
    for r in resources:
        if r.rtype != "azurerm_key_vault":
            continue

        val = r.values.get("purge_protection_enabled")
        if val is True:
            continue

        findings.append(
            Finding(
                rule_id="AZ003",
                title="Key Vault purge protection is not enabled",
                severity="high",
                category="Security",
                resource_type=r.rtype,
                resource_name=r.name,
                file=r.file,
                evidence="purge_protection_enabled is missing or not set to true.",
                remediation="Set purge_protection_enabled = true on the azurerm_key_vault.",
                confidence=0.9,
            )
        )

    return findings