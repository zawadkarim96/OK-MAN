"""Post news continuation strategy pack."""

from __future__ import annotations

from typing import Dict, List

from .base import StrategyPack


class PostNewsContinuation(StrategyPack):
    name = "post_news_continuation"

    def features(self) -> List[Dict[str, str]]:
        return [{"news_sentiment": "latest"}, {"volume_spike": "M1_15"}, {"lob_imbalance": "300ms"}]

    def trigger(self) -> Dict[str, List[str]]:
        return {"all": ["news.sentiment_bias > 0", "price_in_direction_of_news"]}

    def filters(self) -> Dict[str, List[str]]:
        return {"all": ["news.is_tier1 == true", "volatility_cap"]}

    def entry(self) -> Dict[str, object]:
        return {"type": "market", "ttl_bars": 2}

    def exit(self) -> Dict[str, object]:
        return {"stop": "1.2 * atr(M1)", "time_stop_bars": 4}

    def risk_profile(self) -> Dict[str, object]:
        return {"method": "kelly_capped", "max_frac": 0.004}

    def routing_profile(self) -> Dict[str, object]:
        return {"prefer": "market_on_signal"}


__all__ = ["PostNewsContinuation"]
