"""BTCUSD playbook adjustments."""

from __future__ import annotations

from typing import Dict

from src.common.types import SignalCandidate


def score(candidate: SignalCandidate, features: Dict[str, float]) -> float:
    """Incorporate sentiment and spread sensitivity for BTC."""

    base = candidate.confidence
    sentiment = features.get("sentiment", 0.0)
    spread = features.get("spread", 0.0005)
    regime = features.get("regime", 0)
    adjustment = sentiment * 0.1
    if regime == 0:  # range
        adjustment -= 0.05
    adjustment -= min(spread * 10, 0.15)
    return max(0.0, min(1.0, base + adjustment))


__all__ = ["score"]
