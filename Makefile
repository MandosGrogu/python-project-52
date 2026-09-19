install:
	pip install uv
	pip install gunicorn uvicorn
	pip install django
	pip install django-filter
	pip install dj-database-url
	pip install tailwind
	pip install django-tailwind-cli

build:
	./build.sh

setup: install collectstatic migrate

render-start:
	gunicorn task_manager.wsgi

sync:
	uv sync

makemigrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

build-styles:
	uv run manage.py tailwind build

collectstatic:
	uv run manage.py collectstatic --no-input

check:
	uv run ruff check

start:
	uv run manage.py runserver