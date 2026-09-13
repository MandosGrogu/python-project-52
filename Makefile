install:
	pip install uv
	pip install gunicorn uvicorn

build:
	./build.sh

setup: install collectstatic migrate

render-start:
	gunicorn task_manager.wsgi

sync:
	uv sync

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --no-input

check:
	uv run ruff check

start:
	python manage.py runserver