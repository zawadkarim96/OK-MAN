"""Strategy ensemble logic combining TA, ML, order-flow, and sentiment."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, Iterable, Optional

from structlog import get_logger

from src.common.types import SignalCandidate
from src.strategy.playbooks import btcusd, eurusd, gbpjpy, us100, xauusd

LOGGER = get_logger(__name__)

PLAYBOOKS = {
    "XAUUSD": xauusd,
    "US100": us100,
    "BTCUSD": btcusd,
    "GBPJPY": gbpjpy,
    "EURUSD": eurusd,
}


@dataclass(slots=True)
class EnsembleInputs:
    """Inputs feeding the ensemble scoring function."""

    candidate: SignalCandidate
    orderflow_score: float
    ml_probability: Optional[float]
    sentiment_bias: float
    feature_overrides: Dict[str, float]


class SignalEnsemble:
    """Combine multiple signals into a final confidence and position size factor."""

    def __init__(self, weight_ta: float = 0.3, weight_orderflow: float = 0.3, weight_ml: float = 0.2, weight_sentiment: float = 0.2) -> None:
        total = weight_ta + weight_orderflow + weight_ml + weight_sentiment
        if total == 0:
            raise ValueError("Weights must sum to a positive value")
        self._weights = {
            "ta": weight_ta / total,
            "orderflow": weight_orderflow / total,
            "ml": weight_ml / total,
            "sentiment": weight_sentiment / total,
        }

    def combine(self, inputs: EnsembleInputs) -> SignalCandidate:
        """Blend scores and return an updated candidate."""

        base = inputs.candidate.confidence * self._weights["ta"]
        orderflow_component = inputs.orderflow_score * self._weights["orderflow"]
        ml_component = (inputs.ml_probability or inputs.candidate.confidence) * self._weights["ml"]
        sentiment_component = (inputs.sentiment_bias + 1) / 2 * self._weights["sentiment"]
        combined_confidence = base + orderflow_component + ml_component + sentiment_component
        adjusted_confidence = self._apply_playbook(inputs.candidate, inputs.feature_overrides, combined_confidence)
        return SignalCandidate(
            symbol=inputs.candidate.symbol,
            direction=inputs.candidate.direction,
            confidence=max(0.0, min(1.0, adjusted_confidence)),
            ttl=inputs.candidate.ttl,
            invalidation=inputs.candidate.invalidation,
            strategy=inputs.candidate.strategy,
            metadata=inputs.candidate.metadata,
        )

    def _apply_playbook(self, candidate: SignalCandidate, features: Dict[str, float], confidence: float) -> float:
        module = PLAYBOOKS.get(candidate.symbol.upper())
        if module is None:
            return confidence
        adjusted_candidate = SignalCandidate(
            symbol=candidate.symbol,
            direction=candidate.direction,
            confidence=confidence,
            ttl=candidate.ttl,
            invalidation=candidate.invalidation,
            strategy=candidate.strategy,
            metadata=candidate.metadata,
        )
        return module.score(adjusted_candidate, features)


def run_mode(mode: str) -> None:
    """Entry point triggered by :mod:`argparse` commands."""

    LOGGER.info("signal_ensemble_run", mode=mode)
    # TODO: wire real services. For now we log the mode for integration tests.


def main(argv: Optional[Iterable[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Signal ensemble runner")
    parser.add_argument("--mode", choices=["live", "paper"], default="paper")
    args = parser.parse_args(list(argv) if argv is not None else None)
    run_mode(args.mode)


if __name__ == "__main__":
    main()
