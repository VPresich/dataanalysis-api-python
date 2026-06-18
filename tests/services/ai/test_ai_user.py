import pytest
from sqlalchemy import select
from app.models import Data
from app.dependencies import authenticate


@pytest.mark.asyncio
async def test_ai_user_data_extraction_success(async_client, db_session, user_evaluate_payload, monkeypatch):
    """
    Integration: Verifies user ownership validation, database extraction, and 
    prompt formatting logic for protected routes while isolating OpenAI.
    """
    captured_message = None

    # 1. Stub the isolated outbound LLM function in utils
    async def fake_send_to_llm_agent(user_message: str):
        nonlocal captured_message
        captured_message = user_message
        return "Mocked AI Response for authenticated user trajectory points"

    # Rule: Path to the FILE where the function is executed
    monkeypatch.setattr(
        "app.services.ai.execute_ai_analysis_workflow.send_to_llm_agent",
        fake_send_to_llm_agent
    )

    # 2. Extract the REAL owner ID from your test database fixture
    # We query the DataSource from the payload to find its legitimate owner (id_user)
    from uuid import UUID
    from app.models import DataSource

    db_source_result = await db_session.execute(
        select(DataSource).where(DataSource._id == UUID(user_evaluate_payload["id_source"]))
    )
    real_data_source = db_source_result.scalar_one_or_none()
    assert real_data_source is not None, "Test fixture id_source does not exist in the replica database!"

    # Capture the exact owner UUID to pass through the auth guard
    legitimate_user_id = str(real_data_source.id_user)

    # 3. Explicitly mock the security guard middleware layer to return the correct profile
    async def fake_authenticate_dependency():
        class MockUserObject:
            _id = legitimate_user_id
            id = legitimate_user_id
            email = "authenticated_engineer@test.com"
            name = "Valid Track Analyst"

            def __getitem__(self, key):
                return getattr(self, key)

        return MockUserObject()

    # Inject our fake credential into FastAPI dependency overrides
    target_app = async_client._transport.app
    target_app.dependency_overrides[authenticate] = fake_authenticate_dependency

    # 4. Dispatch the HTTP POST request utilizing the real async test client
    response = await async_client.post("/api/ai/user-evaluate", json=user_evaluate_payload)

    # 5. Clear runtime overrides immediately to isolate subsequent test runners cleanly
    target_app.dependency_overrides.clear()

    # 6. Assert standard HTTP response schemas and text matches
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["response"] == "Mocked AI Response for authenticated user trajectory points"

    # 7. AUTOMATED DATA VALIDATION: Cross-verify prompt contents against direct SQL query
    assert captured_message is not None
    assert f"Analyze track number: {user_evaluate_payload['TrackNum']}" in captured_message

    prompt_records_count = captured_message.count("Time:")

    db_data_result = await db_session.execute(
        select(Data).where(
            (Data.id_source == real_data_source._id)
            & (Data.TrackNum == user_evaluate_payload["TrackNum"])
            & (
                (Data.IMMconsistent == "0")
                | (Data.TrackConsistent == "0")
                | (Data.VelocityConsistent == "0")
            )
        )
    )
    real_db_records = db_data_result.scalars().all()

    # The ultimate integration assert: check that the code pulled EXACTLY what is in the DB for this user
    assert len(real_db_records) == prompt_records_count
    assert prompt_records_count > 0

    with open("captured_user_prompt_result.txt", "w", encoding="utf-8") as f:
        f.write(captured_message)


@pytest.mark.asyncio
async def test_ai_user_evaluate_unauthorized_source_owner(async_client, db_session, user_evaluate_payload, monkeypatch):
    """
    Integration: Verifies that if a different logged-in user tries to access 
    this id_source, the system securely blocks the request with a 401/404 error.
    """
    # 1. Stub the outbound LLM function to fail if it gets called
    # If the security layer fails, the code will hit this stub and crash the test
    async def fake_send_to_llm_agent(user_message: str):
        pytest.fail("SECURITY BREACH: The service invoked the LLM layer for an unauthorized user!")

    monkeypatch.setattr(
        "app.services.ai.execute_ai_analysis_workflow.send_to_llm_agent",
        fake_send_to_llm_agent
    )

    # 2. Generate a completely random, FAKE user UUID (the attacker)
    # This user does NOT own the data source inside the replica database
    attacker_user_id = "00000000-0000-0000-0000-000000000000"

    # 3. Explicitly mock the security guard to return the ATTACKER'S profile
    async def fake_authenticate_dependency():
        class MockUserObject:
            _id = attacker_user_id
            id = attacker_user_id
            email = "attacker_hacker@test.com"
            name = "Malicious Attacker User"

            def __getitem__(self, key):
                return getattr(self, key)

        return MockUserObject()

    # Inject the attacker's credentials into the current app instance
    target_app = async_client._transport.app
    target_app.dependency_overrides[authenticate] = fake_authenticate_dependency

    # 4. Dispatch the HTTP POST request using the attacker's session
    response = await async_client.post("/api/ai/user-evaluate", json=user_evaluate_payload)

    # 5. Clear runtime overrides immediately
    target_app.dependency_overrides.clear()

    # 6. CORE SECURITY ASSERTS
    # The application must refuse access and return 404 (or 401 depending on your design)
    assert response.status_code == 404

    data = response.json()
    # Verifies that your standard exception handling message is returned
    assert "Source not found for this user" in data["detail"]
