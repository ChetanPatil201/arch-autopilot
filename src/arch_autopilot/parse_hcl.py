from __future__ import annotations

from pathlib import Path
from typing import Any

import hcl2

from .model import Resource

def _safe_load_hcl(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return hcl2.load(f)
    except Exception:
        return {}

def parse_terraform_files(tf_files: list[Path]) -> list[Resource]:
    resources: list[Resource] = []
    
    for tf in tf_files:
        doc = _safe_load_hcl(tf)

        blocks = doc.get("resource", [])
        if not isinstance(blocks, list):
            continue

        for block in blocks:
            if not isinstance(block, dict):
                continue

            for rtype, named in block.items():
                if not isinstance(named, dict):
                    continue

                for name, values in named.items():
                    if not isinstance(values, dict):
                        values = {}
                    resources.append(Resource(rtype=rtype, name=name, file=tf, values=values))

    return resources