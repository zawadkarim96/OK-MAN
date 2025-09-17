"""Backtest engine smoke tests."""

from src.backtest.engine import BacktestConfig, run_backtest


def test_backtest_win_rate_above_threshold() -> None:
    config = BacktestConfig(engine="vectorbt", symbol="XAUUSD")
    metrics = run_backtest(config)
    assert metrics["win_rate"] >= 0.75
    assert metrics["profit_factor"] > 1.0
