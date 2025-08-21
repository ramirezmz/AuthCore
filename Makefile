.PHONY: run test lint

run:
	poetry run uvicorn app.main:app --reload

test:
	PYTHONPATH=. poetry run pytest

lint:
	PYTHONPATH=. poetry run black . && poetry run flake8 .

populate:
	PYTHONPATH=. poetry run python scripts/populate_db.py