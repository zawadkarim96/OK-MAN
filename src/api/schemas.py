"""Lightweight schema definitions without external dependencies."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(slots=True)
class HealthResponse:
    status: str


@dataclass(slots=True)
class StrategyRunRequest:
    mode: str


@dataclass(slots=True)
class BridgeCommand:
    command: str
    payload: Dict[str, str] = field(default_factory=dict)
