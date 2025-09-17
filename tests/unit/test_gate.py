from datetime import datetime

from src.strategy.gates import GateInputs, MultiTimeframeGate


def test_multi_timeframe_gate_generates_candidate() -> None:
    gate = MultiTimeframeGate(ttl=2)
    inputs = GateInputs(
        symbol="XAUUSD",
        price=2000.0,
        timeframe_features={
            "HTF": {"ema_fast": 2010.0, "ema_slow": 1990.0, "adx": 25.0},
            "LTF": {"macd_hist": 0.5, "rsi": 55.0},
            "MTF": {"swing_low": 1985.0},
        },
        volume_features={"rel_volume": 0.8},
        orderflow_features={"imbalance": 0.2},
        ml_probability=0.7,
        created_at=datetime.utcnow(),
    )
    candidate = gate.evaluate(inputs)
    assert candidate is not None
    assert 0 <= candidate.confidence <= 1
