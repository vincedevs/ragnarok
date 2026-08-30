from unittest.mock import Mock

from langchain_core.documents import Document

from app.services.retrieval_service import RetrievalService


def test_retrieve_expands_and_deduplicates_parent_chunks() -> None:
    repository = Mock()
    repository.similarity_search.return_value = [
        Document(
            page_content="matching child one",
            metadata={
                "document_id": "doc-1",
                "filename": "guide.pdf",
                "page_number": 2,
                "chunk_index": 1,
                "parent_id": "doc-1:parent:0",
                "parent_content": "complete parent context",
            },
        ),
        Document(
            page_content="matching child two",
            metadata={
                "document_id": "doc-1",
                "filename": "guide.pdf",
                "page_number": 2,
                "chunk_index": 2,
                "parent_id": "doc-1:parent:0",
                "parent_content": "complete parent context",
            },
        ),
    ]
    repository.keyword_search.return_value = []

    documents = RetrievalService(repository).retrieve("question")

    assert len(documents) == 1
    assert documents[0].page_content == "complete parent context"
    assert "parent_content" not in documents[0].metadata
    repository.similarity_search.assert_called_once_with(
        query="question", k=20, document_ids=None
    )
    repository.keyword_search.assert_called_once_with(
        query="question", k=20, document_ids=None
    )


def test_retrieve_supports_legacy_chunks_without_parent_metadata() -> None:
    repository = Mock()
    repository.similarity_search.return_value = [
        Document(page_content="legacy content", metadata={"filename": "old.pdf"})
    ]
    repository.keyword_search.return_value = []

    documents = RetrievalService(repository).retrieve("question")

    assert documents[0].page_content == "legacy content"


def test_retrieve_limits_expanded_parent_contexts() -> None:
    repository = Mock()
    repository.similarity_search.return_value = [
        Document(
            page_content=f"child {index}",
            metadata={
                "parent_id": f"parent-{index}",
                "parent_content": f"parent context {index}",
            },
        )
        for index in range(8)
    ]
    repository.keyword_search.return_value = []

    documents = RetrievalService(repository).retrieve("question")

    assert len(documents) == 5
    assert documents[-1].page_content == "parent context 4"


def test_retrieve_fuses_keyword_results_and_forwards_filter() -> None:
    repository = Mock()
    semantic = Document(
        page_content="semantic child",
        metadata={
            "document_id": "doc-1",
            "chunk_index": 1,
            "parent_id": "semantic-parent",
            "parent_content": "semantic context",
        },
    )
    exact = Document(
        page_content="ZX-81 exact term",
        metadata={
            "document_id": "doc-1",
            "chunk_index": 2,
            "parent_id": "exact-parent",
            "parent_content": "ZX-81 exact term context",
        },
    )
    repository.similarity_search.return_value = [semantic, exact]
    repository.keyword_search.return_value = [exact]

    documents = RetrievalService(repository).retrieve("ZX-81", ["doc-1"])

    assert documents[0].page_content == "ZX-81 exact term context"
    assert documents[0].metadata["relevance_score"] == 1.0
    repository.similarity_search.assert_called_once_with(
        query="ZX-81", k=20, document_ids=["doc-1"]
    )
