from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request"""

    question: str = Field(..., min_length=1, description="The user's question")


class ChatResponse(BaseModel):
    """Chat response"""

    answer: str
