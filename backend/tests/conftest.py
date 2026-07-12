import os
from collections.abc import Generator
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from langchain_core.documents import Document

from app.main import app

TEST_DATA_DIR = Path(__file__).resolve().parent / "data"
TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
(TEST_DATA_DIR / "chroma").mkdir(parents=True, exist_ok=True)
(TEST_DATA_DIR / "uploads").mkdir(parents=True, exist_ok=True)

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("CHROMA_PERSIST_DIRECTORY", str(TEST_DATA_DIR / "chroma"))
os.environ.setdefault("UPLOAD_DIRECTORY", str(TEST_DATA_DIR / "uploads"))


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
