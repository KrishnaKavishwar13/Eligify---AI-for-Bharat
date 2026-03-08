.PHONY: install dev test lint format deploy clean

install:
	pip install -r requirements.txt

dev:
	uvicorn src.main:app --reload --port 8000

test:
	pytest

lint:
	flake8 src tests
	mypy src

format:
	black src tests

deploy:
	serverless deploy

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
