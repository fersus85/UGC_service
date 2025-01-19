.PHONY: up install install-dev lint format help

PYTHON = python3
BLACK_LINE_LENGTH = --line-length 79
SRC_DIR = src
TEST_PATH = $(CURDIR)/tests
MONGO_COMPOSE_PATH = $(CURDIR)/docker-compose-mongodb.yml


all: up

# Запуск приложения UGC2
up-ugc2:
	@docker compose up -d --build

# Остановка приложения UGC2 и очистка временных файлов
down-ugc2:
	@echo "Остановка UGC2..."
	@docker compose down
	@echo "Очистка временных файлов и контейнеров..."
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete

# Запуск кластера MongoDB
up-mongo:
	@echo "Запуск кластера MongoDB..."
	@docker compose -f $(MONGO_COMPOSE_PATH) up -d --build

# Инициализация кластера MongoDB
init-mongo:
	@echo "Инициализация MongoDB..."
	@mongo/init.sh

# Oстановкa кластера MongoDB
down-mongo:
	@echo "Остановка кластера MongoDB..."
	@docker compose -f $(MONGO_COMPOSE_PATH) down

# Установка зависимостей продакшен
install:
	@echo "Установка зависимостей..."
	@pip install -r requirements.txt

# Установка зависимостей dev
install-dev:
	@echo "Установка зависимостей..."
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt

# Линтинг
lint:
	@echo "Запуск линтинга с помощью flake8..."
	@$(PYTHON) -m flake8 $(SRC_DIR)
	@echo "All done! ✨ 🍰 ✨"

# Автоформатирование
format:
	@echo "Запуск форматирования с помощью black..."
	@$(PYTHON) -m black $(BLACK_LINE_LENGTH) $(SRC_DIR)


# Запуск тестов
test:
	PYTHONPATH=$(CURDIR)/src pytest tests/

# Вывод справки
help:
	@echo "Доступные команды:"
	@echo "  make up-ugc2             - Запуск сервиса UGC2"
	@echo "  make down-ugc2           - Остановка UGC2 и очистка"
	@echo "  make up-mongo            - Запуск кластера MongoDB"
	@echo "  make init-mongo          - Инициализация кластера MongoDB"
	@echo "  make down-mongo          - Остановка кластера MongoDB"
	@echo "  make install             - Установка зависимостей prod"
	@echo "  make install-dev         - Установка зависимостей dev"
	@echo "  make lint                - Запуск линтера"
	@echo "  make format              - Автоформатирование кода"
	@echo "  make test                - Запуск тестов"
