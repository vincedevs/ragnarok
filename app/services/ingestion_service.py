from pathlib import Path

from langchain_core.documents import Document
from loguru import logger

from app.repositories.chroma_repository import ChromaRepository
from app.services.chunk_service import ChunkService
from app.services.pdf_service import PDFService


class IngestionService:
    """Coordinates document ingestion workflow"""

    def __init__(
        self,
        pdf_service: PDFService,
        chunk_service: ChunkService,
        repository: ChromaRepository,
    ) -> None:
        self._pdf_service = pdf_service
        self._chunk_service = chunk_service
        self._chroma_repository = repository

    def ingest(self, document_id: str, filename: str, pdf_path: Path) -> None:
        """Extract, chunk, and store a PDF document"""
        logger.info(f"Starting ingestion for '{filename}'")

        text = self._pdf_service.extract_text(pdf_path)
        chunks = self._chunk_service.split_text(text)

        logger.info(f"Generated {len(chunks)} chunks")

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

        logger.info(f"Successfully indexed '{filename}'")
