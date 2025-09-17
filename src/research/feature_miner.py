"""Automatically mine candidate features from research corpus."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from structlog import get_logger

from .corpus_store import CorpusStore

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class FeatureIdea:
    name: str
    description: str


class FeatureMiner:
    def __init__(self, corpus: CorpusStore) -> None:
        self._corpus = corpus

    def discover(self, query: str) -> List[FeatureIdea]:
        documents = self._corpus.query(query)
        ideas = [FeatureIdea(name=f"feature_{idx}", description=doc[:120]) for idx, doc in enumerate(documents)]
        LOGGER.info("feature_miner_discover", count=len(ideas))
        return ideas


__all__ = ["FeatureMiner", "FeatureIdea"]
