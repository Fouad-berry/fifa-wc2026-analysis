.PHONY: install clean lint format test run pipeline all cli-all

PYTHON = python
PYTHONPATH = .

install:
	pip install -r requirements.txt

clean:
	find data/processed data/exports -name '*.csv' -exec rm -f {} +
	find data/datamarts -mindepth 2 -name '*.csv' -exec rm -f {} +
	find figures -name '*.png' -exec rm -f {} +
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

lint:
	flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503

format:
	black --line-length=100 src/ tests/
	isort --profile black --line-length=100 src/ tests/

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest tests/ -v --cov=src/ --cov-report=term

run: pipeline

pipeline:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/ingestion/load_data.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/transformation/clean_transform.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/datamarts/build_datamarts.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/analysis/metrics.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/analysis/profiling.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/analysis/viz.py

cli-all:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) cli.py all

all: lint test pipeline
