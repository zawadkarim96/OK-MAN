"""Volume and volatility metrics implemented without third-party deps."""

from __future__ import annotations

from typing import Iterable


def relative_volume(volume_series: Iterable[float], lookback: int = 60) -> float:
    volumes = [float(v) for v in volume_series][-lookback:]
    if not volumes:
        return 0.0
    latest = volumes[-1]
    count = sum(1 for v in volumes if v <= latest)
    return count / len(volumes)


def realized_volatility(return_series: Iterable[float]) -> float:
    values = [float(r) for r in return_series]
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return variance**0.5


def atr_percentile(atr_series: Iterable[float], atr_value: float) -> float:
    atrs = [float(v) for v in atr_series]
    if not atrs:
        return 0.0
    count = sum(1 for value in atrs if value <= atr_value)
    return count / len(atrs)


__all__ = ["relative_volume", "realized_volatility", "atr_percentile"]
