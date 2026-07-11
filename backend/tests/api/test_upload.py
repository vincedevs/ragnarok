from unittest.mock import Mock

from backend.app.dependencies import get_ingestion_service
from backend.app.main import app
from fastapi.testclient import TestClient


def test_upload_pdf(
    client: TestClient,
    mock_ingestion_service: Mock,
) -> None:
    app.dependency_overrides[get_ingestion_service] = lambda: mock_ingestion_service

    response = client.post(
        "/upload",
        files={
            "file": (
                "sample.pdf",
                b"dummy pdf",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 201


def test_upload_rejects_non_pdf(
    client: TestClient,
) -> None:
    response = client.post(
        "/upload",
        files={
            "file": (
                "hello.txt",
                b"hello",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
