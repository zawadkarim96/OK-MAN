"""Technical indicator calculations used throughout the project."""

from __future__ import annotations

from typing import Iterable, List, Tuple


def _to_list(series: Iterable[float]) -> List[float]:
    return [float(value) for value in series]


def ema(series: Iterable[float], period: int) -> float:
    values = _to_list(series)
    if not values:
        return 0.0
    k = 2 / (period + 1)
    ema_value = values[0]
    for value in values[1:]:
        ema_value = value * k + ema_value * (1 - k)
    return ema_value


def rsi(series: Iterable[float], period: int = 14) -> float:
    values = _to_list(series)
    if len(values) <= period:
        return 50.0
    gains = []
    losses = []
    for prev, curr in zip(values[:-1], values[1:]):
        change = curr - prev
        if change > 0:
            gains.append(change)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(-change)
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def atr(high: Iterable[float], low: Iterable[float], close: Iterable[float], period: int = 14) -> float:
    highs = _to_list(high)
    lows = _to_list(low)
    closes = _to_list(close)
    if len(highs) < 2 or len(highs) != len(lows) or len(highs) != len(closes):
        return 0.0
    trs: List[float] = []
    for i in range(1, len(highs)):
        hl = highs[i] - lows[i]
        hc = abs(highs[i] - closes[i - 1])
        lc = abs(lows[i] - closes[i - 1])
        trs.append(max(hl, hc, lc))
    if len(trs) < period:
        return sum(trs) / max(len(trs), 1)
    return sum(trs[-period:]) / period


def adx(high: Iterable[float], low: Iterable[float], close: Iterable[float], period: int = 14) -> float:
    highs = _to_list(high)
    lows = _to_list(low)
    closes = _to_list(close)
    if len(highs) <= period:
        return 0.0
    dm_plus: List[float] = []
    dm_minus: List[float] = []
    trs: List[float] = []
    for i in range(1, len(highs)):
        up_move = highs[i] - highs[i - 1]
        down_move = lows[i - 1] - lows[i]
        dm_plus.append(up_move if up_move > down_move and up_move > 0 else 0.0)
        dm_minus.append(down_move if down_move > up_move and down_move > 0 else 0.0)
        trs.append(max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1])))
    tr_avg = sum(trs[-period:]) / period if len(trs) >= period else sum(trs) / max(len(trs), 1)
    if tr_avg == 0:
        return 0.0
    di_plus = (sum(dm_plus[-period:]) / period) / tr_avg * 100
    di_minus = (sum(dm_minus[-period:]) / period) / tr_avg * 100
    if di_plus + di_minus == 0:
        return 0.0
    dx = abs(di_plus - di_minus) / (di_plus + di_minus) * 100
    return dx


def macd(series: Iterable[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[float, float, float]:
    values = _to_list(series)
    if not values:
        return 0.0, 0.0, 0.0
    macd_values = []
    for i in range(len(values)):
        macd_values.append(ema(values[: i + 1], fast) - ema(values[: i + 1], slow))
    macd_line = macd_values[-1]
    signal_line = ema(macd_values, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


__all__ = ["ema", "rsi", "atr", "adx", "macd"]
