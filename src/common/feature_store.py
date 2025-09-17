"""Feature store to share computed indicators across modules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from threading import RLock
from typing import Any, Dict, Tuple

from .types import FeatureWindow


@dataclass(slots=True)
class FeatureEntry:
    """Internal representation of a feature stored in memory."""

    window: FeatureWindow


class FeatureStore:
    """Thread-safe in-memory store for computed features."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._data: Dict[Tuple[str, str], FeatureEntry] = {}

    def upsert(self, feature: FeatureWindow) -> None:
        with self._lock:
            self._data[(feature.name, feature.timeframe)] = FeatureEntry(window=feature)

    def get(self, name: str, timeframe: str) -> FeatureWindow | None:
        with self._lock:
            entry = self._data.get((name, timeframe))
            return entry.window if entry else None

    def latest_values(self, timeframe: str) -> Dict[str, Any]:
        with self._lock:
            return {
                name: entry.window.value
                for (name, tf), entry in self._data.items()
                if tf == timeframe
            }

    def purge_older_than(self, timestamp: datetime) -> None:
        with self._lock:
            keys_to_remove = [key for key, entry in self._data.items() if entry.window.timestamp < timestamp]
            for key in keys_to_remove:
                self._data.pop(key, None)

    def persist(self) -> None:
        """TODO: Persist the feature store to disk or external database."""

    def load(self) -> None:
        """TODO: Reload persisted features for warm start."""


__all__ = ["FeatureStore", "FeatureEntry"]
