import pytest
from app.dependencies import authenticate


def assert_ai_evaluation_response(data, expected_text):
    """
    Helper assertion function to validate the structured format of the AI router response payload.
    """
    assert "status" in data
    assert "response" in data
    assert data["status"] == "success"
    assert data["response"] == expected_text


def test_ai_user_evaluate_route_success(fake_login_client, user_evaluate_payload, monkeypatch):
    """
    Tests a successful secure track evaluation request via the '/api/ai/user-evaluate' route.
    Explicitly overrides the business service layer and the authentication guard for clear isolation.
    """
    # 1. Explicitly mock the heavy backend service layer inside the test context
    async def fake_user_service(*args, **kwargs):
        return {"status": "success", "response": "Mocked User Trajectory Evaluation Result"}
    monkeypatch.setattr(
        "app.controllers.ai.ai_agent_user_controller.ai_agent_user",
        fake_user_service
    )

    # 2. Explicitly mock the security guard middleware layer to return a profile object layout

    async def fake_authenticate_dependency():
        class MockUserObject:
            _id = "fake-user-uuid-123"
            id = "fake-user-uuid-123"
            email = "fake@test.com"
            name = "Fake User"

            # Allows accessing attributes via dictionary subscription item keys if needed
            def __getitem__(self, key):
                return getattr(self, key)

        return MockUserObject()

    app = fake_login_client.app
    app.dependency_overrides[authenticate] = fake_authenticate_dependency

    # 3. Dispatch the HTTP POST request utilizing the synchronous test client instance
    response = fake_login_client.post("/api/ai/user-evaluate", json=user_evaluate_payload)

    # 4. Clear runtime overrides immediately to isolate subsequent test runners cleanly
    app.dependency_overrides.clear()

    # 5. Process responses and assert outcomes
    assert response.status_code == 200
    data = response.json()
    assert_ai_evaluation_response(data, "Mocked User Trajectory Evaluation Result")


def test_ai_noname_evaluate_route_success(fake_db_client, noname_evaluate_payload, monkeypatch):
    """
    Tests a successful public track evaluation request via the open '/api/ai/noname-evaluate' route.
    Bypasses real databases by overriding the anonymous service handler directly.
    """
    # 1. Explicitly mock the public backend service layer inside the test context
    async def fake_noname_service(*args, **kwargs):
        return {"status": "success", "response": "Mocked Noname Trajectory Evaluation Result"}
    monkeypatch.setattr(
        "app.controllers.ai.ai_agent_noname_controller.ai_agent_noname",
        fake_noname_service
    )

    # 2. Dispatch public call utilizing an unauthenticated mock database client session
    response = fake_db_client.post("/api/ai/noname-evaluate", json=noname_evaluate_payload)

    # 3. Assert response schemas and text matches
    assert response.status_code == 200
    data = response.json()
    assert_ai_evaluation_response(data, "Mocked Noname Trajectory Evaluation Result")


def test_ai_user_evaluate_route_unauthorized(fake_db_client, user_evaluate_payload):
    """
    Verifies that calling the protected user route without passing authentication headers 
    correctly triggers a 401 Unauthorized block from your core dependency validation layer.
    """
    # No dependency_overrides assigned here, so the real authentication middleware catches the empty payload
    response = fake_db_client.post("/api/ai/user-evaluate", json=user_evaluate_payload)

    # Asserting your standard application guard security response
    assert response.status_code == 401
