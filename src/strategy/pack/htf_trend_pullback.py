"""HTF Trend Pullback strategy pack."""

from __future__ import annotations

from typing import Dict, List

from .base import StrategyPack


class HTFTrendPullback(StrategyPack):
    name = "htf_trend_pullback"

    def features(self) -> List[Dict[str, str]]:
        return [
            {"ema": "H1_200"},
            {"ema": "H1_50"},
            {"adx": "H1_14"},
            {"macd": "M1_default"},
            {"rsi": "M1_14"},
            {"relvol": "M1_60"},
            {"lob_imbalance": "500ms"},
        ]

    def trigger(self) -> Dict[str, List[str]]:
        return {"all": ["close(H1) > ema(H1,200)", "macd_hist(M1) crosses_up 0", "rsi(M1) > 40"]}

    def filters(self) -> Dict[str, List[str]]:
        return {"all": ["relvol(M1) > q70", "lob_imbalance > theta1", "news.hard == false"]}

    def entry(self) -> Dict[str, object]:
        return {"type": "market_or_limit_smart", "ttl_bars": 3}

    def exit(self) -> Dict[str, object]:
        return {
            "stop": "k1 * atr(M1)",
            "partial_tp": [{"at_r": 0.5, "pct": 0.5}],
            "trail": {"mult_atr": "k2"},
            "move_be_at_r": 1.0,
        }

    def risk_profile(self) -> Dict[str, object]:
        return {"method": "kelly_capped", "max_frac": 0.01}

    def routing_profile(self) -> Dict[str, object]:
        return {"prefer": "market_on_signal", "split_threshold": "size > S0"}


__all__ = ["HTFTrendPullback"]
