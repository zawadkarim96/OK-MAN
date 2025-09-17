"""Genetic algorithm optimisation stubs."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Dict, List

from deap import base, creator, tools
from structlog import get_logger

LOGGER = get_logger(__name__)


def _objective(individual: List[float], evaluator: Callable[[List[float]], float]) -> tuple[float]:
    return (evaluator(individual),)


@dataclass(slots=True)
class GAConfig:
    population: int = 20
    generations: int = 5
    cx_prob: float = 0.7
    mut_prob: float = 0.2


class StrategyOptimizer:
    """Run a basic GA to tune strategy weights."""

    def __init__(self, config: GAConfig | None = None) -> None:
        self._config = config or GAConfig()
        if not hasattr(creator, "FitnessMax"):
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # type: ignore[arg-type]
        if not hasattr(creator, "Individual"):
            creator.create("Individual", list, fitness=creator.FitnessMax)  # type: ignore[attr-defined]

    def optimise(self, evaluator: Callable[[List[float]], float], dimensions: int) -> Dict[str, List[float]]:
        toolbox = base.Toolbox()
        toolbox.register("individual", tools.initIterate, creator.Individual, lambda: [0.5] * dimensions)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", _objective, evaluator=evaluator)
        toolbox.register("mate", tools.cxBlend, alpha=0.5)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)

        population = toolbox.population(n=self._config.population)
        for _ in range(self._config.generations):
            offspring = toolbox.select(population, len(population))
            offspring = list(map(toolbox.clone, offspring))
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self._config.cx_prob:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            for mutant in offspring:
                if random.random() < self._config.mut_prob:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
            invalid = [ind for ind in offspring if not ind.fitness.valid]
            for ind in invalid:
                ind.fitness.values = toolbox.evaluate(ind)
            population[:] = offspring
        best = tools.selBest(population, 1)[0]
        LOGGER.info("ga_optimum", fitness=best.fitness.values)
        return {"weights": list(best)}


def main() -> None:
    LOGGER.info("ga_gp_placeholder_run")


if __name__ == "__main__":
    main()
