from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from arch_autopilot.graph.guards import extract_json_array, same_finding_set
from arch_autopilot.graph.evaluator import FindingsEvaluator



# Load environment variables from .env file if it exists
env_path = Path(__file__).parent.parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

def _llm() -> AzureChatOpenAI:
    required_vars = {
        "AZURE_OPENAI_ENDPOINT": os.environ.get("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_KEY": os.environ.get("AZURE_OPENAI_KEY"),
        "AZURE_OPENAI_DEPLOYMENT": os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    }
    
    missing = [var for var, value in required_vars.items() if not value]
    if missing:
        raise SystemExit(
            f"Error: Missing required environment variables: {', '.join(missing)}\n"
            f"Please set these variables or create a .env file in the project root with:\n"
            f"  AZURE_OPENAI_ENDPOINT=your_endpoint\n"
            f"  AZURE_OPENAI_KEY=your_key\n"
            f"  AZURE_OPENAI_DEPLOYMENT=your_deployment\n"
            f"  AZURE_OPENAI_API_VERSION=2024-02-15-preview (optional)"
        )
    
    return AzureChatOpenAI(
        azure_endpoint=required_vars["AZURE_OPENAI_ENDPOINT"],
        api_key=required_vars["AZURE_OPENAI_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_deployment=required_vars["AZURE_OPENAI_DEPLOYMENT"],
        temperature=0.2,
    )

def _extract_json(text: str) -> Any:
    """Extract JSON from LLM response, handling markdown code blocks and extra text."""
    if not text or not text.strip():
        raise ValueError("Empty response from LLM")
    
    # Try to find JSON in markdown code blocks (```json ... ``` or ``` ... ```)
    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if json_match:
        text = json_match.group(1).strip()
    
    # Try to find JSON array or object in the text
    # Look for patterns like [...], {...}, or just the JSON itself
    json_patterns = [
        r'\[.*\]',  # JSON array
        r'\{.*\}',  # JSON object
    ]
    
    for pattern in json_patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            text = match.group(0)
            break
    
    # Try to parse the JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # If parsing fails, try to find the first valid JSON structure
        # Look for the start of an array or object
        start_chars = {'[', '{'}
        for i, char in enumerate(text):
            if char in start_chars:
                # Try to find the matching closing bracket/brace
                try:
                    return json.loads(text[i:])
                except json.JSONDecodeError:
                    continue
        
        # If all else fails, raise a helpful error
        raise ValueError(
            f"Failed to parse JSON from LLM response.\n"
            f"Error: {e}\n"
            f"Response content (first 500 chars): {text[:500]}"
        ) from e

def generate_report_node(state: dict[str, Any]) -> dict[str, Any]:
    findings = state["findings"]
    warning = state.get("eval_warning")
    rules_run = state.get("rules_run", [])

    user_content = (
        f"Rules executed:\n{json.dumps(rules_run, indent=2)}\n\n"
        f"Findings JSON:\n{json.dumps(findings, indent=2)}"
    )

    if warning:
        user_content = f"NOTE: The prioritization step was rejected: {warning}\n\n" + user_content


    system = (
        "You are Cloud Architecture Autopilot for Microsoft Azure.\n"
        "ONLY use the provided findings and rules_run. Do NOT invent resources or evidence.\n"
        "Treat findings[i].category as the Azure Well-Architected pillar (e.g., Security, Reliability).\n"
        "Write a concise Markdown report with:\n"
        "1) Executive summary\n"
        "2) Pillar summary (group findings by category)\n"
        "3) Top risks (bullets)\n"
        "4) Prioritized fix plan\n"
        "5) Rules executed (from rules_run)\n"
        "6) Appendix: findings list\n"
    )


    msg = _llm().invoke(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]
    )


    return {"report_md": msg.content}

def prioritize_findings_node(state: dict[str, Any]) -> dict[str, Any]:
    findings = state["findings"]

    system = (
        "You are an Azure cloud security architect.\n"
        "ONLY use the provided findings.\n"
        "Return the same findings reordered from highest priority to lowest.\n"
        "Prioritize by: severity, exploitability, blast radius, ease of fix.\n"
        "Output MUST be valid JSON array of findings objects (same keys as input).\n"
        "Do NOT add or remove findings.\n"
        "Return ONLY the JSON array, no markdown, no explanations, no code blocks.\n"
    )

    msg = _llm().invoke(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Findings JSON:\n{json.dumps(findings, indent=2)}"},
        ]
    )

    ordered = extract_json_array(msg.content)
    evaluator = FindingsEvaluator()
    result = evaluator.evaluate(findings, ordered)

    if not result.passed:
        # Safe fallback: keep original order if AI misbehaved
        return {"findings": findings, "eval_warning": result.reason}

    return {"findings": ordered}
