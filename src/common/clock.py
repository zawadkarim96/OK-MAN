"""Trading calendar and clock utilities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timezone
from typing import Dict

import pytz


@dataclass(slots=True)
class SessionWindow:
    """Represents a trading session in local exchange time."""

    name: str
    start: time
    end: time

    def contains(self, dt: datetime) -> bool:
        """Return whether *dt* falls inside the session (inclusive)."""

        current = dt.time()
        return self.start <= current <= self.end


class TradingClock:
    """Utility wrapper to evaluate session windows with timezone awareness."""

    def __init__(self, timezone_name: str, sessions: Dict[str, Dict[str, str]]) -> None:
        self._tz = pytz.timezone(timezone_name)
        self._sessions = {
            name: SessionWindow(name=name, start=_parse_time(info["start"]), end=_parse_time(info["end"]))
            for name, info in sessions.items()
        }

    def now(self) -> datetime:
        """Return the current time in the configured timezone."""

        return datetime.now(tz=self._tz)

    def active_sessions(self, dt: datetime | None = None) -> Dict[str, SessionWindow]:
        """Return sessions active at *dt* (defaults to :meth:`now`)."""

        moment = dt or self.now()
        return {name: window for name, window in self._sessions.items() if window.contains(moment)}


def _parse_time(value: str) -> time:
    hour, minute = (int(part) for part in value.split(":", maxsplit=1))
    return time(hour=hour, minute=minute, tzinfo=timezone.utc)


__all__ = ["TradingClock", "SessionWindow"]
