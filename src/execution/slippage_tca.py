"""Transaction cost analysis utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class Fill:
    price: float
    size: float


@dataclass(slots=True)
class TCAReport:
    average_slippage: float
    fills: List[Fill] = field(default_factory=list)


def analyse(fills: List[Fill], benchmark_price: float) -> TCAReport:
    """Compute average slippage relative to benchmark."""

    if not fills:
        return TCAReport(average_slippage=0.0)
    total_slippage = sum((fill.price - benchmark_price) * fill.size for fill in fills)
    total_size = sum(fill.size for fill in fills)
    if total_size == 0:
        return TCAReport(average_slippage=0.0, fills=fills)
    return TCAReport(average_slippage=total_slippage / total_size, fills=fills)


__all__ = ["analyse", "TCAReport", "Fill"]
