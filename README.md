# Data Analysis API

REST API для работы с данными на FastAPI и PostgreSQL (Supabase).

## Технологии

- Python 3.12
- FastAPI
- PostgreSQL (Supabase)
- Poetry
- Pydantic, Asyncpg
- Black, Flake8, isort

## Структура проекта

app/
├── main.py
├── routers/
├── controllers/
├── services/
├── models/
├── schemas/
├── utils/
└── middlewares/
pyproject.toml
poetry.lock
.env

1. Установить зависимости:
poetry install 

2. Запуск проекта
poetry run uvicorn app.main:app --reload

