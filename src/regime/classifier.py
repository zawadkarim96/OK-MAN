"""Regime classification heuristics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np

from src.common.types import Regime


@dataclass(slots=True)
class RegimeSnapshot:
    """Represents the latest regime assessment."""

    regime: Regime
    confidence: float


class RegimeClassifier:
    """Lightweight classifier blending volatility and trend measures."""

    def __init__(self, volatility_threshold: float = 1.0) -> None:
        self._volatility_threshold = volatility_threshold

    def classify(self, features: Dict[str, float]) -> RegimeSnapshot:
        """Return the most likely regime from provided features."""

        atr_pct = features.get("atr_percentile", 0.5)
        adx_value = features.get("adx", 15.0)
        volume_rel = features.get("relative_volume", 0.5)
        if atr_pct > self._volatility_threshold and adx_value > 25:
            regime = Regime.VOLATILE_TREND
        elif adx_value > 20:
            regime = Regime.TREND
        elif atr_pct < 0.7 and volume_rel < 0.4:
            regime = Regime.QUIET
        else:
            regime = Regime.RANGE
        confidence = float(np.mean([atr_pct, adx_value / 50, volume_rel]))
        return RegimeSnapshot(regime=regime, confidence=min(confidence, 1.0))


__all__ = ["RegimeClassifier", "RegimeSnapshot"]
