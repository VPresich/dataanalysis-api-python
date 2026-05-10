import pytest
from tests.helpers.factories import create_user


@pytest.mark.asyncio
async def test_logout_flow_real_db(async_client, db_session):
    user, password = await create_user(db_session)

    login_response = await async_client.post("/api/auth/login", json={
        "email": user.email,
        "password": password
    })

    assert login_response.status_code == 200
    token_from_login = login_response.json()["token"]

    await db_session.refresh(user)
    assert user.token is not None
    assert user.token == token_from_login

    headers = {"Authorization": f"Bearer {token_from_login}"}
    logout_response = await async_client.post("/api/auth/logout", headers=headers)
    assert logout_response.status_code == 204

    await db_session.refresh(user)
    assert user.token is None

    retry_response = await async_client.get("/api/users/current", headers=headers)
    assert retry_response.status_code == 401
    assert retry_response.json()["message"] == "Token mismatch"
