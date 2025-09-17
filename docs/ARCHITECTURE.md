# Architecture Overview

The system is organised into modular domains. Market and news data flow through ingest adapters into feature stores and regime classifiers before passing through the strategy layer and execution stack.

1. **Ingest** – `src/ingest/` handles tick, order book, macro feeds, and sentiment scoring. Data is normalised and published into the feature store.
2. **Regime Detection** – `src/regime/classifier.py` produces state labels (trend, range, volatile) consumed by strategies and risk modules.
3. **Strategy Layer** – `src/strategy/` contains confluence gates, symbol playbooks, strategy packs, and ensembles. Decisions are expressed as `SignalCandidate` objects.
4. **Risk & Execution** – `src/risk/` modules size positions, enforce drawdown limits, and set stops. `src/execution/` routes orders through MT5 or other venues with slippage tracking.
5. **Optimization & Research** – `src/optimize/` and `src/research/` implement continuous improvement via GA/GP, walk-forward tests, RL, and LLM-guided ideation.
6. **Ops & API** – `src/api/` exposes a FastAPI service for orchestration. `src/ops/` integrates logging, metrics, and health monitoring.

The complete lifecycle is: **Ingest → Feature Store → Regime → Gate → Playbook → Ensemble → Risk → Router → Bridge → MT5**. Observability flows to Prometheus and structured logs for auditability.
