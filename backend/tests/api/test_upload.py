from pathlib import Path
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.core.exceptions import InvalidDocumentError
from app.dependencies import get_ingestion_service, get_storage_service
from app.main import app


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
                b"%PDF-dummy pdf",
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


def test_upload_rejects_spoofed_pdf(client: TestClient) -> None:
    response = client.post(
        "/upload",
        files={"file": ("fake.pdf", b"not a pdf", "application/pdf")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Only valid PDF files are supported"}


def test_upload_removes_file_when_document_is_invalid(
    client: TestClient,
    mock_ingestion_service: Mock,
    tmp_path: Path,
) -> None:
    storage_service = Mock()
    path = tmp_path / "doc-1_broken.pdf"
    storage_service.save_file.return_value = ("doc-1", path)
    mock_ingestion_service.ingest.side_effect = InvalidDocumentError("broken PDF")
    app.dependency_overrides[get_ingestion_service] = lambda: mock_ingestion_service
    app.dependency_overrides[get_storage_service] = lambda: storage_service

    response = client.post(
        "/upload",
        files={"file": ("broken.pdf", b"%PDF-broken", "application/pdf")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "broken PDF"}
    storage_service.delete_file.assert_called_once_with(path)


def test_upload_hides_internal_ingestion_errors(
    client: TestClient,
    mock_ingestion_service: Mock,
    tmp_path: Path,
) -> None:
    storage_service = Mock()
    path = tmp_path / "doc-1_sample.pdf"
    storage_service.save_file.return_value = ("doc-1", path)
    mock_ingestion_service.ingest.side_effect = RuntimeError("provider secret")
    app.dependency_overrides[get_ingestion_service] = lambda: mock_ingestion_service
    app.dependency_overrides[get_storage_service] = lambda: storage_service

    response = client.post(
        "/upload",
        files={"file": ("sample.pdf", b"%PDF-dummy", "application/pdf")},
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "The document could not be indexed. Please try again."
    }
    storage_service.delete_file.assert_called_once_with(path)
