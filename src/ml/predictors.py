"""Machine learning predictors for short-horizon forecasting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class PredictorResult:
    probability_up: float
    probability_down: float


class SimpleMomentumPredictor:
    """Minimal predictor using momentum heuristics as placeholder."""

    def predict(self, returns: Iterable[float]) -> PredictorResult:
        values = list(returns)
        if not values:
            return PredictorResult(probability_up=0.5, probability_down=0.5)
        mean_return = float(np.mean(values))
        prob_up = 0.5 + np.tanh(mean_return)
        prob_up = max(0.0, min(1.0, prob_up))
        return PredictorResult(probability_up=prob_up, probability_down=1 - prob_up)


__all__ = ["SimpleMomentumPredictor", "PredictorResult"]
