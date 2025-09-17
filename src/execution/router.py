"""Order routing logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from structlog import get_logger

from src.common.types import OrderRequest

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class RoutingDecision:
    order: OrderRequest
    prefer: str
    split: bool


class ExecutionRouter:
    """Decide between market and limit style orders."""

    def __init__(self, routing_profiles: Dict[str, Dict[str, object]]) -> None:
        self._profiles = routing_profiles

    def route(self, order: OrderRequest, profile_name: str) -> RoutingDecision:
        profile = self._profiles.get(profile_name, {})
        prefer = str(profile.get("prefer", "market"))
        split_threshold = float(profile.get("split_threshold", 0))
        split = order.metadata.get("notional", 0.0) > split_threshold > 0
        LOGGER.debug("routing_decision", order=order, prefer=prefer, split=split)
        return RoutingDecision(order=order, prefer=prefer, split=split)


__all__ = ["ExecutionRouter", "RoutingDecision"]
