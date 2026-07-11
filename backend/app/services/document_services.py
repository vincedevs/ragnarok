from backend.app.core.config import get_settings
from backend.app.core.exceptions import DocumentNotFoundError
from backend.app.repositories.chroma_repository import ChromaRepository
from loguru import logger


class DocumentService:
    """Manage uploaded documents"""

    def __init__(self, repository: ChromaRepository) -> None:
        self._repository = repository
        self._settings = get_settings()

    def list_documents(self) -> list[dict]:
        return self._repository.list_documents()

    def delete_document(self, document_id: str) -> None:
        logger.info(f"Deleting document '{document_id}'")

        documents = self._repository.list_documents()

        document = next(
            (doc for doc in documents if doc["document_id"] == document_id), None
        )

        if document is None:
            raise DocumentNotFoundError(f"Document '{document_id}' not found")

        upload_dir = self._settings.upload_directory

        for file in upload_dir.glob(f"{document_id}_*"):
            file.unlink(missing_ok=True)

        self._repository.delete_document(document_id)
