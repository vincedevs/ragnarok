from unittest.mock import Mock

from langchain_core.documents import Document

from app.services.chat_service import ChatService


def test_chat_returns_llm_response(
    sample_documents: list[Document],
    sample_question: str,
) -> None:
    """ChatService should orchestrate retrieval, prompt building, and LLM generation."""

    retrieval_service = Mock()
    prompt_service = Mock()
    llm_service = Mock()

    retrieval_service.retrieve.return_value = sample_documents
    prompt_service.build.return_value = "PROMPT"
    llm_service.generate.return_value = "ANSWER"

    service = ChatService(
        retrieval_service=retrieval_service,
        prompt_service=prompt_service,
        llm_service=llm_service,
    )

    result = service.chat(sample_question)

    assert result == ("ANSWER", sample_documents)

    retrieval_service.retrieve.assert_called_once_with(
        sample_question, document_ids=None
    )
    prompt_service.build.assert_called_once_with(
        question=sample_question,
        documents=sample_documents,
    )
    llm_service.generate.assert_called_once_with("PROMPT")


def test_chat_filters_selected_documents(
    sample_documents: list[Document], sample_question: str
) -> None:
    retrieval_service = Mock()
    prompt_service = Mock()
    llm_service = Mock()
    retrieval_service.retrieve.return_value = sample_documents
    llm_service.generate.return_value = "ANSWER"
    service = ChatService(retrieval_service, prompt_service, llm_service)

    service.chat(sample_question, document_ids=["doc-1"])

    retrieval_service.retrieve.assert_called_once_with(
        sample_question, document_ids=["doc-1"]
    )
