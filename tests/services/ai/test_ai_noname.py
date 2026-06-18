import pytest


@pytest.mark.asyncio
async def test_ai_noname_data_extraction_success(async_client, db_session, noname_evaluate_payload, monkeypatch):
    """
    Integration: Verifies that database extraction and data formatting operations 
    succeed when anomalies are found, while isolating outbound OpenAI calls.
    """
    captured_message = None

    # 1. Stub the isolated outbound LLM function to intercept the formatted data
    async def fake_send_to_llm_agent(user_message: str):
        nonlocal captured_message
        captured_message = user_message
        return "Mocked AI Response from captured database points"

    # Rule: Path to the FILE where the function is executed
    monkeypatch.setattr(
        "app.services.ai.execute_ai_analysis_workflow.send_to_llm_agent",
        fake_send_to_llm_agent
    )

    # 2. Execute request through the actual async test client
    response = await async_client.post("/api/ai/noname-evaluate", json=noname_evaluate_payload)

    # 3. Assert HTTP status and payload delivery
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["response"] == "Mocked AI Response from captured database points"

    # 4. Assert core data integration attributes
    assert captured_message is not None
    assert f"Analyze track number: {noname_evaluate_payload['TrackNum']}" in captured_message
    assert "Time:" in captured_message
    assert "IMM_consistent:" in captured_message
    assert "Speed:" in captured_message

    with open("captured_prompt_result.txt", "w", encoding="utf-8") as f:
        f.write(captured_message)
