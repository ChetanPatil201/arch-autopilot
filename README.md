# Arch Autopilot
![Arch Autopilot CI](https://github.com/ChetanPatil201/arch-autopilot/actions/workflows/arch-autopilot.yml/badge.svg)

Arch Autopilot is an AI-powered **Infrastructure-as-Code (IaC) reasoning engine** for Microsoft Azure.

It analyzes Terraform configurations, identifies **real cloud risks**, and produces **prioritized, explainable decisions** — safely and automatically inside CI.

This is not a checklist scanner.  
It is a **decision system** for cloud architecture.

---

## Why Arch Autopilot exists

Most IaC tools today:
- Generate hundreds of low-signal findings
- Focus on syntax instead of architectural risk
- Use AI without guardrails (hard to trust)
- Run outside developer workflows

Arch Autopilot was built with a different philosophy:

> **Understand infrastructure intent, enforce trust in AI, and stop risky changes before production.**

---

## Core ideas

### 1. IaC Reasoning (not line scanning)
Terraform files are converted into **semantic resources** (e.g., storage accounts, key vaults).  
Rules reason about **risk, exposure, and blast radius**, not individual lines.

### 2. Guardrailed AI (enterprise-safe)
AI is used only for:
- Prioritization
- Explanation
- Narrative reporting

Guardrails ensure the AI:
- Cannot add or remove findings
- Cannot hallucinate resources
- Falls back safely if it violates constraints

### 3. CI-first by design
Arch Autopilot runs inside GitHub Actions:
- On pull requests
- Before merge
- With optional build failure on high-risk findings

This is where cloud incidents are prevented.

---

## What it does today

- Parses Terraform into structured resources
- Runs opinionated Azure security rules
- Aggregates findings via a rule registry
- Prioritizes risks using Azure OpenAI (LangGraph)
- Generates:
  - findings.json (machine-readable)
  - report.md (executive-ready)
- Integrates with GitHub Actions CI

---

## How it’s different

| Typical IaC scanners | Arch Autopilot |
|---------------------|----------------|
| Hundreds of generic checks | Few high-signal rules |
| Line-based warnings | Resource-level reasoning |
| AI summaries without trust | Guardrailed AI decisions |
| Offline / manual scans | CI-native enforcement |
| Raw output | Prioritized, explainable reports |

---

## Architecture (high level)

Terraform (.tf)
  ↓
Semantic Resources
  ↓
Rule Registry (AZ001, AZ002, ...)
  ↓
Findings
  ↓
AI Prioritization (LangGraph + Azure OpenAI)
  ↓
Guardrails & Evaluation
  ↓
Report + CI Enforcement

---

## Example output

- out/findings.json  
  Structured findings suitable for automation and audits

- out/report.md  
  Human-readable report with:
  - Executive summary
  - Pillar-based grouping
  - Top risks
  - Fix plan

---

## Quick start (local)

poetry install  
poetry run arch-autopilot <terraform-path> --pillar Security --fail-on none --narrative

### Required environment variables
Use a .env file (not committed):

AZURE_OPENAI_ENDPOINT=...  
AZURE_OPENAI_API_KEY=...  
AZURE_OPENAI_API_VERSION=2024-02-15-preview  
AZURE_OPENAI_DEPLOYMENT=...

---

## CI usage (GitHub Actions)

Arch Autopilot runs automatically on pull requests and uploads findings as an artifact.

Typical CI behavior:
- Report all findings
- Fail the build only on high-severity risks (configurable)

This enables **shift-left cloud governance**.

---

## Current status

Early, but production-minded.

The focus is on:
- Correctness over coverage
- Trust over noise
- Architecture over checklists

The rule set is intentionally small and will grow toward **40–60 high-impact enterprise rules**.

---

## Who this is for

- Platform / Cloud teams
- Security engineers
- Azure architects
- Organizations practicing Terraform-based cloud governance

---

## Philosophy

Don’t overwhelm engineers.  
Don’t trust AI blindly.  
Make the right decision obvious — before production.

---

## Roadmap

**Near-term (v0.1–v0.2)**
- Expand to ~10 high-impact Azure security rules
- Rule tagging by Azure Well-Architected pillars
- CI enforcement modes (warn vs block)
- Improve prioritization logic for multi-risk repos

**Mid-term (v0.3)**
- IAM and identity blast-radius rules
- Network exposure and ingress analysis
- Cross-resource reasoning (e.g., storage + network + identity)
- Configurable rule enablement (per repo)

**Long-term**
- Enterprise rule packs
- Org-level policy baselines
- Advanced architectural anti-pattern detection

---

## Contact

Built by Chetan Patil.

- LinkedIn: https://www.linkedin.com/in/chetan-patil-2492a738/
- GitHub: https://github.com/ChetanPatil201/arch-autopilot

If you’re working on Azure platform, cloud security, or IaC governance and want to collaborate or pilot this internally, feel free to reach out.
