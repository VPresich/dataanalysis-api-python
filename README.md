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
├── __init__.py
├── database.py
├── init_server.py
├── main.py
├── controllers/
│   ├── __init__.py
│   └── auth/
│       ├── __init__.py
│       ├── register_controller.py
│       ├── login_controller.py
│       ├── logout_controller.py
│       └── verify_controller.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── theme.py
│   ├── source_data.py
│   └── data_analysis.py
├── services/
│   ├── __init__.py
│   └── auth/
│       ├── __init__.py
│       ├── register_service.py
│       ├── login_service.py
│       ├── logout_service.py
│       └── verify_service.py
├── routers/
│   ├── __init__.py
│   ├── auth_router.py
│   └── users_router.py
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
