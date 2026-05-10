import pytest
from app.models import User
from app.database import AsyncSessionLocal
from sqlalchemy import select
import app.config.flags as flags
import asyncio


def assert_user_in_responce(data, register_payload):
    assert "user" in data
    assert data["user"]["name"] == register_payload["name"]
    assert data["user"]["email"] == register_payload["email"]


def test_register_router(fake_db_client, register_payload):
    response = fake_db_client.post("/api/auth/register", json=register_payload)
    assert response.status_code == 201


def test_register_verification_on(fake_db_client, register_payload, monkeypatch):
    monkeypatch.setattr(flags, "REQUIRE_EMAIL_VERIFICATION", True)
    monkeypatch.setattr("app.services.auth.send_token", lambda *args, **kwargs: None)

    response = fake_db_client.post("/api/auth/register", json=register_payload)

    assert response.status_code == 201
    data = response.json()

    assert "token" not in data
    assert "message" in data
    assert data["verifyRequired"] is True
    assert_user_in_responce(data, register_payload)


def test_register_verification_off(fake_db_client, register_payload, monkeypatch):

    monkeypatch.setattr(flags, "REQUIRE_EMAIL_VERIFICATION", False)

    response = fake_db_client.post("/api/auth/register", json=register_payload)
    assert response.status_code == 201
    data = response.json()

    assert "token" in data
    assert_user_in_responce(data, register_payload)
    assert "theme" in data["user"]
    assert "avatarURL" in data["user"]
