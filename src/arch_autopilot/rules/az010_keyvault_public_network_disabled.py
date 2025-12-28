from __future__ import annotations

from arch_autopilot.finding import Finding
from arch_autopilot.model import Resource


def az010_keyvault_public_network_disabled(resources: list[Resource]) -> list[Finding]:
    """
    AZ010: Key Vault should disable public network access.
    Best-effort offline check:
      - public_network_access_enabled == false
      OR
      - public_network_access == "Disabled"
    """
    findings: list[Finding] = []

    for r in resources:
        if r.rtype != "azurerm_key_vault":
            continue

        pnae = r.values.get("public_network_access_enabled")
        pna = r.values.get("public_network_access")

        ok = (pnae is False) or (str(pna).strip().lower() == "disabled")
        if ok:
            continue

        findings.append(
            Finding(
                rule_id="AZ010",
                title="Key Vault allows public network access",
                severity="high",
                category="Security",
                resource_type=r.rtype,
                resource_name=r.name,
                file=r.file,
                evidence="Public network access is not explicitly disabled.",
                remediation="Disable public access and use Private Endpoint/VNet integration for Key Vault.",
                confidence=0.8,
            )
        )

    return findings