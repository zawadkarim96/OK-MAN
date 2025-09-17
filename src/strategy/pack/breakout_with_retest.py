"""Breakout with retest strategy pack."""

from __future__ import annotations

from typing import Dict, List

from .base import StrategyPack


class BreakoutWithRetest(StrategyPack):
    name = "breakout_with_retest"

    def features(self) -> List[Dict[str, str]]:
        return [
            {"structure_levels": "200"},
            {"imbalance": "800ms"},
            {"depth_slope": "500ms"},
        ]

    def trigger(self) -> Dict[str, List[str]]:
        return {"all": ["level_break_confirmed", "retest_holds"]}

    def filters(self) -> Dict[str, List[str]]:
        return {"all": ["relvol(M1) > q60", "no_opposing_level_within(5)"]}

    def entry(self) -> Dict[str, object]:
        return {"type": "limit", "ttl_bars": 4}

    def exit(self) -> Dict[str, object]:
        return {"stop": "structure_low", "take_profit": "next_htf_level"}

    def risk_profile(self) -> Dict[str, object]:
        return {"method": "kelly_capped", "max_frac": 0.008}

    def routing_profile(self) -> Dict[str, object]:
        return {"prefer": "split_large"}


__all__ = ["BreakoutWithRetest"]
