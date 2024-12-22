# Makefile for Finance Tracker

.PHONY: help clean test lint docs install dev-install

# Variables
PYTHON = python3
PIP = $(PYTHON) -m pip
PYTEST = pytest
SPHINX = sphinx-build
BLACK = black
ISORT = isort
FLAKE8 = flake8
MYPY = mypy

help:
	@echo "Finance Tracker development commands:"
	@echo "make install      - Install production dependencies"
	@echo "make dev-install  - Install development dependencies"
	@echo "make test        - Run tests"
	@echo "make coverage    - Run tests with coverage report"
	@echo "make lint        - Run code quality checks"
	@echo "make format      - Format code with black and isort"
	@echo "make docs        - Build documentation"
	@echo "make clean       - Clean build artifacts"
	@echo "make run         - Run the application"

install:
	$(PIP) install -r requirements.txt

dev-install:
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	pre-commit install

test:
	$(PYTEST)

coverage:
	$(PYTEST) --cov=src tests/ --cov-report=html

lint:
	$(BLACK) --check src/ tests/
	$(ISORT) --check-only src/ tests/
	$(FLAKE8) src/ tests/
	$(MYPY) src/

format:
	$(BLACK) src/ tests/
	$(ISORT) src/ tests/

docs:
	$(SPHINX) -b html docs/ docs/_build/html

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf docs/_build
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

run:
	$(PYTHON) src/main.py

# Database commands
db-init:
	$(PYTHON) -m src.utils.db_utils --init

db-reset:
	$(PYTHON) -m src.utils.db_utils --reset

db-migrate:
	$(PYTHON) -m src.utils.db_utils --migrate

# Development helpers
dev-setup: dev-install db-init
	@echo "Development environment setup complete"

check: lint test
	@echo "All checks passed"

# Documentation helpers
docs-live:
	$(SPHINX) -b html docs/ docs/_build/html -W -a -E -n -b html
