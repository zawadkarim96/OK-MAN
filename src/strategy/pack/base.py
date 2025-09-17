"""Strategy pack interface definition used by DSL compiler."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List


class StrategyPack(ABC):
    """Abstract base class for declarative strategy packs."""

    name: str

    @abstractmethod
    def features(self) -> List[Dict[str, str]]:
        """Return a description of required features."""

    @abstractmethod
    def trigger(self) -> Dict[str, List[str]]:
        """Return trigger expressions for DSL runtime."""

    @abstractmethod
    def filters(self) -> Dict[str, List[str]]:
        """Return additional filter expressions."""

    @abstractmethod
    def entry(self) -> Dict[str, str | int | float | List[Dict[str, float]]]:
        """Return entry configuration."""

    @abstractmethod
    def exit(self) -> Dict[str, str | float | List[Dict[str, float]]]:
        """Return exit configuration."""

    @abstractmethod
    def risk_profile(self) -> Dict[str, float | str]:
        """Return risk metadata."""

    @abstractmethod
    def routing_profile(self) -> Dict[str, str | float]:
        """Return routing preferences."""

    def to_dict(self) -> Dict[str, object]:
        """Return the entire pack configuration as a dictionary."""

        return {
            "name": self.name,
            "features": self.features(),
            "trigger": self.trigger(),
            "filters": self.filters(),
            "entry": self.entry(),
            "exit": self.exit(),
            "risk": self.risk_profile(),
            "routing": self.routing_profile(),
        }


__all__ = ["StrategyPack"]
