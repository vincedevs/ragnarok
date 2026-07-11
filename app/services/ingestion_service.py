from pathlib import Path

from langchain_core.documents import Document

from app.repositories.chroma_repository import ChromaRepository
from app.services.chunk_service import ChunkService
from app.services.pdf_service import PDFService


class IngestionService:
    """Coordinates document ingestion workflow"""

    def __init__(self) -> None:
        self._pdf_service = PDFService()
        self._chunk_service = ChunkService()
        self._chroma_repository = ChromaRepository()

    def ingest(self, document_id: str, filename: str, pdf_path: Path) -> None:
        """Extract, chunk, and store a PDF document"""
        text = self._pdf_service.extract_text(pdf_path)
        chunks = self._chunk_service.split_text(text)

        documents = [
            Document(
                page_content=chunk,
                metadata={
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": index,
                },
            )
            for index, chunk in enumerate(chunks)
        ]

        self._chroma_repository.add_documents(documents)
