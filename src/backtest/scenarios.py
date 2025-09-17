"""Stress test scenario definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(slots=True)
class Scenario:
    name: str
    description: str
    start: str
    end: str


SCENARIOS: List[Scenario] = [
    Scenario(name="2008-crisis", description="Financial crisis volatility", start="2008-09-01", end="2008-12-31"),
    Scenario(name="2010-flash-crash", description="Flash crash event", start="2010-05-01", end="2010-05-15"),
    Scenario(name="2020-pandemic", description="COVID-19 volatility", start="2020-02-15", end="2020-04-30"),
]


def get_scenario(name: str) -> Scenario:
    for scenario in SCENARIOS:
        if scenario.name == name:
            return scenario
    raise KeyError(name)


__all__ = ["Scenario", "SCENARIOS", "get_scenario"]
