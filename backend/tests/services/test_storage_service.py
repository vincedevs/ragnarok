from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi import UploadFile

from app.core.config import Settings
from app.core.exceptions import InvalidDocumentError
from app.services.storage_services import StorageService


def test_save_file(tmp_path: Path) -> None:
    settings = Settings(
        openai_api_key="test",
        chat_model="gpt-4.1-mini",
        embedding_model="text-embedding-3-small",
        chroma_persist_directory=tmp_path,
        upload_directory=tmp_path,
        chunk_size=500,
        chunk_overlap=100,
        retrieval_k=5,
    )

    upload = UploadFile(
        filename="sample.pdf",
        file=BytesIO(b"hello"),
    )

    with patch(
        "app.services.storage_services.get_settings",
        return_value=settings,
    ):
        service = StorageService()

        document_id, path = service.save_file(upload)

    assert document_id

    assert path.exists()

    assert path.name.endswith("sample.pdf")


def test_validate_pdf_rewinds_valid_upload(tmp_path: Path) -> None:
    settings = Settings(
        openai_api_key="test",
        chroma_persist_directory=tmp_path,
        upload_directory=tmp_path,
    )
    upload = UploadFile(
        filename="sample.pdf",
        file=BytesIO(b"%PDF-content"),
        headers={"content-type": "application/pdf"},
    )

    with patch("app.services.storage_services.get_settings", return_value=settings):
        service = StorageService()

    service.validate_pdf(upload)

    assert upload.file.read() == b"%PDF-content"


def test_validate_pdf_rejects_invalid_content(tmp_path: Path) -> None:
    settings = Settings(
        openai_api_key="test",
        chroma_persist_directory=tmp_path,
        upload_directory=tmp_path,
    )
    upload = UploadFile(
        filename="sample.pdf",
        file=BytesIO(b"plain text"),
        headers={"content-type": "application/pdf"},
    )

    with patch("app.services.storage_services.get_settings", return_value=settings):
        service = StorageService()

    with pytest.raises(InvalidDocumentError):
        service.validate_pdf(upload)


def test_save_file_sanitizes_filename_and_delete_file(tmp_path: Path) -> None:
    settings = Settings(
        openai_api_key="test",
        chroma_persist_directory=tmp_path,
        upload_directory=tmp_path,
    )
    upload = UploadFile(filename="../sample.pdf", file=BytesIO(b"%PDF-content"))

    with patch("app.services.storage_services.get_settings", return_value=settings):
        service = StorageService()
        _, path = service.save_file(upload)

    assert path.parent == tmp_path
    assert path.name.endswith("_sample.pdf")

    service.delete_file(path)

    assert not path.exists()
