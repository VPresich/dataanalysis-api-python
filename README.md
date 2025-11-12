# Data Analysis API

REST API для работы с данными на FastAPI и PostgreSQL (Supabase).

## Технологии

- Python 3.12
- FastAPI
- PostgreSQL (Supabase)
- Poetry
- Pydantic, Asyncpg
- Black, Flake8, isort

FastAPI (framework)
│
├── SQLAlchemy async + PostgreSQL
├── Pydantic (validation)
├── Alembic (migration)
├── PyJWT (tokens)
├── python-dotenv (environment)
├── httpx (queries)
├── Jinja2 (email templates)
└── Celery + Redis (-)

## Структура проекта

app/
├── __init__.py
├── database.py
├── init_server.py
├── main.py
│
├── controllers/
│   ├── __init__.py
│   ├──auth/
│   │   ├── __init__.py
│   │   ├── register_controller.py
│   │   ├── login_controller.py
│   │   ├── logout_controller.py
│   │   ├── get_google_tokens_controller.py
│   │   ├── google_login_controller.py
│   │   └── ....  .py
│   ├──users/
│   │    ├──__init__.py
│   │    ├── get_current_controller.py
│   │    ├── update_profile_controller.py
│   │    ├── update_theme_controller.py
│   │    ├── update_avatar_controller.py
│   │    └── .... .py
│   ├──sources/
│   │    ├──__init__.py
│   │    ├── get_all_sources_controller.py
│   │    ├── delete_all_sources_controller.py
│   │    ├── update_source_controller.py
│   │    ├── upload_source_controller.py
│   │    └── ...  .py
│   └── data/
│        ├──__init__.py
│        ├── get_data_by_source_controller.py
│        ├── get_filtered_data_by_source_controller.py
│        └── ... .py
│
├── dependencies/
│        ├──__init__.py
│        ├── authenticate.py
│        ├── .py
│        └── ... .py
│
├── middlewares/
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── theme.py
│   ├── data_source.py
│   └── data.py
│
├── services/
│   ├── __init__.py
│   ├──auth/
│   │   ├── __init__.py
│   │   ├── register_service.py
│   │   ├── login_service.py
│   │   ├── logout_service.py
│   │   ├── get_google_tokens.py
│   │   ├── get_google_user_info.py
│   │   ├── google_login_service.py
│   │   └── ....  .py
│   ├──users/
│   │    ├──__init__.py
│   │    ├── get_current_service.py
│   │    ├── update_profile_service.py
│   │    ├── update_theme_service.py
│   │    ├── update_avatar_service.py
│   │    └── .... .py
│   ├──sources/
│   │    ├──__init__.py
│   │    ├── get_all_sources_service.py
│   │    ├── delete_all_sources_service.py
│   │    ├── update_source_service.py
│   │    ├── eupload_source_service.py
│   │    └── ... .py
│   └── data/
│        ├──__init__.py
│        ├── get_data_by_source_service.py
│        ├── get_filtered_data_by_source_service.py
│        └── ... .py
│
├── routers/
│   ├── __init__.py
│   ├── auth_router.py
│   ├── data_router.py
│   ├── sources_router.py
│   ├── users_router.py
│   └── ... .py
│
├── validation/
│   ├── __init__.py
│   ├── user_validation.py
│   ├── source_validation.py
│   └── ... .py
│
└── utils/
pyproject.toml
poetry.lock
.env
.env.example

1. Install dependencies:
poetry install

2. Run the project:
poetry run uvicorn app.main:app --reload
