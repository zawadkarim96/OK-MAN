"""Dependency and code scanner stubs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from structlog import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class ScanIssue:
    severity: str
    description: str


def scan_dependencies(requirements: List[str]) -> List[ScanIssue]:
    LOGGER.info("scan_dependencies", count=len(requirements))
    return []


__all__ = ["ScanIssue", "scan_dependencies"]
