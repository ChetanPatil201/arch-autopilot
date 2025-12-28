from __future__ import annotations

from arch_autopilot.finding import Finding
from arch_autopilot.model import Resource


def az008_storage_min_tls(resources: list[Resource]) -> list[Finding]:
    """
    AZ008: Storage account must enforce TLS 1.2+.
    Terraform: azurerm_storage_account.min_tls_version should be "TLS1_2" (or higher if supported).
    """
    findings: list[Finding] = []

    for r in resources:
        if r.rtype != "azurerm_storage_account":
            continue

        tls = r.values.get("min_tls_version")
        tls_str = str(tls).strip().upper() if tls is not None else ""

        # Accept TLS1_2 (and if provider ever supports TLS1_3, that’s fine too)
        if tls_str in {"TLS1_2", "TLS1_3"}:
            continue

        findings.append(
            Finding(
                rule_id="AZ008",
                title="Storage account does not enforce TLS 1.2+",
                severity="high",
                category="Security",
                resource_type=r.rtype,
                resource_name=r.name,
                file=r.file,
                evidence="min_tls_version is missing or not set to TLS1_2 (or higher).",
                remediation='Set min_tls_version = "TLS1_2" on the azurerm_storage_account.',
                confidence=0.85,
            )
        )

    return findings
