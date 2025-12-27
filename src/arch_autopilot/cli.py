from __future__ import annotations

import argparse
from pathlib import Path

from arch_autopilot.collect import collect_tf_files
from arch_autopilot.parse_hcl import parse_terraform_files
from arch_autopilot.report import write_findings_json
from arch_autopilot.rules.az001_storage_https_only import az001_storage_https_only
from arch_autopilot.rules.az002_storage_public_blob_access import az002_storage_public_blob_access
from arch_autopilot.rules.az003_keyvault_purge_protection import az003_keyvault_purge_protection
from arch_autopilot.rules.registry import get_enabled_rules



import json




def main() -> None:
    parser = argparse.ArgumentParser(prog="arch-autopilot")
    parser.add_argument("path", nargs="?", default=".", help="Path to Terraform repo/folder")
    parser.add_argument("--narrative", action="store_true", help="Generate report.md using Azure OpenAI")
    parser.add_argument("--pillar", help="Run only rules for a specific Azure Well-Architected pillar (e.g., Security)")
    parser.add_argument(
        "--fail-on",
        default="high",
        choices=["none", "low", "medium", "high"],
        help="Exit non-zero if findings at or above this severity exist (default: high).",
    )



    args = parser.parse_args()

    repo_path = Path(args.path).expanduser().resolve()
    if not repo_path.exists():
        raise SystemExit(f"Error: Path {repo_path} does not exist")

    tf_files = collect_tf_files(repo_path)
    resources = parse_terraform_files(tf_files)

    findings = []
    enabled = get_enabled_rules()
    if args.pillar:
        enabled = [r for r in enabled if r.pillar.lower() == args.pillar.lower()]

    print(f"Running {len(enabled)} rules")
    for r in enabled:
        print(f" - {r.rule_id} ({r.pillar})")

    for rule in enabled:
        findings.extend(rule.func(resources))


    print(f"Findings: {len(findings)}")
    for f in findings[:10]:
        print(f" - {f.rule_id}: {f.title} ({f.file})")

    severity_rank = {"low": 1, "medium": 2, "high": 3}
    threshold = args.fail_on

    if threshold != "none":
        t = severity_rank[threshold]
        should_fail = any(severity_rank.get(f.severity, 0) >= t for f in findings)
        if should_fail:
            print(f"CI FAIL: Found findings with severity >= {threshold}")
            raise SystemExit(2)

    out_dir = repo_path / "out"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "findings.json"
    write_findings_json(findings, out_file)
    print(f"Wrote {out_file}")
    if args.narrative:
        from arch_autopilot.graph.build_graph import build_graph
        
        findings_json = json.loads(out_file.read_text(encoding="utf-8"))
        rules_run = [{"rule_id": r.rule_id, "title": r.title, "pillar": r.pillar} for r in enabled]
        graph = build_graph()
        result = graph.invoke({"findings": findings_json, "rules_run": rules_run})
        md_path = out_dir / "report.md"
        md_path.write_text(result["report_md"], encoding="utf-8")
        print(f"Wrote {md_path}")



if __name__ == "__main__":
    main()
