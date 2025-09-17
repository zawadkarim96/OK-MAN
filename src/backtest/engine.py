"""Backtest engine wrapper."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from structlog import get_logger

LOGGER = get_logger(__name__)


@dataclass(slots=True)
class BacktestConfig:
    engine: str
    symbol: str


def run_backtest(config: BacktestConfig) -> Dict[str, float]:
    """Placeholder backtest routine returning mock metrics."""

    LOGGER.info("run_backtest", engine=config.engine, symbol=config.symbol)
    return {"win_rate": 0.8, "profit_factor": 2.1, "max_drawdown": -0.03}


def cli(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Backtest runner")
    parser.add_argument("--config", required=True)
    parser.add_argument("--symbol", required=True)
    args = parser.parse_args(argv)
    config_path = Path(args.config)
    config = BacktestConfig(engine="vectorbt", symbol=args.symbol)
    metrics = run_backtest(config)
    LOGGER.info("backtest_metrics", metrics=metrics, config_file=str(config_path))


if __name__ == "__main__":
    cli()
