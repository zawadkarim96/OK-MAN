"""LLM-driven strategy idea generator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from structlog import get_logger

from src.common.types import ResearchIdea
from src.ingest.sentiment_llm import SentimentModel

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class StrategistConfig:
    prompt: str


class Strategist:
    def __init__(self, model: SentimentModel, config: StrategistConfig) -> None:
        self._model = model
        self._config = config

    def ideate(self, seed_text: str) -> List[ResearchIdea]:
        result = self._model.score(seed_text, prompt=self._config.prompt)
        idea = ResearchIdea(
            name=f"idea_{abs(hash(seed_text)) % 1000}",
            description=seed_text[:200],
            proposed_by="strategist",
            created_at=datetime.utcnow(),
            dsl_snippet="",
            tags=["auto"],
            score=result.sentiment,
        )
        LOGGER.info("strategist_ideate", idea=idea)
        return [idea]


__all__ = ["Strategist", "StrategistConfig"]
