"""Momentum ignition strategy pack."""

from __future__ import annotations

from typing import Dict, List

from .base import StrategyPack


class MomentumIgnition(StrategyPack):
    name = "momentum_ignition"

    def features(self) -> List[Dict[str, str]]:
        return [
            {"tape_burst": "5s"},
            {"aggressor_ratio": "5s"},
            {"spread": "live"},
        ]

    def trigger(self) -> Dict[str, List[str]]:
        return {"all": ["tape_burst > theta", "aggressor_ratio > theta", "spread < cap"]}

    def filters(self) -> Dict[str, List[str]]:
        return {"all": ["session != lunch"]}

    def entry(self) -> Dict[str, object]:
        return {"type": "market", "ttl_bars": 1}

    def exit(self) -> Dict[str, object]:
        return {"stop": "0.5 * atr(M1)", "time_stop_bars": 3}

    def risk_profile(self) -> Dict[str, object]:
        return {"method": "kelly_capped", "max_frac": 0.003}

    def routing_profile(self) -> Dict[str, object]:
        return {"prefer": "market_on_signal"}


__all__ = ["MomentumIgnition"]
