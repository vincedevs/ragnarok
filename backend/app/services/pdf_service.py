from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from app.core.exceptions import InvalidDocumentError


@dataclass(frozen=True)
class ExtractedPage:
    """Text extracted from one PDF page."""

    page_number: int
    text: str


class PDFService:
    """Extract text from PDF documents"""

    def extract_pages(self, pdf_path: Path) -> list[ExtractedPage]:
        """Extract text while preserving page boundaries and removing page furniture."""
        try:
            loader = PyPDFLoader(str(pdf_path))
            documents = loader.load()
        except Exception as error:
            raise InvalidDocumentError(str(error)) from error

        pages = [
            ExtractedPage(page_number=index, text=document.page_content.strip())
            for index, document in enumerate(documents, start=1)
            if document.page_content.strip()
        ]

        if not pages:
            raise InvalidDocumentError(
                "The PDF does not contain extractable text. Scanned PDFs are not "
                "currently supported."
            )

        return self._remove_repeated_margins(pages)

    def _remove_repeated_margins(
        self, pages: list[ExtractedPage]
    ) -> list[ExtractedPage]:
        """Remove first and last lines repeated across at least half the pages."""
        if len(pages) < 2:
            return pages

        page_lines = [page.text.splitlines() for page in pages]
        first_lines = Counter(self._normalize(lines[0]) for lines in page_lines)
        last_lines = Counter(self._normalize(lines[-1]) for lines in page_lines)
        threshold = max(2, (len(pages) + 1) // 2)
        repeated_first = {
            line for line, count in first_lines.items() if line and count >= threshold
        }
        repeated_last = {
            line for line, count in last_lines.items() if line and count >= threshold
        }
        cleaned: list[ExtractedPage] = []

        for page, lines in zip(pages, page_lines, strict=True):
            if lines and self._normalize(lines[0]) in repeated_first:
                lines = lines[1:]
            if lines and self._normalize(lines[-1]) in repeated_last:
                lines = lines[:-1]

            text = "\n".join(lines).strip()
            if text:
                cleaned.append(ExtractedPage(page.page_number, text))

        return cleaned

    @staticmethod
    def _normalize(line: str) -> str:
        return " ".join(line.casefold().split())
