from pydantic import BaseModel


class DocumentResponse(BaseModel):
    """Uploaded document"""

    document_id: str
    filename: str
