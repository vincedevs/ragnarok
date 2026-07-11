from langchain_openai import ChatOpenAI

from app.core.config import get_settings


class LLMService:
    """Interacts with the chat model"""

    def __init__(self) -> None:
        settings = get_settings()

        self._llm = ChatOpenAI(
            model=settings.chat_model,
            api_key=settings.openai_api_key,
            temperature=0,
        )

    def generate(self, prompt: str) -> str:
        """Generate an answer from the LLM"""
        response = self._llm.invoke(prompt)

        return response.content
