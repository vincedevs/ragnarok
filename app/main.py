from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="RAGnarok API",
    version="0.1.0",
    description="A Retrievel-Augmented Generation platform",
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "message": "RAGnarok API is running",
        "chat_model": settings.chat_model,
        "embedding_model": settings.embedding_model,
    }
