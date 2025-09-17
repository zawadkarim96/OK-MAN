"""Risk limit evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from src.common.types import RiskLimits


@dataclass(slots=True)
class LimitState:
    """Maintains drawdown and streak counters."""

    current_drawdown_pct: float = 0.0
    losing_streak: int = 0


class LimitEvaluator:
    """Evaluates whether trading should be halted."""

    def __init__(self, config: RiskLimits) -> None:
        self._config = config
        self._state = LimitState()

    def record_trade(self, pnl_pct: float) -> None:
        if pnl_pct < 0:
            self._state.losing_streak += 1
            self._state.current_drawdown_pct += abs(pnl_pct)
        else:
            self._state.losing_streak = 0
            self._state.current_drawdown_pct = max(0.0, self._state.current_drawdown_pct - pnl_pct)

    def can_trade(self, market_state: Dict[str, float]) -> bool:
        if self._state.current_drawdown_pct >= self._config.daily_drawdown_pct:
            return False
        if self._state.losing_streak >= self._config.max_losing_streak:
            return False
        if market_state.get("spread_bps", 0.0) > self._config.spread_cap_bps:
            return False
        if market_state.get("latency_ms", 0.0) > self._config.latency_cap_ms:
            return False
        return True


__all__ = ["LimitEvaluator", "LimitState"]
