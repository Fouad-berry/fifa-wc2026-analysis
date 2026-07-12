.PHONY: install clean lint format typecheck test run pipeline all cli-all

PYTHON ?= python3
PYTHONPATH = .

install:
	pip install -e .
	pip install -e ".[dev]"

clean:
	find data/processed data/exports -name '*.csv' -exec rm -f {} +
	find data/datamarts -mindepth 2 -name '*.csv' -exec rm -f {} +
	find figures -name '*.png' -exec rm -f {} +
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

lint:
	$(PYTHON) -m flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503

format:
	$(PYTHON) -m black --line-length=100 src/ tests/
	$(PYTHON) -m isort --profile black --line-length=100 src/ tests/

typecheck:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m mypy src/ tests/ --no-error-summary

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest tests/ -v --cov=src/ --cov-report=term

run: pipeline

pipeline: cli-all

cli-all:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) cli.py all

all: lint typecheck test pipeline
