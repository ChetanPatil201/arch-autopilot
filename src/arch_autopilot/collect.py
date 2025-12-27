from __future__ import annotations
from pathlib import Path

def collect_tf_files(root: Path) -> list[Path]:
    """Return all .tf files under root, ignoring common noise folders."""
    skip_dirs = {".terraform", ".git",".node_modules", ".venv","venv","__pycache__"}
    tf_files: list[Path] = []

    for p in root.rglob("*.tf"):
        if any(part in skip_dirs for part in p.parts):
            continue
        tf_files.append(p)

    return sorted(tf_files)

