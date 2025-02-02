.PHONY: up start install help

PYTHON = python3
SRC_DIR = src

# Запуск монго и постгрес
up:
	@docker compose up -d --build
	@bash ./mongo/init.sh

# Остановка монго и постгрес
down:
	@docker compose down


# Вывод справки
help:
	@echo "Доступные команды:"
	@echo "  make up                  - Запуск монго и постгрес"
	@echo "  make down                - Остановка монго и постгрес"
