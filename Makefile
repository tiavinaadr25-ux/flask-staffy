PYTHON ?= ./.venv/bin/python

.PHONY: format lint test run init-db seed-demo up down

format:
	$(PYTHON) -m black app.py staffly tests

lint:
	$(PYTHON) -m flake8 app.py staffly tests

test:
	$(PYTHON) -m pytest -q

run:
	$(PYTHON) -m flask --app app run

init-db:
	$(PYTHON) -m flask --app app init-db

seed-demo:
	$(PYTHON) -m flask --app app seed-demo-data

up:
	docker compose up --build

down:
	docker compose down
