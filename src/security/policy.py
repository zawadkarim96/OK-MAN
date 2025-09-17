"""Security policies for AI codegen."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Set


@dataclass(slots=True)
class Policy:
    allowed_paths: Set[Path]

    def is_allowed(self, path: Path) -> bool:
        return any(str(path).startswith(str(allowed)) for allowed in self.allowed_paths)


DEFAULT_POLICY = Policy(allowed_paths={Path("src"), Path("configs/strategies.d")})


__all__ = ["Policy", "DEFAULT_POLICY"]
