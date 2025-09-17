"""Execution router tests."""

from src.common.types import OrderRequest
from src.execution.router import ExecutionRouter


def test_execution_router_split_logic() -> None:
    router = ExecutionRouter(routing_profiles={"market_on_signal": {"prefer": "market", "split_threshold": 1000}})
    order = OrderRequest(
        symbol="XAUUSD",
        direction="long",
        size=1.0,
        order_type="market",
        price=None,
        stop_loss=None,
        take_profit=None,
        metadata={"notional": 2000},
    )
    decision = router.route(order, "market_on_signal")
    assert decision.split is True
    assert decision.prefer == "market"


def test_execution_router_no_split_when_below_threshold() -> None:
    router = ExecutionRouter(routing_profiles={"market_on_signal": {"prefer": "limit", "split_threshold": 5000}})
    order = OrderRequest(
        symbol="US100",
        direction="short",
        size=0.5,
        order_type="limit",
        price=15000,
        stop_loss=15050,
        take_profit=14900,
        metadata={"notional": 2000},
    )
    decision = router.route(order, "market_on_signal")
    assert decision.split is False
    assert decision.prefer == "limit"
