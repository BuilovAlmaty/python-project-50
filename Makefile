#Makefile
.PHONY: install reinstall

install:
	uv tool uninstall gendiff || true
	uv tool install -e .
install:
	uv tool install -e .

gendiff: # запуск проекта
	uv run gendiff

build: # сборка пакета
	uv build

package-install: # установка пакета
	uv tool install dist/*.whl

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix
