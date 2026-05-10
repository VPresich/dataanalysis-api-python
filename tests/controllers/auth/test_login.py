
def assert_login_response(data, login_payload):
    assert "token" in data
    assert "user" in data
    assert "name" in data["user"]
    assert data["user"]["email"] == login_payload["email"]
    assert "password" not in data["user"]
    assert "theme" in data["user"]


def test_login_router_fake_db(fake_login_client, login_payload):
    response = fake_login_client.post("/api/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert_login_response(data, login_payload)


def test_login_invalid_password_fake_db(fake_login_client, login_payload):

    user = {"email": login_payload["email"],
            "password": "invalid_password"}

    response = fake_login_client.post("/api/auth/login", json=user)
    assert response.status_code == 401
    data = response.json()
    assert data["message"] == "Email or password is wrong"


def test_login_not_registered_fake_db(fake_db_client, login_payload):

    response = fake_db_client.post("/api/auth/login", json=login_payload)

    assert response.status_code == 401
    data = response.json()
    assert data["message"] == "Email or password is wrong"
