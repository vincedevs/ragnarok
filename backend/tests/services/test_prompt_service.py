from langchain_core.documents import Document

from app.services.prompt_service import PromptService


def test_build_creates_prompt_with_context_and_question(
    sample_documents: list[Document],
    sample_question: str,
) -> None:
    """Prompt should contain the retrieved context and the user's question."""

    service = PromptService()

    prompt = service.build(
        question=sample_question,
        documents=sample_documents,
    )

    messages = prompt.to_messages()

    assert len(messages) == 2

    system_message = messages[0].content
    human_message = messages[1].content

    assert "Answer the user's question" in system_message

    for document in sample_documents:
        assert document.page_content in human_message

    assert sample_question in human_message


def test_build_labels_context_with_source_metadata() -> None:
    document = Document(
        page_content="Relevant section text",
        metadata={
            "filename": "guide.pdf",
            "page_number": 7,
            "section_heading": "ARCHITECTURE",
        },
    )

    prompt = PromptService().build("What is the architecture?", [document])
    human_message = prompt.to_messages()[1].content

    assert "[guide.pdf, p. 7, ARCHITECTURE]" in human_message


def test_build_rewrite_includes_history_and_latest_question() -> None:
    history = [
        {"role": "user", "content": "What is zero trust?"},
        {"role": "assistant", "content": "It is a security model."},
    ]

    prompt = PromptService().build_rewrite("How is it implemented?", history)
    messages = prompt.to_messages()

    assert "Return only the rewritten question" in messages[0].content
    assert "User: What is zero trust?" in messages[1].content
    assert "Assistant: It is a security model." in messages[1].content
    assert "How is it implemented?" in messages[1].content
