from __future__ import annotations

from arch_autopilot.rules.spec import RuleSpec


def get_enabled_rules() -> list[RuleSpec]:
    from arch_autopilot.rules.az001_storage_https_only import az001_storage_https_only
    from arch_autopilot.rules.az002_storage_public_blob_access import az002_storage_public_blob_access
    from arch_autopilot.rules.az003_keyvault_purge_protection import az003_keyvault_purge_protection

    rules = [
        RuleSpec(
            rule_id="AZ001",
            title="Storage account must enforce HTTPS-only traffic",
            pillar="Security",
            default_enabled=True,
            func=az001_storage_https_only,
        ),
        RuleSpec(
            rule_id="AZ002",
            title="Storage account must disable public blob access",
            pillar="Security",
            default_enabled=True,
            func=az002_storage_public_blob_access,
        ),
        RuleSpec(
            rule_id="AZ003",
            title="Key Vault must enable purge protection",
            pillar="Security",
            default_enabled=True,
            func=az003_keyvault_purge_protection,
        ),
    ]

    return [r for r in rules if r.default_enabled]
