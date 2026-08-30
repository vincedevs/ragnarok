from pathlib import Path
from unittest.mock import Mock

import pytest

from app.core.exceptions import InvalidDocumentError
from app.services.ingestion_service import IngestionService


def test_ingest_builds_documents_with_metadata(tmp_path: Path) -> None:
    pdf_service = Mock()
    chunk_service = Mock()
    repository = Mock()
    pdf_service.extract_text.return_value = "extracted text"
    chunk_service.split_text.return_value = ["first", "second"]
    service = IngestionService(pdf_service, chunk_service, repository)
    path = tmp_path / "sample.pdf"

    service.ingest("doc-1", "sample.pdf", path)

    pdf_service.extract_text.assert_called_once_with(path)
    chunk_service.split_text.assert_called_once_with("extracted text")
    indexed = repository.add_documents.call_args.args[0]
    assert [document.page_content for document in indexed] == ["first", "second"]
    assert indexed[1].metadata == {
        "document_id": "doc-1",
        "filename": "sample.pdf",
        "chunk_index": 1,
    }


def test_ingest_rejects_empty_chunks(tmp_path: Path) -> None:
    pdf_service = Mock()
    chunk_service = Mock()
    repository = Mock()
    pdf_service.extract_text.return_value = "text"
    chunk_service.split_text.return_value = []
    service = IngestionService(pdf_service, chunk_service, repository)

    with pytest.raises(InvalidDocumentError, match="indexable text"):
        service.ingest("doc-1", "sample.pdf", tmp_path / "sample.pdf")

    repository.add_documents.assert_not_called()
