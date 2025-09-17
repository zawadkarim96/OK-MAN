"""Real-time news and economic calendar ingestion."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, AsyncIterator, Dict

from structlog import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class NewsEvent:
    """Structured representation of a news headline or calendar event."""

    source: str
    symbol: str
    timestamp: datetime
    importance: str
    headline: str
    metadata: Dict[str, Any]


class NewsFeed:
    """Simple async iterator mocking a real news feed connection."""

    def __init__(self) -> None:
        self._running = False

    async def __aiter__(self) -> AsyncIterator[NewsEvent]:
        """Yield placeholder events until stopped."""

        self._running = True
        while self._running:
            await asyncio.sleep(1.0)
            yield NewsEvent(
                source="mock",
                symbol="XAUUSD",
                timestamp=datetime.utcnow(),
                importance="medium",
                headline="Placeholder economic headline",
                metadata={"sentiment": 0.0},
            )

    async def stop(self) -> None:
        """Stop the feed."""

        self._running = False


__all__ = ["NewsFeed", "NewsEvent"]
