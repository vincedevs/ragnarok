from langchain_core.documents import Document

from app.core.config import get_settings
from app.core.text import tokenize
from app.repositories.chroma_repository import ChromaRepository


class RetrievalService:
    """Retrieves relevant document chunks"""

    def __init__(self, repository: ChromaRepository) -> None:
        self._chroma_repository = repository
        self._settings = get_settings()

    def retrieve(
        self, question: str, document_ids: list[str] | None = None
    ) -> list[Document]:
        """Fuse semantic and lexical matches, then rerank expanded parents."""
        candidate_k = self._settings.hybrid_candidate_k
        dense = self._chroma_repository.similarity_search(
            query=question,
            k=candidate_k,
            document_ids=document_ids,
        )
        keyword = self._chroma_repository.keyword_search(
            query=question,
            k=candidate_k,
            document_ids=document_ids,
        )
        children = self._reciprocal_rank_fusion(dense, keyword)
        parent_candidates: dict[str, tuple[float, Document]] = {}

        for score, child in children:
            parent_id = str(child.metadata.get("parent_id", ""))
            metadata = dict(child.metadata)
            parent_content = str(metadata.pop("parent_content", child.page_content))
            identity = parent_id or self._child_identity(child)
            existing = parent_candidates.get(identity)

            if existing is None or score > existing[0]:
                parent_candidates[identity] = (
                    score,
                    Document(page_content=parent_content, metadata=metadata),
                )

        return self._rerank_parents(question, list(parent_candidates.values()))

    def _reciprocal_rank_fusion(
        self, dense: list[Document], keyword: list[Document]
    ) -> list[tuple[float, Document]]:
        fused: dict[str, tuple[float, Document]] = {}

        for ranking in (dense, keyword):
            for rank, document in enumerate(ranking, start=1):
                identity = self._child_identity(document)
                previous_score = fused.get(identity, (0.0, document))[0]
                fused[identity] = (
                    previous_score + 1 / (self._settings.rrf_k + rank),
                    document,
                )

        return sorted(fused.values(), key=lambda item: item[0], reverse=True)

    def _rerank_parents(
        self, question: str, candidates: list[tuple[float, Document]]
    ) -> list[Document]:
        if not candidates:
            return []

        query_tokens = set(tokenize(question))
        raw_scores = [score for score, _ in candidates]
        minimum = min(raw_scores)
        maximum = max(raw_scores)
        reranked: list[tuple[float, Document]] = []

        for fusion_score, document in candidates:
            normalized_fusion = (
                (fusion_score - minimum) / (maximum - minimum)
                if maximum > minimum
                else 1.0
            )
            parent_tokens = set(tokenize(document.page_content))
            lexical_coverage = (
                len(query_tokens & parent_tokens) / len(query_tokens)
                if query_tokens
                else 0.0
            )
            score = 0.8 * normalized_fusion + 0.2 * lexical_coverage
            if score < self._settings.retrieval_score_threshold:
                continue

            document.metadata["relevance_score"] = round(score, 4)
            reranked.append((score, document))

        reranked.sort(key=lambda item: item[0], reverse=True)
        return [document for _, document in reranked[: self._settings.retrieval_k]]

    @staticmethod
    def _child_identity(document: Document) -> str:
        metadata = document.metadata
        return ":".join(
            (
                str(metadata.get("document_id", "legacy")),
                str(metadata.get("chunk_index", hash(document.page_content))),
            )
        )
