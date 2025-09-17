import asyncio

from src.api.server import health, run_strategy
from src.api.schemas import StrategyRunRequest


def test_health_endpoint_direct() -> None:
    response = asyncio.run(health())
    assert response.status == "ok"


def test_run_endpoint_direct() -> None:
    result = asyncio.run(run_strategy(StrategyRunRequest(mode="paper")))
    assert result["mode"] == "paper"
