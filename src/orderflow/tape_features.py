"""Tape-based feature extraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class TapePrint:
    """Represents a trade print."""

    timestamp_ms: int
    size: float
    side: str


def trades_per_second(prints: Iterable[TapePrint]) -> float:
    """Compute trade velocity for the provided prints."""

    prints_list = list(prints)
    if not prints_list:
        return 0.0
    duration = (prints_list[-1].timestamp_ms - prints_list[0].timestamp_ms) / 1000
    if duration <= 0:
        return float(len(prints_list))
    return float(len(prints_list) / duration)


def average_trade_size(prints: Iterable[TapePrint]) -> float:
    """Return average trade size."""

    prints_list = list(prints)
    if not prints_list:
        return 0.0
    return float(sum(print_.size for print_ in prints_list) / len(prints_list))


def aggressor_ratio(prints: Iterable[TapePrint]) -> float:
    """Share of aggressive buy volume."""

    prints_list = list(prints)
    if not prints_list:
        return 0.5
    buy_volume = sum(print_.size for print_ in prints_list if print_.side == "buy")
    total_volume = sum(print_.size for print_ in prints_list)
    if total_volume == 0:
        return 0.5
    return float(buy_volume / total_volume)


__all__ = ["TapePrint", "trades_per_second", "average_trade_size", "aggressor_ratio"]
