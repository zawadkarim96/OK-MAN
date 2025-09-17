# Risk Management

Risk is central to `ai-scalper-god`. The system balances Kelly-style position sizing with strict circuit breakers.

## Position Sizing

- Base fraction derived from capped Kelly formula using estimated edge and variance.
- Confidence multipliers scale down size when indicator or model certainty is low.
- Portfolio caps ensure correlated exposures remain within tolerance.

## Stops & Targets

- ATR-based stop default with optional volatility wideners per symbol.
- Automatic move to break-even at +1R with partial profit taking along the path.
- Trailing logic attaches to residual size using ATR or structure-based offsets.

## Circuit Breakers

- Daily drawdown and loss-streak halts disable new entries.
- Spread, latency, and slippage caps provide pre-trade vetoes.
- News filters from sentiment ingestion tighten or block trading around events.
