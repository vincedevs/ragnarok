from backend.app.core.config import get_settings
from langchain_openai import OpenAIEmbeddings


class EmbeddingService:
    """Creates OpenAI embeddings"""

    def __init__(self) -> None:
        settings = get_settings()

        self._embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key,
        )

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        """Returns the OpenAI embeddings instance"""
        return self._embeddings
