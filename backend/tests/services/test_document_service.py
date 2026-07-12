from pathlib import Path
from unittest.mock import Mock

from app.services.document_services import DocumentService


def test_delete_document_deletes_vectors_and_file(
    tmp_path: Path,
) -> None:
    repository = Mock()

    repository.list_documents.return_value = [
        {
            "document_id": "123",
            "filename": "sample.pdf",
        }
    ]

    service = DocumentService(repository=repository)

    service.delete_document("123")

    repository.delete_document.assert_called_once_with("123")
