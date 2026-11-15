
from fastapi.testclient import TestClient
from api import app
from unittest.mock import MagicMock, patch
from schemas import ResearchBrief, ReviewResult

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_research_disabled(monkeypatch):
    monkeypatch.delenv("ENABLE_LIVE_API", raising=False)

    response = client.post(
        "/api/research",
        json={
            "question": "How is AI changing software engineering?"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "disabled"


def test_research_invalid_question():
    response = client.post(
        "/api/research",
        json={"question": "AI"}
    )

    assert response.status_code == 422


def test_research_success(monkeypatch):
    # Enable the live path, but mock all external operations.
    monkeypatch.setenv("ENABLE_LIVE_API", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    mock_result = {
        "review": ReviewResult(
            score=91,
            approved=True,
            feedback=[]
        ),
        "brief": ResearchBrief(
            executive_summary="AI assists software development.",
            key_findings=["Improves productivity."],
            uncertainties=["Long-term impact is unclear."],
            recommendations=["Review AI-generated code."]
        ),
        "revision_count": 0
    }

    with patch("api.OpenAI") as mock_openai:
        with patch("api.run_research", return_value=mock_result) as mock_run:
            response = client.post(
                "/api/research",
                json={
                    "question": "How is AI changing software engineering?"
                }
            )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "completed"
    assert data["review"]["score"] == 91
    assert data["review"]["approved"] is True
    assert data["brief"]["executive_summary"] == (
        "AI assists software development."
    )
    assert data["revision_count"] == 0

    mock_openai.assert_called_once()
    mock_run.assert_called_once()


def test_research_failure(monkeypatch):
    monkeypatch.setenv("ENABLE_LIVE_API", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    with patch("api.OpenAI"):
        with patch(
            "api.run_research",
            side_effect=RuntimeError("Simulated workflow failure")
        ):
            response = client.post(
                "/api/research",
                json={
                    "question": "How is AI changing software engineering?"
                }
            )

    assert response.status_code == 502
    assert response.json()["detail"] == "Research workflow failed."


def test_research_rejects_whitespace_question():
    response = client.post(
        "/api/research",
        json={"question": "               "}
    )

    assert response.status_code == 422


def test_research_trims_question(monkeypatch):
    monkeypatch.delenv("ENABLE_LIVE_API", raising=False)

    response = client.post(
        "/api/research",
        json={
            "question": "   How does AI improve software development?   "
        }
    )

    assert response.status_code == 200
    assert response.json()["question"] == (
        "How does AI improve software development?"
    )


    

