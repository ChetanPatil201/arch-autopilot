from __future__ import annotations

from arch_autopilot.finding import Finding
from arch_autopilot.model import Resource


def az007_storage_encryption_at_rest(resources: list[Resource]) -> list[Finding]:
    """
    AZ007: Storage account should enforce encryption at rest.
    Best-effort check on azurerm_storage_account.
    """
    findings: list[Finding] = []

    for r in resources:
        if r.rtype != "azurerm_storage_account":
            continue

        enc = r.values.get("encryption")
        if isinstance(enc, dict):
            services = enc.get("services", {})
            blob = services.get("blob", {})
            enabled = blob.get("enabled")
            if enabled is True:
                continue

        findings.append(
            Finding(
                rule_id="AZ007",
                title="Storage account encryption at rest is not explicitly enabled",
                severity="high",
                category="Security",
                resource_type=r.rtype,
                resource_name=r.name,
                file=r.file,
                evidence="Encryption settings for storage account are missing or incomplete.",
                remediation="Ensure encryption.services.blob.enabled = true on azurerm_storage_account.",
                confidence=0.8,
            )
        )

    return findings
