"""Risk management utility tests."""

from src.common.types import RiskLimits
from src.risk.limits import LimitEvaluator
from src.risk.sizing import KellyConfig, confidence_scaled_size, kelly_fraction


def test_kelly_fraction_caps() -> None:
    config = KellyConfig(max_fraction=0.02, floor_fraction=0.001)
    fraction = kelly_fraction(edge=2.0, win_rate=0.6, config=config)
    assert 0.0 < fraction <= config.max_fraction


def test_limit_evaluator_blocks_when_limits_hit() -> None:
    limits = RiskLimits(
        daily_drawdown_pct=1.0,
        max_losing_streak=2,
        correlation_limit=0.5,
        spread_cap_bps=10,
        latency_cap_ms=200,
    )
    evaluator = LimitEvaluator(limits)
    evaluator.record_trade(-0.6)
    evaluator.record_trade(-0.6)
    assert evaluator.can_trade({"spread_bps": 5, "latency_ms": 100}) is False


def test_confidence_scaled_size() -> None:
    size = confidence_scaled_size(confidence=0.5, base_fraction=0.01, notional=100000)
    assert size == 500.0
