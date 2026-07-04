.PHONY: install clean lint format test run pipeline all

PYTHON = python
PYTHONPATH = .

install:
	pip install -r requirements.txt

clean:
	rm -rf data/processed/*.csv data/exports/*.csv data/datamarts/**/*.csv
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
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/transformation/clean_transform.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/datamarts/build_datamarts.py
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/analysis/metrics.py

all: lint test pipeline
