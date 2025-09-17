"""Walk-forward optimisation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable, List

from structlog import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class WalkForwardResult:
    window_start: datetime
    window_end: datetime
    oos_win_rate: float
    profit_factor: float


def schedule(start: datetime, end: datetime, window_days: int, step_days: int) -> List[tuple[datetime, datetime]]:
    """Generate walk-forward windows."""

    windows = []
    current = start
    delta = timedelta(days=window_days)
    step = timedelta(days=step_days)
    while current < end:
        window_end = min(current + delta, end)
        windows.append((current, window_end))
        current += step
    return windows


def evaluate(results: Iterable[WalkForwardResult], win_rate_threshold: float, profit_factor_threshold: float) -> bool:
    """Return True if all windows meet thresholds."""

    for result in results:
        LOGGER.debug("walk_forward_window", result=result)
        if result.oos_win_rate < win_rate_threshold or result.profit_factor < profit_factor_threshold:
            return False
    return True


__all__ = ["schedule", "evaluate", "WalkForwardResult"]
