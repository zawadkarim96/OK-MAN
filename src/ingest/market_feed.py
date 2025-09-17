"""Market data ingestion for ticks, L2/LOB, and auxiliary feeds."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, AsyncIterator, Dict, Iterable

from structlog import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class MarketEvent:
    """Represents a single market data update."""

    symbol: str
    timestamp: datetime
    payload: Dict[str, Any]


class MarketFeed:
    """Async generator that yields market events from multiple sources."""

    def __init__(self, symbols: Iterable[str]) -> None:
        self._symbols = list(symbols)
        self._running = False

    async def __aiter__(self) -> AsyncIterator[MarketEvent]:
        """Yield events from the simulated feed.

        TODO: Replace with real connections to MT5 bridge, websockets, or FIX hubs.
        """

        self._running = True
        while self._running:
            for symbol in self._symbols:
                await asyncio.sleep(0.01)
                yield MarketEvent(symbol=symbol, timestamp=datetime.utcnow(), payload={"price": 0.0})

    async def stop(self) -> None:
        """Stop the feed loop."""

        self._running = False


__all__ = ["MarketFeed", "MarketEvent"]
