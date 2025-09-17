"""Dataset utilities for ML modules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple


def _to_float_list(series: Iterable[float]) -> List[float]:
    return [float(value) for value in series]


@dataclass(slots=True)
class WindowConfig:
    lookback: int
    horizon: int


def window_series(series: Iterable[float], config: WindowConfig) -> List[Tuple[List[float], List[float]]]:
    data = _to_float_list(series)
    windows: List[Tuple[List[float], List[float]]] = []
    for idx in range(len(data) - config.lookback - config.horizon + 1):
        X = data[idx : idx + config.lookback]
        y = data[idx + config.lookback : idx + config.lookback + config.horizon]
        windows.append((X, y))
    return windows


__all__ = ["WindowConfig", "window_series"]
