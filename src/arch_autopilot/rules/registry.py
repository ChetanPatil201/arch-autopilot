from __future__ import annotations

from arch_autopilot.rules.spec import RuleSpec


def get_enabled_rules() -> list[RuleSpec]:
    from arch_autopilot.rules.az001_storage_https_only import az001_storage_https_only
    from arch_autopilot.rules.az002_storage_public_blob_access import az002_storage_public_blob_access
    from arch_autopilot.rules.az003_keyvault_purge_protection import az003_keyvault_purge_protection
    from arch_autopilot.rules.az004_keyvault_soft_delete_retention import az004_keyvault_soft_delete_retention
    from arch_autopilot.rules.az005_nsg_open_ssh_rdp import az005_nsg_open_ssh_rdp
    from arch_autopilot.rules.az006_sql_public_network_access import az006_sql_public_network_access
    from arch_autopilot.rules.az007_storage_encryption_at_rest import az007_storage_encryption_at_rest
    from arch_autopilot.rules.az008_storage_min_tls import az008_storage_min_tls
    from arch_autopilot.rules.az009_storage_network_default_deny import az009_storage_network_default_deny
    from arch_autopilot.rules.az010_keyvault_public_network_disabled import az010_keyvault_public_network_disabled


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
        RuleSpec(
            rule_id="AZ004",
            title="Key Vault must set adequate soft delete retention",
            pillar="Security",
            default_enabled=True,
            func=az004_keyvault_soft_delete_retention,
        ),
        RuleSpec(
            rule_id="AZ005",
            title="NSG must not allow inbound SSH/RDP from the internet",
            pillar="Security",
            default_enabled=True,
            func=az005_nsg_open_ssh_rdp,
        ),
        RuleSpec(
            rule_id="AZ006",
            title="Azure SQL must not allow public network access",
            pillar="Security",
            default_enabled=True,
            func=az006_sql_public_network_access,
        ),
        RuleSpec(
            rule_id="AZ007",
            title="Storage account must enforce encryption at rest",
            pillar="Security",
            default_enabled=True,
            func=az007_storage_encryption_at_rest,
        ),
        RuleSpec(
            rule_id="AZ008",
            title="Storage account must enforce TLS 1.2+",
            pillar="Security",
            default_enabled=True,
            func=az008_storage_min_tls,
        ),
        RuleSpec(
            rule_id="AZ009",
            title="Storage account network rules must default to Deny",
            pillar="Security",
            default_enabled=True,
            func=az009_storage_network_default_deny,
        ),
        RuleSpec(
            rule_id="AZ010",
            title="Key Vault must disable public network access",
            pillar="Security",
            default_enabled=True,
            func=az010_keyvault_public_network_disabled,
        ),

    ]

    return [r for r in rules if r.default_enabled]
