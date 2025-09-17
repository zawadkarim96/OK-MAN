"""Volatility band mean reversion strategy pack."""

from __future__ import annotations

from typing import Dict, List

from .base import StrategyPack


class VolatilityBandMeanReversion(StrategyPack):
    name = "volatility_band_mean_reversion"

    def features(self) -> List[Dict[str, str]]:
        return [
            {"bollinger": "M1_20_2"},
            {"rsi": "M1_14"},
            {"cvd": "tick_90s"},
        ]

    def trigger(self) -> Dict[str, List[str]]:
        return {"any": ["close_below_lower_band", "close_above_upper_band"]}

    def filters(self) -> Dict[str, List[str]]:
        return {"all": ["adx(M5) < 15", "news.hard == false", "lob_absorption == true"]}

    def entry(self) -> Dict[str, object]:
        return {"type": "limit", "ttl_bars": 2}

    def exit(self) -> Dict[str, object]:
        return {"stop": "0.75 * atr(M1)", "take_profit": "mid_band", "time_stop_bars": 5}

    def risk_profile(self) -> Dict[str, object]:
        return {"method": "kelly_capped", "max_frac": 0.004}

    def routing_profile(self) -> Dict[str, object]:
        return {"prefer": "maker_edge"}


__all__ = ["VolatilityBandMeanReversion"]
