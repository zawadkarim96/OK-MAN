"""Opening range breakout strategy pack."""

from __future__ import annotations

from typing import Dict, List

from .base import StrategyPack


class OpeningRangeBreakout(StrategyPack):
    name = "opening_range_breakout"

    def features(self) -> List[Dict[str, str]]:
        return [
            {"opening_range": "M1_15"},
            {"volume_spike": "M1_30"},
            {"tape_tps": "tick_60s"},
            {"vix": "global"},
        ]

    def trigger(self) -> Dict[str, List[str]]:
        return {"any": ["breaks_opening_range_high", "breaks_opening_range_low"]}

    def filters(self) -> Dict[str, List[str]]:
        return {"all": ["volume_spike > q80", "tape_tps > q80", "vix < 25"]}

    def entry(self) -> Dict[str, object]:
        return {"type": "market", "ttl_bars": 1}

    def exit(self) -> Dict[str, object]:
        return {"stop": "atr(M1)", "time_stop_bars": 10, "trail": {"mult_atr": 1.0}}

    def risk_profile(self) -> Dict[str, object]:
        return {"method": "kelly_capped", "max_frac": 0.005}

    def routing_profile(self) -> Dict[str, object]:
        return {"prefer": "market_on_signal"}


__all__ = ["OpeningRangeBreakout"]
