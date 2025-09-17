"""Multi-timeframe confluence gate implementation."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional

from src.common.ta_confluence import ConfluenceEvaluator
from src.common.types import Direction, FeatureWindow, SignalCandidate


def _gate_now() -> datetime:
    """Return timezone-aware UTC timestamp for gate inputs."""

    return datetime.now(tz=timezone.utc)


@dataclass(slots=True)
class GateInputs:
    """Inputs required to evaluate the confluence gate."""

    symbol: str
    price: float
    timeframe_features: Dict[str, Dict[str, float]]
    volume_features: Dict[str, float]
    orderflow_features: Dict[str, float]
    ml_probability: Optional[float] = None
    created_at: datetime = field(default_factory=_gate_now)


class MultiTimeframeGate:
    """Combine technical, volume, order-flow, and ML cues into signal candidates."""

    def __init__(
        self,
        ttl_seconds: int = 180,
        min_adx: float = 18.0,
        min_relative_volume: float = 0.6,
        min_confidence: float = 0.55,
    ) -> None:
        self._confluence = ConfluenceEvaluator()
        self._ttl_seconds = ttl_seconds
        self._min_adx = min_adx
        self._min_relative_volume = min_relative_volume
        self._min_confidence = min_confidence

    def evaluate(self, inputs: GateInputs) -> Optional[SignalCandidate]:
        """Return a :class:`SignalCandidate` if confluence criteria align."""

        htf = inputs.timeframe_features.get("HTF", {})
        ltf = inputs.timeframe_features.get("LTF", {})
        mid = inputs.timeframe_features.get("MTF", {})
        ema_fast = float(htf.get("ema_fast", inputs.price))
        ema_slow = float(htf.get("ema_slow", inputs.price))
        adx_value = float(htf.get("adx", 0.0))
        macd_hist = float(ltf.get("macd_hist", 0.0))
        rsi_value = float(ltf.get("rsi", 50.0))
        rel_vol = float(inputs.volume_features.get("rel_volume", 0.5))
        orderflow_bias = float(inputs.orderflow_features.get("imbalance", 0.0))

        direction: Direction = "long" if ema_fast >= ema_slow else "short"
        if adx_value < self._min_adx:
            return None
        if rel_vol < self._min_relative_volume:
            return None

        if direction == "long" and macd_hist <= 0:
            return None
        if direction == "short" and macd_hist >= 0:
            return None
        if direction == "long" and rsi_value < 40:
            return None
        if direction == "short" and rsi_value > 60:
            return None
        if (direction == "long" and orderflow_bias < -0.1) or (direction == "short" and orderflow_bias > 0.1):
            return None

        trend_bias = 1.0 if direction == "long" else 0.0
        momentum_bias = _clamp(0.5 + 0.3 * math.tanh(macd_hist) + 0.2 * ((rsi_value - 50.0) / 50.0))
        volume_bias = _clamp(rel_vol)
        orderflow_component = _clamp(0.5 + 0.5 * orderflow_bias)

        feature_windows = [
            FeatureWindow(name=f"{scope.lower()}_{name}", timeframe=scope, timestamp=inputs.created_at, value=value)
            for scope, scope_features in inputs.timeframe_features.items()
            for name, value in scope_features.items()
        ]
        feature_windows.extend(
            [
                FeatureWindow(
                    name="trend_bias",
                    timeframe="derived",
                    timestamp=inputs.created_at,
                    value=trend_bias,
                ),
                FeatureWindow(
                    name="momentum_bias",
                    timeframe="derived",
                    timestamp=inputs.created_at,
                    value=momentum_bias,
                ),
                FeatureWindow(
                    name="volume_bias",
                    timeframe="derived",
                    timestamp=inputs.created_at,
                    value=volume_bias,
                ),
                FeatureWindow(
                    name="orderflow_bias",
                    timeframe="derived",
                    timestamp=inputs.created_at,
                    value=orderflow_component,
                ),
            ]
        )

        confluence_score = self._confluence.evaluate(feature_windows)
        confidence = confluence_score.total
        ml_probability = _clamp(inputs.ml_probability) if inputs.ml_probability is not None else None
        if ml_probability is not None:
            confidence = (confidence * 0.6) + (ml_probability * 0.4)

        if confidence < self._min_confidence:
            return None

        invalidation_key = "swing_low" if direction == "long" else "swing_high"
        invalidation = float(mid.get(invalidation_key, inputs.price))
        metadata = {
            "adx": adx_value,
            "rel_volume": rel_vol,
            "orderflow_bias": orderflow_bias,
            "score_components": {
                "trend": trend_bias,
                "momentum": momentum_bias,
                "volume": volume_bias,
                "orderflow": orderflow_component,
                "ml_probability": ml_probability,
            },
        }

        return SignalCandidate(
            symbol=inputs.symbol,
            direction=direction,
            confidence=min(confidence, 1.0),
            ttl=self._ttl_seconds,
            invalidation=invalidation,
            strategy="mtf_gate",
            metadata=metadata,
            created_at=inputs.created_at,
        )


__all__ = ["MultiTimeframeGate", "GateInputs"]


def _clamp(value: Optional[float], lower: float = 0.0, upper: float = 1.0) -> float:
    """Clamp ``value`` to the inclusive ``[lower, upper]`` interval."""

    if value is None or math.isnan(value):
        return lower
    return max(lower, min(upper, float(value)))
