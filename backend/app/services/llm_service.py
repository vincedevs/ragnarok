from langchain_core.prompt_values import PromptValue
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.core.config import get_settings


class LLMService:
    """Interacts with the chat model"""

    def __init__(self) -> None:
        settings = get_settings()

        self._llm = ChatOpenAI(
            model=settings.chat_model,
            api_key=SecretStr(settings.openai_api_key),
            temperature=0,
        )

    def generate(self, prompt: PromptValue) -> str:
        """Generate an answer from the LLM"""
        response = self._llm.invoke(prompt)

        if not isinstance(response.content, str):
            raise TypeError("The chat model returned unsupported content")

        return response.content
