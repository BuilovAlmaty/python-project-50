#Makefile
.PHONY: install test lint check build

install:
	uv pip install -e .[dev]

gendiff: # запуск проекта
	uv run gendiff

build: # сборка пакета
	uv build

package-install: # установка пакета
	uv tool install dist/*.whl

test:
	uv run pytest -s -v

lint:
	ruff check .

check:
	test lint

lint-fix:
	uv run ruff check . --fix
