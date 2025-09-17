"""Reviewer agent bridging to research reviewer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from structlog import get_logger

from src.common.types import ResearchIdea
from src.research.reviewer import ReviewResult, Reviewer

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class ReviewerAgent:
    reviewer: Reviewer

    def review(self, ideas: List[ResearchIdea]) -> List[ReviewResult]:
        results = [self.reviewer.review(idea) for idea in ideas]
        LOGGER.info("reviewer_agent", results=len(results))
        return results


__all__ = ["ReviewerAgent"]
