"""Tests for the Strategy DSL parser."""

from pathlib import Path

import pytest

from src.strategy.dsl import StrategyDSLParser


def test_strategy_dsl_parser_loads(tmp_path: Path) -> None:
    content = """
{"schema_version": 1, "strategies": [{"name": "test", "regime_allow": ["trend"], "features": [{}], "trigger": {"all": ["expr"]}, "filters": {"all": ["expr"]}, "entry": {"type": "market"}, "exit": {"stop": "test"}, "risk": {"method": "test"}, "routing": {"prefer": "market"}}]}
"""
    path = tmp_path / "strategies.yaml"
    path.write_text(content)
    parser = StrategyDSLParser(path)
    result = parser.parse()
    assert result[0].name == "test"
    assert result[0].regimes[0].value == "trend"
    assert result[0].trigger["all"] == ["expr"]


def test_strategy_dsl_parser_rejects_unknown_regime(tmp_path: Path) -> None:
    content = """
{"strategies": [{"name": "test", "regime_allow": ["invalid"], "features": [], "trigger": {"all": []}, "filters": {"all": []}, "entry": {"type": "market"}, "exit": {"stop": "test"}, "risk": {"method": "test"}, "routing": {"prefer": "market"}}]}
"""
    path = tmp_path / "strategies.yaml"
    path.write_text(content)
    parser = StrategyDSLParser(path)
    with pytest.raises(ValueError):
        parser.parse()
