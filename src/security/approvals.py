"""Approval workflow for new strategies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from structlog import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class ApprovalRecord:
    strategy: str
    approved: bool
    reviewer: str


class ApprovalWorkflow:
    def __init__(self) -> None:
        self._records: List[ApprovalRecord] = []

    def record(self, strategy: str, approved: bool, reviewer: str) -> None:
        record = ApprovalRecord(strategy=strategy, approved=approved, reviewer=reviewer)
        self._records.append(record)
        LOGGER.info("approval_record", record=record)

    def last(self) -> ApprovalRecord | None:
        return self._records[-1] if self._records else None


__all__ = ["ApprovalWorkflow", "ApprovalRecord"]
