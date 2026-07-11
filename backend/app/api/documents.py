from backend.app.dependencies import DocumentServiceDep
from backend.app.schemas.document import DocumentResponse
from fastapi import APIRouter

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("", response_model=list[DocumentResponse])
def list_documents(service: DocumentServiceDep):
    return service.list_documents()


@router.delete("/{document_id}")
def delete_document(document_id: str, service: DocumentServiceDep):
    service.delete_document(document_id)

    return {"message": "Documente deleted successfully"}
