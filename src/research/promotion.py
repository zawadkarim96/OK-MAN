"""Governance for promoting strategies."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import List

from structlog import get_logger

from src.common.types import ResearchIdea

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class PromotionDecision:
    promoted: List[str]
    rejected: List[str]


class PromotionManager:
    def decide(self, ideas: List[ResearchIdea]) -> PromotionDecision:
        promoted = [idea.name for idea in ideas if (idea.score or 0) > 0.7]
        rejected = [idea.name for idea in ideas if idea.name not in promoted]
        LOGGER.info("promotion_decision", promoted=promoted, rejected=rejected)
        return PromotionDecision(promoted=promoted, rejected=rejected)


def cli(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Promotion manager")
    parser.add_argument("--action", choices=["promote", "rollback"], default="promote")
    parser.add_argument("--release", default="latest")
    args = parser.parse_args(argv)
    LOGGER.info("promotion_cli", action=args.action, release=args.release)


if __name__ == "__main__":
    cli()
