"""Position sizing utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(slots=True)
class KellyConfig:
    """Configuration for Kelly sizing."""

    max_fraction: float
    floor_fraction: float


def kelly_fraction(edge: float, win_rate: float, config: KellyConfig) -> float:
    """Compute capped Kelly fraction."""

    if win_rate <= 0 or win_rate >= 1:
        return config.floor_fraction
    fraction = win_rate - (1 - win_rate) / max(edge, 1e-6)
    fraction = max(config.floor_fraction, min(config.max_fraction, fraction))
    return fraction


def confidence_scaled_size(confidence: float, base_fraction: float, notional: float) -> float:
    """Scale size by confidence and account notional."""

    return round(notional * base_fraction * confidence, 4)


def portfolio_guard(sizes: Dict[str, float], correlation_limit: float) -> Dict[str, float]:
    """Placeholder portfolio cap ensuring exposures remain within correlation limit."""

    scale = 1.0
    if len(sizes) > 1:
        scale = min(1.0, correlation_limit / max(sum(abs(size) for size in sizes.values()), 1e-6))
    return {symbol: size * scale for symbol, size in sizes.items()}


__all__ = ["KellyConfig", "kelly_fraction", "confidence_scaled_size", "portfolio_guard"]
