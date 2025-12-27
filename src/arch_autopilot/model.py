from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass(frozen=True)
class Resource:
    rtype: str
    name: str
    file: Path
    values: dict[str, Any]

