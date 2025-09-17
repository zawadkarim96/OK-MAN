"""Strategy DSL parser and validator."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

try:  # pragma: no cover - optional dependency
    import yaml
except Exception:  # pragma: no cover - fallback when PyYAML unavailable
    yaml = None  # type: ignore[assignment]

REQUIRED_FIELDS = {"name", "regime_allow", "features", "trigger", "filters", "entry", "exit", "risk", "routing"}


@dataclass(slots=True)
class StrategyDefinition:
    """Represents a validated strategy definition."""

    name: str
    raw: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return self.raw


class StrategyDSLParser:
    """Parse YAML or JSON DSL files into validated strategy definitions."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def parse(self) -> List[StrategyDefinition]:
        text = self._path.read_text(encoding="utf-8")
        document = self._load_document(text)
        if not isinstance(document, dict):
            raise ValueError("Strategy DSL root must be a mapping")
        strategies = document.get("strategies", [])
        if not isinstance(strategies, list):
            raise ValueError("Strategies must be a list")
        return [self._validate(strategy) for strategy in strategies]

    def _load_document(self, text: str) -> Dict[str, Any]:
        if yaml is not None:
            return yaml.safe_load(text)  # type: ignore[return-value]
        return json.loads(text)

    def _validate(self, strategy: Dict[str, Any]) -> StrategyDefinition:
        missing = REQUIRED_FIELDS - strategy.keys()
        if missing:
            raise ValueError(f"Strategy missing fields: {sorted(missing)}")
        name = strategy["name"]
        if not isinstance(name, str):
            raise ValueError("Strategy name must be a string")
        return StrategyDefinition(name=name, raw=strategy)


__all__ = ["StrategyDSLParser", "StrategyDefinition"]
