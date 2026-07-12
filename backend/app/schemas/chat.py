from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request"""

    question: str = Field(..., min_length=1, description="The user's question")


class ChatSource(BaseModel):
    """Chat source"""

    document_id: str
    filename: str
    chunk_index: int


class ChatResponse(BaseModel):
    """Chat response"""

    answer: str
    sources: list[ChatSource]
