from fastapi import APIRouter

from app.dependencies import ChatServiceDep
from app.schemas.chat import ChatRequest, ChatResponse, ChatSource

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
    answer, documents = service.chat(request.question)

    return ChatResponse(
        answer=answer,
        sources=[
            ChatSource(
                document_id=document.metadata["document_id"],
                filename=document.metadata["filename"],
                chunk_index=document.metadata["chunk_index"],
                page_number=document.metadata.get("page_number"),
                section_heading=document.metadata.get("section_heading"),
            )
            for document in documents
        ],
    )
