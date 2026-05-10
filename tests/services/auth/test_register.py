import pytest
from app.models import User
from app.database import AsyncSessionLocal
from sqlalchemy import select
import app.config.flags as flags
import asyncio


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
    assert not user.verify
    assert user.verification_token is not None


# @pytest.mark.skip()
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
    assert user.verify
    assert user.verification_token is None


# @pytest.mark.skip()
@pytest.mark.asyncio
async def test_register_duplicate_email(async_client, register_payload, db_session):

    response = await async_client.post("/api/auth/register", json=register_payload)
    assert response.status_code == 201

    response_duplicate = await async_client.post("/api/auth/register", json=register_payload)
    assert response_duplicate.status_code == 409
