"""Order book feature extraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(slots=True)
class LOBSnapshot:
    """Represents an order book depth snapshot."""

    bids: List[List[float]]
    asks: List[List[float]]


def order_imbalance(snapshot: LOBSnapshot, levels: int = 5) -> float:
    bid_volume = sum(level[1] for level in snapshot.bids[:levels])
    ask_volume = sum(level[1] for level in snapshot.asks[:levels])
    denom = max(bid_volume + ask_volume, 1e-9)
    return (bid_volume - ask_volume) / denom


def cumulative_volume_delta(trades: List[Dict[str, float]]) -> float:
    delta = 0.0
    for trade in trades:
        sign = 1.0 if trade.get("side", "buy") == "buy" else -1.0
        delta += sign * trade.get("size", 0.0)
    return delta


def depth_slope(snapshot: LOBSnapshot, levels: int = 5) -> float:
    points = snapshot.bids[:levels] + snapshot.asks[:levels]
    if len(points) < 2:
        return 0.0
    prices = [point[0] for point in points]
    volumes = [point[1] for point in points]
    mean_price = sum(prices) / len(prices)
    mean_volume = sum(volumes) / len(volumes)
    numerator = sum((p - mean_price) * (v - mean_volume) for p, v in zip(prices, volumes))
    denominator = sum((p - mean_price) ** 2 for p in prices)
    if denominator == 0:
        return 0.0
    return numerator / denominator


__all__ = ["LOBSnapshot", "order_imbalance", "cumulative_volume_delta", "depth_slope"]
