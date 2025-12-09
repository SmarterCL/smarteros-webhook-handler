.PHONY: dev test coverage lint format clean

dev:
uvicorn src.main:app --reload --port 8000

test:
pytest tests/ -v

coverage:
pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:
ruff check src/ tests/
mypy src/

format:
black src/ tests/
ruff check --fix src/ tests/

clean:
rm -rf __pycache__ .pytest_cache .coverage htmlcov *.db
find . -type d -name __pycache__ -exec rm -rf {} +
