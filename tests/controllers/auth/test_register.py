import pytest
import uuid

from app.models import User
from sqlalchemy import select
from app.database import get_db_session_ctx
from app.database import AsyncSessionLocal

import app.config.flags as flags


def test_register_router(fake_db_client):
    response = fake_db_client.post("/api/auth/register", json={
        "name": "test name",
        "email": "test@test.com",
        "password": "123456"
    })

    assert response.status_code == 201


def test_register_verification_on(fake_db_client, monkeypatch):
    monkeypatch.setattr(flags, "REQUIRE_EMAIL_VERIFICATION", True)
    monkeypatch.setattr("app.services.auth.send_token", lambda *args, **kwargs: None)

    user = {"name": "Test User",
            "email": "verify@test.com",
            "password": "password123"}

    response = fake_db_client.post("/api/auth/register", json=user)

    assert response.status_code == 201
    data = response.json()

    assert "token" not in data
    assert "message" in data
    assert data["verifyRequired"] is True
    assert "user" in data
    assert data["user"]["name"] == user["name"]
    assert data["user"]["email"] == user["email"]


def test_register_verification_off(fake_db_client, monkeypatch):

    monkeypatch.setattr(flags, "REQUIRE_EMAIL_VERIFICATION", False)

    user = {"name": "Not Verify",
            "email": "notverify@test.com",
            "password": "password123"}

    response = fake_db_client.post("/api/auth/register", json=user)
    assert response.status_code == 201
    data = response.json()

    assert "token" in data
    assert "user" in data
    assert data["user"]["name"] == user["name"]
    assert data["user"]["email"] == user["email"]
    assert "theme" in data["user"]
    assert "avatarURL" in data["user"]
