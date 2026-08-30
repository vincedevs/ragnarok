from langchain_core.documents import Document

from app.core.config import get_settings
from app.repositories.chroma_repository import ChromaRepository


class RetrievalService:
    """Retrieves relevant document chunks"""

    def __init__(self, repository: ChromaRepository) -> None:
        self._chroma_repository = repository
        self._settings = get_settings()

    def retrieve(self, question: str) -> list[Document]:
        """Retrieve matching children and expand them into unique parent contexts."""
        children = self._chroma_repository.similarity_search(
            query=question, k=self._settings.child_retrieval_k
        )
        parents: list[Document] = []
        seen_parent_ids: set[str] = set()

        for child in children:
            parent_id = str(child.metadata.get("parent_id", ""))
            if parent_id and parent_id in seen_parent_ids:
                continue

            if parent_id:
                seen_parent_ids.add(parent_id)

            metadata = dict(child.metadata)
            parent_content = str(metadata.pop("parent_content", child.page_content))
            parents.append(Document(page_content=parent_content, metadata=metadata))

            if len(parents) >= self._settings.retrieval_k:
                break

        return parents
