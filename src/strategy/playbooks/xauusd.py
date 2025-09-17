"""XAUUSD symbol-specific playbook adjustments."""

from __future__ import annotations

from typing import Dict

from src.common.types import SignalCandidate


def score(candidate: SignalCandidate, features: Dict[str, float]) -> float:
    """Return adjusted confidence score for XAUUSD."""

    base = candidate.confidence
    rel_volume = features.get("relative_volume", 0.5)
    session = features.get("session_overlap", 0.0)
    news_risk = features.get("news_risk", 0.0)
    score_adjustment = 0.1 if rel_volume > 0.7 and session > 0 else -0.1
    if news_risk > 0:
        score_adjustment -= 0.2
    return max(0.0, min(1.0, base + score_adjustment))


__all__ = ["score"]
