from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.repositories.chroma_repository import ChromaRepository
from app.services.chat_service import ChatService
from app.services.chunk_service import ChunkService
from app.services.document_services import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.ingestion_service import IngestionService
from app.services.llm_service import LLMService
from app.services.pdf_service import PDFService
from app.services.prompt_service import PromptService
from app.services.retrieval_service import RetrievalService
from app.services.storage_services import StorageService


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


@lru_cache
def get_chroma_repository() -> ChromaRepository:
    return ChromaRepository()


@lru_cache
def get_llm_service() -> LLMService:
    return LLMService()


def get_pdf_service() -> PDFService:
    return PDFService()


def get_chunk_service() -> ChunkService:
    return ChunkService()


def get_prompt_service() -> PromptService:
    return PromptService()


def get_storage_service() -> StorageService:
    return StorageService()


def get_retrieval_service() -> RetrievalService:
    return RetrievalService(
        repository=get_chroma_repository(),
    )


def get_chat_service() -> ChatService:
    return ChatService(
        retrieval_service=get_retrieval_service(),
        prompt_service=get_prompt_service(),
        llm_service=get_llm_service(),
    )


def get_document_service() -> DocumentService:
    return DocumentService(repository=get_chroma_repository())


def get_ingestion_service() -> IngestionService:
    return IngestionService(
        pdf_service=get_pdf_service(),
        chunk_service=get_chunk_service(),
        repository=get_chroma_repository(),
    )


# Type aliases
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]

DocumentServiceDep = Annotated[DocumentService, Depends(get_document_service)]

StorageServiceDep = Annotated[StorageService, Depends(get_storage_service)]

IngestionServiceDep = Annotated[IngestionService, Depends(get_ingestion_service)]
