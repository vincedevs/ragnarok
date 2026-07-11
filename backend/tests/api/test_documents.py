from unittest.mock import Mock

from backend.app.dependencies import get_document_service
from backend.app.main import app
from fastapi.testclient import TestClient


def test_list_documents(
    client: TestClient,
    mock_document_service: Mock,
) -> None:
    mock_document_service.list_documents.return_value = [
        {
            "document_id": "123",
            "filename": "rag.pdf",
        }
    ]

    app.dependency_overrides[get_document_service] = lambda: mock_document_service

    response = client.get("/documents")

    assert response.status_code == 200

    assert response.json() == [
        {
            "document_id": "123",
            "filename": "rag.pdf",
        }
    ]


def test_delete_document(
    client: TestClient,
    mock_document_service: Mock,
) -> None:
    app.dependency_overrides[get_document_service] = lambda: mock_document_service

    response = client.delete("/documents/123")

    assert response.status_code == 200

    mock_document_service.delete_document.assert_called_once_with("123")
