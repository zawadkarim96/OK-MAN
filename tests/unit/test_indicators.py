"""Unit tests covering lightweight indicator helpers."""

from src.common import indicators


def test_ema_basic() -> None:
    data = [1, 2, 3, 4, 5]
    value = indicators.ema(data, period=3)
    assert value > 0


def test_macd_returns_tuple() -> None:
    macd_line, signal_line, hist = indicators.macd([1, 2, 3, 4, 5, 6])
    assert isinstance(macd_line, float)
    assert isinstance(signal_line, float)
    assert isinstance(hist, float)
    assert hist == macd_line - signal_line
