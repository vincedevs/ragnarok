from fastapi import APIRouter

from app.dependencies import DocumentServiceDep
from app.schemas.document import DocumentResponse

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("", response_model=list[DocumentResponse])
def list_documents(service: DocumentServiceDep) -> list[dict]:
    return service.list_documents()


@router.delete("/{document_id}")
def delete_document(document_id: str, service: DocumentServiceDep) -> dict[str, str]:
    service.delete_document(document_id)

    return {"message": "Document deleted successfully"}
