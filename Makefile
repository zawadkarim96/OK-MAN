PYTHON ?= python3
PIP ?= pip
VENV ?= .venv
ACTIVATE = source $(VENV)/bin/activate

.PHONY: dev install format lint test backtest bridge api optimize run researcher paper promote rollback

dev: $(VENV)/bin/activate
$(PYTHON) -m venv $(VENV)
$(ACTIVATE) && $(PIP) install --upgrade pip
$(ACTIVATE) && $(PIP) install -r requirements.txt
$(ACTIVATE) && pre-commit install

install:
$(PIP) install -r requirements.txt

format:
$(ACTIVATE) && ruff format src tests

lint:
$(ACTIVATE) && ruff check src tests
$(ACTIVATE) && mypy src

test:
$(ACTIVATE) && pytest

backtest:
$(ACTIVATE) && $(PYTHON) -m src.backtest.engine --config $(CFG) --symbol $(SYMBOL)

bridge:
$(ACTIVATE) && $(PYTHON) -m src.execution.mt5_bridge.bridge

api:
$(ACTIVATE) && uvicorn src.api.server:app --host 0.0.0.0 --port 8080

optimize:
$(ACTIVATE) && $(PYTHON) -m src.optimize.ga_gp

run:
$(ACTIVATE) && $(PYTHON) -m src.strategy.signal_ensemble --mode live

researcher:
$(ACTIVATE) && $(PYTHON) -m src.research.sandbox_runner

paper:
$(ACTIVATE) && $(PYTHON) -m src.strategy.signal_ensemble --mode paper

promote:
$(ACTIVATE) && $(PYTHON) -m src.research.promotion --action promote

rollback:
$(ACTIVATE) && $(PYTHON) -m src.research.promotion --action rollback --release $(RELEASE)
