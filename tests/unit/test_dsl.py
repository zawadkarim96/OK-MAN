from pathlib import Path

from src.strategy.dsl import StrategyDSLParser


def test_strategy_dsl_parser_loads(tmp_path: Path) -> None:
    content = """
{"strategies": [{"name": "test", "regime_allow": ["trend"], "features": [], "trigger": {"all": []}, "filters": {"all": []}, "entry": {"type": "market"}, "exit": {"stop": "test"}, "risk": {"method": "test"}, "routing": {"prefer": "market"}}]}
"""
    path = tmp_path / "strategies.yaml"
    path.write_text(content)
    parser = StrategyDSLParser(path)
    result = parser.parse()
    assert result[0].name == "test"
