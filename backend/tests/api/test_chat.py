from unittest.mock import Mock

from backend.app.dependencies import get_chat_service
from backend.app.main import app
from fastapi.testclient import TestClient


def test_chat_returns_answer(
    client: TestClient,
    mock_chat_service: Mock,
) -> None:
    mock_chat_service.chat.return_value = "FastAPI is a web framework."

    app.dependency_overrides[get_chat_service] = lambda: mock_chat_service

    response = client.post(
        "/chat",
        json={
            "question": "What is FastAPI?",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "answer": "FastAPI is a web framework.",
    }

    mock_chat_service.chat.assert_called_once_with("What is FastAPI?")


def test_chat_requires_question(
    client: TestClient,
) -> None:
    response = client.post(
        "/chat",
        json={},
    )

    assert response.status_code == 422
