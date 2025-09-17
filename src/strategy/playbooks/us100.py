"""US100 playbook adjustments."""

from __future__ import annotations

from typing import Dict

from src.common.types import SignalCandidate


def score(candidate: SignalCandidate, features: Dict[str, float]) -> float:
    """Adjust confidence emphasising opening range and tape confirmation."""

    base = candidate.confidence
    orb_break = features.get("orb_break", 0.0)
    tape_aggression = features.get("tape_aggression", 0.5)
    slippage = features.get("slippage", 0.0)
    adjustment = 0.05 if orb_break > 0 else -0.05
    adjustment += 0.1 if tape_aggression > 0.6 else 0.0
    adjustment -= min(slippage / 2, 0.1)
    return max(0.0, min(1.0, base + adjustment))


__all__ = ["score"]
