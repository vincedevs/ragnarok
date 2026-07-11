from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chat_service = ChatService()


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(request: ChatRequest) -> ChatResponse:
    """Answer a question using the RAG pipeline"""
    answer = chat_service.chat(request.question)

    return ChatResponse(answer=answer)
