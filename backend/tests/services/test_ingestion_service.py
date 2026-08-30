from pathlib import Path
from unittest.mock import Mock

import pytest

from app.core.exceptions import InvalidDocumentError
from app.services.chunk_service import TextChunk
from app.services.ingestion_service import IngestionService
from app.services.pdf_service import ExtractedPage


def test_ingest_builds_documents_with_metadata(tmp_path: Path) -> None:
    pdf_service = Mock()
    chunk_service = Mock()
    repository = Mock()
    pages = [ExtractedPage(2, "extracted text")]
    chunks = [
        TextChunk("first", "parent text", 0, 0, 2, "OVERVIEW"),
        TextChunk("second", "parent text", 0, 1, 2, "OVERVIEW"),
    ]
    pdf_service.extract_pages.return_value = pages
    chunk_service.split_pages.return_value = chunks
    service = IngestionService(pdf_service, chunk_service, repository)
    path = tmp_path / "sample.pdf"

    service.ingest("doc-1", "sample.pdf", path)

    pdf_service.extract_pages.assert_called_once_with(path)
    chunk_service.split_pages.assert_called_once_with(pages)
    indexed = repository.add_documents.call_args.args[0]
    assert [document.page_content for document in indexed] == ["first", "second"]
    assert indexed[1].metadata == {
        "document_id": "doc-1",
        "filename": "sample.pdf",
        "chunk_index": 1,
        "page_number": 2,
        "parent_id": "doc-1:parent:0",
        "parent_content": "parent text",
        "section_heading": "OVERVIEW",
    }


def test_ingest_rejects_empty_chunks(tmp_path: Path) -> None:
    pdf_service = Mock()
    chunk_service = Mock()
    repository = Mock()
    pages = [ExtractedPage(1, "text")]
    pdf_service.extract_pages.return_value = pages
    chunk_service.split_pages.return_value = []
    service = IngestionService(pdf_service, chunk_service, repository)

    with pytest.raises(InvalidDocumentError, match="indexable text"):
        service.ingest("doc-1", "sample.pdf", tmp_path / "sample.pdf")

    repository.add_documents.assert_not_called()
