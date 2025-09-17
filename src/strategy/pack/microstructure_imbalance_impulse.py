"""Microstructure imbalance impulse strategy pack."""

from __future__ import annotations

from typing import Dict, List

from .base import StrategyPack


class MicrostructureImbalanceImpulse(StrategyPack):
    name = "microstructure_imbalance_impulse"

    def features(self) -> List[Dict[str, str]]:
        return [
            {"imbalance": "300ms"},
            {"depth_slope": "300ms"},
            {"microprice_drift": "300ms"},
        ]

    def trigger(self) -> Dict[str, List[str]]:
        return {"all": ["imbalance > theta", "depth_slope > theta", "microprice_drift > 0"]}

    def filters(self) -> Dict[str, List[str]]:
        return {"any": ["imbalance_duration > T"]}

    def entry(self) -> Dict[str, object]:
        return {"type": "market", "ttl_bars": 1}

    def exit(self) -> Dict[str, object]:
        return {"stop": "fixed_ticks", "time_stop_bars": 2}

    def risk_profile(self) -> Dict[str, object]:
        return {"method": "kelly_capped", "max_frac": 0.002}

    def routing_profile(self) -> Dict[str, object]:
        return {"prefer": "market_on_signal"}


__all__ = ["MicrostructureImbalanceImpulse"]
