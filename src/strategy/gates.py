"""Multi-timeframe confluence gate implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

from src.common.ta_confluence import ConfluenceEvaluator
from src.common.types import Direction, FeatureWindow, SignalCandidate


@dataclass(slots=True)
class GateInputs:
    """Inputs required to evaluate the confluence gate."""

    symbol: str
    price: float
    timeframe_features: Dict[str, Dict[str, float]]
    volume_features: Dict[str, float]
    orderflow_features: Dict[str, float]
    ml_probability: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


class MultiTimeframeGate:
    """Combine technical, volume, order-flow, and ML cues into signal candidates."""

    def __init__(self, ttl: int = 3) -> None:
        self._confluence = ConfluenceEvaluator()
        self._ttl = ttl

    def evaluate(self, inputs: GateInputs) -> Optional[SignalCandidate]:
        """Return a :class:`SignalCandidate` if confluence criteria align."""

        htf = inputs.timeframe_features.get("HTF", {})
        ltf = inputs.timeframe_features.get("LTF", {})
        mid = inputs.timeframe_features.get("MTF", {})
        ema_fast = htf.get("ema_fast", inputs.price)
        ema_slow = htf.get("ema_slow", inputs.price)
        adx_value = htf.get("adx", 15.0)
        macd_hist = ltf.get("macd_hist", 0.0)
        rsi_value = ltf.get("rsi", 50.0)
        rel_vol = inputs.volume_features.get("rel_volume", 0.5)
        orderflow_bias = inputs.orderflow_features.get("imbalance", 0.0)

        direction: Direction = "long" if ema_fast >= ema_slow else "short"
        if adx_value < 18:
            return None
        if direction == "long" and macd_hist <= 0:
            return None
        if direction == "short" and macd_hist >= 0:
            return None
        if direction == "long" and rsi_value < 40:
            return None
        if direction == "short" and rsi_value > 60:
            return None
        if rel_vol < 0.6:
            return None
        if (direction == "long" and orderflow_bias < -0.1) or (direction == "short" and orderflow_bias > 0.1):
            return None

        features = [
            FeatureWindow(name=f"{scope.lower()}_{name}", timeframe=scope, timestamp=inputs.created_at, value=value)
            for scope, scope_features in inputs.timeframe_features.items()
            for name, value in scope_features.items()
        ]
        confluence_score = self._confluence.evaluate(features)

        confidence = confluence_score.total
        if inputs.ml_probability is not None:
            confidence = (confidence + float(inputs.ml_probability)) / 2

        invalidation_key = "swing_low" if direction == "long" else "swing_high"
        invalidation = mid.get(invalidation_key, inputs.price)
        metadata = {
            "created_at": inputs.created_at,
            "adx": adx_value,
            "rel_volume": rel_vol,
            "orderflow_bias": orderflow_bias,
        }

        return SignalCandidate(
            symbol=inputs.symbol,
            direction=direction,
            confidence=min(confidence, 1.0),
            ttl=self._ttl,
            invalidation=float(invalidation),
            strategy="mtf_gate",
            metadata=metadata,
        )


__all__ = ["MultiTimeframeGate", "GateInputs"]
