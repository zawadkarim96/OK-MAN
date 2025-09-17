"""Prometheus metrics exporters."""

from __future__ import annotations

from prometheus_client import Counter, Gauge

research_cycle_duration = Gauge("research_cycle_duration_seconds", "Duration of research cycles")
ideas_generated_total = Counter("ideas_generated_total", "Total ideas generated")
ideas_accepted_total = Counter("ideas_accepted_total", "Ideas accepted for promotion")
ideas_rejected_total = Counter("ideas_rejected_total", "Ideas rejected")
oos_win_rate = Gauge("oos_win_rate", "Out-of-sample win rate")
profit_factor = Gauge("profit_factor", "Profit factor from evaluations")
max_drawdown = Gauge("max_drawdown", "Maximum drawdown observed")
api_rate_limit_hits = Counter("api_rate_limit_hits", "API rate limit hits")
cache_hit_ratio = Gauge("cache_hit_ratio", "Cache hit ratio for web fetchers")
