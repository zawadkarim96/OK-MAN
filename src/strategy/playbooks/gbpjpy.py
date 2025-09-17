"""GBPJPY playbook adjustments."""

from __future__ import annotations

from typing import Dict

from src.common.types import SignalCandidate


def score(candidate: SignalCandidate, features: Dict[str, float]) -> float:
    """Adjust for higher volatility and news sensitivity."""

    base = candidate.confidence
    volatility = features.get("volatility", 1.0)
    news_halt = features.get("news_halt", 0.0)
    adjustment = -0.1 if volatility > 2.0 else 0.05
    if news_halt:
        adjustment = -1.0
    return max(0.0, min(1.0, base + adjustment))


__all__ = ["score"]
