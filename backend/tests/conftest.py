from collections.abc import Generator
from unittest.mock import Mock

import pytest
from backend.app.main import app
from fastapi.testclient import TestClient
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


@pytest.fixture
def client() -> Generator[TestClient]:
    app.dependency_overrides.clear()

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def mock_chat_service() -> Mock:
    return Mock()


@pytest.fixture
def mock_ingestion_service() -> Mock:
    return Mock()


@pytest.fixture
def mock_document_service() -> Mock:
    return Mock()
