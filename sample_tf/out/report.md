# Azure Well-Architected Review Report

## Executive Summary
This review identified **10 high-severity security risks** in your Azure environment. These findings highlight critical misconfigurations in network security, storage accounts, Key Vault, and Azure SQL Server. Immediate remediation is recommended to enhance the security posture and protect sensitive resources from unauthorized access or data breaches.

---

## Pillar Summary: Security
### Key Findings:
1. **Network Security Group (NSG):**
   - **Inbound SSH/RDP from the public internet** is allowed, exposing resources to potential attacks.

2. **Storage Accounts:**
   - HTTPS-only traffic is not enforced.
   - Public blob access is allowed.
   - TLS 1.2+ is not enforced.
   - Encryption at rest is not explicitly enabled.
   - Network rules do not default to "Deny."

3. **Key Vault:**
   - Purge protection is not enabled.
   - Soft delete retention is missing or too low.
   - Public network access is allowed.

4. **Azure SQL Server:**
   - Public network access is enabled.

---

## Top Risks
- **Unrestricted public access** to critical resources (NSG, Key Vault, Azure SQL Server).
- **Weak storage account configurations**, including lack of HTTPS, encryption, and secure network rules.
- **Insufficient Key Vault protections**, such as missing purge protection and soft delete retention.
- **Non-compliance with TLS 1.2+ standards** for secure communication.

---

## Prioritized Fix Plan
1. **Restrict Public Access:**
   - Update NSG rules to allow SSH/RDP only from trusted IP ranges or use Azure Bastion.
   - Disable public network access for Key Vault and Azure SQL Server; implement private endpoints or VNet integration.

2. **Secure Storage Accounts:**
   - Enforce HTTPS-only traffic (`enable_https_traffic_only = true`).
   - Disable public blob access (`allow_blob_public_access = false`).
   - Set `min_tls_version = "TLS1_2"` for secure communication.
   - Enable encryption at rest (`encryption.services.blob.enabled = true`).
   - Configure network rules to default to "Deny" and explicitly allow trusted networks.

3. **Enhance Key Vault Protections:**
   - Enable purge protection (`purge_protection_enabled = true`).
   - Set soft delete retention to at least 7 days (`soft_delete_retention_days >= 7`).

4. **Review and Validate Changes:**
   - Conduct a thorough review of all changes to ensure compliance with security best practices.
   - Implement automated monitoring to detect and prevent future misconfigurations.

---

## Rules Executed
No rules were executed during this review.

---

## Appendix: Findings List
1. **AZ005:** NSG allows inbound SSH/RDP from the public internet.
2. **AZ001:** Storage account does not enforce HTTPS-only traffic.
3. **AZ002:** Storage account allows public blob access.
4. **AZ003:** Key Vault purge protection is not enabled.
5. **AZ006:** Azure SQL server allows public network access.
6. **AZ004:** Key Vault soft delete retention is missing or too low.
7. **AZ008:** Storage account does not enforce TLS 1.2+.
8. **AZ007:** Storage account encryption at rest is not explicitly enabled.
9. **AZ009:** Storage account network rules do not default to Deny.
10. **AZ010:** Key Vault allows public network access.