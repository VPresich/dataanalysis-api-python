import pytest
from app.models import User
from sqlalchemy import select
import app.config.flags as flags


def assert_user_in_db(user, register_payload):
    assert user is not None
    assert user.email == register_payload["email"]
    assert user.name == register_payload["name"]
    assert user.password is not None
    assert user.theme.value == "default"
    assert user.avatar_url is not None
    assert user.google_id is None


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


@pytest.mark.asyncio
async def test_register_creates_user_router(async_client, register_payload, db_session):

    response = await async_client.post("/api/auth/register", json=register_payload)

    assert response.status_code == 201

    result = await db_session.execute(
        select(User).where(User.email == register_payload["email"])
    )
    user = result.scalar_one_or_none()

    assert user is not None
    assert user.email == register_payload["email"]


@pytest.mark.asyncio
async def test_register_creates_user_verification_on(async_client, db_session, register_payload, monkeypatch):

    monkeypatch.setattr(flags, "REQUIRE_EMAIL_VERIFICATION", True)

    response = await async_client.post("/api/auth/register", json=register_payload)
    assert response.status_code == 201
    data = response.json()

    assert data["verifyRequired"] is True
    assert "token" not in data
    assert "message" in data
    assert_user_in_responce(data, register_payload)

    result = await db_session.execute(
        select(User).where(User.email == register_payload["email"])
    )
    user = result.scalar_one_or_none()
    assert_user_in_db(user, register_payload)
    assert user.token is None
    assert user.verify == False
    assert user.verification_token is not None


@pytest.mark.asyncio
async def test_register_creates_user_verification_off(async_client, db_session, register_payload, monkeypatch):

    monkeypatch.setattr(flags, "REQUIRE_EMAIL_VERIFICATION", False)
    response = await async_client.post("/api/auth/register", json=register_payload)

    assert response.status_code == 201
    data = response.json()

    assert "token" in data
    assert_user_in_responce(data, register_payload)
    assert data["user"]["theme"] == "default"
    assert "avatarURL" in data["user"]

    result = await db_session.execute(
        select(User).where(User.email == register_payload["email"])
    )
    user = result.scalar_one_or_none()
    assert_user_in_db(user, register_payload)
    assert user.token is not None
    assert user.verify == True
    assert user.verification_token is None
