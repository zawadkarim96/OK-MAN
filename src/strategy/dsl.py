"""Strategy DSL parser and validator."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping

try:  # pragma: no cover - optional dependency
    import yaml
except Exception:  # pragma: no cover - fallback when PyYAML unavailable
    yaml = None  # type: ignore[assignment]

from src.common.types import Regime

REQUIRED_FIELDS = {"name", "regime_allow", "features", "trigger", "filters", "entry", "exit", "risk", "routing"}


@dataclass(slots=True)
class StrategyDefinition:
    """Represents a validated strategy definition."""

    name: str
    raw: Dict[str, Any]
    regimes: List[Regime] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return self.raw

    @property
    def trigger(self) -> Mapping[str, List[str]]:
        return self.raw["trigger"]

    @property
    def filters(self) -> Mapping[str, List[str]]:
        return self.raw["filters"]

    def summary(self) -> str:
        regime_names = ", ".join(regime.value for regime in self.regimes) or "n/a"
        return f"{self.name} [{regime_names}]"


class StrategyDSLParser:
    """Parse YAML or JSON DSL files into validated strategy definitions."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def parse(self) -> List[StrategyDefinition]:
        text = self._path.read_text(encoding="utf-8")
        document = self._load_document(text)
        if not isinstance(document, MutableMapping):
            raise ValueError("Strategy DSL root must be a mapping")
        schema_version = document.get("schema_version", 1)
        if schema_version != 1:
            raise ValueError(f"Unsupported strategy DSL schema version: {schema_version}")
        strategies = document.get("strategies", [])
        if not isinstance(strategies, list):
            raise ValueError("Strategies must be a list")
        return [self._validate(index, strategy) for index, strategy in enumerate(strategies)]

    def _load_document(self, text: str) -> Dict[str, Any]:
        if yaml is not None:
            return yaml.safe_load(text)  # type: ignore[return-value]
        return json.loads(text)

    def _validate(self, index: int, strategy: Any) -> StrategyDefinition:
        if not isinstance(strategy, MutableMapping):
            raise ValueError(f"Strategy at index {index} must be a mapping")
        missing = REQUIRED_FIELDS - strategy.keys()
        if missing:
            raise ValueError(f"Strategy '{strategy.get('name', index)}' missing fields: {sorted(missing)}")
        name = strategy["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Strategy name must be a non-empty string")

        regimes = self._parse_regimes(name, strategy["regime_allow"])
        features = self._ensure_list_of_mappings(name, "features", strategy["features"])
        triggers = self._ensure_expression_mapping(name, "trigger", strategy["trigger"])
        filters = self._ensure_expression_mapping(name, "filters", strategy["filters"])
        self._ensure_mapping(name, "entry", strategy["entry"])
        self._ensure_mapping(name, "exit", strategy["exit"])
        self._ensure_mapping(name, "risk", strategy["risk"])
        self._ensure_mapping(name, "routing", strategy["routing"])

        validated: Dict[str, Any] = {
            "name": name,
            "regime_allow": [regime.value for regime in regimes],
            "features": features,
            "trigger": triggers,
            "filters": filters,
            "entry": strategy["entry"],
            "exit": strategy["exit"],
            "risk": strategy["risk"],
            "routing": strategy["routing"],
        }
        return StrategyDefinition(name=name, raw=validated, regimes=regimes)

    @staticmethod
    def _parse_regimes(name: str, regimes: Iterable[Any]) -> List[Regime]:
        if not isinstance(regimes, Iterable) or isinstance(regimes, (str, bytes)):
            raise ValueError(f"Strategy '{name}' regime_allow must be a list")
        parsed: List[Regime] = []
        for value in regimes:
            try:
                parsed.append(Regime(str(value)))
            except ValueError as exc:  # pragma: no cover - defensive branch
                raise ValueError(f"Strategy '{name}' has unknown regime '{value}'") from exc
        if not parsed:
            raise ValueError(f"Strategy '{name}' must allow at least one regime")
        return parsed

    @staticmethod
    def _ensure_list_of_mappings(name: str, field: str, value: Any) -> List[Mapping[str, Any]]:
        if not isinstance(value, list):
            raise ValueError(f"Strategy '{name}' field '{field}' must be a list")
        result: List[Mapping[str, Any]] = []
        for item in value:
            if not isinstance(item, Mapping):
                raise ValueError(f"Strategy '{name}' field '{field}' entries must be mappings")
            result.append(dict(item))
        return result

    @staticmethod
    def _ensure_expression_mapping(name: str, field: str, value: Any) -> Dict[str, List[str]]:
        mapping = StrategyDSLParser._ensure_mapping(name, field, value)
        normalised: Dict[str, List[str]] = {}
        for key, expressions in mapping.items():
            if not isinstance(expressions, list) or not all(isinstance(expr, str) for expr in expressions):
                raise ValueError(f"Strategy '{name}' field '{field}' must map to lists of strings")
            normalised[key] = [expr.strip() for expr in expressions if expr.strip()]
        return normalised

    @staticmethod
    def _ensure_mapping(name: str, field: str, value: Any) -> Dict[str, Any]:
        if not isinstance(value, MutableMapping):
            raise ValueError(f"Strategy '{name}' field '{field}' must be a mapping")
        return dict(value)


__all__ = ["StrategyDSLParser", "StrategyDefinition"]
