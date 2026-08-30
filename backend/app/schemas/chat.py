from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request"""

    question: str = Field(..., min_length=1, description="The user's question")
    document_ids: list[str] | None = None


class ChatSource(BaseModel):
    """Chat source"""

    document_id: str
    filename: str
    chunk_index: int
    page_number: int | None = None
    section_heading: str | None = None
    relevance_score: float | None = None


class ChatResponse(BaseModel):
    """Chat response"""

    answer: str
    sources: list[ChatSource]
