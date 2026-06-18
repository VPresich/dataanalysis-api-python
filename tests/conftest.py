import pytest
import bcrypt
import uuid
from app.models import User, ThemeEnum
from app.database import get_db_session
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import init_server
from app.database import get_db_session, AsyncSessionLocal


@pytest.fixture(autouse=True)
async def cleanup_db_engine():
    yield
    from app.database import engine
    await engine.dispose()


async def override_get_db():
    """For register"""
    class FakeSession:
        async def execute(self, *args, **kwargs):
            class Result:
                def scalar_one_or_none(self):
                    return None
            return Result()

        def add(self, obj):
            pass

        async def commit(self):
            pass

        async def refresh(self, obj):
            if hasattr(obj, '_id'):
                obj._id = "fake-uuid-123"

        async def rollback(self):
            pass

        async def close(self):
            pass

    yield FakeSession()


async def override_get_db_user():
    """For login"""
    class FakeSession:
        async def execute(self, *args, **kwargs):
            class Result:
                def scalar_one_or_none(self):
                    return User(
                        name="Fake User",
                        email="fake@test.com",
                        password=bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
                        theme=ThemeEnum.default,
                        avatar_url="http://example.com",
                        verify=True
                    )
            return Result()

        async def commit(self): pass
        async def rollback(self): pass
        async def close(self): pass
    yield FakeSession()


@pytest.fixture
def fake_db_client():
    app = init_server(lifespan=None)
    app.dependency_overrides[get_db_session] = override_get_db

    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def fake_login_client():
    app = init_server(lifespan=None)
    app.dependency_overrides[get_db_session] = override_get_db_user
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def real_db_client():
    app = init_server(lifespan=None)
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def async_client():
    from app.main import init_server
    app = init_server(lifespan=None)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        await session.begin_nested()
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


# @pytest.fixture
# async def async_client(db_session):
#     """
#     Asynchronous client fixture that forces FastAPI database dependencies
#     to reuse the active test transaction session, ensuring automated cleanups.
#     """
#     from app.main import init_server
#     app = init_server(lifespan=None)

#     # Injects the current database test session into the FastAPI runtime context
#     async def override_get_db_session():
#         yield db_session

#     # Establishes the core dependency link between test files and router layers
#     from app.database import get_db_session
#     app.dependency_overrides[get_db_session] = override_get_db_session

#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         yield client

#     # Clears out runtime context overrides to prevent cross-test logic pollution
#     app.dependency_overrides.clear()


@pytest.fixture
def register_payload():
    return {
        "name": "Test User",
        "email": f"test_{uuid.uuid4().hex[:6]}@test.com",
        "password": "password123"
    }


@pytest.fixture(autouse=True)
def mock_brevo_api(monkeypatch):
    """
    Globally disables real HTTP requests to Brevo.
    """
    path = "app.utils.send_mail_brevo.send_mail"

    # Simulating a successful response from the Brevo API
    async def fake_send(*args, **kwargs):
        return {"messageId": "fake-id-123"}

    monkeypatch.setattr(path, fake_send)
