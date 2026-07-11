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

    def chat(self, question: str) -> str:
        """Answer a user's question"""
        documents = self._retrieval_service.retrieve(question)
        prompt = self._prompt_service.build(question, documents)

        return self._llm_service.generate(prompt)
