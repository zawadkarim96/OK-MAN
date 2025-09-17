"""Async HTTP fetchers with caching and backoff."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Optional

import aiohttp
from structlog import get_logger

from .cache import WebCache

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class FetchConfig:
    """Configuration for rate limiting and retries."""

    max_retries: int = 3
    backoff_seconds: float = 0.5
    rate_limit_per_minute: Optional[int] = None


class HttpFetcher:
    """Fetch data from REST endpoints with caching and retry logic."""

    def __init__(self, cache: WebCache, config: FetchConfig | None = None) -> None:
        self._cache = cache
        self._config = config or FetchConfig()
        self._semaphore = (
            asyncio.Semaphore(self._config.rate_limit_per_minute or 5)
            if self._config.rate_limit_per_minute
            else None
        )

    async def get(self, url: str, *, ttl_minutes: int = 5) -> Dict[str, Any]:
        cached = self._cache.get(url)
        if cached:
            return {"cached": True, "payload": cached.payload.decode("utf-8")}
        payload = await self._fetch_with_retry(url)
        self._cache.set(url, payload.encode("utf-8"), ttl_minutes)
        return {"cached": False, "payload": payload}

    async def _fetch_with_retry(self, url: str) -> str:
        attempt = 0
        while True:
            attempt += 1
            try:
                if self._semaphore:
                    async with self._semaphore:
                        return await self._fetch(url)
                return await self._fetch(url)
            except Exception as exc:  # pragma: no cover - network failure branch
                LOGGER.warning("fetch_retry", url=url, attempt=attempt, error=str(exc))
                if attempt >= self._config.max_retries:
                    raise
                await asyncio.sleep(self._config.backoff_seconds * attempt)

    async def _fetch(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                response.raise_for_status()
                return await response.text()


__all__ = ["HttpFetcher", "FetchConfig"]
