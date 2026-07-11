from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from fastapi import UploadFile

from app.core.config import Settings
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
