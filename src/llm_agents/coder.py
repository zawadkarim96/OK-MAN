"""Coder agent producing code diffs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from structlog import get_logger

from src.security.policy import Policy

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class CodeChange:
    path: Path
    content: str


@dataclass(slots=True)
class CoderAgent:
    policy: Policy

    def generate(self, prompt: str) -> List[CodeChange]:
        LOGGER.info("coder_agent_prompt", prompt=prompt[:80])
        # TODO: integrate with local LLM; placeholder returns no changes.
        return []


__all__ = ["CoderAgent", "CodeChange"]
