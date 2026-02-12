# Makefile for RBAC-FastAPI

# Load .env file if it exists
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

APP_MODULE = app.main:app

# Construct server flags only if variables are defined
SERVER_FLAGS =
ifneq ($(HOST),)
	SERVER_FLAGS += --host $(HOST)
endif
ifneq ($(PORT),)
	SERVER_FLAGS += --port $(PORT)
endif

.PHONY: help install dev run migrate migration clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies using uv"
	@echo "  make dev        - Run development server with hot reload"
	@echo "  make run        - Run production server"
	@echo "  make migrate    - Apply database migrations"
	@echo "  make migration  - Create a new migration (usage: make migration msg=\"your message\")"
	@echo "  make clean      - Clean cache files"

install:
	uv sync

dev:
	uv run uvicorn $(APP_MODULE) --reload $(SERVER_FLAGS)

run:
	uv run uvicorn $(APP_MODULE) $(SERVER_FLAGS)

migrate:
	uv run alembic upgrade head

# Usage: make migration msg="add new table"
migration:
	@if [ -z "$(msg)" ]; then echo "Error: msg is undefined. Usage: make migration msg=\"message\""; exit 1; fi
	uv run alembic revision --autogenerate -m "$(msg)"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
