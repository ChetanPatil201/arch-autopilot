from __future__ import annotations

from arch_autopilot.finding import Finding
from arch_autopilot.model import Resource


def az009_storage_network_default_deny(resources: list[Resource]) -> list[Finding]:
    """
    AZ009: Storage account should use network_rules with default_action = "Deny".
    Best-effort offline check: azurerm_storage_account.network_rules.default_action == "Deny".
    """
    findings: list[Finding] = []

    for r in resources:
        if r.rtype != "azurerm_storage_account":
            continue

        network_rules = r.values.get("network_rules")

        # network_rules can be dict (sometimes list depending on parser/provider patterns)
        nr = None
        if isinstance(network_rules, dict):
            nr = network_rules
        elif isinstance(network_rules, list) and network_rules and isinstance(network_rules[0], dict):
            nr = network_rules[0]

        default_action = str((nr or {}).get("default_action", "")).strip().lower()

        if default_action == "deny":
            continue

        findings.append(
            Finding(
                rule_id="AZ009",
                title="Storage account network rules do not default to Deny",
                severity="high",
                category="Security",
                resource_type=r.rtype,
                resource_name=r.name,
                file=r.file,
                evidence="network_rules.default_action is missing or not set to Deny.",
                remediation='Add network_rules { default_action = "Deny" } and explicitly allow trusted networks.',
                confidence=0.8,
            )
        )

    return findings
