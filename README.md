# Data Analysis API

Backend REST API for data processing, storage, and visualization built with **FastAPI + PostgreSQL (Supabase)**.

This project is part of a larger web system for data collection, processing, and visualization.

## Features

- REST API built with FastAPI
- JWT Authentication & Authorization
- Google OAuth login
- PostgreSQL database integration
- Async ORM (SQLAlchemy + asyncpg)
- File & image handling
- Data filtering and processing
- Frontend integration (React)
- Data visualization support


## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- asyncpg
- Pydantic
- PyJWT
- Poetry
- httpx
- Jinja2
- python-dotenv
- Black / Flake8 / isort


## Project Structure

The project follows a layered architecture:

app/
- controllers/ # API request handlers
- services/ # business logic layer
- models/ # database models (ORM)
- routers/ # API routing
- schemas/ # data validation (Pydantic)
- validation/ # input validation rules
- dependencies/ # auth & DI
- utils/ # helper functions
- database.py # DB connection
- main.py # application entry point


## Architecture Flow

Client → Routers → Controllers → Services → Models → Database

## Installation

### 1. Install dependencies

poetry install

2. Run the server
poetry run uvicorn app.main:app --reload


## Port Management (Windows)
Check if a port is in use
netstat -aon | findstr :PORT

Example:
netstat -aon | findstr :5173

Kill process using a port
taskkill /PID PID_NUMBER /F

Example:
taskkill /PID 12345 /F


## Environment Variables

Create a .env file in the root directory:

APP_PORT=
DATABASE_URL=

JWT_SECRET=
JWT_EXPIRES_IN=

SMTP_HOST=
SMTP_USER=
SMTP_PASSWORD=

CLOUDINARY_URL=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

BACKEND_BASE_URL=

REQUIRE_EMAIL_VERIFICATION=
ENABLE_CLOUDINARY=

ALLOWED_ORIGINS=

## Notes
This is a research / educational backend project
Designed for scalable web-service architecture
Works together with a React frontend
Uses modern async Python stack
