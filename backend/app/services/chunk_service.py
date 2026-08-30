import re
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import get_settings
from app.services.pdf_service import ExtractedPage


@dataclass(frozen=True)
class TextChunk:
    """A searchable child chunk linked to a larger parent context."""

    content: str
    parent_content: str
    parent_index: int
    chunk_index: int
    page_number: int
    section_heading: str | None


class ChunkService:
    """Splits extracted text into chunks"""

    def __init__(self) -> None:
        settings = get_settings()

        self._child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap
        )
        self._parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.parent_chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def split_text(self, text: str) -> list[str]:
        """Split text into searchable child chunks."""
        return self._child_splitter.split_text(text)

    def split_pages(self, pages: list[ExtractedPage]) -> list[TextChunk]:
        """Create section-aware parent chunks and smaller searchable children."""
        chunks: list[TextChunk] = []
        parent_index = 0
        chunk_index = 0

        for page in pages:
            for heading, section_text in self._split_sections(page.text):
                for parent_content in self._parent_splitter.split_text(section_text):
                    for content in self.split_text(parent_content):
                        chunks.append(
                            TextChunk(
                                content=content,
                                parent_content=parent_content,
                                parent_index=parent_index,
                                chunk_index=chunk_index,
                                page_number=page.page_number,
                                section_heading=heading,
                            )
                        )
                        chunk_index += 1
                    parent_index += 1

        return chunks

    def _split_sections(self, text: str) -> list[tuple[str | None, str]]:
        sections: list[tuple[str | None, str]] = []
        heading: str | None = None
        lines: list[str] = []

        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                if lines:
                    lines.append("")
                continue

            if self._is_heading(line) and lines:
                sections.append((heading, "\n".join(lines).strip()))
                heading = line
                lines = [line]
            else:
                if self._is_heading(line) and not lines:
                    heading = line
                lines.append(line)

        if lines:
            sections.append((heading, "\n".join(lines).strip()))

        return sections

    @staticmethod
    def _is_heading(line: str) -> bool:
        if len(line) > 100 or line.endswith((".", ";", ",")):
            return False

        numbered = re.match(r"^\d+(?:\.\d+)*[.)]?\s+\S+", line)
        letters = [character for character in line if character.isalpha()]
        uppercase = bool(letters) and all(character.isupper() for character in letters)
        return bool(numbered or uppercase)
