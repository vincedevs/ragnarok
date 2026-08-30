import math
from collections import Counter
from typing import Any, cast

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import get_settings
from app.core.text import tokenize
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
            persist_directory=str(settings.chroma_persist_directory),
        )

    def add_documents(self, documents: list[Document]) -> None:
        """Store documents in Chroma"""
        self._vector_store.add_documents(documents=documents)

    def similarity_search(
        self,
        query: str,
        k: int | None = None,
        document_ids: list[str] | None = None,
    ) -> list[Document]:
        """Search for similar documents in Chroma"""
        settings = get_settings()

        return self._vector_store.similarity_search(
            query=query,
            k=k or settings.retrieval_k,
            filter=self._document_filter(document_ids),
        )

    def keyword_search(
        self,
        query: str,
        k: int,
        document_ids: list[str] | None = None,
    ) -> list[Document]:
        """Rank stored child chunks with an in-process BM25 implementation."""
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        collection = self._vector_store.get(include=["documents", "metadatas"])
        raw_documents = cast(list[str | None], collection.get("documents") or [])
        raw_metadatas = cast(
            list[dict[str, Any] | None], collection.get("metadatas") or []
        )
        allowed_ids = set(document_ids or [])
        corpus: list[tuple[str, dict[str, Any], list[str]]] = []

        for content, metadata in zip(raw_documents, raw_metadatas, strict=True):
            if not content or metadata is None:
                continue
            if allowed_ids and metadata.get("document_id") not in allowed_ids:
                continue
            corpus.append((content, metadata, tokenize(content)))

        if not corpus:
            return []

        document_frequencies = Counter(
            token for _, _, tokens in corpus for token in set(tokens)
        )
        average_length = sum(len(tokens) for _, _, tokens in corpus) / len(corpus)
        scored: list[tuple[float, str, dict[str, Any]]] = []

        for content, metadata, tokens in corpus:
            score = self._bm25_score(
                query_tokens,
                tokens,
                document_frequencies,
                len(corpus),
                average_length,
            )
            if score > 0:
                scored.append((score, content, metadata))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            Document(page_content=content, metadata=metadata)
            for _, content, metadata in scored[:k]
        ]

    @staticmethod
    def _bm25_score(
        query_tokens: list[str],
        document_tokens: list[str],
        document_frequencies: Counter[str],
        corpus_size: int,
        average_length: float,
    ) -> float:
        if not document_tokens or not average_length:
            return 0.0

        frequencies = Counter(document_tokens)
        score = 0.0
        k1 = 1.5
        b = 0.75

        for token in set(query_tokens):
            frequency = frequencies[token]
            if not frequency:
                continue
            document_frequency = document_frequencies[token]
            inverse_document_frequency = math.log(
                1
                + (corpus_size - document_frequency + 0.5) / (document_frequency + 0.5)
            )
            denominator = frequency + k1 * (
                1 - b + b * len(document_tokens) / average_length
            )
            score += inverse_document_frequency * frequency * (k1 + 1) / denominator

        return score

    @staticmethod
    def _document_filter(document_ids: list[str] | None) -> dict[str, Any] | None:
        if not document_ids:
            return None
        if len(document_ids) == 1:
            return {"document_id": document_ids[0]}
        return {"document_id": {"$in": document_ids}}

    def delete_document(self, document_id: str) -> None:
        """Delete all vectors belonging to a document"""
        self._vector_store.delete(where={"document_id": document_id})

    def list_documents(self) -> list[dict]:
        """Return unique uploaded documents"""
        collection = self._vector_store.get()
        documents: dict[str, dict] = {}

        for metadata in collection["metadatas"]:
            document_id = metadata["document_id"]

            if document_id not in documents:
                documents[document_id] = {
                    "document_id": document_id,
                    "filename": metadata["filename"],
                }

        return list(documents.values())
