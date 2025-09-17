"""Tests for the multi-timeframe gate module."""

from datetime import datetime, timedelta, timezone

from src.strategy.gates import GateInputs, MultiTimeframeGate


def test_multi_timeframe_gate_generates_candidate() -> None:
    gate = MultiTimeframeGate(ttl_seconds=120)
    created_at = datetime.now(tz=timezone.utc)
    inputs = GateInputs(
        symbol="XAUUSD",
        price=2000.0,
        timeframe_features={
            "HTF": {"ema_fast": 2010.0, "ema_slow": 1990.0, "adx": 25.0},
            "LTF": {"macd_hist": 0.8, "rsi": 62.0},
            "MTF": {"swing_low": 1985.0},
        },
        volume_features={"rel_volume": 0.85},
        orderflow_features={"imbalance": 0.35},
        ml_probability=0.72,
        created_at=created_at,
    )
    candidate = gate.evaluate(inputs)
    assert candidate is not None
    assert 0 <= candidate.confidence <= 1
    assert candidate.metadata["score_components"]["momentum"] > 0.5
    assert candidate.is_valid(created_at + timedelta(seconds=60))
    assert candidate.is_valid(created_at + timedelta(seconds=119))
    assert candidate.is_valid(created_at + timedelta(seconds=120)) is True
    assert candidate.is_valid(created_at + timedelta(seconds=121)) is False


def test_multi_timeframe_gate_rejects_when_confidence_low() -> None:
    gate = MultiTimeframeGate(ttl_seconds=60)
    inputs = GateInputs(
        symbol="XAUUSD",
        price=2000.0,
        timeframe_features={
            "HTF": {"ema_fast": 1990.0, "ema_slow": 2000.0, "adx": 12.0},
            "LTF": {"macd_hist": -0.3, "rsi": 30.0},
            "MTF": {},
        },
        volume_features={"rel_volume": 0.2},
        orderflow_features={"imbalance": -0.4},
        ml_probability=0.1,
        created_at=datetime.now(tz=timezone.utc),
    )
    assert gate.evaluate(inputs) is None
