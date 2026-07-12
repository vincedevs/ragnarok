from unittest.mock import Mock

from fastapi.testclient import TestClient
from langchain_core.documents import Document

from app.dependencies import get_chat_service
from app.main import app


def test_chat_returns_answer(
    client: TestClient,
    mock_chat_service: Mock,
) -> None:
    documents = [
        Document(
            page_content="FastAPI is a web framework.",
            metadata={
                "document_id": "doc-1",
                "filename": "fastapi.md",
                "chunk_index": 0,
            },
        )
    ]
    mock_chat_service.chat.return_value = ("FastAPI is a web framework.", documents)

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
        "sources": [
            {
                "document_id": "doc-1",
                "filename": "fastapi.md",
                "chunk_index": 0,
            }
        ],
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
