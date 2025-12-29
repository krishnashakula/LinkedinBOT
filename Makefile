.PHONY: help install test lint format check clean dev up down logs

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests with coverage"
	@echo "  make lint       - Run ruff linter"
	@echo "  make format     - Format code with ruff and black"
	@echo "  make check      - Run all checks (lint + test)"
	@echo "  make clean      - Clean up generated files"
	@echo "  make dev        - Start local development environment"
	@echo "  make up         - Start docker-compose services"
	@echo "  make down       - Stop docker-compose services"
	@echo "  make logs       - View docker-compose logs"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest tests/ -v --cov --cov-report=term-missing --cov-report=html

test-unit:
	pytest tests/unit/ -v -m unit

test-integration:
	pytest tests/integration/ -v -m integration

lint:
	ruff check src/ tests/
	mypy src/ tests/

format:
	ruff check --fix src/ tests/
	black src/ tests/

check: lint test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/ .coverage coverage.xml

dev:
	docker-compose up --build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f n8n
