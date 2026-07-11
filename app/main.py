from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.core.config import get_settings
from app.core.exceptions import DocumentNotFoundError, InvalidDocumentError

settings = get_settings()

app = FastAPI(
    title="RAGnarok API",
    version="0.1.0",
    description="A Retrievel-Augmented Generation platform",
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(documents_router)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "message": "RAGnarok API is running",
        "chat_model": settings.chat_model,
        "embedding_model": settings.embedding_model,
    }


@app.exception_handler(DocumentNotFoundError)
async def document_not_found_handler(request: Request, exc: DocumentNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(InvalidDocumentError)
async def invalid_document_handler(
    request: Request,
    exc: InvalidDocumentError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
        },
    )
