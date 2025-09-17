"""LLM reviewer for strategy safety."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from structlog import get_logger

from src.common.types import ResearchIdea

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class ReviewResult:
    idea: ResearchIdea
    approved: bool
    notes: List[str]


class Reviewer:
    def review(self, idea: ResearchIdea) -> ReviewResult:
        notes = []
        approved = True
        if "martingale" in idea.description.lower():
            notes.append("Reject: martingale detected")
            approved = False
        LOGGER.info("reviewer_result", idea=idea.name, approved=approved)
        return ReviewResult(idea=idea, approved=approved, notes=notes)


__all__ = ["Reviewer", "ReviewResult"]
