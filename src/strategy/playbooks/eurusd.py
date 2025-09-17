"""EURUSD playbook adjustments."""

from __future__ import annotations

from typing import Dict

from src.common.types import SignalCandidate


def score(candidate: SignalCandidate, features: Dict[str, float]) -> float:
    """Focus on mean reversion efficiency for EURUSD."""

    base = candidate.confidence
    spread = features.get("spread", 0.0001)
    range_score = features.get("range_score", 0.5)
    adjustment = 0.1 * (range_score - 0.5)
    adjustment -= min(spread * 1000, 0.1)
    return max(0.0, min(1.0, base + adjustment))


__all__ = ["score"]
