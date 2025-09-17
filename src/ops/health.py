"""Health check helpers."""

from __future__ import annotations

from typing import Dict


def check_services(status_map: Dict[str, bool]) -> bool:
    """Return True if all services healthy."""

    return all(status_map.values())


__all__ = ["check_services"]
