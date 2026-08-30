from langchain_core.documents import Document

from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService
from app.services.retrieval_service import RetrievalService


class ChatService:
    """Coordinates the RAG question-answering pipeline"""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        prompt_service: PromptService,
        llm_service: LLMService,
    ) -> None:
        self._retrieval_service = retrieval_service
        self._prompt_service = prompt_service
        self._llm_service = llm_service

    def chat(
        self, question: str, document_ids: list[str] | None = None
    ) -> tuple[str, list[Document]]:
        """Answer a user's question"""
        documents = self._retrieval_service.retrieve(
            question, document_ids=document_ids
        )
        prompt = self._prompt_service.build(question=question, documents=documents)

        answer = self._llm_service.generate(prompt)

        return answer, documents
