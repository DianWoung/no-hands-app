from fastapi.testclient import TestClient
import pytest

from app.main import app

def test_get_knowledge_answer_service_unavailable(client: TestClient, monkeypatch):
    """
    Test the /knowledge/answer endpoint when the KnowledgeService is not available.
    It should return a 503 error with the corrected, helpful message.
    """
    monkeypatch.setattr(app.state, "knowledge_service", None)

    response = client.post("/api/knowledge/answer", json={"question": "What is the return policy?"})

    assert response.status_code == 503
    response_json = response.json()
    assert "detail" in response_json
    # Assert that the old, incorrect message is GONE
    assert "OPENAI_API_KEY" not in response_json["detail"]
    # Assert that the new, helpful message is present
    assert "vector store has not been built" in response_json["detail"]