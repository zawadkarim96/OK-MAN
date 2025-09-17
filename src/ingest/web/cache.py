"""Simple SQLite-backed cache for HTTP fetchers."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator, Optional


@dataclass(slots=True)
class CacheEntry:
    """Represents a cached payload."""

    url: str
    payload: bytes
    expires_at: datetime


class WebCache:
    """SQLite cache with TTL-based eviction."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._ensure_schema()

    @contextmanager
    def _connect(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self._path)
        try:
            yield conn
        finally:
            conn.close()

    def _ensure_schema(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    url TEXT PRIMARY KEY,
                    payload BLOB NOT NULL,
                    expires_at TIMESTAMP NOT NULL
                )
                """
            )
            conn.commit()

    def set(self, url: str, payload: bytes, ttl_minutes: int) -> None:
        expires = datetime.utcnow() + timedelta(minutes=ttl_minutes)
        with self._connect() as conn:
            conn.execute(
                "REPLACE INTO cache(url, payload, expires_at) VALUES(?,?,?)",
                (url, payload, expires.isoformat()),
            )
            conn.commit()

    def get(self, url: str) -> Optional[CacheEntry]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT payload, expires_at FROM cache WHERE url=?", (url,))
            row = cursor.fetchone()
        if row is None:
            return None
        payload, expires_at_str = row
        expires_at = datetime.fromisoformat(expires_at_str)
        if expires_at < datetime.utcnow():
            self.delete(url)
            return None
        return CacheEntry(url=url, payload=payload, expires_at=expires_at)

    def delete(self, url: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM cache WHERE url=?", (url,))
            conn.commit()


__all__ = ["WebCache", "CacheEntry"]
