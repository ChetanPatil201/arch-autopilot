from __future__ import annotations

from arch_autopilot.finding import Finding
from arch_autopilot.model import Resource


def az005_nsg_open_ssh_rdp(resources: list[Resource]) -> list[Finding]:
    """
    AZ005: NSG should not allow inbound SSH (22) or RDP (3389) from 0.0.0.0/0 or Internet.
    Best-effort offline check on azurerm_network_security_rule.
    """
    findings: list[Finding] = []

    for r in resources:
        if r.rtype != "azurerm_network_security_rule":
            continue

        vals = r.values
        direction = str(vals.get("direction", "")).lower()
        access = str(vals.get("access", "")).lower()
        protocol = str(vals.get("protocol", "")).lower()

        if direction != "inbound" or access != "allow":
            continue

        # source can be "0.0.0.0/0", "*", or "Internet"
        src = vals.get("source_address_prefix", vals.get("source_address_prefixes"))
        src_text = str(src).lower()

        risky_src = ("0.0.0.0/0" in src_text) or ("internet" in src_text) or (src_text.strip() in {"*", "['*']", '["*"]'})
        if not risky_src:
            continue

        # destination port can be a single port or range
        dport = vals.get("destination_port_range", vals.get("destination_port_ranges"))
        dport_text = str(dport).lower()

        risky_port = ("22" in dport_text) or ("3389" in dport_text) or ("*" in dport_text)

        if not risky_port:
            continue

        findings.append(
            Finding(
                rule_id="AZ005",
                title="NSG allows inbound SSH/RDP from the public internet",
                severity="high",
                category="Security",
                resource_type=r.rtype,
                resource_name=r.name,
                file=r.file,
                evidence=f"Allow inbound with public source ({src_text}) and destination port ({dport_text}).",
                remediation="Restrict inbound SSH/RDP to trusted IP ranges, use VPN/Bastion, or remove the rule.",
                confidence=0.8,
            )
        )

    return findings
