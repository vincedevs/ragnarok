from collections.abc import Mapping, Sequence

from langchain_core.documents import Document

from app.core.constants import INSUFFICIENT_CONTEXT_RESPONSE
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
        self,
        question: str,
        document_ids: list[str] | None = None,
        history: Sequence[Mapping[str, str]] = (),
    ) -> tuple[str, list[Document]]:
        """Answer a user's question"""
        retrieval_question = question
        if history:
            rewrite_prompt = self._prompt_service.build_rewrite(question, history)
            rewritten = self._llm_service.generate(rewrite_prompt).strip()
            if rewritten:
                retrieval_question = rewritten

        documents = self._retrieval_service.retrieve(
            retrieval_question, document_ids=document_ids
        )
        if not documents:
            return INSUFFICIENT_CONTEXT_RESPONSE, []

        prompt = self._prompt_service.build(
            question=retrieval_question, documents=documents
        )

        answer = self._llm_service.generate(prompt)

        return answer, documents
