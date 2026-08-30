from unittest.mock import Mock

from langchain_core.documents import Document

from app.repositories.chroma_repository import ChromaRepository


def make_repository() -> tuple[ChromaRepository, Mock]:
    repository = ChromaRepository.__new__(ChromaRepository)
    vector_store = Mock()
    repository._vector_store = vector_store
    return repository, vector_store


def test_similarity_search_applies_document_filter() -> None:
    repository, vector_store = make_repository()
    vector_store.similarity_search.return_value = []

    repository.similarity_search("question", k=10, document_ids=["one", "two"])

    vector_store.similarity_search.assert_called_once_with(
        query="question",
        k=10,
        filter={"document_id": {"$in": ["one", "two"]}},
    )


def test_similarity_search_uses_single_document_filter() -> None:
    repository, vector_store = make_repository()
    vector_store.similarity_search.return_value = []

    repository.similarity_search("question", k=10, document_ids=["one"])

    assert vector_store.similarity_search.call_args.kwargs["filter"] == {
        "document_id": "one"
    }


def test_keyword_search_ranks_exact_terms_and_filters_documents() -> None:
    repository, vector_store = make_repository()
    vector_store.get.return_value = {
        "documents": [
            "zero trust architecture identity access",
            "zero networking overview",
            "unrelated cooking instructions",
        ],
        "metadatas": [
            {"document_id": "security", "chunk_index": 0},
            {"document_id": "security", "chunk_index": 1},
            {"document_id": "cooking", "chunk_index": 0},
        ],
    }

    documents = repository.keyword_search("zero trust", k=5, document_ids=["security"])

    assert [document.page_content for document in documents] == [
        "zero trust architecture identity access",
        "zero networking overview",
    ]


def test_keyword_search_returns_empty_for_empty_query() -> None:
    repository, vector_store = make_repository()

    assert repository.keyword_search("?!", k=5) == []
    vector_store.get.assert_not_called()


def test_repository_add_delete_and_list_documents() -> None:
    repository, vector_store = make_repository()
    documents = [Document(page_content="content")]
    vector_store.get.return_value = {
        "metadatas": [
            {"document_id": "one", "filename": "one.pdf"},
            {"document_id": "one", "filename": "one.pdf"},
            {"document_id": "two", "filename": "two.pdf"},
        ]
    }

    repository.add_documents(documents)
    listed = repository.list_documents()
    repository.delete_document("one")

    vector_store.add_documents.assert_called_once_with(documents=documents)
    vector_store.delete.assert_called_once_with(where={"document_id": "one"})
    assert listed == [
        {"document_id": "one", "filename": "one.pdf"},
        {"document_id": "two", "filename": "two.pdf"},
    ]
