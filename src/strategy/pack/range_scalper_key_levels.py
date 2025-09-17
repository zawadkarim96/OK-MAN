"""Range scalper at key levels strategy pack."""

from __future__ import annotations

from typing import Dict, List

from .base import StrategyPack


class RangeScalperKeyLevels(StrategyPack):
    name = "range_scalper_key_levels"

    def features(self) -> List[Dict[str, str]]:
        return [
            {"pivots": "1d"},
            {"stoch": "M3"},
            {"aggression": "45s"},
        ]

    def trigger(self) -> Dict[str, List[str]]:
        return {"all": ["touch_key_level", "stoch_cross", "aggression_declining"]}

    def filters(self) -> Dict[str, List[str]]:
        return {"all": ["spread < cap", "trend_alert == false"]}

    def entry(self) -> Dict[str, object]:
        return {"type": "limit", "ttl_bars": 2}

    def exit(self) -> Dict[str, object]:
        return {"stop": "0.6 * atr(M3)", "take_profit": "mid_range", "move_be_at_r": 0.6}

    def risk_profile(self) -> Dict[str, object]:
        return {"method": "kelly_capped", "max_frac": 0.004}

    def routing_profile(self) -> Dict[str, object]:
        return {"prefer": "maker_edge"}


__all__ = ["RangeScalperKeyLevels"]
