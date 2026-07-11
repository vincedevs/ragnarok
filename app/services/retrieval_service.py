from langchain_core.documents import Document

from app.repositories.chroma_repository import ChromaRepository


class RetrievalService:
    """Retrieves relevant document chunks"""

    def __init__(self) -> None:
        self._chroma_repository = ChromaRepository()

    def retrieve(self, question: str) -> list[Document]:
        """Retrieve relevant chunks"""
        return self._chroma_repository.similarity_search(query=question)
