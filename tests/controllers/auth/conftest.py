import pytest


@pytest.fixture
def login_payload():
    return {
        "email": "fake@test.com",
        "password": "password123"
    }
