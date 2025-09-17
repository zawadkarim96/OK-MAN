# ai-scalper-god

`ai-scalper-god` is a research-grade template for a self-learning, ultra-low-latency scalping system designed for metals, indices, FX, and crypto. The repository stitches together ingest, analysis, risk, and execution layers with automated research and governance loops. All modules are implemented as typed Python skeletons with clear extension points for production deployments.

## Features

- Multi-timeframe confluence gates spanning technical analysis, order-flow, and machine learning predictors.
- Symbol-specific playbooks and strategy packs powered by a declarative Strategy DSL.
- Order-flow analytics with order book, tape, and microstructure signals.
- Continuous optimization via genetic programming, Bayesian search, reinforcement learning, and walk-forward validation.
- Local LLM-driven news sentiment, research ideation, and safety-aware auto-coding agents.
- FastAPI control plane with observability, Prometheus metrics, and CI/CD integration.

## Quick Start

```bash
make dev
```

The command installs dependencies, configures pre-commit hooks, and prepares local caches. Review `configs/` for runtime defaults and environment-specific overrides.

### Backtest

```bash
make backtest SYMBOL=XAUUSD CFG=configs/backtest.yaml
```

### Paper Trading / Bridge

```bash
make bridge   # Start MT5 bridge services
make run      # Launch live (paper) trading loop
```

### Research Automation

```bash
make researcher
```

This launches the always-online research daemon responsible for ideation, evaluation, and gated promotion of new strategies.

## Repository Layout

The repository mirrors the architecture described in `docs/ARCHITECTURE.md`. Core modules live under `src/`, configuration defaults reside in `configs/`, and tests are organised by scope under `tests/`.

## Contributing

1. Install dependencies via `make dev`.
2. Create a feature branch (outside the scope of automated agents).
3. Run `pre-commit run --all-files` and `pytest` before submitting pull requests.
4. Document changes in the appropriate markdown files under `docs/`.

## License

See [LICENSE](LICENSE) for licensing information.
