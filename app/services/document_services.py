from app.core.config import get_settings
from app.repositories.chroma_repository import ChromaRepository


class DocumentService:
    """Manage uploaded documents"""

    def __init__(self) -> None:
        self._repository = ChromaRepository()
        self._settings = get_settings()

    def list_documents(self) -> list[dict]:
        return self._repository.list_documents()

    def delete_document(self, document_id: str) -> None:
        documents = self._repository.list_documents()

        document = next(
            (doc for doc in documents if doc["document_id"] == document_id), None
        )

        if document is None:
            return

        upload_dir = self._settings.upload_directory

        for file in upload_dir.glob(f"{document_id}_*"):
            file.unlink(missing_ok=True)

        self._repository.delete_document(document_id=document_id)
