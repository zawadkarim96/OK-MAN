"""Researcher agent using local LLM and corpus."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from structlog import get_logger

from src.common.types import ResearchIdea
from src.research.corpus_store import CorpusStore
from src.research.feature_miner import FeatureMiner

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class ResearcherConfig:
    query: str


class ResearcherAgent:
    def __init__(self, corpus: CorpusStore, config: ResearcherConfig) -> None:
        self._miner = FeatureMiner(corpus)
        self._config = config

    def run(self) -> List[ResearchIdea]:
        ideas = [
            ResearchIdea(
                name=f"auto_feature_{idx}",
                description=idea.description,
                proposed_by="researcher_agent",
                created_at=datetime.utcnow(),
                dsl_snippet="",
                tags=["feature"],
            )
            for idx, idea in enumerate(self._miner.discover(self._config.query))
        ]
        LOGGER.info("researcher_agent_run", count=len(ideas))
        return ideas


__all__ = ["ResearcherAgent", "ResearcherConfig"]
