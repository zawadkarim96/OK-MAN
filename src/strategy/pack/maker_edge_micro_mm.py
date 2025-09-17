"""Maker edge micro market making strategy pack."""

from __future__ import annotations

from typing import Dict, List

from .base import StrategyPack


class MakerEdgeMicroMM(StrategyPack):
    name = "maker_edge_micro_mm"

    def features(self) -> List[Dict[str, str]]:
        return [{"spread": "live"}, {"queue_position": "200ms"}, {"imbalance": "200ms"}]

    def trigger(self) -> Dict[str, List[str]]:
        return {"all": ["spread < tight_cap", "imbalance_supports"]}

    def filters(self) -> Dict[str, List[str]]:
        return {"all": ["inventory_within_limits"]}

    def entry(self) -> Dict[str, object]:
        return {"type": "post_inside_spread", "ttl_bars": 1}

    def exit(self) -> Dict[str, object]:
        return {"stop": "scratch", "time_stop_bars": 1}

    def risk_profile(self) -> Dict[str, object]:
        return {"method": "inventory_cap", "max_inventory": 2}

    def routing_profile(self) -> Dict[str, object]:
        return {"prefer": "maker_edge"}


__all__ = ["MakerEdgeMicroMM"]
