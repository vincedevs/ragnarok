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
                "page_number": 3,
                "section_heading": "OVERVIEW",
                "relevance_score": None,
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
                "page_number": 3,
                "section_heading": "OVERVIEW",
                "relevance_score": None,
                "excerpt": "FastAPI is a web framework.",
            }
        ],
    }

    mock_chat_service.chat.assert_called_once_with(
        "What is FastAPI?", document_ids=None, history=[]
    )


def test_chat_requires_question(
    client: TestClient,
) -> None:
    response = client.post(
        "/chat",
        json={},
    )

    assert response.status_code == 422


def test_chat_supports_legacy_sources_without_page_metadata(
    client: TestClient,
    mock_chat_service: Mock,
) -> None:
    document = Document(
        page_content="Legacy content",
        metadata={
            "document_id": "doc-1",
            "filename": "legacy.pdf",
            "chunk_index": 0,
        },
    )
    mock_chat_service.chat.return_value = ("Legacy answer", [document])
    app.dependency_overrides[get_chat_service] = lambda: mock_chat_service

    response = client.post("/chat", json={"question": "Legacy question?"})

    assert response.status_code == 200
    assert response.json()["sources"][0]["page_number"] is None


def test_chat_passes_document_filters(
    client: TestClient,
    mock_chat_service: Mock,
) -> None:
    mock_chat_service.chat.return_value = ("Answer", [])
    app.dependency_overrides[get_chat_service] = lambda: mock_chat_service

    response = client.post(
        "/chat",
        json={"question": "Question?", "document_ids": ["doc-1", "doc-2"]},
    )

    assert response.status_code == 200
    mock_chat_service.chat.assert_called_once_with(
        "Question?", document_ids=["doc-1", "doc-2"], history=[]
    )


def test_chat_passes_bounded_history(
    client: TestClient,
    mock_chat_service: Mock,
) -> None:
    mock_chat_service.chat.return_value = ("Answer", [])
    app.dependency_overrides[get_chat_service] = lambda: mock_chat_service
    history = [
        {"role": "user", "content": "What is zero trust?"},
        {"role": "assistant", "content": "It is a security model."},
    ]

    response = client.post(
        "/chat", json={"question": "How is it implemented?", "history": history}
    )

    assert response.status_code == 200
    mock_chat_service.chat.assert_called_once_with(
        "How is it implemented?", document_ids=None, history=history
    )


def test_chat_rejects_more_than_ten_history_messages(client: TestClient) -> None:
    history = [{"role": "user", "content": "Previous"}] * 11

    response = client.post("/chat", json={"question": "Question?", "history": history})

    assert response.status_code == 422
