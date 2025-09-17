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
