"""
APPLICATION CONFIGURATION
"""

from functools import lru_cache

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables"""

    openai_api_key: str
    chat_model: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"
    chroma_persist_directory: DirectoryPath
    upload_directory: DirectoryPath
    chunk_size: int = 500
    chunk_overlap: int = 100
    parent_chunk_size: int = 2000
    hybrid_candidate_k: int = 20
    rrf_k: int = 60
    retrieval_score_threshold: float = 0.15
    retrieval_k: int = 5

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance"""
    return Settings()  # type: ignore[call-arg]
