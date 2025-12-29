.PHONY: help install test lint format check clean dev up down logs cli

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make cli        - Show CLI help"
	@echo "  make health     - Check n8n health"
	@echo "  make validate   - Validate configuration"
	@echo "  make info       - Show environment info"
	@echo "  make test       - Run tests with coverage"
	@echo "  make lint       - Run ruff linter"
	@echo "  make format     - Format code with ruff and black"
	@echo "  make check      - Run all checks (lint + test)"
	@echo "  make clean      - Clean up generated files"
	@echo "  make dev        - Start local development environment"
	@echo "  make up         - Start docker-compose services"
	@echo "  make down       - Stop docker-compose services"
	@echo "  make logs       - View docker-compose logs"

cli:
	python cli.py --help

health:
	python cli.py health

validate:
	python cli.py validate

info:
	python cli.py info

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test:
	python cli.py test --coverage

test-unit:
	python cli.py test --unit

test-integration:
	python cli.py test --integration

lint:
	python cli.py lint

format:
	python cli.py format

check:
	python cli.py lint
	python cli.py test --coverage

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
