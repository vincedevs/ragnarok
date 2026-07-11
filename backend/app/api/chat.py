from fastapi import APIRouter

from app.dependencies import ChatServiceDep
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(request: ChatRequest, service: ChatServiceDep) -> ChatResponse:
    """Answer a question using the RAG pipeline"""
    answer = service.chat(request.question)

    return ChatResponse(answer=answer)
