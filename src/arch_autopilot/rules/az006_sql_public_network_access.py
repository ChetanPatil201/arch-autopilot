from __future__ import annotations

from arch_autopilot.finding import Finding
from arch_autopilot.model import Resource


def az006_sql_public_network_access(resources: list[Resource]) -> list[Finding]:
    """
    AZ006: Azure SQL should not be publicly accessible.
    Best-effort offline check:
      - azurerm_mssql_server.public_network_access_enabled should be false
      - (or) azurerm_sql_server.public_network_access_enabled should be false
    """
    findings: list[Finding] = []

    for r in resources:
        if r.rtype not in {"azurerm_mssql_server", "azurerm_sql_server"}:
            continue

        val = r.values.get("public_network_access_enabled")

        # Secure is explicitly False. Missing treated as risky for v1.
        if val is False:
            continue

        findings.append(
            Finding(
                rule_id="AZ006",
                title="Azure SQL server allows public network access",
                severity="high",
                category="Security",
                resource_type=r.rtype,
                resource_name=r.name,
                file=r.file,
                evidence="public_network_access_enabled is missing or not set to false.",
                remediation="Set public_network_access_enabled = false and use private endpoints/VNet integration.",
                confidence=0.85,
            )
        )

    return findings
