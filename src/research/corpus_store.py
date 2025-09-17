"""Vector store for research documents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import chromadb


@dataclass(slots=True)
class Document:
    id: str
    content: str


class CorpusStore:
    """Store research documents and support similarity search."""

    def __init__(self, path: Path) -> None:
        self._client = chromadb.PersistentClient(path=str(path))
        self._collection = self._client.get_or_create_collection(name="research")

    def add(self, documents: List[Document]) -> None:
        self._collection.add(ids=[doc.id for doc in documents], documents=[doc.content for doc in documents])

    def query(self, text: str, top_k: int = 5) -> List[str]:
        result = self._collection.query(query_texts=[text], n_results=top_k)
        return list(result.get("documents", [[]])[0])


__all__ = ["CorpusStore", "Document"]
