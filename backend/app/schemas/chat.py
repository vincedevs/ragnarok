from typing import Literal

from pydantic import BaseModel, Field


class ChatHistoryMessage(BaseModel):
    """One prior message used to resolve follow-up questions."""

    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    """Chat request"""

    question: str = Field(..., min_length=1, description="The user's question")
    document_ids: list[str] | None = None
    history: list[ChatHistoryMessage] = Field(default_factory=list, max_length=10)


class ChatSource(BaseModel):
    """Chat source"""

    document_id: str
    filename: str
    chunk_index: int
    page_number: int | None = None
    section_heading: str | None = None
    relevance_score: float | None = None
    excerpt: str


class ChatResponse(BaseModel):
    """Chat response"""

    answer: str
    sources: list[ChatSource]
