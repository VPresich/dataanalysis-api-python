import pytest
from tests.helpers.factories import create_user
import app.config.flags as flags


def assert_login_response(data, user):
    assert "token" in data
    assert "user" in data
    assert data["token"] == user.token
    assert data["user"]["email"] == user.email
    assert data["user"]["name"] == user.name
    assert data["user"]["theme"] == user.theme.value
    assert data["user"]["avatarURL"] == user.avatar_url


@pytest.mark.asyncio
async def test_login_success_real_db(async_client, db_session):

    user, password = await create_user(db_session)

    response = await async_client.post("/api/auth/login", json={
        "email": user.email,
        "password": password
    })
    assert response.status_code == 200
    data = response.json()
    await db_session.refresh(user)
    assert_login_response(data, user)


@pytest.mark.asyncio
async def test_login_wrong_password_real_db(async_client, db_session):

    user, password = await create_user(db_session)

    response = await async_client.post("/api/auth/login", json={
        "email": user.email,
        "password": "wrong_password"
    })

    assert response.status_code == 401
    data = response.json()
    assert data["message"] == "Email or password is wrong"


@pytest.mark.asyncio
async def test_login_requires_verification_real_db(async_client, db_session, monkeypatch):

    monkeypatch.setattr(flags, "REQUIRE_EMAIL_VERIFICATION", True)
    user, password = await create_user(db_session, verify=False)

    response = await async_client.post(
        "/api/auth/login",
        json={
            "email": user.email,
            "password": password
        }
    )

    assert response.status_code == 403

    data = response.json()
    assert data["message"] == "Please verify your email before logging in."
