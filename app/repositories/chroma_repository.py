from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import get_settings
from app.services.embedding_service import EmbeddingService


class ChromaRepository:
    """Repository for interacting with Chroma"""

    COLLECTION_NAME = "documents"

    def __init__(self) -> None:
        settings = get_settings()
        embedding_service = EmbeddingService()

        self._vector_store = Chroma(
            collection_name=self.COLLECTION_NAME,
            embedding_function=embedding_service.embeddings,
            persist_directory=settings.chroma_persist_directory,
        )

    def add_documents(self, documents: list[Document]) -> None:
        """Store documents in Chroma"""
        self._vector_store.add_documents(documents=documents)

    def similarity_search(self, query: str, k: int | None = None) -> list[Document]:
        """Search for similar documents in Chroma"""
        settings = get_settings()

        return self._vector_store.similarity_search(
            query=query, k=k or settings.retrieval_k
        )

    def delete(self, ids: list[str]) -> None:
        """Delete documents by vector IDs"""
        self._vector_store.delete(ids=ids)
