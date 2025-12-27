from __future__ import annotations

import json
from typing import Any

def extract_json_array(text: str) -> list[Any]:
    text = text.strip()

    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except Exception:
        pass

    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON array found in model output")

    candidate = text[start : end + 1]
    data = json.loads(candidate)
    if not isinstance(data, list):
        raise ValueError("Extracted JSON is not a list")

    return data

def same_finding_set(original: list[dict[str, Any]], ordered: list[dict[str, Any]]) -> bool:
    """
    Ensure model didn't add/remove findings. We compare by a stable key tuple.
    """
    def key(f: dict[str, Any]) -> tuple:
        return (
            f.get("rule_id"),
            f.get("resource_type"),
            f.get("resource_name"),
            f.get("file"),
        )

    return sorted(map(key, original)) == sorted(map(key, ordered))