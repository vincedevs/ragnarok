from fastapi import APIRouter

from app.schemas.document import DocumentResponse
from app.services.document_services import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])

service = DocumentService()


@router.get("", response_model=list[DocumentResponse])
def list_documents():
    return service.list_documents()


@router.delete("/{document_id}")
def delete_document(document_id: str):
    service.delete_document(document_id)

    return {"message": "Documente deleted successfully"}
