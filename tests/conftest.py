import pytest
from langchain_core.documents import Document


@pytest.fixture
def sample_documents() -> list[Document]:
    return [
        Document(page_content="FastAPI is a modern Python web framework."),
        Document(page_content="LangChain helps build LLM applications."),
    ]


@pytest.fixture
def sample_question() -> str:
    return "What is FastAPI?"
