from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from app.core.exceptions import InvalidDocumentError
from app.services.pdf_service import ExtractedPage, PDFService


def test_extract_pages_preserves_page_numbers(tmp_path: Path) -> None:
    pages = [
        Mock(page_content="first page"),
        Mock(page_content="  "),
        Mock(page_content="second page"),
    ]

    with patch("app.services.pdf_service.PyPDFLoader") as loader:
        loader.return_value.load.return_value = pages
        result = PDFService().extract_pages(tmp_path / "sample.pdf")

    assert result == [
        ExtractedPage(page_number=1, text="first page"),
        ExtractedPage(page_number=3, text="second page"),
    ]


def test_extract_pages_rejects_empty_pdf(tmp_path: Path) -> None:
    with patch("app.services.pdf_service.PyPDFLoader") as loader:
        loader.return_value.load.return_value = [Mock(page_content="  ")]

        with pytest.raises(InvalidDocumentError, match="extractable text"):
            PDFService().extract_pages(tmp_path / "empty.pdf")


def test_extract_pages_wraps_parser_errors(tmp_path: Path) -> None:
    with patch("app.services.pdf_service.PyPDFLoader", side_effect=ValueError("bad")):
        with pytest.raises(InvalidDocumentError, match="bad"):
            PDFService().extract_pages(tmp_path / "broken.pdf")


def test_extract_pages_removes_repeated_headers_and_footers(tmp_path: Path) -> None:
    pages = [
        Mock(page_content="RAG GUIDE\nFirst body\nConfidential"),
        Mock(page_content="RAG GUIDE\nSecond body\nConfidential"),
        Mock(page_content="RAG GUIDE\nThird body\nDifferent footer"),
    ]

    with patch("app.services.pdf_service.PyPDFLoader") as loader:
        loader.return_value.load.return_value = pages
        result = PDFService().extract_pages(tmp_path / "sample.pdf")

    assert result == [
        ExtractedPage(1, "First body"),
        ExtractedPage(2, "Second body"),
        ExtractedPage(3, "Third body\nDifferent footer"),
    ]
