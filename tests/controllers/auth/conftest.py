import pytest
import uuid


@pytest.fixture
def register_payload():
    return {
        "name": "Test User",
        "email": f"test_{uuid.uuid4().hex[:6]}@test.com",
        "password": "password123"
    }
