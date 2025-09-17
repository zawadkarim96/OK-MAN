"""Bayesian optimisation stub."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

from bayes_opt import BayesianOptimization
from structlog import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class BayesOptConfig:
    init_points: int = 2
    n_iter: int = 5


def optimise(function: Callable[[float, float], float], bounds: Dict[str, tuple[float, float]]) -> Dict[str, float]:
    optimizer = BayesianOptimization(f=function, pbounds=bounds, verbose=0, allow_duplicate_points=True)
    optimizer.maximize(init_points=BayesOptConfig.init_points, n_iter=BayesOptConfig.n_iter)  # type: ignore[attr-defined]
    LOGGER.info("bayes_optimum", result=optimizer.max)
    return optimizer.max  # type: ignore[return-value]


__all__ = ["optimise"]
