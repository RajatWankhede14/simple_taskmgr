.PHONY: help install run migrate migrations shell test lint format clean infra-up infra-down

help:
	@echo "Available commands:"
	@echo "  install      : Install dependencies"
	@echo "  run          : Run the development server"
	@echo "  migrate      : Apply database migrations"
	@echo "  migrations   : Create new database migrations"
	@echo "  shell        : Open Django shell"
	@echo "  test         : Run tests"
	@echo "  lint         : Run ruff lint check"
	@echo "  format       : Run ruff formatter"
	@echo "  infra-up     : Start docker-compose infrastructure (DB, Redis)"
	@echo "  infra-down   : Stop docker-compose infrastructure"
	@echo "  clean        : Remove pyc files and cache"

install:
	pip install .

run:
	python manage.py runserver

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

shell:
	python manage.py shell

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

infra-up:
	docker-compose up -d

infra-down:
	docker-compose down

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf staticfiles
