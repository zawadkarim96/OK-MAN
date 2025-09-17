"""Regime switcher meta strategy pack."""

from __future__ import annotations

from typing import Dict, List

from .base import StrategyPack


class RegimeSwitcherMacro(StrategyPack):
    name = "regime_switcher_macro"

    def features(self) -> List[Dict[str, str]]:
        return [{"regime_classifier": "latest"}, {"pack_weights": "dynamic"}]

    def trigger(self) -> Dict[str, List[str]]:
        return {"all": ["regime_classifier.valid"]}

    def filters(self) -> Dict[str, List[str]]:
        return {"all": ["pack_kpis_stable"]}

    def entry(self) -> Dict[str, object]:
        return {"type": "delegate", "delegate_packs": [
            "htf_trend_pullback",
            "volatility_band_mean_reversion",
            "opening_range_breakout",
            "breakout_with_retest",
        ]}

    def exit(self) -> Dict[str, object]:
        return {"stop": "delegated"}

    def risk_profile(self) -> Dict[str, object]:
        return {"method": "portfolio_allocator", "max_fraction": 0.02}

    def routing_profile(self) -> Dict[str, object]:
        return {"prefer": "dynamic"}


__all__ = ["RegimeSwitcherMacro"]
