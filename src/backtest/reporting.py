"""Backtest reporting utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(slots=True)
class PerformanceReport:
    win_rate: float
    profit_factor: float
    max_drawdown: float


def generate(metrics: Dict[str, float]) -> PerformanceReport:
    return PerformanceReport(
        win_rate=float(metrics.get("win_rate", 0.0)),
        profit_factor=float(metrics.get("profit_factor", 0.0)),
        max_drawdown=float(metrics.get("max_drawdown", 0.0)),
    )


__all__ = ["PerformanceReport", "generate"]
