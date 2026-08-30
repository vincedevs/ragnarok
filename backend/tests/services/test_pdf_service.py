from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from app.core.exceptions import InvalidDocumentError
from app.services.pdf_service import PDFService


def test_extract_text_combines_non_empty_pages(tmp_path: Path) -> None:
    pages = [
        Mock(page_content="first page"),
        Mock(page_content="  "),
        Mock(page_content="second page"),
    ]

    with patch("app.services.pdf_service.PyPDFLoader") as loader:
        loader.return_value.load.return_value = pages
        result = PDFService().extract_text(tmp_path / "sample.pdf")

    assert result == "first page\n\nsecond page"


def test_extract_text_rejects_empty_pdf(tmp_path: Path) -> None:
    with patch("app.services.pdf_service.PyPDFLoader") as loader:
        loader.return_value.load.return_value = [Mock(page_content="  ")]

        with pytest.raises(InvalidDocumentError, match="extractable text"):
            PDFService().extract_text(tmp_path / "empty.pdf")


def test_extract_text_wraps_parser_errors(tmp_path: Path) -> None:
    with patch("app.services.pdf_service.PyPDFLoader", side_effect=ValueError("bad")):
        with pytest.raises(InvalidDocumentError, match="bad"):
            PDFService().extract_text(tmp_path / "broken.pdf")
