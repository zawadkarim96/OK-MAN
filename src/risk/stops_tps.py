"""Stop-loss and take-profit logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(slots=True)
class StopConfig:
    """Configuration for stop and target calculations."""

    atr_multiplier: float
    break_even_r: float
    partial_take_profits: Dict[float, float]
    trailing_atr_multiplier: float


def atr_stop(entry_price: float, atr_value: float, direction: str, config: StopConfig) -> float:
    """Return ATR-based stop level."""

    offset = atr_value * config.atr_multiplier
    if direction == "long":
        return entry_price - offset
    return entry_price + offset


def move_to_break_even(current_profit_r: float, config: StopConfig) -> bool:
    """Return True when break-even trigger reached."""

    return current_profit_r >= config.break_even_r


__all__ = ["StopConfig", "atr_stop", "move_to_break_even"]
