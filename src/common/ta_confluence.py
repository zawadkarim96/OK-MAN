"""Indicator confluence helpers for the multi-timeframe gate."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

from .types import FeatureWindow


@dataclass(slots=True)
class ConfluenceScore:
    """Captures aggregated scores from multiple indicator families."""

    trend: float
    momentum: float
    volume: float
    orderflow: float

    @property
    def total(self) -> float:
        """Return the combined score clipped between 0 and 1."""

        raw = self.trend * 0.35 + self.momentum * 0.25 + self.volume * 0.2 + self.orderflow * 0.2
        return max(0.0, min(1.0, raw))


class ConfluenceEvaluator:
    """Aggregates features into a :class:`ConfluenceScore`."""

    def __init__(self, weights: Dict[str, float] | None = None) -> None:
        self._weights = weights or {"trend": 0.35, "momentum": 0.25, "volume": 0.2, "orderflow": 0.2}

    def evaluate(self, features: Iterable[FeatureWindow]) -> ConfluenceScore:
        """Simple heuristic aggregator for early experimentation."""

        feature_map = {feature.name: feature.value for feature in features}
        trend = float(feature_map.get("trend_bias", 0.5))
        momentum = float(feature_map.get("momentum_bias", 0.5))
        volume = float(feature_map.get("volume_bias", 0.5))
        orderflow = float(feature_map.get("orderflow_bias", 0.5))
        return ConfluenceScore(trend=trend, momentum=momentum, volume=volume, orderflow=orderflow)

    def weight(self, component: str) -> float:
        """Return configured weight for a component."""

        return self._weights.get(component, 0.0)


__all__ = ["ConfluenceScore", "ConfluenceEvaluator"]
