from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Response returned after a successful document upload"""

    document_id: str
    filename: str
    size_bytes: int
    content_type: str
